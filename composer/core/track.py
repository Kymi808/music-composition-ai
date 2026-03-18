"""Track - represents a single instrument part in the composition."""

from __future__ import annotations

from dataclasses import dataclass, field

from composer.generators.melody import NoteEvent


@dataclass
class Track:
    """A single instrument track containing note events."""

    name: str
    instrument_name: str
    midi_program: int
    channel: int
    notes: list[NoteEvent] = field(default_factory=list)
    is_drum: bool = False
    pan: int = 64
    volume: int = 100

    @property
    def duration(self) -> float:
        """Total duration in beats."""
        if not self.notes:
            return 0
        return max(n.start + n.duration for n in self.notes)

    @property
    def note_count(self) -> int:
        return len(self.notes)

    def transpose(self, semitones: int) -> None:
        """Transpose all notes by the given number of semitones."""
        if self.is_drum:
            return
        for note in self.notes:
            note.pitch += semitones

    def scale_velocity(self, factor: float) -> None:
        """Scale all velocities by a factor."""
        for note in self.notes:
            note.velocity = max(1, min(127, int(note.velocity * factor)))

    def time_shift(self, beats: float) -> None:
        """Shift all notes forward/backward in time."""
        for note in self.notes:
            note.start += beats

    def trim(self, start_beat: float, end_beat: float) -> Track:
        """Return a new track with only notes in the given range."""
        trimmed_notes = []
        for note in self.notes:
            if start_beat <= note.start < end_beat:
                trimmed_notes.append(NoteEvent(
                    pitch=note.pitch,
                    start=note.start - start_beat,
                    duration=min(note.duration, end_beat - note.start),
                    velocity=note.velocity,
                ))
        return Track(
            name=self.name,
            instrument_name=self.instrument_name,
            midi_program=self.midi_program,
            channel=self.channel,
            notes=trimmed_notes,
            is_drum=self.is_drum,
            pan=self.pan,
            volume=self.volume,
        )

    def __repr__(self) -> str:
        return f"Track({self.name}, {self.note_count} notes, {self.duration:.1f} beats)"
