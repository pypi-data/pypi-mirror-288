from typing import Dict

from classiq.interface.generator.constant import Constant
from classiq.interface.generator.types.enum_declaration import EnumDeclaration
from classiq.interface.generator.types.qstruct_declaration import QStructDeclaration
from classiq.interface.model.native_function_definition import NativeFunctionDefinition

from classiq import StructDeclaration


class ModelStateContainer:
    enum_decls: Dict[str, EnumDeclaration]
    type_decls: Dict[str, StructDeclaration]
    qstruct_decls: Dict[str, QStructDeclaration]
    native_defs: Dict[str, NativeFunctionDefinition]
    constants: Dict[str, Constant]


QMODULE = ModelStateContainer()
