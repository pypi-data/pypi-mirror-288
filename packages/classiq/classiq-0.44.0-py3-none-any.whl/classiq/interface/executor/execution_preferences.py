from typing import Optional

import pydantic

from classiq.interface.backend.backend_preferences import (
    BackendPreferencesTypes,
    backend_preferences_field,
)
from classiq.interface.backend.quantum_backend_providers import (
    ClassiqSimulatorBackendNames,
)
from classiq.interface.executor.optimizer_preferences import OptimizerType
from classiq.interface.generator.model.preferences.preferences import (
    TranspilationOption,
)
from classiq.interface.generator.model.preferences.randomness import create_random_seed
from classiq.interface.generator.noise_properties import NoiseProperties

from classiq._internals.enum_utils import ReprEnum


class QaeWithQpeEstimationMethod(int, ReprEnum):
    MAXIMUM_LIKELIHOOD = 0
    BEST_FIT = 1


class ExecutionPreferences(pydantic.BaseModel):
    noise_properties: Optional[NoiseProperties] = pydantic.Field(
        default=None, description="Properties of the noise in the circuit"
    )
    random_seed: int = pydantic.Field(
        default_factory=create_random_seed,
        description="The random seed used for the execution",
    )
    backend_preferences: BackendPreferencesTypes = backend_preferences_field(
        backend_name=ClassiqSimulatorBackendNames.SIMULATOR
    )
    num_shots: Optional[pydantic.PositiveInt] = pydantic.Field(default=None)
    transpile_to_hardware: TranspilationOption = pydantic.Field(
        default=TranspilationOption.DECOMPOSE,
        description="Transpile the circuit to the hardware basis gates before execution",
        title="Transpilation Option",
    )
    job_name: Optional[str] = pydantic.Field(
        min_length=1,
        description="The job name",
    )


__all__ = [
    "ExecutionPreferences",
    "OptimizerType",
    "NoiseProperties",
    "QaeWithQpeEstimationMethod",
]
