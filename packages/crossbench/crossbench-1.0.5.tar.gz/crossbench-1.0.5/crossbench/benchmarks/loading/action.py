# Copyright 2023 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import annotations

import abc
import argparse
import datetime as dt
import enum
import json
import logging
from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Type, TypeVar

from crossbench import cli_helper, exception
from crossbench.benchmarks.loading.action_runner.base import ActionRunner
from crossbench.config import ConfigEnum, ConfigObject, ConfigParser

if TYPE_CHECKING:
  import crossbench.path as pth
  from crossbench.runner.run import Run
  from crossbench.types import JsonDict


@enum.unique
class ActionType(ConfigEnum):
  GET: "ActionType" = ("get", "Open a URL")
  JS: "ActionType" = ("js", "Run a custom script")
  WAIT: "ActionType" = ("wait", "Wait for a given time")
  SCROLL: "ActionType" = ("scroll", "Scroll on page")
  CLICK: "ActionType" = ("click", "Click on element")
  TAP: "ActionType" = ("tap", "Tap on element")
  SWIPE: "ActionType" = ("swipe", "Swipe on screen")
  WAIT_FOR_ELEMENT: "ActionType" = ("wait_for_element",
                                    "Wait until element appears on the page")
  INJECT_NEW_DOCUMENT_SCRIPT: "ActionType" = ("inject_new_document_script", (
      "Evaluates given script in every frame upon creation "
      "(before loading frame's scripts). "
      "Only supported in chromium-based browsers."))


class ActionTypeConfigParser(ConfigParser):
  """Custom ConfigParser for ActionType that works on
  Action Configs. This way we can pop the 'value' or 'type' key from the
  config dict."""

  def __init__(self):
    super().__init__("ActionType parser", ActionType)
    self.add_argument(
        "action",
        aliases=("type",),
        type=cli_helper.parse_non_empty_str,
        required=True)

  def new_instance_from_kwargs(self, kwargs: Dict[str, Any]) -> ActionType:
    return ActionType(kwargs["action"])


_ACTION_TYPE_CONFIG_PARSER = ActionTypeConfigParser()


@enum.unique
class ButtonClick(ConfigEnum):
  LEFT: "ButtonClick" = ("left", "Press left mouse button")
  RIGHT: "ButtonClick" = ("right", "Press right mouse button")
  MIDDLE: "ButtonClick" = ("middle", "Press middle mouse button")


ACTION_TIMEOUT = dt.timedelta(seconds=20)

ActionT = TypeVar("ActionT", bound="Action")


class Action(ConfigObject, metaclass=abc.ABCMeta):
  TYPE: ActionType = ActionType.GET

  @classmethod
  def loads(cls: Type[ActionT], value: str) -> ActionT:
    raise NotImplementedError("Not supported")

  @classmethod
  def load_dict(cls: Type[ActionT], config: Dict[str, Any]) -> ActionT:
    action_type: ActionType = _ACTION_TYPE_CONFIG_PARSER.parse(config)
    action_cls: Type[ActionT] = ACTIONS[action_type]
    with exception.annotate_argparsing(
        f"Parsing Action details  ...{{ action: \"{action_type}\", ...}}:"):
      action = action_cls.config_parser().parse(config)
    assert isinstance(action, cls), f"Expected {cls} but got {type(action)}"
    return action

  @classmethod
  def config_parser(cls: Type[ActionT]) -> ConfigParser[ActionT]:
    parser = ConfigParser(f"{cls.__name__} parser", cls)
    parser.add_argument(
        "timeout",
        type=cli_helper.Duration.parse_non_zero,
        default=ACTION_TIMEOUT)
    return parser

  def __init__(self, timeout: dt.timedelta = ACTION_TIMEOUT):
    self._timeout: dt.timedelta = timeout
    self.validate()

  @property
  def duration(self) -> dt.timedelta:
    return dt.timedelta(milliseconds=10)

  @property
  def timeout(self) -> dt.timedelta:
    return self._timeout

  @property
  def has_timeout(self) -> bool:
    return self._timeout != dt.timedelta.max

  @abc.abstractmethod
  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    pass

  def validate(self) -> None:
    if self._timeout.total_seconds() < 0:
      raise ValueError(
          f"{self}.timeout should be positive, but got {self.timeout}")

  def to_json(self) -> JsonDict:
    return {"type": str(self.TYPE), "timeout": self.timeout.total_seconds()}

  def __str__(self) -> str:
    return type(self).__name__

  def __eq__(self, other: object) -> bool:
    if isinstance(other, Action):
      return self.to_json() == other.to_json()
    return False


@enum.unique
class ReadyState(ConfigEnum):
  """See https://developer.mozilla.org/en-US/docs/Web/API/Document/readyState"""
  # Non-blocking:
  ANY: "ReadyState" = ("any", "Ignore ready state")
  # Blocking (on dom event):
  LOADING: "ReadyState" = ("loading", "The document is still loading.")
  INTERACTIVE: "ReadyState" = ("interactive",
                               "The document has finished loading "
                               "but sub-resources might still be loading")
  COMPLETE: "ReadyState" = (
      "complete", "The document and all sub-resources have finished loading.")


@enum.unique
class WindowTarget(ConfigEnum):
  """See https://developer.mozilla.org/en-US/docs/Web/API/Window/open"""
  SELF: "WindowTarget" = ("_self", "The current browsing context. (Default)")
  BLANK: "WindowTarget" = (
      "_blank", "Usually a new tab, but users can configure browsers "
      "to open a new window instead.")
  PARENT: "WindowTarget" = ("_parent",
                            "The parent browsing context of the current one. "
                            "If no parent, behaves as _self.")
  TOP: "WindowTarget" = (
      "_top", "The topmost browsing context "
      "(the 'highest' context that's an ancestor of the current one). "
      "If no ancestors, behaves as _self.")


class BaseDurationAction(Action):

  def __init__(self,
               duration: dt.timedelta,
               timeout: dt.timedelta = ACTION_TIMEOUT) -> None:
    self._duration: dt.timedelta = duration
    super().__init__(timeout)

  @property
  def duration(self) -> dt.timedelta:
    return self._duration

  def validate(self) -> None:
    super().validate()
    self.validate_duration()

  def validate_duration(self) -> None:
    if self.duration.total_seconds() <= 0:
      raise ValueError(
          f"{self}.duration should be positive, but got {self.duration}")

  def to_json(self) -> JsonDict:
    details = super().to_json()
    details["duration"] = self.duration.total_seconds()
    return details


class GetAction(BaseDurationAction):
  TYPE: ActionType = ActionType.GET

  @classmethod
  def config_parser(cls: Type[ActionT]) -> ConfigParser[ActionT]:
    parser = super().config_parser()
    parser.add_argument("url", type=cli_helper.parse_url_str, required=True)
    parser.add_argument(
        "duration", type=cli_helper.Duration.parse_zero, default=dt.timedelta())
    parser.add_argument(
        "ready_state", type=ReadyState.parse, default=ReadyState.ANY)
    parser.add_argument(
        "target", type=WindowTarget.parse, default=WindowTarget.SELF)
    return parser

  def __init__(self,
               url: str,
               duration: dt.timedelta = dt.timedelta(),
               timeout: dt.timedelta = ACTION_TIMEOUT,
               ready_state: ReadyState = ReadyState.ANY,
               target: WindowTarget = WindowTarget.SELF):
    if not url:
      raise ValueError(f"{self}.url is missing")
    self._url: str = url
    self._ready_state = ready_state
    self._target = target
    super().__init__(duration, timeout)

  def validate_duration(self) -> None:
    if self.ready_state != ReadyState.ANY:
      if self.duration != dt.timedelta():
        raise ValueError(
            f"Expected empty duration with ReadyState {self.ready_state} "
            f"but got: {self.duration}")
      self._duration = dt.timedelta()

  @property
  def url(self) -> str:
    return self._url

  @property
  def ready_state(self) -> ReadyState:
    return self._ready_state

  @property
  def duration(self) -> dt.timedelta:
    return self._duration

  @property
  def target(self) -> WindowTarget:
    return self._target

  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    action_runner.get(run, self)

  def to_json(self) -> JsonDict:
    details = super().to_json()
    details["url"] = self.url
    details["ready_state"] = str(self.ready_state)
    details["target"] = str(self.target)
    return details


class DurationAction(BaseDurationAction):
  TYPE: ActionType = ActionType.WAIT

  @classmethod
  def config_parser(cls: Type[ActionT]) -> ConfigParser[ActionT]:
    parser = super().config_parser()
    parser.add_argument(
        "duration", type=cli_helper.Duration.parse_non_zero, required=True)
    return parser


class WaitAction(DurationAction):
  TYPE: ActionType = ActionType.WAIT

  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    action_runner.wait(run, self)


class ScrollAction(BaseDurationAction):
  TYPE: ActionType = ActionType.SCROLL

  @classmethod
  def config_parser(cls: Type[ActionT]) -> ConfigParser[ActionT]:
    parser = super().config_parser()
    parser.add_argument("distance", type=cli_helper.parse_float, default=500)
    parser.add_argument(
        "duration",
        type=cli_helper.Duration.parse_non_zero,
        default=dt.timedelta(seconds=1))
    return parser

  def __init__(self,
               distance: float = 500.0,
               duration: dt.timedelta = dt.timedelta(seconds=1),
               timeout: dt.timedelta = ACTION_TIMEOUT) -> None:
    self._distance = distance
    super().__init__(duration, timeout)

  @property
  def distance(self) -> float:
    return self._distance

  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    action_runner.scroll(run, self)

  def validate(self) -> None:
    super().validate()
    if not self.distance:
      raise ValueError(f"{self}.distance is not provided")

  def to_json(self) -> JsonDict:
    details = super().to_json()
    details["distance"] = str(self.distance)
    return details


class ClickAction(Action):
  TYPE: ActionType = ActionType.CLICK

  @classmethod
  def config_parser(cls: Type[ActionT]) -> ConfigParser[ActionT]:
    parser = super().config_parser()
    parser.add_argument(
        "selector", type=cli_helper.parse_non_empty_str, required=True)
    parser.add_argument("required", type=cli_helper.parse_bool, default=False)
    parser.add_argument(
        "scroll_into_view", type=cli_helper.parse_bool, default=False)
    return parser

  def __init__(self,
               selector: str,
               required: bool = False,
               scroll_into_view: bool = False,
               timeout: dt.timedelta = ACTION_TIMEOUT):
    # TODO: convert to custom selector object.
    self._selector = selector
    self._scroll_into_view: bool = scroll_into_view
    self._required: bool = required
    super().__init__(timeout)

  @property
  def scroll_into_view(self) -> bool:
    return self._scroll_into_view

  @property
  def selector(self) -> str:
    return self._selector

  @property
  def required(self) -> bool:
    return self._required

  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    action_runner.click(run, self)

  def validate(self) -> None:
    super().validate()
    if not self.selector:
      raise ValueError(f"{self}.selector is missing.")

  def to_json(self) -> JsonDict:
    details = super().to_json()
    details["selector"] = self.selector
    details["required"] = self.required
    details["scroll_into_view"] = self.scroll_into_view
    return details


class TapAction(Action):
  TYPE: ActionType = ActionType.TAP

  @classmethod
  def config_parser(cls: Type[ActionT]) -> ConfigParser[ActionT]:
    parser = super().config_parser()
    parser.add_argument("selector", type=cli_helper.parse_non_empty_str)
    parser.add_argument("x", type=cli_helper.parse_positive_zero_int)
    parser.add_argument("y", type=cli_helper.parse_positive_zero_int)
    return parser

  def __init__(self,
               selector: Optional[str] = None,
               x: Optional[int] = None,
               y: Optional[int] = None,
               timeout: dt.timedelta = ACTION_TIMEOUT):
    # TODO: convert to custom selector object.
    self._selector = selector
    self._x = x
    self._y = y
    super().__init__(timeout)

  @property
  def selector(self) -> Optional[str]:
    return self._selector

  @property
  def x(self) -> Optional[int]:
    return self._x

  @property
  def y(self) -> Optional[int]:
    return self._y

  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    action_runner.tap(run, self)

  def validate(self) -> None:
    super().validate()
    if self.selector:
      if self.x is not None or self.y is not None:
        raise ValueError("Only one is allowed: either selector or coordinates")
    else:
      if self.x is None or self.y is None:
        raise ValueError("Both selector and coordinates are missing")

  def to_json(self) -> JsonDict:
    details = super().to_json()
    if self.selector:
      details["selector"] = self.selector
    else:
      details["x"] = self.x
      details["y"] = self.y
    return details


class SwipeAction(DurationAction):
  TYPE: ActionType = ActionType.SWIPE

  @classmethod
  def config_parser(cls: Type[ActionT]) -> ConfigParser[ActionT]:
    parser = super().config_parser()
    parser.add_argument("startx", type=cli_helper.parse_int, required=True)
    parser.add_argument("starty", type=cli_helper.parse_int, required=True)
    parser.add_argument("endx", type=cli_helper.parse_int, required=True)
    parser.add_argument("endy", type=cli_helper.parse_int, required=True)
    return parser

  def __init__(self,
               startx: int,
               starty: int,
               endx: int,
               endy: int,
               duration: dt.timedelta = dt.timedelta(seconds=1),
               timeout: dt.timedelta = ACTION_TIMEOUT) -> None:
    self._startx: int = startx
    self._starty: int = starty
    self._endx: int = endx
    self._endy: int = endy
    super().__init__(duration, timeout)

  @property
  def startx(self) -> int:
    return self._startx

  @property
  def starty(self) -> int:
    return self._starty

  @property
  def endx(self) -> int:
    return self._endx

  @property
  def endy(self) -> int:
    return self._endy

  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    action_runner.swipe(run, self)

  def to_json(self) -> JsonDict:
    details = super().to_json()
    details["startx"] = self._startx
    details["starty"] = self._starty
    details["endx"] = self._endx
    details["endy"] = self._endy
    return details


class WaitForElementAction(Action):
  TYPE: ActionType = ActionType.WAIT_FOR_ELEMENT

  @classmethod
  def config_parser(cls: Type[ActionT]) -> ConfigParser[ActionT]:
    parser = super().config_parser()
    parser.add_argument(
        "selector", type=cli_helper.parse_non_empty_str, required=True)
    return parser

  def __init__(self, selector: str, timeout: dt.timedelta = ACTION_TIMEOUT):
    self._selector = selector
    super().__init__(timeout)

  @property
  def selector(self) -> str:
    return self._selector

  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    action_runner.wait_for_element(run, self)

  def validate(self) -> None:
    super().validate()
    if not self.selector:
      raise ValueError(f"{self}.selector is missing.")

  def to_json(self) -> JsonDict:
    details = super().to_json()
    details["selector"] = self.selector
    return details


def parse_replacement_dict(value: Any) -> Dict[str, str]:
  dict_value = cli_helper.parse_dict(value)
  for replace_key, replace_value in dict_value.items():
    with exception.annotate_argparsing(
        f"Parsing ...[{repr(replace_key)}] = {repr(value)}"):
      cli_helper.parse_non_empty_str(replace_key, "replacement key")
      cli_helper.parse_str(replace_value, "replacement value")
  return dict_value


class JsAction(Action):
  TYPE: ActionType = ActionType.JS

  @classmethod
  def config_parser(cls: Type[ActionT]) -> ConfigParser[ActionT]:
    parser = super().config_parser()
    parser.add_argument("script", type=cli_helper.parse_non_empty_str)
    parser.add_argument(
        "script_path",
        aliases=("path",),
        type=cli_helper.parse_existing_file_path)
    parser.add_argument(
        "replacements", aliases=("replace",), type=parse_replacement_dict)
    return parser

  def __init__(self,
               script: Optional[str],
               script_path: Optional[pth.LocalPath],
               replacements: Optional[Dict[str, str]] = None,
               timeout: dt.timedelta = ACTION_TIMEOUT) -> None:
    self._original_script = script
    self._script_path = script_path
    self._script = ""
    if bool(script) == bool(script_path):
      raise ValueError(
          f"One of {self}.script or {self}.script_path, but not both, "
          "have to specified. ")
    if script:
      self._script = script
    elif script_path:
      self._script = script_path.read_text()
      logging.debug("Loading script from %s: %s", script_path, script)
      # TODO: support argument injection into shared file script.
    self._replacements = replacements
    if replacements:
      for key, value in replacements.items():
        self._script = self._script.replace(key, value)
    super().__init__(timeout)

  @property
  def script(self) -> str:
    return self._script

  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    action_runner.js(run, self)

  def validate(self) -> None:
    super().validate()
    if not self.script:
      raise ValueError(
          f"{self}.script is missing or the provided script file is empty.")

  def to_json(self) -> JsonDict:
    details = super().to_json()
    if self._original_script:
      details["script"] = self._original_script
    if self._script_path:
      details["script_path"] = str(self._script_path)
    if self._replacements:
      details["replacements"] = self._replacements
    return details


class InjectNewDocumentScriptAction(JsAction):
  TYPE: ActionType = ActionType.INJECT_NEW_DOCUMENT_SCRIPT

  def run_with(self, run: Run, action_runner: ActionRunner) -> None:
    action_runner.inject_new_document_script(run, self)


ACTIONS_TUPLE: Tuple[Type[Action], ...] = (
    ClickAction,
    TapAction,
    GetAction,
    JsAction,
    ScrollAction,
    SwipeAction,
    WaitAction,
    WaitForElementAction,
    InjectNewDocumentScriptAction,
)

ACTIONS: Dict[ActionType, Type] = {
    action_cls.TYPE: action_cls for action_cls in ACTIONS_TUPLE
}

assert len(ACTIONS_TUPLE) == len(ACTIONS), "Non unique Action.TYPE present"
