# Copyright 2024 The Chromium Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import annotations

from crossbench.benchmarks.loading import action as i_action
from crossbench.benchmarks.loading.action_runner.basic_action_runner import \
    BasicActionRunner
from crossbench.runner.run import Run

class ChromeOSInputActionRunner(BasicActionRunner):

    def tap(self, run: Run, action: i_action.TapAction) -> None:
        raise NotImplementedError(
            "Tap action not implemented in ChromeOSInputActionRunner")

    def swipe(self, run: Run, action: i_action.SwipeAction) -> None:
        raise NotImplementedError(
            "Swipe action not implemented in ChromeOSInputActionRunner")
