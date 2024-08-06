import enum

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import (
    ClassicalList,
    Integer,
    Real,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.type_name import Enum, Struct
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)


class FeatureMapType(enum.Enum):
    BlochSphere = "bloch_sphere"
    Pauli = "pauli"


QSVM_PAULI_FEATURE_MAP_SIZE = "get_field(feature_map, 'feature_dimension')"
QSVM_PAULI_FEATURE_MAP = NamedParamsQuantumFunctionDeclaration(
    name="pauli_feature_map",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="feature_map", classical_type=Struct(name="QSVMFeatureMapPauli")
        ),
        PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr=QSVM_PAULI_FEATURE_MAP_SIZE),
        ),
    ],
)

QSVM_BLOCH_SPHERE_FEATURE_MAP_SIZE = "ceiling(feature_dimension/2)"
QSVM_BLOCH_SPHERE_FEATURE_MAP = NamedParamsQuantumFunctionDeclaration(
    name="bloch_sphere_feature_map",
    positional_arg_declarations=[
        ClassicalParameterDeclaration(
            name="feature_dimension", classical_type=Integer()
        ),
        PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr=QSVM_BLOCH_SPHERE_FEATURE_MAP_SIZE),
        ),
    ],
)

QSVM_FEATURE_MAP_PAULI = StructDeclaration(
    name="QSVMFeatureMapPauli",
    variables={
        "feature_dimension": Integer(),
        "reps": Integer(),
        "entanglement": Integer(),
        "alpha": Real(),
        "paulis": ClassicalList(
            element_type=ClassicalList(element_type=Enum(name="Pauli"))
        ),
    },
)

QSVM_RESULT = StructDeclaration(
    name="QsvmResult",
    variables={
        "test_score": Real(),
        "predicted_labels": ClassicalList(element_type=Real()),
    },
)

__all__ = [
    "QSVM_RESULT",
    "QSVM_PAULI_FEATURE_MAP",
    "QSVM_BLOCH_SPHERE_FEATURE_MAP",
    "QSVM_FEATURE_MAP_PAULI",
]
