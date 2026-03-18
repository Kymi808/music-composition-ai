"""Main Composition class - orchestrates the entire generation pipeline."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from composer.core.prompt_parser import PromptParser, CompositionParams
from composer.core.track import Track
from composer.core.section import Section
from composer.theory.scales import Scale
from composer.theory.chords import Chord
from composer.theory.progressions import ChordProgression
from composer.theory.rhythm import RhythmPattern, TimeSignature
from composer.generators.melody import MelodyGenerator, NoteEvent
from composer.generators.bass import BassGenerator
from composer.generators.drums import DrumGenerator
from composer.generators.accompaniment import AccompanimentGenerator
from composer.generators.orchestrator import Orchestrator, TrackAssignment
from composer.instruments.presets import GenrePresets
from composer.styles.library import StyleLibrary
from composer.styles.style import Style
from composer.moods.mood import MoodLibrary, Mood
from composer.structure.arrangement import Arranger, SectionPlan


@dataclass
class Composition:
    """A complete musical composition."""

    params: CompositionParams
    tracks: list[Track] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)
    tempo: int = 120
    key: str = "C"
    scale_type: str = "major"
    time_signature: tuple[int, int] = (4, 4)
    total_beats: float = 0.0

    @staticmethod
    def from_prompt(prompt: str, **overrides) -> Composition:
        """Create a composition from a text prompt.

        This is the main entry point for generating music.
        """
        # Parse the prompt
        parser = PromptParser()
        params = parser.parse(prompt)

        # Apply any overrides
        for key, value in overrides.items():
            if hasattr(params, key):
                setattr(params, key, value)

        return Composition.from_params(params)

    @staticmethod
    def from_params(params: CompositionParams) -> Composition:
        """Create a composition from explicit parameters."""
        # Get style and mood
        style = StyleLibrary.get(params.genre)
        mood = MoodLibrary.get(params.mood)

        # Merge mood preferences into params
        _apply_mood(params, mood)
        _apply_style(params, style)

        # Create the scale
        scale = Scale(params.key, params.scale_type)
        time_sig = TimeSignature(*params.time_signature)

        # Calculate total beats from duration
        beats_per_second = params.tempo / 60.0
        total_beats = params.duration_seconds * beats_per_second
        beats_per_measure = time_sig.measure_duration

        # Get instrument palette
        palette = GenrePresets.get(params.genre)
        palette = GenrePresets.override_with_requested(palette, params.instruments)

        # Create arrangement
        section_names = Arranger.get_section_names_for_duration(
            style.typical_sections,
            total_beats,
            int(beats_per_measure),
            style.measures_per_section,
        )
        section_plans = Arranger.create_arrangement(
            section_names,
            style.measures_per_section,
            total_beats,
            int(beats_per_measure),
        )

        # Generate music for each section
        all_melody: list[NoteEvent] = []
        all_bass: list[NoteEvent] = []
        all_drums: list[NoteEvent] = []
        all_accompaniment: list[NoteEvent] = []
        sections: list[Section] = []

        current_beat = 0.0

        for plan in section_plans:
            section_beats = plan.measures * beats_per_measure
            is_minor = scale.is_minor()

            # Generate chord progression for this section
            progression = _generate_progression(
                params, scale, is_minor, style, plan
            )

            # Calculate beats per chord
            num_chords = len(progression.chords)
            beats_per_chord = section_beats / num_chords if num_chords > 0 else section_beats

            section_tracks: list[Track] = []

            # Melody
            if plan.use_melody:
                melody_gen = MelodyGenerator(
                    scale=scale,
                    tempo=params.tempo,
                    velocity_base=style.base_velocity,
                    note_range=_melody_range(palette.get("melody", 0)),
                )
                contour = random.choice(mood.preferred_contours) if mood.preferred_contours else "arch"
                melody_notes = melody_gen.generate(
                    chords=progression.chords,
                    beats_per_chord=beats_per_chord,
                    contour=contour,
                    variation=style.melody_variation,
                    density=style.melody_density * plan.intensity,
                )
                _offset_notes(melody_notes, current_beat)
                all_melody.extend(melody_notes)

            # Bass
            if plan.use_bass:
                bass_style = random.choice(mood.preferred_bass_styles) if mood.preferred_bass_styles else "root"
                bass_gen = BassGenerator(
                    scale=scale,
                    velocity_base=style.base_velocity,
                    style=bass_style,
                )
                bass_notes = bass_gen.generate(
                    chords=progression.chords,
                    beats_per_chord=beats_per_chord,
                )
                _offset_notes(bass_notes, current_beat)
                all_bass.extend(bass_notes)

            # Drums
            if plan.use_drums and style.use_drums:
                drum_gen = DrumGenerator(
                    genre=style.drum_genre,
                    velocity_base=int(style.base_velocity * plan.intensity),
                    swing=style.swing,
                    intensity=style.drum_intensity * plan.intensity,
                )
                drum_notes = drum_gen.generate(
                    num_measures=plan.measures,
                    time_sig=time_sig,
                    fill_every=4,
                )
                _offset_notes(drum_notes, current_beat)
                all_drums.extend(drum_notes)

            # Accompaniment
            if plan.use_accompaniment:
                acc_style = random.choice(mood.preferred_acc_styles) if mood.preferred_acc_styles else "block"
                acc_gen = AccompanimentGenerator(
                    scale=scale,
                    velocity_base=int(style.base_velocity * 0.85),
                    style=acc_style,
                )
                acc_notes = acc_gen.generate(
                    chords=progression.chords,
                    beats_per_chord=beats_per_chord,
                )
                _offset_notes(acc_notes, current_beat)
                all_accompaniment.extend(acc_notes)

            sections.append(Section(
                name=plan.name,
                duration_beats=section_beats,
                intensity=plan.intensity,
            ))

            current_beat += section_beats

        # Orchestrate - assign instruments and create final tracks
        orchestrator = Orchestrator(
            intensity=params.intensity,
            dynamic_curve=params.dynamic_curve,
        )
        track_assignments = orchestrator.orchestrate(
            melody_notes=all_melody,
            bass_notes=all_bass,
            drum_notes=all_drums,
            accompaniment_notes=all_accompaniment,
            instrument_palette=palette,
            total_beats=current_beat,
        )

        # Convert to Track objects
        tracks = []
        for assignment in track_assignments:
            tracks.append(Track(
                name=assignment.instrument_name,
                instrument_name=assignment.instrument_name,
                midi_program=assignment.midi_program,
                channel=assignment.channel,
                notes=assignment.notes,
                is_drum=assignment.is_drum,
                pan=assignment.pan,
                volume=assignment.volume,
            ))

        return Composition(
            params=params,
            tracks=tracks,
            sections=sections,
            tempo=params.tempo,
            key=params.key,
            scale_type=params.scale_type,
            time_signature=params.time_signature,
            total_beats=current_beat,
        )

    @property
    def duration_seconds(self) -> float:
        """Duration in seconds."""
        return self.total_beats / (self.tempo / 60.0) if self.tempo > 0 else 0

    @property
    def total_notes(self) -> int:
        return sum(t.note_count for t in self.tracks)

    def summary(self) -> str:
        """Human-readable summary of the composition."""
        lines = [
            f"Composition: {self.params.prompt or 'Untitled'}",
            f"  Key: {self.key} {self.scale_type}",
            f"  Tempo: {self.tempo} BPM",
            f"  Time Signature: {self.time_signature[0]}/{self.time_signature[1]}",
            f"  Duration: {self.duration_seconds:.1f}s ({self.total_beats:.0f} beats)",
            f"  Mood: {self.params.mood}",
            f"  Genre: {self.params.genre}",
            f"  Sections: {' → '.join(s.name for s in self.sections)}",
            f"  Tracks ({len(self.tracks)}):",
        ]
        for track in self.tracks:
            lines.append(f"    - {track.name}: {track.note_count} notes")
        lines.append(f"  Total notes: {self.total_notes}")
        return "\n".join(lines)


def _apply_mood(params: CompositionParams, mood: Mood) -> None:
    """Apply mood settings to params (without overriding explicit user choices)."""
    if params.dynamic_curve == "arc":  # Default
        params.dynamic_curve = mood.dynamic_curve
    params.intensity = max(params.intensity, mood.intensity * 0.5)


def _apply_style(params: CompositionParams, style: Style) -> None:
    """Apply style settings to params."""
    params.use_seventh_chords = style.use_seventh_chords
    if params.bass_style == "root":
        params.bass_style = style.bass_style
    if params.accompaniment_style == "block":
        params.accompaniment_style = style.accompaniment_style


def _generate_progression(
    params: CompositionParams,
    scale: Scale,
    is_minor: bool,
    style: Style,
    plan: SectionPlan,
) -> ChordProgression:
    """Generate a chord progression appropriate for the section."""
    try:
        prog = ChordProgression.for_mood(
            key=params.key,
            mood=params.mood,
            is_minor=is_minor,
            use_seventh=params.use_seventh_chords,
        )
    except (ValueError, KeyError):
        prog = ChordProgression.for_genre(
            key=params.key,
            genre=params.genre,
            is_minor=is_minor,
            use_seventh=params.use_seventh_chords,
        )

    # Repeat progression to fill the section
    chords_needed = plan.measures // max(len(prog.chords), 1)
    chords_needed = max(1, chords_needed)
    extended_chords = prog.chords * chords_needed

    # Trim to exactly fit
    total_needed = plan.measures
    extended_chords = extended_chords[:total_needed]
    if not extended_chords:
        extended_chords = prog.chords[:1] or [Chord(params.key, __import__('composer.theory.chords', fromlist=['ChordType']).ChordType.MAJOR)]

    return ChordProgression(chords=extended_chords, degrees=prog.degrees, name=prog.name)


def _offset_notes(notes: list[NoteEvent], offset: float) -> None:
    """Shift all notes forward by offset beats."""
    for note in notes:
        note.start += offset


def _melody_range(program: int) -> tuple[int, int]:
    """Get a reasonable melody range based on the instrument program."""
    from composer.theory.constants import INSTRUMENT_RANGES, GM_INSTRUMENTS

    for name, prog in GM_INSTRUMENTS.items():
        if prog == program and name in INSTRUMENT_RANGES:
            low, high = INSTRUMENT_RANGES[name]
            # Use the upper portion of the range for melody
            mid = (low + high) // 2
            return (mid, high)

    # Default: C4 to C6
    return (60, 84)
