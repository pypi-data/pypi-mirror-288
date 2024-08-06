from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import (
    ClassicalList,
    Integer,
    Real,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)

DEFAULT_TARGET_NAME = "target"

H_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="H",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


X_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="X",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


Y_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="Y",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)

Z_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="Z",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


I_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="I",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


S_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="S",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


T_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="T",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


SDG_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="SDG",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


TDG_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="TDG",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


PHASE_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="PHASE",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


RX_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="RX",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


RY_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="RY",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


RZ_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="RZ",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)

R_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="R",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        ClassicalParameterDeclaration(
            name="phi",
            classical_type=Real(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


RXX_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="RXX",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        ),
    ],
)


RYY_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="RYY",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        ),
    ],
)


RZZ_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="RZZ",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        ),
    ],
)


CH_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="CH",
    positional_arg_declarations=[
        PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


CX_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="CX",
    positional_arg_declarations=[
        PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


CY_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="CY",
    positional_arg_declarations=[
        PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


CZ_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="CZ",
    positional_arg_declarations=[
        PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


CRX_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="CRX",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


CRY_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="CRY",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


CRZ_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="CRZ",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


CPHASE_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="CPHASE",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


SWAP_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="SWAP",
    positional_arg_declarations=[
        PortDeclaration(
            name="qbit0",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        PortDeclaration(
            name="qbit1",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


IDENTITY_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="IDENTITY",
    positional_arg_declarations=[
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
        )
    ],
)

UNITARY_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="unitary",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="elements",
            classical_type=ClassicalList(
                element_type=ClassicalList(element_type=Real())
            ),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="log(get_field(elements[0], 'len'), 2)"),
        ),
    ],
)


PREPARE_STATE_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="prepare_state",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="probabilities",
            classical_type=ClassicalList(element_type=Real()),
        ),
        ClassicalParameterDeclaration(name="bound", classical_type=Real()),
        PortDeclaration(
            name="out",
            direction=PortDeclarationDirection.Output,
            size=Expression(expr="log(get_field(probabilities, 'len'), 2)"),
        ),
    ],
)

PREPARE_AMPLITUDES_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="prepare_amplitudes",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="amplitudes",
            classical_type=ClassicalList(element_type=Real()),
        ),
        ClassicalParameterDeclaration(
            name="bound",
            classical_type=Real(),
        ),
        PortDeclaration(
            name="out",
            direction=PortDeclarationDirection.Output,
            size=Expression(expr="log(get_field(amplitudes, 'len'), 2)"),
        ),
    ],
)

ADD_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="add",
    positional_arg_declarations=[
        PortDeclaration(
            name="left",
            direction=PortDeclarationDirection.Inout,
        ),
        PortDeclaration(
            name="right",
            direction=PortDeclarationDirection.Inout,
        ),
        PortDeclaration(
            name="result",
            direction=PortDeclarationDirection.Output,
            size=Expression(
                expr="Max(get_field(left, 'len'), get_field(right, 'len')) + 1"
            ),
        ),
    ],
)


MODULAR_ADD_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="modular_add",
    positional_arg_declarations=[
        PortDeclaration(
            name="left",
            direction=PortDeclarationDirection.Inout,
        ),
        PortDeclaration(
            name="right",
            direction=PortDeclarationDirection.Inout,
        ),
    ],
)


INTEGER_XOR_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="integer_xor",
    positional_arg_declarations=[
        PortDeclaration(
            name="left",
            direction=PortDeclarationDirection.Inout,
        ),
        PortDeclaration(
            name="right",
            direction=PortDeclarationDirection.Inout,
        ),
    ],
)


U_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="U",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="theta",
            classical_type=Real(),
        ),
        ClassicalParameterDeclaration(
            name="phi",
            classical_type=Real(),
        ),
        ClassicalParameterDeclaration(
            name="lam",
            classical_type=Real(),
        ),
        ClassicalParameterDeclaration(
            name="gam",
            classical_type=Real(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


CCX_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="CCX",
    positional_arg_declarations=[
        PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    ],
)


ALLOCATE_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="allocate",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="num_qubits",
            classical_type=Integer(),
        ),
        PortDeclaration(
            name="out",
            direction=PortDeclarationDirection.Output,
            size=Expression(expr="num_qubits"),
        ),
    ],
)


FREE_FUNCTION = NamedParamsQuantumFunctionDeclaration(
    name="free",
    positional_arg_declarations=[
        PortDeclaration(
            name="in",
            direction=PortDeclarationDirection.Input,
        )
    ],
)


RANDOMIZED_BENCHMARKING = NamedParamsQuantumFunctionDeclaration(
    name="randomized_benchmarking",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="num_of_cliffords",
            classical_type=Integer(),
        ),
        PortDeclaration(
            name=DEFAULT_TARGET_NAME,
            direction=PortDeclarationDirection.Inout,
        ),
    ],
)


INPLACE_PREPARE_STATE = NamedParamsQuantumFunctionDeclaration(
    name="inplace_prepare_state",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="probabilities",
            classical_type=ClassicalList(element_type=Real()),
        ),
        ClassicalParameterDeclaration(
            name="bound",
            classical_type=Real(),
        ),
        PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="log(get_field(probabilities, 'len'), 2)"),
        ),
    ],
)


INPLACE_PREPARE_AMPLITUDES = NamedParamsQuantumFunctionDeclaration(
    name="inplace_prepare_amplitudes",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="amplitudes",
            classical_type=ClassicalList(element_type=Real()),
        ),
        ClassicalParameterDeclaration(
            name="bound",
            classical_type=Real(),
        ),
        PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="log(get_field(amplitudes, 'len'), 2)"),
        ),
    ],
)


__all__ = [
    "H_FUNCTION",
    "X_FUNCTION",
    "Y_FUNCTION",
    "Z_FUNCTION",
    "I_FUNCTION",
    "S_FUNCTION",
    "T_FUNCTION",
    "SDG_FUNCTION",
    "TDG_FUNCTION",
    "PHASE_FUNCTION",
    "RX_FUNCTION",
    "RY_FUNCTION",
    "RZ_FUNCTION",
    "R_FUNCTION",
    "RXX_FUNCTION",
    "RYY_FUNCTION",
    "RZZ_FUNCTION",
    "CH_FUNCTION",
    "CX_FUNCTION",
    "CY_FUNCTION",
    "CZ_FUNCTION",
    "CRX_FUNCTION",
    "CRY_FUNCTION",
    "CRZ_FUNCTION",
    "CPHASE_FUNCTION",
    "SWAP_FUNCTION",
    "IDENTITY_FUNCTION",
    "PREPARE_STATE_FUNCTION",
    "PREPARE_AMPLITUDES_FUNCTION",
    "UNITARY_FUNCTION",
    "ADD_FUNCTION",
    "MODULAR_ADD_FUNCTION",
    "INTEGER_XOR_FUNCTION",
    "U_FUNCTION",
    "CCX_FUNCTION",
    "ALLOCATE_FUNCTION",
    "FREE_FUNCTION",
    "RANDOMIZED_BENCHMARKING",
    "INPLACE_PREPARE_STATE",
    "INPLACE_PREPARE_AMPLITUDES",
]
