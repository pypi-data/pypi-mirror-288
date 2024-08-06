from typing import Literal, Mapping, Sequence

from classiq.interface.generator.functions.builtins.core_library import (
    INTEGER_XOR_FUNCTION,
    MODULAR_ADD_FUNCTION,
)
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.handle_binding import ConcreteHandleBinding, HandleBinding
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_statement import HandleMetadata, QuantumOperation

from classiq._internals.enum_utils import StrEnum


class BinaryOperation(StrEnum):
    Addition = "inplace_add"
    Xor = "inplace_xor"

    @property
    def internal_function_declaration(self) -> NamedParamsQuantumFunctionDeclaration:
        return {
            BinaryOperation.Addition: MODULAR_ADD_FUNCTION,
            BinaryOperation.Xor: INTEGER_XOR_FUNCTION,
        }[self]


class InplaceBinaryOperation(QuantumOperation):
    kind: Literal["InplaceBinaryOperation"]

    target: ConcreteHandleBinding
    value: ConcreteHandleBinding
    operation: BinaryOperation

    @property
    def wiring_inouts(self) -> Mapping[str, HandleBinding]:
        return nameables_to_dict([self.target, self.value])

    @property
    def readable_inouts(self) -> Sequence[HandleMetadata]:
        suffix = f" of an in-place {self.operation.name.lower()} statement"
        return [
            HandleMetadata(
                handle=self.target, readable_location=f"as the target{suffix}"
            ),
            HandleMetadata(
                handle=self.value, readable_location=f"as the value{suffix}"
            ),
        ]
