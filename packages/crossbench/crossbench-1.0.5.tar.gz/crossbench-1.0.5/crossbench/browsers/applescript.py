# Copyright 2023 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import annotations

import abc
import json
import logging
import os
import subprocess
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Tuple

import psutil

from crossbench import helper, plt
from crossbench.browsers.browser import Browser
from crossbench.env import HostEnvironment, ValidationError

if TYPE_CHECKING:
  import datetime as dt

  from crossbench.path import RemotePath
  from crossbench.runner.groups import BrowserSessionRunGroup
  from crossbench.runner.run import Run
  from crossbench.runner.runner import Runner


class AppleScript:

  @classmethod
  def with_args(cls, app_path: RemotePath, apple_script: str,
                **kwargs) -> Tuple[str, List[str]]:
    variables = []
    replacements = {}
    args: List[str] = []
    for variable, value in kwargs.items():
      args.append(value)
      unique_variable = f"cb_input_{variable}"
      replacements[variable] = unique_variable
      variables.append(f"set {unique_variable} to (item {len(args)} of argv)")
    variables_str = "\n".join(variables)
    formatted_script = apple_script.strip() % replacements
    wrapper = f"""
      {variables_str}
      tell application "{app_path}"
        {formatted_script}
      end tell
    """
    return wrapper.strip(), args

  @classmethod
  def js_script_with_args(cls, script: str, args: Sequence[object]) -> str:
    """Create a script that returns [JSON.stringify(result), true] on success,
    and [exception.toString(), false] when failing."""
    args_str: str = json.dumps(args)
    script = """JSON.stringify((function exceptionWrapper(){
        try {
          return [(function(...arguments){%(script)s}).apply(window, %(args_str)s), true]
        } catch(e) {
          return [e + "", false]
        }
      })())""" % {
        "script": script,
        "args_str": args_str
    }
    return script.strip()

  class JavaScriptFromAppleScriptException(ValueError):
    pass


def try_get_parent_app_name(platform: plt.Platform) -> str:
  if platform.is_remote:
    return ""
  launched_apps: Dict[str, str] = {}
  try:
    for line in platform.sh_stdout("launchctl", "list").splitlines():
      parts = line.split()
      if len(parts) == 3:
        pid, _, label = parts
        # Input:  "application.com.google.Chrome.46262139.72133274"
        # Output: "Chrome"
        label_parts = label.split(".")
        if len(label_parts) <= 3:
          continue
        launched_apps[pid] = label_parts[3]
  except Exception as e:
    logging.debug("Could not list all parents: %s", e)
    return ""
  if not launched_apps:
    logging.debug("Could not find any apps")
    return ""
  try:
    for parent in psutil.Process(os.getpid()).parents():
      if label := launched_apps.get(str(parent.pid), ""):
        return label
  except Exception as e:
    logging.debug("Could not find parent parent app process: %s", e)
  return ""


SYSTEM_EVENTS_CHECK = (
    'tell application "System Events" to log (count of windows)')

class AppleScriptBrowser(Browser, metaclass=abc.ABCMeta):
  APPLE_SCRIPT_ALLOW_JS_MENU: str = ""
  APPLE_SCRIPT_JS_COMMAND: str = ""
  APPLE_SCRIPT_SET_URL: str = ""

  _browser_process: subprocess.Popen

  def _exec_apple_script(self, apple_script: str, **kwargs) -> Any:
    assert self.platform.is_macos, (
        f"Sorry, f{self.__class__} is only supported on MacOS for now")
    wrapper_script, args = AppleScript.with_args(self.app_path, apple_script,
                                                 **kwargs)
    return self.platform.exec_apple_script(wrapper_script, *args)

  def validate_env(self, env: HostEnvironment) -> None:
    super().validate_env(env)
    self._check_system_events_allowed(env)

  def start(self, session: BrowserSessionRunGroup) -> None:
    assert not self._is_running
    # Start process directly
    startup_flags = self._get_browser_flags_for_session(session)
    self._log_browser_start(startup_flags)
    self._browser_process = self.platform.popen(
        self.path, *startup_flags, shell=False)
    if self._browser_process.poll():
      raise ValueError("Could not start browser process.")
    self._pid = self._browser_process.pid
    self.platform.sleep(3)
    self._exec_apple_script("activate")
    self._setup_window()
    self._check_js_from_apple_script_allowed(session.runner)

  def _check_system_events_allowed(self, env: HostEnvironment) -> None:
    try:
      self._exec_apple_script(SYSTEM_EVENTS_CHECK)
    except plt.SubprocessError as e:
      logging.error("Not allowed to run AppleScript and send System Events!")
      logging.debug("    SubprocessError: %s", e)
      app_name = try_get_parent_app_name(self.platform) or "parent"
      env.handle_warning(
          f"Enable the 'System Events' permission for the {app_name} App. \n"
          "  See 'System Settings' > 'Privacy & Security' > 'Automation'.\n")
    try:
      self._exec_apple_script(SYSTEM_EVENTS_CHECK)
    except plt.SubprocessError as e:
      raise ValidationError(
          " Not allowed to run AppleScript and send System Events!") from e

  def _check_js_from_apple_script_allowed(self, runner: Runner) -> None:
    try:
      self.js(runner, "return 1")
    except plt.SubprocessError as e:
      logging.error("Browser does not allow JS from AppleScript!")
      logging.debug("    SubprocessError: %s", e)
      runner.env.handle_warning("Enable JavaScript from Apple Script Events: "
                                f"'{self.APPLE_SCRIPT_ALLOW_JS_MENU}'")
    try:
      self.js(runner, "return 1;")
    except plt.SubprocessError as e:
      raise ValidationError(
          " JavaScript from Apple Script Events was not enabled") from e
    self._is_running = True

  @abc.abstractmethod
  def _setup_window(self) -> None:
    pass

  def js(
      self,
      runner: Runner,
      script: str,
      timeout: Optional[dt.timedelta] = None,
      arguments: Sequence[object] = ()
  ) -> Any:
    del runner, timeout
    js_script = AppleScript.js_script_with_args(script, arguments)
    json_result: str = self._exec_apple_script(
        self.APPLE_SCRIPT_JS_COMMAND.strip(), js_script=js_script).rstrip()
    result, is_success = json.loads(json_result)
    if not is_success:
      raise AppleScript.JavaScriptFromAppleScriptException(result)
    return result

  def show_url(self,
               runner: Runner,
               url: str,
               target: Optional[str] = None) -> None:
    del runner
    self._exec_apple_script(self.APPLE_SCRIPT_SET_URL, url=url)
    self.platform.sleep(0.5)

  def quit(self, runner: Runner) -> None:
    del runner
    self._exec_apple_script("quit")
    helper.wait_and_kill(self._browser_process)
