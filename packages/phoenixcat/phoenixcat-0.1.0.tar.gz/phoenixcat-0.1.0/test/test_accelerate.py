# Copyright 2021 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# from __future__ import annotations

import contextlib
import functools
import json
import math
import os
import re
import shutil
import sys
import warnings
from collections import OrderedDict
from contextlib import contextmanager
from functools import partial
from types import MethodType
from typing import Any, Callable, Union

import torch
import torch.utils.hooks as hooks

from accelerate.checkpointing import (
    load_accelerator_state,
    load_custom_state,
    save_accelerator_state,
    save_custom_state,
)
from accelerate.data_loader import (
    DataLoaderDispatcher,
    prepare_data_loader,
    skip_first_batches,
)
from accelerate.hooks import AlignDevicesHook
from accelerate.logging import get_logger
from accelerate.optimizer import AcceleratedOptimizer
from accelerate.scheduler import AcceleratedScheduler
from accelerate.state import AcceleratorState, GradientState, PartialState
from accelerate.tracking import LOGGER_TYPE_TO_CLASS, GeneralTracker, filter_trackers
from accelerate.utils import (
    MODEL_NAME,
    SAFE_WEIGHTS_INDEX_NAME,
    SAFE_WEIGHTS_NAME,
    WEIGHTS_INDEX_NAME,
    WEIGHTS_NAME,
    AutocastKwargs,
    DataLoaderConfiguration,
    DeepSpeedPlugin,
    DistributedDataParallelKwargs,
    DistributedType,
    DynamoBackend,
    FP8RecipeKwargs,
    FullyShardedDataParallelPlugin,
    GradientAccumulationPlugin,
    GradScalerKwargs,
    InitProcessGroupKwargs,
    KwargsHandler,
    LoggerType,
    MegatronLMPlugin,
    PrecisionType,
    ProjectConfiguration,
    RNGType,
    TorchDynamoPlugin,
    check_os_kernel,
    clean_state_dict_for_safetensors,
    compare_versions,
    convert_model,
    convert_outputs_to_fp32,
    extract_model_from_parallel,
    gather,
    gather_object,
    get_mixed_precision_context_manager,
    get_pretty_name,
    has_transformer_engine_layers,
    is_bf16_available,
    is_deepspeed_available,
    is_fp8_available,
    is_ipex_available,
    is_megatron_lm_available,
    is_msamp_available,
    is_npu_available,
    is_torch_version,
    is_torch_xla_available,
    is_xpu_available,
    load_fsdp_model,
    load_fsdp_optimizer,
    pad_across_processes,
    parse_choice_from_env,
    recursively_apply,
    reduce,
    release_memory,
    save,
    save_fsdp_model,
    save_fsdp_optimizer,
    shard_checkpoint,
    wait_for_everyone,
)
from accelerate.utils.constants import FSDP_PYTORCH_VERSION
from accelerate.utils.modeling import get_state_dict_offloaded_model
from accelerate.utils.other import is_compiled_module


if is_deepspeed_available():
    from accelerate.utils import (
        DeepSpeedEngineWrapper,
        DeepSpeedOptimizerWrapper,
        DeepSpeedSchedulerWrapper,
        DummyOptim,
        DummyScheduler,
    )


if is_megatron_lm_available():
    from accelerate.utils import (
        MegatronEngine,
        MegatronLMDummyDataLoader,
        MegatronLMDummyScheduler,
        MegatronLMOptimizerWrapper,
        MegatronLMSchedulerWrapper,
        megatron_lm_initialize,
        megatron_lm_prepare_data_loader,
        megatron_lm_prepare_model,
        megatron_lm_prepare_optimizer,
        megatron_lm_prepare_scheduler,
    )

from torch.distributed.algorithms.join import Join


# if is_torch_xla_available():
#     import torch_xla.amp as xamp
#     import torch_xla.core.xla_model as xm
#     import torch_xla.distributed.xla_multiprocessing as xmp


# if is_npu_available(check_device=False):
#     import torch_npu  # noqa: F401


try:
    from torch.optim.lr_scheduler import LRScheduler
except ImportError:
    from torch.optim.lr_scheduler import _LRScheduler as LRScheduler

logger = get_logger(__name__)

# Sentinel values for defaults
_split_batches = object()
_dispatch_batches = object()
_even_batches = object()
_use_seedable_sampler = object()

from phoenixcat.configuration.pipeline_utils import PipelineMixin


class Accelerator_my:
    """
    Creates an instance of an accelerator for distributed training (on multi-GPU, TPU) or mixed precision training.

    Args:
        device_placement (`bool`, *optional*, defaults to `True`):
            Whether or not the accelerator should put objects on device (tensors yielded by the dataloader, model,
            etc...).
        mixed_precision (`str`, *optional*):
            Whether or not to use mixed precision training. Choose from 'no','fp16','bf16 or 'fp8'. Will default to the
            value in the environment variable `ACCELERATE_MIXED_PRECISION`, which will use the default value in the
            accelerate config of the current system or the flag passed with the `accelerate.launch` command. 'fp8'
            requires the installation of transformers-engine.
        gradient_accumulation_steps (`int`, *optional*, default to 1):
            The number of steps that should pass before gradients are accumulated. A number > 1 should be combined with
            `Accelerator.accumulate`. If not passed, will default to the value in the environment variable
            `ACCELERATE_GRADIENT_ACCUMULATION_STEPS`. Can also be configured through a `GradientAccumulationPlugin`.
        cpu (`bool`, *optional*):
            Whether or not to force the script to execute on CPU. Will ignore GPU available if set to `True` and force
            the execution on one process only.
        dataloader_config (`DataLoaderConfiguration`, *optional*):
            A configuration for how the dataloaders should be handled in distributed scenarios.
        deepspeed_plugin ([`~utils.DeepSpeedPlugin`], *optional*):
            Tweak your DeepSpeed related args using this argument. This argument is optional and can be configured
            directly using *accelerate config*
        fsdp_plugin ([`~utils.FullyShardedDataParallelPlugin`], *optional*):
            Tweak your FSDP related args using this argument. This argument is optional and can be configured directly
            using *accelerate config*
        megatron_lm_plugin ([`~utils.MegatronLMPlugin`], *optional*):
            Tweak your MegatronLM related args using this argument. This argument is optional and can be configured
            directly using *accelerate config*
        rng_types (list of `str` or [`~utils.RNGType`]):
            The list of random number generators to synchronize at the beginning of each iteration in your prepared
            dataloaders. Should be one or several of:

            - `"torch"`: the base torch random number generator
            - `"cuda"`: the CUDA random number generator (GPU only)
            - `"xla"`: the XLA random number generator (TPU only)
            - `"generator"`: the `torch.Generator` of the sampler (or batch sampler if there is no sampler in your
              dataloader) or of the iterable dataset (if it exists) if the underlying dataset is of that type.

            Will default to `["torch"]` for PyTorch versions <=1.5.1 and `["generator"]` for PyTorch versions >= 1.6.
        log_with (list of `str`, [`~utils.LoggerType`] or [`~tracking.GeneralTracker`], *optional*):
            A list of loggers to be setup for experiment tracking. Should be one or several of:

            - `"all"`
            - `"tensorboard"`
            - `"wandb"`
            - `"comet_ml"`
            If `"all"` is selected, will pick up all available trackers in the environment and initialize them. Can
            also accept implementations of `GeneralTracker` for custom trackers, and can be combined with `"all"`.
        project_config ([`~utils.ProjectConfiguration`], *optional*):
            A configuration for how saving the state can be handled.
        project_dir (`str`, `os.PathLike`, *optional*):
            A path to a directory for storing data such as logs of locally-compatible loggers and potentially saved
            checkpoints.
        step_scheduler_with_optimizer (`bool`, *optional`, defaults to `True`):
            Set `True` if the learning rate scheduler is stepped at the same time as the optimizer, `False` if only
            done under certain circumstances (at the end of each epoch, for instance).
        kwargs_handlers (list of [`~utils.KwargsHandler`], *optional*)
            A list of [`~utils.KwargsHandler`] to customize how the objects related to distributed training or mixed
            precision are created. See [kwargs](kwargs) for more information.
        dynamo_backend (`str` or [`~utils.DynamoBackend`], *optional*, defaults to `"no"`):
            Set to one of the possible dynamo backends to optimize your training with torch dynamo.
        gradient_accumulation_plugin ([`~utils.GradientAccumulationPlugin`], *optional*):
            A configuration for how gradient accumulation should be handled, if more tweaking than just the
            `gradient_accumulation_steps` is needed.

    **Available attributes:**

        - **device** (`torch.device`) -- The device to use.
        - **distributed_type** ([`~utils.DistributedType`]) -- The distributed training configuration.
        - **local_process_index** (`int`) -- The process index on the current machine.
        - **mixed_precision** (`str`) -- The configured mixed precision mode.
        - **num_processes** (`int`) -- The total number of processes used for training.
        - **optimizer_step_was_skipped** (`bool`) -- Whether or not the optimizer update was skipped (because of
          gradient overflow in mixed precision), in which
        case the learning rate should not be changed.
        - **process_index** (`int`) -- The overall index of the current process among all processes.
        - **state** ([`~state.AcceleratorState`]) -- The distributed setup state.
        - **sync_gradients** (`bool`) -- Whether the gradients are currently being synced across all processes.
        - **use_distributed** (`bool`) -- Whether the current configuration is for distributed training.
    """

    def __init__(self):
        pass

    def on_main_process(self, function: Callable[..., Any] = None):

        def _inner(*args, **kwargs):
            return PartialState().on_main_process(function)(*args, **kwargs)

        return _inner

    @on_main_process
    def log(self, values: dict, step: int | None = None, log_kwargs: dict | None = {}):
        print('kill cat')

    # def simple_wrap(self, func=None):
    #     def _inner(*args, **kwargs):
    #         print('before func')
    #         return func(*args, **kwargs)

    #     return _inner

    # @simple_wrap
    # def reset_flag(self):
    #     print('reset')


# a = Accelerator()

import accelerate

acl = accelerate.Accelerator()
acl.init_trackers('aachecker')
