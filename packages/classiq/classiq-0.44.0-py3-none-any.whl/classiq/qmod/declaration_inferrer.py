import dataclasses
import inspect
import sys
from enum import EnumMeta
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    get_args,
    get_origin,
    overload,
)

from typing_extensions import _AnnotatedAlias

from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalArray,
    ClassicalList,
    Integer,
    Real,
)
from classiq.interface.generator.functions.concrete_types import ConcreteClassicalType
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.type_name import Enum
from classiq.interface.generator.types.enum_declaration import (
    EnumDeclaration,
    declaration_from_enum,
)
from classiq.interface.model.classical_parameter_declaration import (
    AnonClassicalParameterDeclaration,
)
from classiq.interface.model.port_declaration import AnonPortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    AnonPositionalArg,
    AnonQuantumOperandDeclaration,
    NamedParamsQuantumFunctionDeclaration,
    PositionalArg,
)

from classiq import Struct, StructDeclaration
from classiq.exceptions import ClassiqValueError
from classiq.qmod.model_state_container import ModelStateContainer
from classiq.qmod.qmod_parameter import CArray, CBool, CInt, CReal
from classiq.qmod.qmod_variable import QVar, get_type_hint_expr
from classiq.qmod.quantum_callable import QCallableList
from classiq.qmod.utilities import unmangle_keyword, version_portable_get_args

if sys.version_info[0:2] >= (3, 9):
    from typing import Annotated


def python_type_to_qmod(
    py_type: type, *, qmodule: ModelStateContainer
) -> Optional[ConcreteClassicalType]:
    if py_type is int or py_type is CInt:
        return Integer()
    elif py_type in (float, complex) or py_type is CReal:
        return Real()
    elif py_type is bool or py_type is CBool:
        return Bool()
    elif get_origin(py_type) is list:
        element_type = python_type_to_qmod(get_args(py_type)[0], qmodule=qmodule)
        if element_type is not None:
            return ClassicalList(element_type=element_type)
    elif get_origin(py_type) is CArray:
        array_args = version_portable_get_args(py_type)
        if len(array_args) == 1:
            return ClassicalList(
                element_type=python_type_to_qmod(array_args[0], qmodule=qmodule)
            )
        elif len(array_args) == 2:
            return ClassicalArray(
                element_type=python_type_to_qmod(array_args[0], qmodule=qmodule),
                size=get_type_hint_expr(array_args[1]),
            )
        raise ClassiqValueError(
            "CArray accepts one or two generic parameters in the form "
            "`CArray[<element-type>]` or `CArray[<element-type>, <size>]`"
        )
    elif inspect.isclass(py_type) and dataclasses.is_dataclass(py_type):
        _add_qmod_struct(py_type, qmodule=qmodule)
        return Struct(name=py_type.__name__)
    elif inspect.isclass(py_type) and isinstance(py_type, EnumMeta):
        _add_qmod_enum(py_type, qmodule=qmodule)
        return Enum(name=py_type.__name__)
    return None


def _add_qmod_enum(py_type: EnumMeta, *, qmodule: ModelStateContainer) -> None:
    if (
        py_type.__name__ in EnumDeclaration.BUILTIN_ENUM_DECLARATIONS
        or py_type.__name__ in qmodule.enum_decls
    ):
        return

    qmodule.enum_decls[py_type.__name__] = declaration_from_enum(py_type)


def _add_qmod_struct(py_type: Type, *, qmodule: ModelStateContainer) -> None:
    if (
        py_type.__name__ in StructDeclaration.BUILTIN_STRUCT_DECLARATIONS
        or py_type.__name__ in qmodule.type_decls
    ):
        return

    qmodule.type_decls[py_type.__name__] = StructDeclaration(
        name=py_type.__name__,
        variables={
            f.name: python_type_to_qmod(f.type, qmodule=qmodule)
            for f in dataclasses.fields(py_type)
        },
    )


def _extract_port_decl(name: Optional[str], py_type: Any) -> AnonPortDeclaration:
    # FIXME: CAD-13409
    qtype: Type[QVar] = QVar.from_type_hint(py_type)  # type:ignore[assignment]
    direction = qtype.port_direction(py_type)
    if isinstance(py_type, _AnnotatedAlias):
        py_type = py_type.__args__[0]
    param = AnonPortDeclaration(
        name=None,
        direction=direction,
        quantum_type=qtype.to_qmod_quantum_type(py_type),
    )
    if name is not None:
        param = param.rename(name)
    return param


def _extract_operand_decl(
    name: Optional[str], py_type: Any, qmodule: ModelStateContainer
) -> AnonQuantumOperandDeclaration:
    is_list = (get_origin(py_type) or py_type) is QCallableList
    if get_origin(py_type) is list:
        is_list = True
        py_type = version_portable_get_args(py_type)
    type_args = version_portable_get_args(py_type)
    param_decls = [_extract_operand_param(arg_type) for arg_type in type_args]
    param = AnonQuantumOperandDeclaration(
        name=name,
        positional_arg_declarations=_extract_positional_args(
            param_decls, qmodule=qmodule
        ),
        is_list=is_list,
    )
    if name is not None:
        param = param.rename(name)
    return param


def _extract_operand_param(py_type: Any) -> Tuple[Optional[str], Any]:
    if sys.version_info[0:2] < (3, 9) or get_origin(py_type) is not Annotated:
        return None, py_type
    args = get_args(py_type)
    if len(args) == 2:
        if isinstance(args[1], PortDeclarationDirection):
            return None, py_type
        elif isinstance(args[1], str):
            return args[1], args[0]
    elif (
        len(args) == 3
        and isinstance(args[1], PortDeclarationDirection)
        and isinstance(args[2], str)
    ):
        return args[2], Annotated[args[0], args[1]]
    raise ClassiqValueError(
        f"Operand parameter declaration must be of the form <param-type> or "
        f"Annotated[<param-type>, <param-name>]. Got {py_type}"
    )


@overload
def _extract_positional_args(
    args: Sequence[Tuple[str, Any]], qmodule: ModelStateContainer
) -> Sequence[PositionalArg]:
    pass


@overload
def _extract_positional_args(
    args: Sequence[Tuple[Optional[str], Any]], qmodule: ModelStateContainer
) -> Sequence[AnonPositionalArg]:
    pass


def _extract_positional_args(
    args: Sequence[Tuple[Optional[str], Any]], qmodule: ModelStateContainer
) -> Sequence[AnonPositionalArg]:
    result: List[AnonPositionalArg] = []
    for name, py_type in args:
        if name == "return":
            continue
        name = unmangle_keyword(name)
        classical_type = python_type_to_qmod(py_type, qmodule=qmodule)
        if classical_type is not None:
            param = AnonClassicalParameterDeclaration(
                name=None,
                classical_type=classical_type,
            )
            if name is not None:
                param = param.rename(name)
            result.append(param)
        elif QVar.from_type_hint(py_type) is not None:
            result.append(_extract_port_decl(name, py_type))
        else:
            result.append(_extract_operand_decl(name, py_type, qmodule=qmodule))
    return result


def infer_func_decl(
    py_func: Callable, qmodule: ModelStateContainer
) -> NamedParamsQuantumFunctionDeclaration:
    return NamedParamsQuantumFunctionDeclaration(
        name=unmangle_keyword(py_func.__name__),
        positional_arg_declarations=_extract_positional_args(
            list(py_func.__annotations__.items()), qmodule=qmodule
        ),
    )
