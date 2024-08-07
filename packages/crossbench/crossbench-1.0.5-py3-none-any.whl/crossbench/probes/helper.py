# Copyright 2022 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import annotations

import csv
from typing import (TYPE_CHECKING, Any, Callable, Dict, Final, List, Optional,
                    Sequence, Set, Tuple)

if TYPE_CHECKING:
  from crossbench.path import LocalPath

INTERNAL_NAME_PREFIX: Final[str] = "cb."

KeyFnType = Callable[[Tuple[str, ...]], Optional[str]]


def _default_flatten_key_fn(path: Tuple[str, ...]) -> str:
  return "/".join(path)


class Flatten:
  """
  Creates a sorted flat list of (key-path, Metric) from hierarchical data.

  input = {"a" : {"aa1":1, "aa2":2}, "b": 12 }
  Flatten(input).data == {
    "a/aa1":  1,
    "a/aa2":  2,
    "b":     12,
  }
  """
  _key_fn: KeyFnType
  _accumulator: Dict[str, Any]

  def __init__(self,
               *args: Dict,
               key_fn: Optional[KeyFnType] = None,
               sort: bool = True) -> None:
    """_summary_

    Args:
        *args (optional): Optional hierarchical data to be flattened
        key_fn (optional): Maps property paths (Tuple[str,...]) to strings used
          as final result keys, or None to skip property paths.
    """
    self._accumulator = {}
    self._key_fn = key_fn or _default_flatten_key_fn
    self._sort = sort
    self.append(*args)

  @property
  def data(self) -> Dict[str, Any]:
    if not self._sort:
      return dict(self._accumulator)
    items = sorted(self._accumulator.items(), key=lambda item: item[0])
    return dict(items)

  def append(self, *args: Dict, ignore_toplevel: bool = False) -> None:
    toplevel_path: Tuple[str, ...] = tuple()
    for merged_data in args:
      self._flatten(toplevel_path, merged_data, ignore_toplevel)

  def _is_leaf_item(self, item: Any) -> bool:
    if isinstance(item, (str, float, int, list)):
      return True
    if "values" in item and isinstance(item["values"], list):
      return True
    return False

  def _flatten(self,
               parent_path: Tuple[str, ...],
               data,
               ignore_toplevel: bool = False) -> None:
    for name, item in data.items():
      if item is None:
        continue
      path = parent_path + (name,)
      if self._is_leaf_item(item):
        if ignore_toplevel and parent_path == ():
          continue
        key = self._key_fn(path)
        if key is None:
          continue
        assert isinstance(key, str)
        if key in self._accumulator:
          raise ValueError(f"Duplicate key='{key}' path={path}")
        self._accumulator[key] = item
      else:
        self._flatten(path, item)


def _ljust_row(sequence: List, n: int, fill_value: Any = None) -> List:
  return sequence + ([fill_value] * (n - len(sequence)))


def merge_csv(csv_list: Sequence[LocalPath],
              headers: Optional[List[str]] = None,
              row_header_len: int = 1,
              delimiter: str = "\t") -> List[List[Any]]:
  """
  Merge multiple CSV files.
  File 1:
    Header,     Col Header 1.1, Col Header  1.2
    ...
    Row Header, Data 1.1,       Data 1.2

  File 2:
    Header,     Col Header 2.1,
    ...
    Row Header, Data 2.1,

  The first Col has to contain the same data:

  Merged:
    Header,     Col Header 1.1, Col Header 1.2,  Col Header 2.1,
    ...
    Row Header, Data 1.1,       Data 1.2,        Data 2.1,


  If no column header is available, filename_as_header=True can be used.

  Merged with file name header:
            , File 1,           , File 2,
  Row Header, Data 1.1, Data 1.2, Data 2.1, Data 2.2
  """
  # Fill in the header column taken from the first file
  table: List[List[Any]] = []
  if headers:
    table_headers = [None] * row_header_len
  else:
    table_headers = []

  # Initial row-headers from the first csv file.
  known_row_headers: Set[Tuple[str, ...]] = set()
  _merge_csv_prepare_row_headers(table, known_row_headers, csv_list[0],
                                 row_header_len, delimiter)

  table_row_len: int = row_header_len
  for csv_file in csv_list:
    with csv_file.open(encoding="utf-8") as f:
      csv_data = list(csv.reader(f, delimiter=delimiter))
    table_row_len = _merge_csv_append(csv_data, table, table_headers,
                                      row_header_len, headers,
                                      known_row_headers, table_row_len)

  if table_headers:
    return [table_headers] + table
  return table


def _merge_csv_prepare_row_headers(table: List[List[Any]],
                                   known_row_headers: Set[Tuple[str, ...]],
                                   csv_file: LocalPath, row_header_len: int,
                                   delimiter: str):
  with csv_file.open(encoding="utf-8") as first_file:
    for csv_row in csv.reader(first_file, delimiter=delimiter):
      assert csv_row, "Mergeable CSV files must have row names."
      row_headers = csv_row[:row_header_len]
      table.append(row_headers)
      csv_row_header_key = tuple(row_headers)
      known_row_headers.add(csv_row_header_key)


def _merge_csv_append(csv_data: List[List[Any]], table: List[List[Any]],
                      table_headers, row_header_len: int, headers,
                      known_row_headers, table_row_len):
  # Find the max row width in added csv_data.
  max_csv_row_len = max(len(row) for row in csv_data) - row_header_len
  if table:
    table_row_len = len(table[0]) + max_csv_row_len
  else:
    table_row_len = max_csv_row_len

  if headers:
    col_header = [headers.pop(0)]
    table_headers.extend(_ljust_row(col_header, max_csv_row_len))

  # Pre-computed potential padding lists.
  skipped_table_row_padding = [None] * max_csv_row_len
  new_row_padding = [None] * (table_row_len - row_header_len - max_csv_row_len)

  table_index = 0
  for csv_row in csv_data:
    csv_row_header = tuple(csv_row[:row_header_len])
    csv_padded_row = _ljust_row(csv_row[row_header_len:], max_csv_row_len)

    if table_index >= len(table):
      # Append all additional rows to the end of the table.
      new_row = list(csv_row_header) + new_row_padding + csv_padded_row
      table.append(new_row)
      table_index += 1
      continue

    table_row = table[table_index]
    table_row_header = tuple(table_row[:row_header_len])

    if table_row_header == csv_row_header:
      # Simple case, row-headers are matching the current table.
      table_row.extend(csv_padded_row)
      table_index += 1
      continue

    csv_row_header_key = tuple(csv_row_header)

    # csv_data does not contain the current table_row_header, continue
    # to find a proper insertion point:
    # - if the know the row-header exists, loop until we find the matching one,
    # - otherwise insert before the next row, whose row-header would be
    #   after csv_row_header when using alpha-compare
    try_insert_alpha_sorted = csv_row_header_key not in known_row_headers
    while True:
      table_row = table[table_index]
      table_row_header = tuple(table_row[:row_header_len])
      if table_row_header == csv_row_header:
        table_row.extend(csv_padded_row)
        break
      if try_insert_alpha_sorted and csv_row_header_key < table_row_header:
        new_row = list(csv_row_header) + new_row_padding + csv_padded_row
        # Try maintaining alpha-sorting by inserting before the next row.
        table.insert(table_index, new_row)
        known_row_headers.add(csv_row_header_key)
        break
      table_row.extend(skipped_table_row_padding)
      table_index += 1
      if table_index >= len(table):
        # Append all additional rows to the end of the table.
        new_row = list(csv_row_header) + new_row_padding + csv_padded_row
        table.append(new_row)
        break
    table_index += 1
  return table_row_len
