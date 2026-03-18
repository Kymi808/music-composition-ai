"""Orchestrator - assigns instruments, manages layering, dynamics, and doubling."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from composer.generators.melody import NoteEvent


@dataclass
class TrackAssignment:
    """An instrument track with its notes and metadata."""
    instrument_name: str
    midi_program: int
    channel: int
    notes: list[NoteEvent] = field(default_factory=list)
    is_drum: bool = False
    pan: int = 64      # 0=left, 64=center, 127=right
    volume: int = 100   # Channel volume (0-127)


@dataclass
class Orchestrator:
    """Assigns instruments to generated parts and manages the full arrangement."""

    intensity: float = 0.7  # 0-1 controls how many layers are active
    dynamic_curve: str = "flat"  # flat, crescendo, decrescendo, arc, wave

    def orchestrate(
        self,
        melody_notes: list[NoteEvent],
        bass_notes: list[NoteEvent],
        drum_notes: list[NoteEvent],
        accompaniment_notes: list[NoteEvent],
        instrument_palette: dict[str, int],
        total_beats: float,
    ) -> list[TrackAssignment]:
        """Create the full orchestration from generated parts.

        Args:
            melody_notes: Generated melody.
            bass_notes: Generated bass line.
            drum_notes: Generated drum pattern.
            accompaniment_notes: Generated accompaniment.
            instrument_palette: Dict of role -> MIDI program number.
            total_beats: Total duration in beats.
        """
        tracks: list[TrackAssignment] = []
        channel = 0

        # Apply dynamic curve to all notes
        if self.dynamic_curve != "flat":
            melody_notes = self._apply_dynamics(melody_notes, total_beats)
            bass_notes = self._apply_dynamics(bass_notes, total_beats)
            accompaniment_notes = self._apply_dynamics(accompaniment_notes, total_beats)

        # Melody track
        if melody_notes:
            melody_program = instrument_palette.get("melody", 0)
            tracks.append(TrackAssignment(
                instrument_name=self._program_name(melody_program),
                midi_program=melody_program,
                channel=channel,
                notes=melody_notes,
                pan=64,
                volume=105,
            ))
            channel += 1

        # Accompaniment track
        if accompaniment_notes:
            acc_program = instrument_palette.get("accompaniment", 0)
            tracks.append(TrackAssignment(
                instrument_name=self._program_name(acc_program),
                midi_program=acc_program,
                channel=channel,
                notes=accompaniment_notes,
                pan=52,  # Slightly left
                volume=85,
            ))
            channel += 1

        # Optional: harmony/doubling track
        if self.intensity > 0.5 and melody_notes:
            harmony_program = instrument_palette.get("harmony", instrument_palette.get("accompaniment", 48))
            harmony_notes = self._create_harmony(melody_notes)
            if harmony_notes:
                tracks.append(TrackAssignment(
                    instrument_name=self._program_name(harmony_program),
                    midi_program=harmony_program,
                    channel=channel,
                    notes=harmony_notes,
                    pan=76,  # Slightly right
                    volume=75,
                ))
                channel += 1

        # Optional: pad/texture layer
        if self.intensity > 0.6 and "pad" in instrument_palette:
            pad_notes = self._create_pad_from_accompaniment(accompaniment_notes)
            tracks.append(TrackAssignment(
                instrument_name=self._program_name(instrument_palette["pad"]),
                midi_program=instrument_palette["pad"],
                channel=channel,
                notes=pad_notes,
                pan=64,
                volume=60,
            ))
            channel += 1

        # Bass track
        if bass_notes:
            bass_program = instrument_palette.get("bass", 32)
            tracks.append(TrackAssignment(
                instrument_name=self._program_name(bass_program),
                midi_program=bass_program,
                channel=channel,
                notes=bass_notes,
                pan=64,
                volume=95,
            ))
            channel += 1

        # Drum track (always channel 9 in GM)
        if drum_notes:
            tracks.append(TrackAssignment(
                instrument_name="Drums",
                midi_program=0,
                channel=9,
                notes=drum_notes,
                is_drum=True,
                pan=64,
                volume=100,
            ))

        return tracks

    def _apply_dynamics(
        self,
        notes: list[NoteEvent],
        total_beats: float,
    ) -> list[NoteEvent]:
        """Apply a dynamic curve to a list of notes."""
        if not notes or total_beats <= 0:
            return notes

        result = []
        for note in notes:
            progress = note.start / total_beats
            multiplier = self._dynamic_multiplier(progress)
            new_vel = int(note.velocity * multiplier)
            new_vel = max(1, min(127, new_vel))
            result.append(NoteEvent(
                pitch=note.pitch,
                start=note.start,
                duration=note.duration,
                velocity=new_vel,
            ))
        return result

    def _dynamic_multiplier(self, progress: float) -> float:
        """Get velocity multiplier based on dynamic curve and progress (0-1)."""
        if self.dynamic_curve == "crescendo":
            return 0.6 + 0.5 * progress
        elif self.dynamic_curve == "decrescendo":
            return 1.1 - 0.5 * progress
        elif self.dynamic_curve == "arc":
            # Build to 60%, then diminish
            if progress < 0.6:
                return 0.7 + 0.4 * (progress / 0.6)
            else:
                return 1.1 - 0.4 * ((progress - 0.6) / 0.4)
        elif self.dynamic_curve == "wave":
            import math
            return 0.8 + 0.25 * math.sin(progress * math.pi * 4)
        return 1.0  # flat

    def _create_harmony(self, melody: list[NoteEvent]) -> list[NoteEvent]:
        """Create a harmony line a third or sixth below the melody."""
        harmony = []
        interval = random.choice([-3, -4, -8, -9])  # Third or sixth below

        for note in melody:
            # Only harmonize some notes
            if random.random() < 0.7:
                harmony.append(NoteEvent(
                    pitch=note.pitch + interval,
                    start=note.start,
                    duration=note.duration,
                    velocity=int(note.velocity * 0.8),
                ))
        return harmony

    def _create_pad_from_accompaniment(self, acc_notes: list[NoteEvent]) -> list[NoteEvent]:
        """Create sustained pad notes from accompaniment, thinned out."""
        if not acc_notes:
            return []
        pad = []
        # Take the first note of each chord change as a pad note
        seen_starts = set()
        for note in acc_notes:
            beat_start = int(note.start)
            if beat_start not in seen_starts:
                seen_starts.add(beat_start)
                pad.append(NoteEvent(
                    pitch=note.pitch,
                    start=note.start,
                    duration=max(note.duration, 4.0),
                    velocity=int(note.velocity * 0.5),
                ))
        return pad

    def _program_name(self, program: int) -> str:
        """Get a human-readable name for a MIDI program number."""
        from composer.theory.constants import GM_INSTRUMENTS
        for name, num in GM_INSTRUMENTS.items():
            if num == program:
                return name.replace("_", " ").title()
        return f"Program {program}"
