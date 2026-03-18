"""Genre-specific instrument combination presets."""

from __future__ import annotations

from composer.theory.constants import GM_INSTRUMENTS


class GenrePresets:
    """Pre-defined instrument palettes for each genre."""

    PRESETS: dict[str, dict[str, int]] = {
        "orchestral": {
            "melody": GM_INSTRUMENTS["violin"],
            "harmony": GM_INSTRUMENTS["viola"],
            "accompaniment": GM_INSTRUMENTS["string_ensemble_1"],
            "bass": GM_INSTRUMENTS["contrabass"],
            "pad": GM_INSTRUMENTS["choir_aahs"],
        },
        "cinematic": {
            "melody": GM_INSTRUMENTS["french_horn"],
            "harmony": GM_INSTRUMENTS["string_ensemble_1"],
            "accompaniment": GM_INSTRUMENTS["choir_aahs"],
            "bass": GM_INSTRUMENTS["contrabass"],
            "pad": GM_INSTRUMENTS["pad_warm"],
        },
        "electronic": {
            "melody": GM_INSTRUMENTS["lead_sawtooth"],
            "harmony": GM_INSTRUMENTS["lead_square"],
            "accompaniment": GM_INSTRUMENTS["pad_polysynth"],
            "bass": GM_INSTRUMENTS["synth_bass_1"],
            "pad": GM_INSTRUMENTS["pad_warm"],
        },
        "jazz": {
            "melody": GM_INSTRUMENTS["alto_sax"],
            "harmony": GM_INSTRUMENTS["acoustic_grand_piano"],
            "accompaniment": GM_INSTRUMENTS["acoustic_grand_piano"],
            "bass": GM_INSTRUMENTS["acoustic_bass"],
        },
        "rock": {
            "melody": GM_INSTRUMENTS["electric_guitar_clean"],
            "harmony": GM_INSTRUMENTS["overdriven_guitar"],
            "accompaniment": GM_INSTRUMENTS["electric_guitar_clean"],
            "bass": GM_INSTRUMENTS["electric_bass_finger"],
        },
        "metal": {
            "melody": GM_INSTRUMENTS["distortion_guitar"],
            "harmony": GM_INSTRUMENTS["overdriven_guitar"],
            "accompaniment": GM_INSTRUMENTS["distortion_guitar"],
            "bass": GM_INSTRUMENTS["electric_bass_pick"],
        },
        "classical": {
            "melody": GM_INSTRUMENTS["acoustic_grand_piano"],
            "harmony": GM_INSTRUMENTS["violin"],
            "accompaniment": GM_INSTRUMENTS["acoustic_grand_piano"],
            "bass": GM_INSTRUMENTS["cello"],
        },
        "ambient": {
            "melody": GM_INSTRUMENTS["pad_choir"],
            "harmony": GM_INSTRUMENTS["pad_warm"],
            "accompaniment": GM_INSTRUMENTS["pad_new_age"],
            "bass": GM_INSTRUMENTS["synth_bass_2"],
            "pad": GM_INSTRUMENTS["pad_sweep"],
        },
        "folk": {
            "melody": GM_INSTRUMENTS["flute"],
            "harmony": GM_INSTRUMENTS["acoustic_guitar_nylon"],
            "accompaniment": GM_INSTRUMENTS["acoustic_guitar_steel"],
            "bass": GM_INSTRUMENTS["acoustic_bass"],
        },
        "blues": {
            "melody": GM_INSTRUMENTS["electric_guitar_clean"],
            "harmony": GM_INSTRUMENTS["acoustic_grand_piano"],
            "accompaniment": GM_INSTRUMENTS["acoustic_grand_piano"],
            "bass": GM_INSTRUMENTS["electric_bass_finger"],
        },
        "rnb": {
            "melody": GM_INSTRUMENTS["electric_piano_1"],
            "harmony": GM_INSTRUMENTS["pad_warm"],
            "accompaniment": GM_INSTRUMENTS["electric_piano_2"],
            "bass": GM_INSTRUMENTS["electric_bass_finger"],
        },
        "pop": {
            "melody": GM_INSTRUMENTS["acoustic_grand_piano"],
            "harmony": GM_INSTRUMENTS["string_ensemble_1"],
            "accompaniment": GM_INSTRUMENTS["acoustic_guitar_steel"],
            "bass": GM_INSTRUMENTS["electric_bass_finger"],
        },
    }

    @classmethod
    def get(cls, genre: str) -> dict[str, int]:
        """Get instrument palette for a genre."""
        return cls.PRESETS.get(genre, cls.PRESETS["cinematic"]).copy()

    @classmethod
    def override_with_requested(
        cls,
        palette: dict[str, int],
        requested_instruments: list[str],
    ) -> dict[str, int]:
        """Override palette with user-requested instruments."""
        if not requested_instruments:
            return palette

        roles = ["melody", "harmony", "accompaniment", "bass", "pad"]
        for i, inst_name in enumerate(requested_instruments):
            if inst_name in GM_INSTRUMENTS:
                role = roles[i % len(roles)]
                palette[role] = GM_INSTRUMENTS[inst_name]

        return palette

    @classmethod
    def list_genres(cls) -> list[str]:
        return sorted(cls.PRESETS.keys())
