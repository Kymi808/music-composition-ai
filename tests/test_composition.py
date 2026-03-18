"""Tests for the main composition engine."""

import random
import tempfile
from pathlib import Path

from composer.core.composition import Composition
from composer.core.prompt_parser import CompositionParams


class TestComposition:
    def setup_method(self):
        random.seed(42)

    def test_from_prompt_basic(self):
        comp = Composition.from_prompt("simple piano piece")
        assert comp.total_notes > 0
        assert len(comp.tracks) > 0
        assert comp.tempo > 0

    def test_from_prompt_epic(self):
        comp = Composition.from_prompt("epic orchestral battle theme")
        assert comp.params.mood == "epic"
        assert comp.params.genre == "orchestral"
        assert comp.total_notes > 0

    def test_from_prompt_jazz(self):
        comp = Composition.from_prompt("jazz trio improvisation")
        assert comp.params.genre == "jazz"
        assert comp.total_notes > 0

    def test_from_prompt_with_overrides(self):
        comp = Composition.from_prompt(
            "test piece",
            key="D",
            scale_type="natural_minor",
            tempo=140,
            duration_seconds=30,
        )
        assert comp.key == "D"
        assert comp.scale_type == "natural_minor"
        assert comp.tempo == 140

    def test_from_params(self):
        params = CompositionParams(
            prompt="test",
            mood="peaceful",
            genre="ambient",
            key="C",
            scale_type="major",
            tempo=70,
            duration_seconds=30,
        )
        comp = Composition.from_params(params)
        assert comp.total_notes > 0
        assert comp.key == "C"

    def test_sections_generated(self):
        comp = Composition.from_prompt("rock song", duration_seconds=60)
        assert len(comp.sections) > 0

    def test_duration_approximate(self):
        comp = Composition.from_prompt("test piece", duration_seconds=60)
        # Duration should be in the right ballpark (not exact due to section quantization)
        assert 20 < comp.duration_seconds < 180

    def test_summary(self):
        comp = Composition.from_prompt("test piece", duration_seconds=30)
        summary = comp.summary()
        assert "Key:" in summary
        assert "Tempo:" in summary
        assert "Tracks" in summary

    def test_track_properties(self):
        comp = Composition.from_prompt("orchestral piece", duration_seconds=30)
        for track in comp.tracks:
            assert track.note_count > 0 or track.is_drum
            for note in track.notes:
                assert 0 <= note.pitch <= 127
                assert 1 <= note.velocity <= 127
                assert note.start >= 0
                assert note.duration > 0

    def test_different_genres_produce_different_instruments(self):
        random.seed(42)
        comp1 = Composition.from_prompt("rock piece", duration_seconds=30)
        random.seed(42)
        comp2 = Composition.from_prompt("jazz piece", duration_seconds=30)
        # They should use different instruments
        programs1 = {t.midi_program for t in comp1.tracks if not t.is_drum}
        programs2 = {t.midi_program for t in comp2.tracks if not t.is_drum}
        assert programs1 != programs2
