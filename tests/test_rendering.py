"""Tests for the rendering pipeline."""

import random
import tempfile
from pathlib import Path

import pytest

from composer.core.composition import Composition
from composer.core.track import Track
from composer.generators.melody import NoteEvent
from composer.rendering.midi_renderer import MidiRenderer


class TestMidiRenderer:
    def test_render_basic(self):
        random.seed(42)
        track = Track(
            name="Piano",
            instrument_name="Acoustic Grand Piano",
            midi_program=0,
            channel=0,
            notes=[
                NoteEvent(pitch=60, start=0, duration=1.0, velocity=80),
                NoteEvent(pitch=64, start=1, duration=1.0, velocity=80),
                NoteEvent(pitch=67, start=2, duration=1.0, velocity=80),
                NoteEvent(pitch=72, start=3, duration=1.0, velocity=80),
            ],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = MidiRenderer.render(
                tracks=[track],
                tempo=120,
                time_signature=(4, 4),
                output_path=Path(tmpdir) / "test",
            )
            assert path.exists()
            assert path.suffix == ".mid"
            assert path.stat().st_size > 0

    def test_render_composition(self):
        random.seed(42)
        comp = Composition.from_prompt("simple test", duration_seconds=15)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = MidiRenderer.render(
                tracks=comp.tracks,
                tempo=comp.tempo,
                time_signature=comp.time_signature,
                output_path=Path(tmpdir) / "composition",
            )
            assert path.exists()
            assert path.stat().st_size > 100  # Should have real content

    def test_render_with_drums(self):
        random.seed(42)
        drum_track = Track(
            name="Drums",
            instrument_name="Drums",
            midi_program=0,
            channel=9,
            is_drum=True,
            notes=[
                NoteEvent(pitch=36, start=0, duration=0.1, velocity=100),
                NoteEvent(pitch=38, start=1, duration=0.1, velocity=90),
                NoteEvent(pitch=36, start=2, duration=0.1, velocity=100),
                NoteEvent(pitch=38, start=3, duration=0.1, velocity=90),
            ],
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            path = MidiRenderer.render(
                tracks=[drum_track],
                tempo=120,
                time_signature=(4, 4),
                output_path=Path(tmpdir) / "drums",
            )
            assert path.exists()

    def test_get_midi_object(self):
        random.seed(42)
        track = Track(
            name="Test",
            instrument_name="Piano",
            midi_program=0,
            channel=0,
            notes=[NoteEvent(pitch=60, start=0, duration=1.0, velocity=80)],
        )
        midi = MidiRenderer.get_midi_object(
            tracks=[track],
            tempo=120,
            time_signature=(4, 4),
        )
        assert len(midi.instruments) == 1
        assert len(midi.instruments[0].notes) == 1

    def test_render_empty_tracks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = MidiRenderer.render(
                tracks=[],
                tempo=120,
                time_signature=(4, 4),
                output_path=Path(tmpdir) / "empty",
            )
            assert path.exists()


class TestTrack:
    def test_transpose(self):
        track = Track(
            name="Test", instrument_name="Piano", midi_program=0, channel=0,
            notes=[NoteEvent(pitch=60, start=0, duration=1.0, velocity=80)],
        )
        track.transpose(7)
        assert track.notes[0].pitch == 67

    def test_scale_velocity(self):
        track = Track(
            name="Test", instrument_name="Piano", midi_program=0, channel=0,
            notes=[NoteEvent(pitch=60, start=0, duration=1.0, velocity=80)],
        )
        track.scale_velocity(0.5)
        assert track.notes[0].velocity == 40

    def test_trim(self):
        track = Track(
            name="Test", instrument_name="Piano", midi_program=0, channel=0,
            notes=[
                NoteEvent(pitch=60, start=0, duration=1.0, velocity=80),
                NoteEvent(pitch=64, start=4, duration=1.0, velocity=80),
                NoteEvent(pitch=67, start=8, duration=1.0, velocity=80),
            ],
        )
        trimmed = track.trim(0, 5)
        assert trimmed.note_count == 2
