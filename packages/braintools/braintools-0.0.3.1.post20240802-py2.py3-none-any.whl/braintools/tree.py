# Copyright 2024 BDP Ecosystem Limited. All Rights Reserved.
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
# ==============================================================================

from __future__ import annotations

from typing import Sequence, TypeVar, Any, Callable

import brainunit as bu
import jax
import jax.tree_util as jtu
import numpy as np

PyTree = Any
T = TypeVar('T')

__all__ = [
  'scale',
  'mul',
  'shift',
  'add',
  'sub',
  'dot',
  'sum',
  'squared_norm',
  'concat',
  'split',
  'idx',
  'expand',
  'take',
  'as_numpy',
]


def scale(
    tree: T,
    x: jax.typing.ArrayLike,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  return jtu.tree_map(lambda a: a * x, tree, is_leaf=is_leaf)


def mul(
    tree: T,
    x: T | jax.typing.ArrayLike,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  if isinstance(x, jax.typing.ArrayLike):
    return scale(tree, x)
  return jtu.tree_map(lambda a, b: a * b, tree, x, is_leaf=is_leaf)


def shift(
    tree1: T,
    x: jax.typing.ArrayLike,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  return jtu.tree_map(lambda a: a + x, tree1, is_leaf=is_leaf)


def add(
    tree1: T,
    tree2: T | jax.typing.ArrayLike,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  if isinstance(tree2, jax.Array):
    return shift(tree1, tree2)
  return jtu.tree_map(lambda a, b: a + b, tree1, tree2, is_leaf=is_leaf)


def sub(
    tree1: T,
    tree2: T,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  return jtu.tree_map(lambda a, b: a - b, tree1, tree2, is_leaf=is_leaf)


def dot(
    a: T,
    b: T,
    is_leaf: Callable[[Any], bool] | None = None
) -> jax.Array:
  return jtu.tree_reduce(
    bu.math.add,
    jtu.tree_map(bu.math.sum, jax.tree_map(jax.lax.mul, a, b, is_leaf=is_leaf), is_leaf=is_leaf),
    is_leaf=is_leaf
  )


def sum(
    tree: PyTree[jax.typing.ArrayLike],
    is_leaf: Callable[[Any], bool] | None = None
) -> jax.Array:
  return jtu.tree_reduce(bu.math.add, jtu.tree_map(bu.math.sum, tree, is_leaf=is_leaf), is_leaf=is_leaf)


def squared_norm(
    tree: PyTree[jax.typing.ArrayLike],
    is_leaf: Callable[[Any], bool] | None = None
) -> jax.Array:
  return jtu.tree_reduce(
    bu.math.add,
    jtu.tree_map(lambda x: bu.math.einsum('...,...->', x, x), tree, is_leaf=is_leaf),
    is_leaf=is_leaf
  )


def concat(
    trees: Sequence[T],
    axis: int = 0,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  return jtu.tree_map(lambda *args: bu.math.concatenate(args, axis=axis), *trees, is_leaf=is_leaf)


def split(
    tree: PyTree[jax.Array],
    sizes: tuple[int],
    is_leaf: Callable[[Any], bool] | None = None
) -> tuple[PyTree[jax.Array], ...]:
  idx = 0
  result: list[PyTree[jax.Array]] = []
  for s in sizes:
    result.append(jtu.tree_map(lambda x: x[idx: idx + s], tree, is_leaf=is_leaf))
    idx += s
  result.append(jtu.tree_map(lambda x: x[idx:], tree, is_leaf=is_leaf))
  return tuple(result)


def idx(
    tree: T,
    idx,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  return jtu.tree_map(lambda x: x[idx], tree, is_leaf=is_leaf)


def expand(
    tree: T,
    axis,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  return jtu.tree_map(lambda x: bu.math.expand_dims(x, axis), tree, is_leaf=is_leaf)


def take(
    tree: T,
    idx,
    axis: int,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  def take_(x):
    indices = idx
    if isinstance(indices, slice):
      slices = [slice(None)] * x.ndim
      slices[axis] = idx
      return x[tuple(slices)]
    return bu.math.take(x, indices, axis)

  return jtu.tree_map(take_, tree, is_leaf=is_leaf)


def as_numpy(
    tree: T,
    is_leaf: Callable[[Any], bool] | None = None
) -> T:
  return jtu.tree_map(lambda x: np.asarray(x), tree, is_leaf=is_leaf)
