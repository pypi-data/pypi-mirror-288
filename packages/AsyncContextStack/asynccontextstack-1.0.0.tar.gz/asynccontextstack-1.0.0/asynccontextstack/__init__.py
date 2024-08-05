"""
AsyncContextStack
---------------
Async context manager for nesting async context stacks

Authors:
Chris Lee <chris@cosmosnexus.co>
"""

from __future__ import annotations  # noqa

from contextlib import AsyncExitStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, AsyncContextManager, Iterable

    from typing_extensions import Self


class AsyncContextStackException(Exception):
    pass


class NotInContext(AsyncContextStackException):
    pass


class AsyncContextMixin:
    if TYPE_CHECKING:
        _async_exit_stack: AsyncExitStack
        _async_entered_contexts: list[Any]

    @property
    def async_contexts(self) -> "Iterable[AsyncContextManager[Any]]":
        return []

    @property
    def async_entered_contexts(self) -> "list[Any]":
        try:
            return self._async_entered_contexts
        except AttributeError as e:
            raise NotInContext() from e

    async def __aenter__(self) -> "Self":
        self._async_exit_stack = AsyncExitStack()
        entered_contexts = []
        for context in self.async_contexts:
            entered_contexts.append(
                await self._async_exit_stack.enter_async_context(context)
            )
        self._async_entered_contexts = entered_contexts
        return self

    async def __aexit__(self, *exc_details) -> None:
        await self._async_exit_stack.__aexit__(*exc_details)
        del self._async_entered_contexts
