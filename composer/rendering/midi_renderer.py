"""MIDI rendering - converts composition to MIDI file using pretty_midi."""

from __future__ import annotations

from pathlib import Path

import pretty_midi

from composer.core.track import Track


class MidiRenderer:
    """Renders a composition to a MIDI file."""

    @staticmethod
    def render(
        tracks: list[Track],
        tempo: int,
        time_signature: tuple[int, int],
        output_path: str | Path,
    ) -> Path:
        """Render tracks to a MIDI file.

        Args:
            tracks: List of Track objects with notes.
            tempo: Tempo in BPM.
            time_signature: (numerator, denominator).
            output_path: Path for the output .mid file.

        Returns:
            Path to the written MIDI file.
        """
        output_path = Path(output_path)
        if not output_path.suffix:
            output_path = output_path.with_suffix(".mid")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create PrettyMIDI object
        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)

        # Add time signature
        ts = pretty_midi.TimeSignature(
            numerator=time_signature[0],
            denominator=time_signature[1],
            time=0.0,
        )
        midi.time_signature_changes.append(ts)

        # Seconds per beat
        spb = 60.0 / tempo

        for track in tracks:
            if not track.notes:
                continue

            # Create instrument
            instrument = pretty_midi.Instrument(
                program=track.midi_program,
                is_drum=track.is_drum,
                name=track.name,
            )

            # Set initial volume and pan via control changes
            instrument.control_changes.append(
                pretty_midi.ControlChange(number=7, value=track.volume, time=0.0)
            )
            instrument.control_changes.append(
                pretty_midi.ControlChange(number=10, value=track.pan, time=0.0)
            )

            # Add notes
            for note_event in track.notes:
                start_time = note_event.start * spb
                end_time = (note_event.start + note_event.duration) * spb
                velocity = max(1, min(127, note_event.velocity))
                pitch = max(0, min(127, note_event.pitch))

                if end_time <= start_time:
                    end_time = start_time + 0.05  # Minimum duration

                note = pretty_midi.Note(
                    velocity=velocity,
                    pitch=pitch,
                    start=start_time,
                    end=end_time,
                )
                instrument.notes.append(note)

            midi.instruments.append(instrument)

        # Write to file
        midi.write(str(output_path))
        return output_path

    @staticmethod
    def get_midi_object(
        tracks: list[Track],
        tempo: int,
        time_signature: tuple[int, int],
    ) -> pretty_midi.PrettyMIDI:
        """Get a PrettyMIDI object without writing to file."""
        midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
        spb = 60.0 / tempo

        ts = pretty_midi.TimeSignature(
            numerator=time_signature[0],
            denominator=time_signature[1],
            time=0.0,
        )
        midi.time_signature_changes.append(ts)

        for track in tracks:
            if not track.notes:
                continue

            instrument = pretty_midi.Instrument(
                program=track.midi_program,
                is_drum=track.is_drum,
                name=track.name,
            )

            for note_event in track.notes:
                start_time = note_event.start * spb
                end_time = (note_event.start + note_event.duration) * spb
                if end_time <= start_time:
                    end_time = start_time + 0.05

                note = pretty_midi.Note(
                    velocity=max(1, min(127, note_event.velocity)),
                    pitch=max(0, min(127, note_event.pitch)),
                    start=start_time,
                    end=end_time,
                )
                instrument.notes.append(note)

            midi.instruments.append(instrument)

        return midi
