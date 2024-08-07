# Copyright 2023 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING, Iterable, Tuple

from ordered_set import OrderedSet

from crossbench import exception

if TYPE_CHECKING:
  from crossbench.browsers.browser import Browser
  from crossbench.runner.groups.session import BrowserSessionRunGroup
  from crossbench.runner.run import Run
  from crossbench.runner.runner import Runner


class RunThreadGroup(threading.Thread):
  """The main interface to start Runs.
  - Typically only a single RunThreadGroup is used.
  - If runs are executed in parallel, multiple RunThreadGroup are used
  """

  def __init__(self, runs: Iterable[Run], throw: bool = False) -> None:
    super().__init__()
    self._exceptions = exception.Annotator(throw)
    self._runs = tuple(runs)
    assert self._runs, "Got unexpected empty runs list"
    self._runner: Runner = self._runs[0].runner
    self._total_run_count = len(self._runner.runs)
    self._browser_sessions: OrderedSet[BrowserSessionRunGroup] = OrderedSet(
        run.browser_session for run in self._runs)
    self.is_dry_run: bool = False
    self._verify_contains_all_browser_session_runs()
    self._verify_same_runner()
    if not self._browser_sessions:
      raise ValueError("No browser sessions / runs")

  def _verify_contains_all_browser_session_runs(self) -> None:
    runs_set = set(self._runs)
    for browser_session in self._browser_sessions:
      for session_run in browser_session.runs:
        assert session_run in runs_set, (
            f"BrowserSession {browser_session} is not allowed to have "
            f"{session_run} in another RunThreadGroup.")

  def _verify_same_runner(self) -> None:
    for run in self._runs:
      assert run.runner is self._runner, "All Runs must have the same Runner."

  @property
  def runner(self) -> Runner:
    return self._runner

  @property
  def runs(self) -> Tuple[Run, ...]:
    return tuple(self._runs)

  @property
  def browser_sessions(self) -> Tuple[BrowserSessionRunGroup, ...]:
    return tuple(self._browser_sessions)

  @property
  def browsers(self) -> Iterable[Browser]:
    for browser_session in self._browser_sessions:
      yield browser_session.browser

  @property
  def exceptions(self) -> exception.Annotator:
    return self._exceptions

  @property
  def is_success(self) -> bool:
    return self._exceptions.is_success

  def _log_run(self, run: Run):
    logging.info("=" * 80)
    label = ""
    if run.is_warmup:
      label = " WARMUP, ignoring results"
    logging.info("RUN %s/%s%s", run.index + 1, self._total_run_count, label)
    logging.info("=" * 80)

  def run(self) -> None:
    for browser_session in self._browser_sessions:
      self._run_browser_session(browser_session)
      if not browser_session.is_success:
        self._exceptions.extend(browser_session.exceptions)
    self.runner.exceptions.extend(self._exceptions)

  def _run_browser_session(self,
                           browser_session: BrowserSessionRunGroup) -> None:
    if browser_session.is_single_run:
      self._log_run(browser_session.first_run)
    else:
      logging.info("=" * 80)
    with browser_session.open() as is_success:
      if not is_success:
        self._handle_session_startup_failure(browser_session)
      else:
        for run in browser_session.runs:
          self._run_browser_session_run(browser_session, run)

  def _handle_session_startup_failure(
      self, browser_session: BrowserSessionRunGroup) -> None:
    runs = tuple(browser_session.runs)
    logging.info("%s: Skipping %s runs due to browser session setup errors.",
                 self, len(runs))
    for run in runs:
      run.exceptions.extend(browser_session.exceptions)

  def _run_browser_session_run(self, browser_session: BrowserSessionRunGroup,
                               run: Run) -> None:
    if not browser_session.is_single_run:
      self._log_run(run)
    if not run.is_success:
      logging.info("%s: Skipping %s due to setup errors.", self, run)
    else:
      run.run(self.is_dry_run)
    if run.is_success:
      run.log_results()
    else:
      browser_session.exceptions.extend(run.exceptions)
