from typing import Callable, Literal, Optional, Union, overload

from classiq.qmod.quantum_callable import QCallable
from classiq.qmod.quantum_function import ExternalQFunc, GenerativeQFunc, QFunc


@overload
def qfunc(func: Callable) -> QFunc: ...


@overload
def qfunc(*, external: Literal[True]) -> Callable[[Callable], ExternalQFunc]: ...


@overload
def qfunc(*, generative: Literal[True]) -> Callable[[Callable], GenerativeQFunc]: ...


def qfunc(
    func: Optional[Callable] = None, *, external: bool = False, generative: bool = False
) -> Union[Callable[[Callable], QCallable], QCallable]:
    def wrapper(func: Callable) -> QCallable:
        if generative:
            return GenerativeQFunc(func)
        if external:
            return ExternalQFunc(func)

        return QFunc(func)

    if func is not None:
        return wrapper(func)

    return wrapper
