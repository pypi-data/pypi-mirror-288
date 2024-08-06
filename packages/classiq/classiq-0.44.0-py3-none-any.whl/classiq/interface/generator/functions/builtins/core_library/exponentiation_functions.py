from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import (
    ClassicalList,
    Integer,
    Real,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.type_name import Enum
from classiq.interface.generator.types.builtin_struct_declarations.pauli_struct_declarations import (
    Hamiltonian,
)
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)

SINGLE_PAULI_EXPONENT_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="single_pauli_exponent",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="pauli_string",
            classical_type=ClassicalList(element_type=Enum(name="Pauli")),
        ),
        ClassicalParameterDeclaration(name="coefficient", classical_type=Real()),
        PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="get_field(pauli_string, 'len')"),
        ),
    ],
)


SUZUKI_TROTTER_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="suzuki_trotter",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="pauli_operator", classical_type=Hamiltonian()
        ),
        ClassicalParameterDeclaration(
            name="evolution_coefficient", classical_type=Real()
        ),
        ClassicalParameterDeclaration(name="order", classical_type=Integer()),
        ClassicalParameterDeclaration(name="repetitions", classical_type=Integer()),
        PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(
                expr="get_field(get_field(pauli_operator[0], 'pauli'), 'len')"
            ),
        ),
    ],
)

QDRIFT_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="qdrift",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="pauli_operator", classical_type=Hamiltonian()
        ),
        ClassicalParameterDeclaration(
            name="evolution_coefficient", classical_type=Real()
        ),
        ClassicalParameterDeclaration(name="num_qdrift", classical_type=Integer()),
        PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(
                expr="get_field(get_field(pauli_operator[0], 'pauli'), 'len')"
            ),
        ),
    ],
)

EXPONENTIATION_WITH_DEPTH_CONSTRAINT = NamedParamsQuantumFunctionDeclaration(
    name="exponentiation_with_depth_constraint",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="pauli_operator", classical_type=Hamiltonian()
        ),
        ClassicalParameterDeclaration(
            name="evolution_coefficient", classical_type=Real()
        ),
        ClassicalParameterDeclaration(name="max_depth", classical_type=Integer()),
        PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(
                expr="get_field(get_field(pauli_operator[0], 'pauli'), 'len')"
            ),
        ),
    ],
)

__all__ = [
    "SINGLE_PAULI_EXPONENT_FUNCTION",
    "SUZUKI_TROTTER_FUNCTION",
    "QDRIFT_FUNCTION",
    "EXPONENTIATION_WITH_DEPTH_CONSTRAINT",
]
