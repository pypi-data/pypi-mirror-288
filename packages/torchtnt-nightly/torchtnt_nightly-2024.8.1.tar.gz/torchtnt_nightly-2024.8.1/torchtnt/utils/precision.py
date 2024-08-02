#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

from typing import Mapping, Optional

import torch
from torch.cuda.amp.grad_scaler import GradScaler as CudaGradScaler

try:
    from torch.amp.grad_scaler import GradScaler
except Exception:
    GradScaler = CudaGradScaler

_DTYPE_STRING_TO_DTYPE_MAPPING: Mapping[str, Optional[torch.dtype]] = {
    "fp16": torch.float16,
    "bf16": torch.bfloat16,
    "fp32": None,
}


def convert_precision_str_to_dtype(precision: str) -> Optional[torch.dtype]:
    """
    Converts precision as a string to a torch.dtype

    Args:
        precision: string containing the precision

    Raises:
        ValueError if an invalid precision string is passed.

    """
    if precision not in _DTYPE_STRING_TO_DTYPE_MAPPING:
        raise ValueError(
            f"Precision {precision} not supported. Please use one of {list(_DTYPE_STRING_TO_DTYPE_MAPPING.keys())}"
        )
    return _DTYPE_STRING_TO_DTYPE_MAPPING[precision]


def get_grad_scaler_from_precision(
    precision: torch.dtype, *, is_fsdp_module: Optional[bool] = False
) -> Optional[GradScaler]:
    """
    Returns the correct grad scaler to use based on the precision and whether
    or not the model is FSDP.

    Args:
        precision: the precision being used
        is_fsdp_module: whether the grad scaler is for an FSDP module

    Returns:
        The appropriate grad scaler to use, ``None`` if no grad scaler should be used.
    """

    if precision == torch.float16:
        if is_fsdp_module:
            from torch.distributed.fsdp.sharded_grad_scaler import ShardedGradScaler

            return ShardedGradScaler()
        else:
            return CudaGradScaler()
    return None
