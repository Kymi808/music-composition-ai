"""Song structure, section ordering, and transitions."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class SectionPlan:
    """Plan for a single section in the arrangement."""
    name: str
    measures: int
    intensity: float  # 0-1
    use_melody: bool = True
    use_drums: bool = True
    use_bass: bool = True
    use_accompaniment: bool = True
    progression_variation: str = "default"  # default, variation, new


# Section intensity profiles
SECTION_PROFILES = {
    "intro": SectionPlan(
        name="intro", measures=4, intensity=0.3,
        use_melody=False, use_drums=False, use_bass=True, use_accompaniment=True,
    ),
    "verse": SectionPlan(
        name="verse", measures=8, intensity=0.5,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "chorus": SectionPlan(
        name="chorus", measures=8, intensity=0.8,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "bridge": SectionPlan(
        name="bridge", measures=8, intensity=0.6,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
        progression_variation="new",
    ),
    "outro": SectionPlan(
        name="outro", measures=4, intensity=0.3,
        use_melody=True, use_drums=False, use_bass=True, use_accompaniment=True,
    ),
    "buildup": SectionPlan(
        name="buildup", measures=4, intensity=0.6,
        use_melody=False, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "drop": SectionPlan(
        name="drop", measures=8, intensity=0.95,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "breakdown": SectionPlan(
        name="breakdown", measures=4, intensity=0.3,
        use_melody=False, use_drums=False, use_bass=True, use_accompaniment=True,
    ),
    "climax": SectionPlan(
        name="climax", measures=8, intensity=0.95,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "theme": SectionPlan(
        name="theme", measures=8, intensity=0.7,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "theme_a": SectionPlan(
        name="theme_a", measures=8, intensity=0.6,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "theme_b": SectionPlan(
        name="theme_b", measures=8, intensity=0.7,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
        progression_variation="variation",
    ),
    "development": SectionPlan(
        name="development", measures=8, intensity=0.65,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
        progression_variation="variation",
    ),
    "resolution": SectionPlan(
        name="resolution", measures=4, intensity=0.4,
        use_melody=True, use_drums=False, use_bass=True, use_accompaniment=True,
    ),
    "head": SectionPlan(
        name="head", measures=8, intensity=0.6,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "solo_a": SectionPlan(
        name="solo_a", measures=8, intensity=0.7,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "solo_b": SectionPlan(
        name="solo_b", measures=8, intensity=0.75,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
    "exposition": SectionPlan(
        name="exposition", measures=16, intensity=0.5,
        use_melody=True, use_drums=False, use_bass=True, use_accompaniment=True,
    ),
    "recapitulation": SectionPlan(
        name="recapitulation", measures=16, intensity=0.6,
        use_melody=True, use_drums=False, use_bass=True, use_accompaniment=True,
    ),
    "coda": SectionPlan(
        name="coda", measures=4, intensity=0.4,
        use_melody=True, use_drums=False, use_bass=True, use_accompaniment=True,
    ),
    "atmosphere_a": SectionPlan(
        name="atmosphere_a", measures=16, intensity=0.3,
        use_melody=True, use_drums=False, use_bass=True, use_accompaniment=True,
    ),
    "atmosphere_b": SectionPlan(
        name="atmosphere_b", measures=16, intensity=0.35,
        use_melody=True, use_drums=False, use_bass=True, use_accompaniment=True,
        progression_variation="variation",
    ),
    "turnaround": SectionPlan(
        name="turnaround", measures=4, intensity=0.5,
        use_melody=True, use_drums=True, use_bass=True, use_accompaniment=True,
    ),
}


class Arranger:
    """Creates song structure arrangements from style parameters."""

    @staticmethod
    def create_arrangement(
        section_names: list[str],
        measures_per_section: int = 8,
        target_duration_beats: float | None = None,
        time_sig_beats: int = 4,
    ) -> list[SectionPlan]:
        """Create a list of section plans from section names.

        Args:
            section_names: List of section names from the style.
            measures_per_section: Default measures per section.
            target_duration_beats: If set, adjust to fit target duration.
            time_sig_beats: Beats per measure.
        """
        plans = []
        for name in section_names:
            if name in SECTION_PROFILES:
                plan = SectionPlan(
                    name=SECTION_PROFILES[name].name,
                    measures=SECTION_PROFILES[name].measures,
                    intensity=SECTION_PROFILES[name].intensity,
                    use_melody=SECTION_PROFILES[name].use_melody,
                    use_drums=SECTION_PROFILES[name].use_drums,
                    use_bass=SECTION_PROFILES[name].use_bass,
                    use_accompaniment=SECTION_PROFILES[name].use_accompaniment,
                    progression_variation=SECTION_PROFILES[name].progression_variation,
                )
            else:
                plan = SectionPlan(
                    name=name,
                    measures=measures_per_section,
                    intensity=0.6,
                )
            plans.append(plan)

        # Adjust to fit target duration if specified
        if target_duration_beats and plans:
            total = sum(p.measures * time_sig_beats for p in plans)
            if total > 0:
                scale = target_duration_beats / total
                for plan in plans:
                    plan.measures = max(2, int(plan.measures * scale))

        return plans

    @staticmethod
    def get_section_names_for_duration(
        base_sections: list[str],
        target_beats: float,
        beats_per_measure: int = 4,
        measures_per_section: int = 8,
    ) -> list[str]:
        """Extend or trim section list to approximately fill the target duration."""
        beats_per_section = measures_per_section * beats_per_measure
        needed = max(1, int(target_beats / beats_per_section))

        result = []
        idx = 0
        while len(result) < needed:
            result.append(base_sections[idx % len(base_sections)])
            idx += 1

        return result
