# Copyright 2024 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Optional

from crossbench import cli_helper
from crossbench.probes.probe import Probe, ProbeConfigParser, ProbeKeyT
from crossbench.probes.probe_context import ProbeContext
from crossbench.probes.result_location import ResultLocation
from crossbench.probes.results import LocalProbeResult, ProbeResult
from crossbench.runner.run import Run

if TYPE_CHECKING:
  from crossbench import path as pth
  from crossbench.env import HostEnvironment
  from crossbench.plt.base import CmdArgT, TupleCmdArgsT
  from crossbench.runner.run import Run


class ShellProbe(Probe):
  """
  Run an arbitrary shell command on the browser platform and store the
  stdout and stderr of the command as a result file.
  """
  NAME = "shell"
  IS_GENERAL_PURPOSE = True
  RESULT_LOCATION = ResultLocation.LOCAL

  @classmethod
  def config_parser(cls) -> ProbeConfigParser:
    parser = super().config_parser()
    parser.add_argument(
        "setup_cmd",
        aliases=("setup",),
        type=cli_helper.parse_sh_cmd,
        required=False,
        help="CMD is run before the browser is started.")
    parser.add_argument(
        "start_cmd",
        type=cli_helper.parse_sh_cmd,
        aliases=("start",),
        required=False,
        help=("CMD is run right before each story is started "
              "and the browser is already running."))
    parser.add_argument(
        "start_story_run_cmd",
        aliases=("start-story",),
        type=cli_helper.parse_sh_cmd,
        required=False,
        help=("CMD is run right before the measurement phase "
              "of a story is started."))
    parser.add_argument(
        "stop_story_run_cmd",
        aliases=("stop-story",),
        type=cli_helper.parse_sh_cmd,
        required=False,
        help=("CMD is run right after the measurement phase "
              "of a story has ended."))
    parser.add_argument(
        "stop_cmd",
        aliases=("cmd", "stop"),
        type=cli_helper.parse_sh_cmd,
        required=True,
        help=("CMD is run right after the workload ended and the browser "
             "is still running."))
    parser.add_argument(
        "teardown_cmd",
        aliases=("teardown",),
        type=cli_helper.parse_sh_cmd,
        required=False,
        help="CMD is run after the browser is stopped.")
    return parser

  def __init__(self,
               setup_cmd: Optional[Iterable[CmdArgT]] = None,
               start_cmd: Optional[Iterable[CmdArgT]] = None,
               start_story_run_cmd: Optional[Iterable[CmdArgT]] = None,
               stop_story_run_cmd: Optional[Iterable[CmdArgT]] = None,
               stop_cmd: Optional[Iterable[CmdArgT]] = None,
               teardown_cmd: Optional[Iterable[CmdArgT]] = None) -> None:
    super().__init__()
    self._setup_cmd: TupleCmdArgsT = tuple(setup_cmd) if setup_cmd else ()
    self._start_cmd: TupleCmdArgsT = tuple(start_cmd) if start_cmd else ()
    self._start_story_run_cmd: TupleCmdArgsT = (
        tuple(start_story_run_cmd) if start_story_run_cmd else ())
    self._stop_story_run_cmd: TupleCmdArgsT = (
        tuple(stop_story_run_cmd) if stop_story_run_cmd else ())
    self._stop_cmd: TupleCmdArgsT = tuple(stop_cmd) if stop_cmd else ()
    self._teardown_cmd: TupleCmdArgsT = (
        tuple(teardown_cmd) if teardown_cmd else ())

  @property
  def key(self) -> ProbeKeyT:
    return super().key + (
        ("setup_cmd", tuple(map(str, self.stop_cmd))),
        ("start_cmd", tuple(map(str, self.start_cmd))),
        ("start_story_run_cmd", tuple(map(str, self.start_story_run_cmd))),
        ("stop_story_run_cmd", tuple(map(str, self.stop_story_run_cmd))),
        ("stop_cmd", tuple(map(str, self.stop_cmd))),
        ("teardown_cmd", tuple(map(str, self.teardown_cmd))),
    )

  @property
  def setup_cmd(self) -> TupleCmdArgsT:
    return self._setup_cmd

  @property
  def start_cmd(self) -> TupleCmdArgsT:
    return self._start_cmd

  @property
  def start_story_run_cmd(self) -> TupleCmdArgsT:
    return self._start_story_run_cmd

  @property
  def stop_story_run_cmd(self) -> TupleCmdArgsT:
    return self._stop_story_run_cmd

  @property
  def stop_cmd(self) -> TupleCmdArgsT:
    return self._stop_cmd

  @property
  def teardown_cmd(self) -> TupleCmdArgsT:
    return self._teardown_cmd

  def validate_env(self, env: HostEnvironment) -> None:
    super().validate_env(env)
    if env.runner.repetitions != 1:
      env.handle_warning(f"Probe={self.NAME} cannot merge data over multiple "
                         f"repetitions={env.runner.repetitions}.")

  def get_context(self, run: Run) -> ShellProbeContext:
    return ShellProbeContext(self, run)


class ShellProbeContext(ProbeContext[ShellProbe]):

  def __init__(self, probe: ShellProbe, run: Run) -> None:
    super().__init__(probe, run)
    self._result_files: List[pth.LocalPath] = []

  def _maybe_run_cmd(self, name: str, cmd: TupleCmdArgsT) -> None:
    if not cmd:
      return
    stdout_path = self.local_result_path / f"{name}.stdout.txt"
    self.runner_platform.touch(stdout_path)
    self._result_files.append(stdout_path)
    stderr_path = self.local_result_path / f"{name}.stderr.txt"
    self.runner_platform.touch(stderr_path)
    self._result_files.append(stderr_path)
    with stdout_path.open("w") as stdout, stderr_path.open("w") as stderr:
      self.browser_platform.sh(*cmd, shell=True, stdout=stdout, stderr=stderr)

  def setup(self) -> None:
    self.runner_platform.mkdir(self.local_result_path)
    self._maybe_run_cmd("setup", self.probe.setup_cmd)

  def start(self) -> None:
    self._maybe_run_cmd("start", self.probe.start_cmd)

  def start_story_run(self) -> None:
    self._maybe_run_cmd("start_story_run", self.probe.start_story_run_cmd)

  def stop_story_run(self) -> None:
    self._maybe_run_cmd("stop_story_run", self.probe.stop_story_run_cmd)

  def stop(self) -> None:
    self._maybe_run_cmd("stop", self.probe.stop_cmd)

  def teardown(self) -> ProbeResult:
    self._maybe_run_cmd("teardown", self.probe.teardown_cmd)
    return LocalProbeResult(file=tuple(self._result_files))
