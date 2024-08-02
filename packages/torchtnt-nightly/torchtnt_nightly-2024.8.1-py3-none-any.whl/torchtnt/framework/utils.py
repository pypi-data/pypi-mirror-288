# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

import logging
from contextlib import contextmanager, nullcontext
from typing import ContextManager, Generator, Tuple, TypeVar

from torch.profiler import record_function
from torchtnt.framework.state import State

_logger: logging.Logger = logging.getLogger(__name__)
T = TypeVar("T")


@contextmanager
def get_timing_context(
    state: State, event_name: str
) -> Generator[Tuple[ContextManager, ContextManager], None, None]:
    """
    Returns a context manager that records an event to a :class:`~torchtnt.utils.timer.Timer` and to PyTorch Profiler.

    Args:
        state: an instance of :class:`~torchtnt.framework.state.State`
        event_name: string identifier to use for timing
    """
    timer_context = (
        state.timer.time(event_name) if state.timer is not None else nullcontext()
    )
    profiler_context = record_function(event_name)
    with timer_context, profiler_context:
        yield (timer_context, profiler_context)
