# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

import logging
from typing import Dict, Iterable, Optional, Protocol, runtime_checkable, TypeVar

import torch
import torch.nn as nn
from torch.nn.parallel.distributed import DistributedDataParallel

_EXPORT_UTILS_AVAIL = True
try:
    from torch.ao.quantization.pt2e.export_utils import model_is_exported
except Exception:
    _EXPORT_UTILS_AVAIL = False

from torchtnt.utils.progress import Progress

_logger: logging.Logger = logging.getLogger(__name__)
T = TypeVar("T")


# Helper functions common across the loops
def _is_done(
    progress: Progress, max_epochs: Optional[int], max_steps: Optional[int]
) -> bool:
    return (max_steps is not None and progress.num_steps_completed >= max_steps) or (
        max_epochs is not None and progress.num_epochs_completed >= max_epochs
    )


def _is_epoch_done(
    progress: Progress, max_steps_per_epoch: Optional[int], max_steps: Optional[int]
) -> bool:
    return (max_steps is not None and progress.num_steps_completed >= max_steps) or (
        max_steps_per_epoch is not None
        and progress.num_steps_completed_in_epoch >= max_steps_per_epoch
    )


def _reason_epoch_completed(
    progress: Progress,
    max_steps_per_epoch: Optional[int],
    max_steps: Optional[int],
    stop_iteration_reached: bool,
) -> str:
    current_epoch = progress.num_epochs_completed
    if stop_iteration_reached:
        return (
            f"Train epoch {current_epoch} ended as it reached end of train dataloader"
        )
    elif (
        max_steps_per_epoch is not None
        and progress.num_steps_completed_in_epoch >= max_steps_per_epoch
    ):
        return f"Train epoch {current_epoch} ended as max steps per epoch reached: {max_steps_per_epoch}"
    elif max_steps is not None and progress.num_steps_completed >= max_steps:
        return f"Train epoch {current_epoch} ended as max steps reached: {max_steps}"
    return f"Unable to determine reason for stopping train epoch {current_epoch}"


@runtime_checkable
class _DistributedSampler(Protocol):
    def set_epoch(self, epoch: int) -> None: ...


def _maybe_set_distributed_sampler_epoch(
    dataloader: Iterable[object],
    current_epoch: int,
) -> None:
    """Set epoch of distributed sampler in dataloader, if applicable.
    See: https://pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler
    """
    # Set current training epoch for any DistributedSampler in dataloader
    if isinstance(dataloader, torch.utils.data.DataLoader) and isinstance(
        dataloader.sampler,
        _DistributedSampler,
    ):
        dataloader.sampler.set_epoch(current_epoch)


def _set_module_training_mode(
    modules: Dict[str, nn.Module], mode: bool
) -> Dict[str, bool]:
    """Returns states to allow for a reset at the end of the loop."""
    prior_module_train_states = {}
    for name, module in modules.items():
        prior_module_train_states[name] = module.training
        is_ddp = isinstance(module, DistributedDataParallel)

        if _EXPORT_UTILS_AVAIL and model_is_exported(
            module.module if is_ddp else module
        ):
            if mode:
                module = torch.ao.quantization.move_exported_model_to_train(
                    module.module if is_ddp else module
                )
            else:
                module = torch.ao.quantization.move_exported_model_to_eval(
                    module.module if is_ddp else module
                )
        else:
            module.train(mode)

    return prior_module_train_states


def _reset_module_training_mode(
    modules: Dict[str, nn.Module], prior_modes: Dict[str, bool]
) -> None:
    # Reset training mode for modules at the end of the epoch
    # This ensures that side-effects made by the loop are reset before
    # returning back to the user
    for name, module in modules.items():
        if name in prior_modes:
            module.train(prior_modes[name])


def _log_api_usage(entry_point: str) -> None:
    torch._C._log_api_usage_once(f"torchtnt.framework.{entry_point}")
