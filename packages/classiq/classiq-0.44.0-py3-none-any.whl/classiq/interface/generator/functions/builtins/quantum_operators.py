from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)

PERMUTE_OPERATOR = NamedParamsQuantumFunctionDeclaration(
    name="permute",
    positional_arg_declarations=[
        QuantumOperandDeclaration(
            name="functions",
            is_list=True,
        )
    ],
)

APPLY_OPERATOR = NamedParamsQuantumFunctionDeclaration(
    name="apply",
    positional_arg_declarations=[QuantumOperandDeclaration(name="operand")],
)

STD_QMOD_OPERATORS = [
    PERMUTE_OPERATOR,
    APPLY_OPERATOR,
]
