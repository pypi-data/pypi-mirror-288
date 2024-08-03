"""Standard type definitions."""

import torch
import transformer_lens as tl

from jaxtyping import Float, Int
from collections import namedtuple
from typing import Protocol, Callable, Literal

Device = Literal["cpu", "cuda", "mps"]
LayerIndex = int
FeatureIndex = int
TokenIndex = int

HookPoint = tl.hook_points.HookPoint
HookName = str
HookNameFilterFn = Callable[[HookName], bool]

# Torch types
Tokens = Int[torch.Tensor, "batch seq"]
SingleTokens = Int[torch.Tensor, " batch"]
Logits = Float[torch.Tensor, "batch seq d_vocab"]
Activations = Float[torch.Tensor, "batch seq ..."]
Model = tl.HookedTransformer
Metric = Float[torch.Tensor, " ()"]


class TLForwardHookFn(Protocol):
    def __call__(self, activations: torch.Tensor, hook: HookPoint) -> torch.Tensor:
        raise NotImplementedError


class TLBackwardHookFn(Protocol):
    def __call__(
        self, activations: torch.Tensor, hook: HookPoint
    ) -> tuple[torch.Tensor]:
        raise NotImplementedError


ForwardHook = namedtuple("ForwardHook", ["hook_name", "hook_fn"])
BackwardHook = namedtuple("BackwardHook", ["hook_name", "hook_fn"])
