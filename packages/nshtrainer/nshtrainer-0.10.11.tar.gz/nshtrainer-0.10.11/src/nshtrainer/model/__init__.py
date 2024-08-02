from typing_extensions import TypeAlias

from ._environment import (
    EnvironmentClassInformationConfig as EnvironmentClassInformationConfig,
)
from ._environment import EnvironmentConfig as EnvironmentConfig
from ._environment import (
    EnvironmentLinuxEnvironmentConfig as EnvironmentLinuxEnvironmentConfig,
)
from ._environment import (
    EnvironmentSLURMInformationConfig as EnvironmentSLURMInformationConfig,
)
from ._environment import EnvironmentSnapshotConfig as EnvironmentSnapshotConfig
from .base import Base as Base
from .base import LightningModuleBase as LightningModuleBase
from .config import BaseConfig as BaseConfig
from .config import BaseLoggerConfig as BaseLoggerConfig
from .config import BaseProfilerConfig as BaseProfilerConfig
from .config import CheckpointLoadingConfig as CheckpointLoadingConfig
from .config import CheckpointSavingConfig as CheckpointSavingConfig
from .config import DirectoryConfig as DirectoryConfig
from .config import EarlyStoppingConfig as EarlyStoppingConfig
from .config import GradientClippingConfig as GradientClippingConfig
from .config import (
    LatestEpochCheckpointCallbackConfig as LatestEpochCheckpointCallbackConfig,
)
from .config import LoggingConfig as LoggingConfig
from .config import MetricConfig as MetricConfig
from .config import ModelCheckpointCallbackConfig as ModelCheckpointCallbackConfig
from .config import (
    OnExceptionCheckpointCallbackConfig as OnExceptionCheckpointCallbackConfig,
)
from .config import OptimizationConfig as OptimizationConfig
from .config import PrimaryMetricConfig as PrimaryMetricConfig
from .config import ReproducibilityConfig as ReproducibilityConfig
from .config import SanityCheckingConfig as SanityCheckingConfig
from .config import TrainerConfig as TrainerConfig
from .config import WandbWatchConfig as WandbWatchConfig

ConfigList: TypeAlias = list[tuple[BaseConfig, type[LightningModuleBase]]]
