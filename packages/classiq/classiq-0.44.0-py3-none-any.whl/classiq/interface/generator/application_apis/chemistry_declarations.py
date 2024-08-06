import functools
from enum import Enum

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_function_declaration import (
    ClassicalFunctionDeclaration,
)
from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalList,
    Integer,
    Real,
    VQEResult,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.type_name import Struct, TypeName
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)

MOLECULE_PROBLEM_PARAM = ClassicalParameterDeclaration(
    name="molecule_problem", classical_type=Struct(name="MoleculeProblem")
)
MOLECULE_PROBLEM_SIZE = "get_field(get_field(molecule_problem_to_hamiltonian(molecule_problem)[0], 'pauli'), 'len')"
MOLECULE_PROBLEM_PORT = PortDeclaration(
    name="qbv",
    direction=PortDeclarationDirection.Inout,
    size=Expression(
        expr=MOLECULE_PROBLEM_SIZE,
    ),
)

FOCK_HAMILTONIAN_PROBLEM_PARAM = ClassicalParameterDeclaration(
    name="fock_hamiltonian_problem",
    classical_type=Struct(name="FockHamiltonianProblem"),
)
FOCK_HAMILTONIAN_SIZE = "get_field(get_field(fock_hamiltonian_problem_to_hamiltonian(fock_hamiltonian_problem)[0], 'pauli'), 'len')"

FOCK_HAMILTONIAN_PROBLEM_PORT = PortDeclaration(
    name="qbv",
    direction=PortDeclarationDirection.Inout,
    size=Expression(expr=FOCK_HAMILTONIAN_SIZE),
)


class ChemistryProblemType(Enum):
    MoleculeProblem = "molecule_problem"
    FockHamiltonianProblem = "fock_hamiltonian_problem"


MOLECULE_UCC_ANSATZ = NamedParamsQuantumFunctionDeclaration(
    name="molecule_ucc",
    positional_arg_declarations=[
        MOLECULE_PROBLEM_PARAM,
        ClassicalParameterDeclaration(
            name="excitations", classical_type=ClassicalList(element_type=Integer())
        ),
        MOLECULE_PROBLEM_PORT,
    ],
)


MOLECULE_HVA_ANSATZ = NamedParamsQuantumFunctionDeclaration(
    name="molecule_hva",
    positional_arg_declarations=[
        MOLECULE_PROBLEM_PARAM,
        ClassicalParameterDeclaration(name="reps", classical_type=Integer()),
        MOLECULE_PROBLEM_PORT,
    ],
)


MOLECULE_HARTREE_FOCK = NamedParamsQuantumFunctionDeclaration(
    name="molecule_hartree_fock",
    positional_arg_declarations=[
        MOLECULE_PROBLEM_PARAM,
        MOLECULE_PROBLEM_PORT,
    ],
)


FOCK_HAMILTONIAN_UCC_ANSATZ = NamedParamsQuantumFunctionDeclaration(
    name="fock_hamiltonian_ucc",
    positional_arg_declarations=[
        FOCK_HAMILTONIAN_PROBLEM_PARAM,
        ClassicalParameterDeclaration(
            name="excitations", classical_type=ClassicalList(element_type=Integer())
        ),
        FOCK_HAMILTONIAN_PROBLEM_PORT,
    ],
)

FOCK_HAMILTONIAN_HVA_ANSATZ = NamedParamsQuantumFunctionDeclaration(
    name="fock_hamiltonian_hva",
    positional_arg_declarations=[
        FOCK_HAMILTONIAN_PROBLEM_PARAM,
        ClassicalParameterDeclaration(name="reps", classical_type=Integer()),
        FOCK_HAMILTONIAN_PROBLEM_PORT,
    ],
)

FOCK_HAMILTONIAN_HARTREE_FOCK = NamedParamsQuantumFunctionDeclaration(
    name="fock_hamiltonian_hartree_fock",
    positional_arg_declarations=[
        FOCK_HAMILTONIAN_PROBLEM_PARAM,
        FOCK_HAMILTONIAN_PROBLEM_PORT,
    ],
)


MOLECULE_PROBLEM = StructDeclaration(
    name="MoleculeProblem",
    variables={
        "mapping": Integer(),
        "z2_symmetries": Bool(),
        # A negative number of qubits is considered None
        # basis: str = pydantic.Field(default="sto3g", description="Molecular basis set")
        "molecule": Struct(name="Molecule"),
        "freeze_core": Bool(),
        "remove_orbitals": ClassicalList(element_type=Integer()),
    },
)

MOLECULE = StructDeclaration(
    name="Molecule",
    variables={
        "atoms": ClassicalList(element_type=Struct(name="ChemistryAtom")),
        "spin": Integer(),
        "charge": Integer(),
    },
)

CHEMISTRY_ATOM = StructDeclaration(
    name="ChemistryAtom",
    variables={
        "element": Integer(),
        "position": Struct(name="Position"),
    },
)

POSITION = StructDeclaration(
    name="Position", variables={"x": Real(), "y": Real(), "z": Real()}
)

FockHamiltonian = functools.partial(
    ClassicalList, element_type=Struct(name="LadderTerm")
)

FOCK_HAMILTONIAN_PROBLEM = StructDeclaration(
    name="FockHamiltonianProblem",
    variables={
        "mapping": Integer(),
        "z2_symmetries": Bool(),
        "terms": FockHamiltonian(),
        "num_particles": ClassicalList(element_type=Integer()),
    },
)

LADDER_TERM = StructDeclaration(
    name="LadderTerm",
    variables={
        "coefficient": Real(),
        "ops": ClassicalList(element_type=Struct(name="LadderOp")),
    },
)

LADDER_OP = StructDeclaration(
    name="LadderOp",
    variables={
        "op": TypeName(name="LadderOperator"),
        "index": Integer(),
    },
)

MOLECULE_RESULT = StructDeclaration(
    name="MoleculeResult",
    variables={
        "energy": Real(),
        "nuclear_repulsion_energy": Real(),
        "total_energy": Real(),
        "hartree_fock_energy": Real(),
        "vqe_result": VQEResult(),
    },
)

MOLECULE_PROBLEM_TO_HAMILTONIAN = ClassicalFunctionDeclaration(
    name="molecule_problem_to_hamiltonian",
    positional_parameters=[
        ClassicalParameterDeclaration(
            name="problem", classical_type=Struct(name="MoleculeProblem")
        ),
    ],
    return_type=ClassicalList(element_type=Struct(name="PauliTerm")),
)

FOCK_HAMILTONIAN_PROBLEM_TO_HAMILTONIAN = ClassicalFunctionDeclaration(
    name="fock_hamiltonian_problem_to_hamiltonian",
    positional_parameters=[
        ClassicalParameterDeclaration(
            name="problem", classical_type=Struct(name="FockHamiltonianProblem")
        ),
    ],
    return_type=ClassicalList(element_type=Struct(name="PauliTerm")),
)


MOLECULE_GROUND_STATE_SOLUTION_POST_PROCESS = ClassicalFunctionDeclaration(
    name="molecule_ground_state_solution_post_process",
    positional_parameters=[
        ClassicalParameterDeclaration(
            name="problem", classical_type=Struct(name="MoleculeProblem")
        ),
        ClassicalParameterDeclaration(name="vqe_result", classical_type=VQEResult()),
    ],
    return_type=Struct(name="MoleculeResult"),
)

__all__ = [
    "MOLECULE_UCC_ANSATZ",
    "MOLECULE_HVA_ANSATZ",
    "MOLECULE_HARTREE_FOCK",
    "FOCK_HAMILTONIAN_UCC_ANSATZ",
    "FOCK_HAMILTONIAN_HVA_ANSATZ",
    "FOCK_HAMILTONIAN_HARTREE_FOCK",
    "MOLECULE_PROBLEM",
    "MOLECULE",
    "CHEMISTRY_ATOM",
    "POSITION",
    "FOCK_HAMILTONIAN_PROBLEM",
    "LADDER_TERM",
    "LADDER_OP",
    "MOLECULE_PROBLEM_TO_HAMILTONIAN",
    "FOCK_HAMILTONIAN_PROBLEM_TO_HAMILTONIAN",
    "MOLECULE_GROUND_STATE_SOLUTION_POST_PROCESS",
    "MOLECULE_RESULT",
]
