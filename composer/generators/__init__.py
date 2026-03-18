"""Music generators - melody, bass, drums, accompaniment, orchestration."""

from composer.generators.melody import MelodyGenerator
from composer.generators.bass import BassGenerator
from composer.generators.drums import DrumGenerator
from composer.generators.accompaniment import AccompanimentGenerator
from composer.generators.orchestrator import Orchestrator

__all__ = [
    "MelodyGenerator",
    "BassGenerator",
    "DrumGenerator",
    "AccompanimentGenerator",
    "Orchestrator",
]
