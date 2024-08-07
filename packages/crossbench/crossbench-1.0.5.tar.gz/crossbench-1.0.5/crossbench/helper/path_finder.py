# Copyright 2024 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import annotations

import abc
import logging
from typing import TYPE_CHECKING, Final, Iterator, Optional, Tuple

from crossbench import path as pth
from crossbench.plt.base import Platform

if TYPE_CHECKING:
  from crossbench.plt.base import Platform


class BaseToolFinder(abc.ABC):

  def __init__(
      self,
      platform: Platform,
      candidates: Tuple[pth.RemotePath, ...] = tuple()) -> None:
    self._platform = platform
    self._candidates = candidates + self._default_candidates()
    self._path: Optional[pth.RemotePath] = self._find_path()
    if self._path:
      assert self._is_valid_path(self._path)

  @property
  def platform(self) -> Platform:
    return self._platform

  @property
  def path(self) -> Optional[pth.RemotePath]:
    return self._path

  @property
  def candidates(self) -> Tuple[pth.RemotePath, ...]:
    return self._candidates

  def _default_candidates(self) -> Tuple[pth.RemotePath, ...]:
    return tuple()

  def _find_path(self) -> Optional[pth.RemotePath]:
    # Try potential build location
    for candidate_dir in self._candidates:
      if self._is_valid_path(candidate_dir):
        return candidate_dir
    return None

  @abc.abstractmethod
  def _is_valid_path(self, candidate: pth.RemotePath) -> bool:
    pass


def default_chromium_candidates(
    platform: Platform) -> Tuple[pth.RemotePath, ...]:
  """Returns a generous list of potential locations of a chromium checkout."""
  candidates = []
  if chromium_src := platform.environ.get("CHROMIUM_SRC"):
    candidates.append(platform.path(chromium_src))
  if platform.is_local:
    candidates.append(chromium_src_relative_local_path())
  home_dir = platform.home()
  candidates += [
      # Guessing default locations
      home_dir / "Documents/chromium/src",
      home_dir / "chromium/src",
      platform.path("C:/src/chromium/src"),
      home_dir / "Documents/chrome/src",
      home_dir / "chrome/src",
      platform.path("C:/src/chrome/src"),
  ]
  return tuple(candidates)


def chromium_src_relative_local_path():
  """Gets the local relative path of `chromium/src`.

  Assuming the cli.py path is `third_party/crossbench/crossbench/cli/cli.py`.
  """
  return pth.LocalPath(__file__).parents[4]


def is_chromium_checkout_dir(platform: Platform,
                             dir_path: pth.RemotePath) -> bool:
  return (platform.is_dir(dir_path / "v8") and
          platform.is_dir(dir_path / "chrome") and
          platform.is_dir(dir_path / ".git"))


class ChromiumCheckoutFinder(BaseToolFinder):
  """Finds a chromium src checkout at either given locations or at
  some preset known checkout locations."""

  def _default_candidates(self) -> Tuple[pth.RemotePath, ...]:
    return default_chromium_candidates(self.platform)

  def _is_valid_path(self, candidate: pth.RemotePath) -> bool:
    return is_chromium_checkout_dir(self.platform, candidate)


class ChromiumBuildBinaryFinder(BaseToolFinder):
  """Finds a custom-built binary in either a given out/BUILD dir or
  tries to find it in build dirs in common known chromium checkout locations."""

  def __init__(
      self,
      platform: Platform,
      binary_name: str,
      candidates: Tuple[pth.RemotePath, ...] = tuple()) -> None:
    self._binary_name = binary_name
    super().__init__(platform, candidates)

  @property
  def binary_name(self) -> str:
    return self._binary_name

  def _iterate_candidate_bin_paths(self) -> Iterator[pth.RemotePath]:
    for candidate_dir in self._candidates:
      yield candidate_dir / self._binary_name

    for candidate in default_chromium_candidates(self.platform):
      candidate_out = candidate / "out"
      if not self.platform.is_dir(candidate_out):
        continue
      # TODO: support remote glob
      for build in ("Release", "release", "rel", "Optdebug", "optdebug", "opt"):
        yield candidate_out / build / self._binary_name

  def _find_path(self) -> Optional[pth.RemotePath]:
    for candidate in self._iterate_candidate_bin_paths():
      if self._is_valid_path(candidate):
        return candidate
    return None

  def _is_valid_path(self, candidate: pth.RemotePath) -> bool:
    assert candidate.name == self._binary_name
    if not self.platform.is_file(candidate):
      return False
    # .../chromium/src/out/Release/BINARY => .../chromium/src/
    # Don't use parents[] access to stop at the root.
    maybe_checkout_dir = candidate.parent.parent.parent
    return is_chromium_checkout_dir(self._platform, maybe_checkout_dir)


class V8CheckoutFinder(BaseToolFinder):

  def _default_candidates(self) -> Tuple[pth.RemotePath, ...]:
    home_dir = self._platform.home()
    return (
        # V8 Checkouts
        home_dir / "Documents/v8/v8",
        home_dir / "v8/v8",
        self._platform.path("C:/src/v8/v8"),
        # Raw V8 checkouts
        home_dir / "Documents/v8",
        home_dir / "v8",
        self._platform.path("C:/src/v8/"),
    )

  def _find_path(self) -> Optional[pth.RemotePath]:
    if v8_checkout := super()._find_path():
      return v8_checkout
    if chromium_checkout := ChromiumCheckoutFinder(self._platform).path:
      return chromium_checkout / "v8"
    maybe_d8_path = self.platform.environ.get("D8_PATH")
    if not maybe_d8_path:
      return None
    for candidate_dir in self.platform.path(maybe_d8_path).parents:
      if self._is_valid_path(candidate_dir):
        return candidate_dir
    return None

  def _is_valid_path(self, candidate: pth.RemotePath) -> bool:
    v8_header_file = candidate / "include/v8.h"
    return (self.platform.is_file(v8_header_file) and
            (self.platform.is_dir(candidate / ".git")))


class V8ToolsFinder:
  """Helper class to find d8 binaries and the tick-processor.
  If no explicit d8 and checkout path are given, $D8_PATH and common v8 and
  chromium installation directories are checked."""

  def __init__(self,
               platform: Platform,
               d8_binary: Optional[pth.RemotePath] = None,
               v8_checkout: Optional[pth.RemotePath] = None) -> None:
    self.platform = platform
    self.d8_binary: Optional[pth.RemotePath] = d8_binary
    self.v8_checkout: Optional[pth.RemotePath] = None
    if v8_checkout:
      self.v8_checkout = v8_checkout
    else:
      self.v8_checkout = V8CheckoutFinder(self.platform).path
    self.tick_processor: Optional[pth.RemotePath] = None
    self.d8_binary = self._find_d8()
    if self.d8_binary:
      self.tick_processor = self._find_v8_tick_processor()
    logging.debug("V8ToolsFinder found d8_binary='%s' tick_processor='%s'",
                  self.d8_binary, self.tick_processor)

  def _find_d8(self) -> Optional[pth.RemotePath]:
    if self.d8_binary and self.platform.is_file(self.d8_binary):
      return self.d8_binary
    environ = self.platform.environ
    if "D8_PATH" in environ:
      candidate = self.platform.path(environ["D8_PATH"]) / "d8"
      if self.platform.is_file(candidate):
        return candidate
      candidate = self.platform.path(environ["D8_PATH"])
      if self.platform.is_file(candidate):
        return candidate
    # Try potential build location
    for candidate_dir in V8CheckoutFinder(self.platform).candidates:
      for build_type in ("release", "optdebug", "Default", "Release"):
        candidates = list(
            self.platform.glob(candidate_dir, f"out/*{build_type}/d8"))
        if not candidates:
          continue
        d8_candidate = candidates[0]
        if self.platform.is_file(d8_candidate):
          return d8_candidate
    return None

  def _find_v8_tick_processor(self) -> Optional[pth.RemotePath]:
    if self.platform.is_linux:
      tick_processor = "tools/linux-tick-processor"
    elif self.platform.is_macos:
      tick_processor = "tools/mac-tick-processor"
    elif self.platform.is_win:
      tick_processor = "tools/windows-tick-processor.bat"
    else:
      logging.debug(
          "Not looking for the v8 tick-processor on unsupported platform: %s",
          self.platform)
      return None
    if self.v8_checkout and self.platform.is_dir(self.v8_checkout):
      candidate = self.v8_checkout / tick_processor
      assert self.platform.is_file(candidate), (
          f"Provided v8_checkout has no '{tick_processor}' at {candidate}")
    assert self.d8_binary
    # Try inferring the V8 checkout from a built d8:
    # .../foo/v8/v8/out/x64.release/d8
    candidate = self.d8_binary.parents[2] / tick_processor
    if self.platform.is_file(candidate):
      return candidate
    if self.v8_checkout:
      candidate = self.v8_checkout / tick_processor
      if self.platform.is_file(candidate):
        return candidate
    return None


class BaseChromiumBinaryToolFinder(BaseToolFinder):

  def _is_valid_path(self, candidate: pth.RemotePath) -> bool:
    return self._platform.is_file(candidate)

  def _default_candidates(self) -> Tuple[pth.RemotePath, ...]:
    relative_path = chromium_src_relative_local_path() / self.chrome_path()
    if maybe_chrome := ChromiumCheckoutFinder(self._platform).path:
      return (relative_path, maybe_chrome / self.chrome_path(),)
    return (relative_path,)


class TraceconvFinder(BaseChromiumBinaryToolFinder):

  @classmethod
  def chrome_path(cls) -> pth.RemotePath:
   return pth.RemotePath(
      "third_party/perfetto/tools/traceconv")


class TraceProcessorFinder(BaseChromiumBinaryToolFinder):

  @classmethod
  def chrome_path(cls) -> pth.RemotePath:
   return pth.RemotePath(
      "third_party/perfetto/tools/trace_processor")


class WprGoToolFinder(BaseChromiumBinaryToolFinder):

  @classmethod
  def chrome_path(cls) -> pth.RemotePath:
   return pth.RemotePath(
      "third_party/catapult/web_page_replay_go/src/wpr.go")


class TsProxyFinder(BaseChromiumBinaryToolFinder):

  @classmethod
  def chrome_path(cls) -> pth.RemotePath:
   return pth.RemotePath(
      "third_party/catapult/third_party/tsproxy/tsproxy.py")
