# Copyright 2022 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import annotations

import abc
import logging
from typing import (TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Set,
                    Tuple, cast)

from immutabledict import immutabledict
from ordered_set import OrderedSet

from crossbench import cli_helper, path as pth
from crossbench.probes.helper import INTERNAL_NAME_PREFIX

if TYPE_CHECKING:
  from crossbench.probes.probe import Probe
  from crossbench.runner.result_origin import ResultOrigin
  from crossbench.types import JsonDict


class DuplicateProbeResult(ValueError):
  pass


class ProbeResult(abc.ABC):

  def __init__(self,
               url: Optional[Iterable[str]] = None,
               file: Optional[Iterable[pth.LocalPath]] = None,
               **kwargs: Iterable[pth.LocalPath]):
    self._url_list: Tuple[str, ...] = ()
    if url:
      self._url_list = cli_helper.parse_unique_sequence(
          tuple(url), "urls", DuplicateProbeResult)
    tmp_files: Dict[str, OrderedSet[pth.LocalPath]] = {}
    if file:
      self._extend(tmp_files, file)
    for suffix, files in kwargs.items():
      self._extend(tmp_files, files, suffix)
    self._files: immutabledict[str, Tuple[pth.LocalPath, ...]] = immutabledict({
        suffix: tuple(files) for suffix, files in tmp_files.items()
    })
    # TODO: Add Metric object for keeping metrics in-memory instead of reloading
    # them from serialized JSON files for merging.
    self._values = None
    self._validate()

  def _append(self,
              tmp_files,
              file: pth.LocalPath,
              suffix: Optional[str] = None) -> None:
    file_suffix_name = file.suffix[1:]
    if not suffix:
      suffix = file_suffix_name
    elif file_suffix_name != suffix:
      raise ValueError(
          f"Expected '.{suffix}' suffix, but got {repr(file.suffix)} "
          f"for {file}")
    if files_with_suffix := tmp_files.get(suffix):
      if file in files_with_suffix:
        raise DuplicateProbeResult(
            f"Cannot append file twice to ProbeResult: {file}")
      files_with_suffix.add(file)
    else:
      tmp_files[suffix] = OrderedSet((file,))

  def _extend(self,
              tmp_files,
              files: Iterable[pth.LocalPath],
              suffix: Optional[str] = None) -> None:
    for file in files:
      self._append(tmp_files, file, suffix)

  def get(self, suffix: str) -> pth.LocalPath:
    if files_with_suffix := self._files.get(suffix):
      if len(files_with_suffix) != 1:
        raise ValueError(f"Expected exactly one file with suffix {suffix}, "
                         f"but got {files_with_suffix}")
      return files_with_suffix[0]
    raise ValueError(f"No files with suffix '.{suffix}'. "
                     f"Options are {tuple(self._files.keys())}")

  def get_all(self, suffix: str) -> List[pth.LocalPath]:
    if files_with_suffix := self._files.get(suffix):
      return list(files_with_suffix)
    return []

  @property
  def is_empty(self) -> bool:
    return not self._url_list and not self._files

  @property
  def is_remote(self) -> bool:
    return False

  def __bool__(self) -> bool:
    return not self.is_empty

  def __eq__(self, other: Any) -> bool:
    if not isinstance(other, ProbeResult):
      return False
    if self is other:
      return True
    if self._files != other._files:
      return False
    return self._url_list == other._url_list

  def merge(self, other: ProbeResult) -> ProbeResult:
    if self.is_empty:
      return other
    if other.is_empty:
      return self
    return LocalProbeResult(
        url=self.url_list + other.url_list,
        file=self.file_list + other.file_list)

  def _validate(self) -> None:
    for path in self.all_files():
      if not path.exists():
        raise ValueError(f"ProbeResult path does not exist: {path}")

  def to_json(self) -> JsonDict:
    result: JsonDict = {}
    if self._url_list:
      result["url"] = self._url_list
    for suffix, files in self._files.items():
      result[suffix] = list(map(str, files))
    return result

  @property
  def has_files(self) -> bool:
    return bool(self._files)

  def all_files(self) -> Iterable[pth.LocalPath]:
    for files in self._files.values():
      yield from files

  @property
  def url(self) -> str:
    if len(self._url_list) != 1:
      raise ValueError("ProbeResult has multiple URLs.")
    return self._url_list[0]

  @property
  def url_list(self) -> List[str]:
    return list(self._url_list)

  @property
  def file(self) -> pth.LocalPath:
    if len(self._files) > 1:
      raise ValueError("ProbeResult has more than one file.")
    for suffix in self._files:
      return self.get(suffix)
    raise ValueError("ProbeResult has no files.")

  @property
  def file_list(self) -> List[pth.LocalPath]:
    return list(self.all_files())

  @property
  def json(self) -> pth.LocalPath:
    return self.get("json")

  @property
  def json_list(self) -> List[pth.LocalPath]:
    return self.get_all("json")

  @property
  def csv(self) -> pth.LocalPath:
    return self.get("csv")

  @property
  def csv_list(self) -> List[pth.LocalPath]:
    return self.get_all("csv")


class EmptyProbeResult(ProbeResult):

  def __init__(self) -> None:
    super().__init__()

  def __bool__(self) -> bool:
    return False


class LocalProbeResult(ProbeResult):
  """LocalProbeResult can be used for files that are always available on the
  runner/local machine."""

  def __init__(self,
               url: Optional[Iterable[str]] = None,
               file: Optional[Iterable[pth.LocalPath]] = None,
               **kwargs: Iterable[pth.LocalPath]):
    super().__init__(url, file, **kwargs)


class BrowserProbeResult(ProbeResult):
  """BrowserProbeResult are stored on the device where the browser runs.
  Result files will be automatically transferred to the local run's results
  folder.
  """

  def __init__(self,
               result_origin: ResultOrigin,
               url: Optional[Iterable[str]] = None,
               file: Optional[Iterable[pth.RemotePath]] = None,
               **kwargs: Iterable[pth.RemotePath]):
    self._browser_file = file
    local_file: Optional[Iterable[pth.LocalPath]] = None
    local_kwargs: Dict[str, Iterable[pth.LocalPath]] = {}
    self._is_remote = result_origin.is_remote
    if self._is_remote:
      if file:
        local_file = self._copy_files(result_origin, file)
      for suffix_name, files in kwargs.items():
        local_kwargs[suffix_name] = self._copy_files(result_origin, files)
    else:
      # Keep local files as is.
      local_file = cast(Iterable[pth.LocalPath], file)
      local_kwargs = cast(Dict[str, Iterable[pth.LocalPath]], kwargs)

    super().__init__(url, local_file, **local_kwargs)

  @property
  def is_remote(self) -> bool:
    return self._is_remote

  def _copy_files(self, result_origin: ResultOrigin,
                  paths: Iterable[pth.RemotePath]) -> Iterable[pth.LocalPath]:
    assert paths, "Got no remote paths to copy."
    # Copy result files from remote tmp dir to local results dir
    browser_platform = result_origin.browser_platform
    remote_tmp_dir = result_origin.browser_tmp_dir
    out_dir = result_origin.out_dir
    local_result_paths: List[pth.LocalPath] = []
    for remote_path in paths:
      try:
        relative_path = remote_path.relative_to(remote_tmp_dir)
      except ValueError:
        logging.debug(
            "Browser result is not in browser tmp dir: "
            "only using the name of '%s'", remote_path)
        relative_path = result_origin.runner_platform.local_path(
            remote_path.name)
      local_result_path = out_dir / relative_path
      browser_platform.rsync(remote_path, local_result_path)
      assert local_result_path.exists(), "Failed to copy result file."
      local_result_paths.append(local_result_path)
    return local_result_paths


class ProbeResultDict:
  """
  Maps Probes to their result files Paths.
  """

  def __init__(self, path: pth.RemotePath) -> None:
    self._path = path
    self._dict: Dict[str, ProbeResult] = {}

  def __setitem__(self, probe: Probe, result: ProbeResult) -> None:
    assert isinstance(result, ProbeResult)
    self._dict[probe.name] = result

  def __getitem__(self, probe: Probe) -> ProbeResult:
    name = probe.name
    if name not in self._dict:
      raise KeyError(f"No results for probe='{name}'")
    return self._dict[name]

  def __contains__(self, probe: Probe) -> bool:
    return probe.name in self._dict

  def __bool__(self) -> bool:
    return bool(self._dict)

  def __len__(self) -> int:
    return len(self._dict)

  def get(self, probe: Probe, default: Any = None) -> ProbeResult:
    return self._dict.get(probe.name, default)

  def get_by_name(self, name: str, default: Any = None) -> ProbeResult:
    # Debug helper only.
    # Use bracket `results[probe]` or `results.get(probe)` instead.
    return self._dict.get(name, default)

  def to_json(self) -> JsonDict:
    data: JsonDict = {}
    for probe_name, results in self._dict.items():
      if isinstance(results, (pth.RemotePath, str)):
        data[probe_name] = str(results)
      else:
        if results.is_empty:
          if not probe_name.startswith(INTERNAL_NAME_PREFIX):
            logging.debug("probe=%s did not produce any data.", probe_name)
          data[probe_name] = None
        else:
          data[probe_name] = results.to_json()
    return data
