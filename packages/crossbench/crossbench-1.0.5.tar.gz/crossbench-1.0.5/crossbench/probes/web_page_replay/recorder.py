# Copyright 2023 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import annotations

import shutil
from typing import TYPE_CHECKING, Any, Iterable, List, Optional, Union

from immutabledict import immutabledict

from crossbench import cli_helper, helper, plt
from crossbench.helper.path_finder import WprGoToolFinder
from crossbench.network.replay.web_page_replay import WprRecorder
from crossbench.probes.probe import Probe, ProbeConfigParser, ProbeContext
from crossbench.probes.results import (EmptyProbeResult, LocalProbeResult,
                                       ProbeResult)
from crossbench.runner.groups import (BrowsersRunGroup, RepetitionsRunGroup,
                                      RunGroup, StoriesRunGroup)

if TYPE_CHECKING:
  from crossbench.browsers.browser import Browser
  from crossbench.path import LocalPath
  from crossbench.runner.run import Run



class WebPageReplayProbe(Probe):
  """
  Probe to collect browser requests to wpr.go archive which then can be
  replayed using a local proxy server.

  Chrome telemetry's wpr.go:
  https://chromium.googlesource.com/catapult/+/HEAD/web_page_replay_go/README.md
  """

  NAME = "wpr"

  @classmethod
  def config_parser(cls) -> ProbeConfigParser:
    parser = super().config_parser()
    parser.add_argument("http_port", type=int, default=8080, required=False)
    parser.add_argument("https_port", type=int, default=8081, required=False)
    parser.add_argument(
        "wpr_go_bin", type=cli_helper.parse_binary_path, required=False)
    parser.add_argument(
        "key_file", type=cli_helper.parse_existing_file_path, required=False)
    parser.add_argument(
        "cert_file", type=cli_helper.parse_existing_file_path, required=False)
    parser.add_argument(
        "inject_scripts",
        is_list=True,
        type=cli_helper.parse_existing_file_path,
        required=False)
    parser.add_argument(
        "use_test_root_certificate", type=bool, default=False, required=False)
    return parser

  def __init__(self,
               http_port: int = 0,
               https_port: int = 0,
               wpr_go_bin: Optional[LocalPath] = None,
               inject_scripts: Optional[Iterable[LocalPath]] = None,
               key_file: Optional[LocalPath] = None,
               cert_file: Optional[LocalPath] = None,
               use_test_root_certificate: bool = False):
    super().__init__()
    runner_platform = plt.PLATFORM
    if not wpr_go_bin:
      if local_wpr_path := WprGoToolFinder(runner_platform).path:
        wpr_go_bin = runner_platform.local_path(local_wpr_path)
    if not wpr_go_bin:
      raise RuntimeError(f"Could not find wpr.go on {runner_platform}")
    self._wpr_go_bin: LocalPath = runner_platform.local_path(
        cli_helper.parse_binary_path(wpr_go_bin, "wpr.go"))

    self._recorder_kwargs: immutabledict[str, Any] = immutabledict(
        bin_path=wpr_go_bin,
        http_port=http_port,
        https_port=https_port,
        inject_scripts=inject_scripts,
        key_file=key_file,
        cert_file=cert_file,
    )

    self._https_port = https_port
    self._http_port = http_port
    self._use_test_root_certificate = use_test_root_certificate

  @property
  def https_port(self) -> int:
    return self._https_port

  @property
  def http_port(self) -> int:
    return self._http_port

  @property
  def recorder_kwargs(self) -> immutabledict:
    return self._recorder_kwargs

  @property
  def use_test_root_certificate(self) -> bool:
    return self._use_test_root_certificate

  @property
  def result_path_name(self) -> str:
    return "archive.wprgo"

  def is_compatible(self, browser: Browser) -> bool:
    return browser.attributes.is_chromium_based and browser.platform.is_local

  def get_context(self, run: Run) -> WprRecorderProbeContext:
    return WprRecorderProbeContext(self, run)

  def merge_repetitions(self, group: RepetitionsRunGroup) -> ProbeResult:
    results = [run.results[self].file for run in group.runs]
    return self.merge_group(results, group)

  def merge_stories(self, group: StoriesRunGroup) -> ProbeResult:
    results = [
        subgroup.results[self].file for subgroup in group.repetitions_groups
    ]
    return self.merge_group(results, group)

  def merge_browsers(self, group: BrowsersRunGroup) -> ProbeResult:
    results = [subgroup.results[self].file for subgroup in group.story_groups]
    return self.merge_group(results, group)

  def merge_group(self, results: List[LocalPath],
                  group: RunGroup) -> ProbeResult:
    result_file = group.get_local_probe_result_path(self)
    if not results:
      return EmptyProbeResult()
    first_wprgo = results.pop(0)
    # TODO migrate to platform
    shutil.copy(first_wprgo, result_file)
    for repetition_file in results:
      self.httparchive_merge(repetition_file, result_file)
    return ProbeResult(file=[result_file])

  def httparchive_merge(self, input_archive: LocalPath,
                        output_archive: LocalPath) -> None:
    cmd: List[Union[str, LocalPath]] = [
        "go",
        "run",
        self._wpr_go_bin.parent / "httparchive.go",
        "merge",
        output_archive,
        input_archive,
        output_archive,
    ]
    with helper.ChangeCWD(self._wpr_go_bin.parent):
      self.runner_platform.sh(*cmd)


class WprRecorderProbeContext(ProbeContext[WebPageReplayProbe]):

  def __init__(self, probe: WebPageReplayProbe, run: Run) -> None:
    super().__init__(probe, run)
    self._wprgo_log: LocalPath = self.local_result_path.with_name(
        "wpr_record.log")
    self._host: str = "127.0.0.1"
    kwargs = dict(self.probe.recorder_kwargs)
    kwargs.update({
        "platform": run.runner_platform,
        "log_path": self._wprgo_log,
        "archive_path": self.result_path,
    })
    self._recorder = WprRecorder(**kwargs)
    self._browser_platform = run.browser_platform

  def setup(self) -> None:
    self._recorder.start()
    self._setup_extra_flags()
    self._setup_port_forwarding()

  def _setup_extra_flags(self) -> None:
    if not self.probe.use_test_root_certificate:
      cert_hash_file = self._recorder.cert_file.parent / "wpr_public_hash.txt"
      if not cert_hash_file.is_file():
        raise ValueError(
            f"Could not read public key hash file: {cert_hash_file}")
      cert_skip_list = ",".join(cert_hash_file.read_text().strip().splitlines())
      self.session.extra_flags[
          "--ignore-certificate-errors-spki-list"] = cert_skip_list
    # TODO: support ts_proxy traffic shaping
    # session.extra_flags[
    #     "--proxy-server"] = "socks://{self._ts_proxy_host}:{self._ts_proxy_port}"
    # session.extra_flags["--proxy-bypass-list"] = "<-loopback>"
    self.session.extra_flags["--host-resolver-rules"] = (
        f"MAP *:80 {self._host}:{self._recorder.http_port},"
        f"MAP *:443 {self._host}:{self._recorder.https_port},"
        "EXCLUDE localhost")
    # TODO: add replay support, see:
    # third_party/catapult/telemetry/telemetry/internal/backends/chrome/chrome_startup_args.py

  def _setup_port_forwarding(self) -> None:
    if self._browser_platform.is_remote:
      self._browser_platform.reverse_port_forward(self._recorder.http_port,
                                                  self._recorder.http_port)
      self._browser_platform.reverse_port_forward(self._recorder.https_port,
                                                  self._recorder.https_port)

  def start(self) -> None:
    pass

  def stop(self) -> None:
    pass

  def teardown(self) -> ProbeResult:
    self._recorder.stop()
    return LocalProbeResult(file=(self.local_result_path,))
