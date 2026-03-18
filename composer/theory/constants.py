"""Musical constants - note names, MIDI mappings, intervals."""

from __future__ import annotations

# Note names (sharps)
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Flat equivalents
FLAT_TO_SHARP = {
    "Db": "C#", "Eb": "D#", "Fb": "E", "Gb": "F#",
    "Ab": "G#", "Bb": "A#", "Cb": "B",
}

SHARP_TO_FLAT = {v: k for k, v in FLAT_TO_SHARP.items()}

# Interval names to semitone counts
INTERVALS = {
    "unison": 0, "P1": 0,
    "minor_second": 1, "m2": 1,
    "major_second": 2, "M2": 2,
    "minor_third": 3, "m3": 3,
    "major_third": 4, "M3": 4,
    "perfect_fourth": 5, "P4": 5,
    "tritone": 6, "aug4": 6, "dim5": 6,
    "perfect_fifth": 7, "P5": 7,
    "minor_sixth": 8, "m6": 8,
    "major_sixth": 9, "M6": 9,
    "minor_seventh": 10, "m7": 10,
    "major_seventh": 11, "M7": 11,
    "octave": 12, "P8": 12,
    "minor_ninth": 13, "m9": 13,
    "major_ninth": 14, "M9": 14,
    "minor_tenth": 15, "m10": 15,
    "major_tenth": 16, "M10": 16,
    "perfect_eleventh": 17, "P11": 17,
    "sharp_eleventh": 18, "#11": 18,
    "perfect_twelfth": 19, "P12": 19,
    "minor_thirteenth": 20, "m13": 20,
    "major_thirteenth": 21, "M13": 21,
}

# Scale interval patterns (in semitones)
SCALE_PATTERNS = {
    "major":             [2, 2, 1, 2, 2, 2, 1],
    "natural_minor":     [2, 1, 2, 2, 1, 2, 2],
    "harmonic_minor":    [2, 1, 2, 2, 1, 3, 1],
    "melodic_minor":     [2, 1, 2, 2, 2, 2, 1],
    "dorian":            [2, 1, 2, 2, 2, 1, 2],
    "phrygian":          [1, 2, 2, 2, 1, 2, 2],
    "lydian":            [2, 2, 2, 1, 2, 2, 1],
    "mixolydian":        [2, 2, 1, 2, 2, 1, 2],
    "locrian":           [1, 2, 2, 1, 2, 2, 2],
    "pentatonic_major":  [2, 2, 3, 2, 3],
    "pentatonic_minor":  [3, 2, 2, 3, 2],
    "blues":             [3, 2, 1, 1, 3, 2],
    "whole_tone":        [2, 2, 2, 2, 2, 2],
    "chromatic":         [1] * 12,
    "hungarian_minor":   [2, 1, 3, 1, 1, 3, 1],
    "phrygian_dominant": [1, 3, 1, 2, 1, 2, 2],
    "double_harmonic":   [1, 3, 1, 2, 1, 3, 1],
}

# Alias commonly used scale names
SCALE_ALIASES = {
    "minor": "natural_minor",
    "aeolian": "natural_minor",
    "ionian": "major",
}

# General MIDI instrument programs (0-indexed)
GM_INSTRUMENTS = {
    # Piano
    "acoustic_grand_piano": 0,
    "bright_acoustic_piano": 1,
    "electric_grand_piano": 2,
    "honky_tonk_piano": 3,
    "electric_piano_1": 4,
    "electric_piano_2": 5,
    "harpsichord": 6,
    "clavinet": 7,
    # Chromatic Percussion
    "celesta": 8,
    "glockenspiel": 9,
    "music_box": 10,
    "vibraphone": 11,
    "marimba": 12,
    "xylophone": 13,
    "tubular_bells": 14,
    "dulcimer": 15,
    # Organ
    "drawbar_organ": 16,
    "percussive_organ": 17,
    "rock_organ": 18,
    "church_organ": 19,
    "reed_organ": 20,
    "accordion": 21,
    "harmonica": 22,
    "tango_accordion": 23,
    # Guitar
    "acoustic_guitar_nylon": 24,
    "acoustic_guitar_steel": 25,
    "electric_guitar_jazz": 26,
    "electric_guitar_clean": 27,
    "electric_guitar_muted": 28,
    "overdriven_guitar": 29,
    "distortion_guitar": 30,
    "guitar_harmonics": 31,
    # Bass
    "acoustic_bass": 32,
    "electric_bass_finger": 33,
    "electric_bass_pick": 34,
    "fretless_bass": 35,
    "slap_bass_1": 36,
    "slap_bass_2": 37,
    "synth_bass_1": 38,
    "synth_bass_2": 39,
    # Strings
    "violin": 40,
    "viola": 41,
    "cello": 42,
    "contrabass": 43,
    "tremolo_strings": 44,
    "pizzicato_strings": 45,
    "orchestral_harp": 46,
    "timpani": 47,
    # Ensemble
    "string_ensemble_1": 48,
    "string_ensemble_2": 49,
    "synth_strings_1": 50,
    "synth_strings_2": 51,
    "choir_aahs": 52,
    "voice_oohs": 53,
    "synth_choir": 54,
    "orchestra_hit": 55,
    # Brass
    "trumpet": 56,
    "trombone": 57,
    "tuba": 58,
    "muted_trumpet": 59,
    "french_horn": 60,
    "brass_section": 61,
    "synth_brass_1": 62,
    "synth_brass_2": 63,
    # Reed
    "soprano_sax": 64,
    "alto_sax": 65,
    "tenor_sax": 66,
    "baritone_sax": 67,
    "oboe": 68,
    "english_horn": 69,
    "bassoon": 70,
    "clarinet": 71,
    # Pipe
    "piccolo": 72,
    "flute": 73,
    "recorder": 74,
    "pan_flute": 75,
    "blown_bottle": 76,
    "shakuhachi": 77,
    "whistle": 78,
    "ocarina": 79,
    # Synth Lead
    "lead_square": 80,
    "lead_sawtooth": 81,
    "lead_calliope": 82,
    "lead_chiff": 83,
    "lead_charang": 84,
    "lead_voice": 85,
    "lead_fifths": 86,
    "lead_bass_lead": 87,
    # Synth Pad
    "pad_new_age": 88,
    "pad_warm": 89,
    "pad_polysynth": 90,
    "pad_choir": 91,
    "pad_bowed": 92,
    "pad_metallic": 93,
    "pad_halo": 94,
    "pad_sweep": 95,
    # Synth Effects
    "fx_rain": 96,
    "fx_soundtrack": 97,
    "fx_crystal": 98,
    "fx_atmosphere": 99,
    "fx_brightness": 100,
    "fx_goblins": 101,
    "fx_echoes": 102,
    "fx_sci_fi": 103,
    # Ethnic
    "sitar": 104,
    "banjo": 105,
    "shamisen": 106,
    "koto": 107,
    "kalimba": 108,
    "bagpipe": 109,
    "fiddle": 110,
    "shanai": 111,
    # Percussive
    "tinkle_bell": 112,
    "agogo": 113,
    "steel_drums": 114,
    "woodblock": 115,
    "taiko_drum": 116,
    "melodic_tom": 117,
    "synth_drum": 118,
    "reverse_cymbal": 119,
    # Sound Effects
    "guitar_fret_noise": 120,
    "breath_noise": 121,
    "seashore": 122,
    "bird_tweet": 123,
    "telephone_ring": 124,
    "helicopter": 125,
    "applause": 126,
    "gunshot": 127,
}

# General MIDI drum map (channel 10, note numbers)
GM_DRUMS = {
    "bass_drum_2": 35,
    "bass_drum_1": 36,
    "side_stick": 37,
    "snare_drum": 38,
    "hand_clap": 39,
    "snare_drum_2": 40,
    "low_floor_tom": 41,
    "closed_hi_hat": 42,
    "high_floor_tom": 43,
    "pedal_hi_hat": 44,
    "low_tom": 45,
    "open_hi_hat": 46,
    "low_mid_tom": 47,
    "hi_mid_tom": 48,
    "crash_cymbal_1": 49,
    "high_tom": 50,
    "ride_cymbal_1": 51,
    "chinese_cymbal": 52,
    "ride_bell": 53,
    "tambourine": 54,
    "splash_cymbal": 55,
    "cowbell": 56,
    "crash_cymbal_2": 57,
    "vibraslap": 58,
    "ride_cymbal_2": 59,
    "hi_bongo": 60,
    "low_bongo": 61,
    "mute_hi_conga": 62,
    "open_hi_conga": 63,
    "low_conga": 64,
    "high_timbale": 65,
    "low_timbale": 66,
    "high_agogo": 67,
    "low_agogo": 68,
    "cabasa": 69,
    "maracas": 70,
    "short_whistle": 71,
    "long_whistle": 72,
    "short_guiro": 73,
    "long_guiro": 74,
    "claves": 75,
    "hi_wood_block": 76,
    "low_wood_block": 77,
    "mute_cuica": 78,
    "open_cuica": 79,
    "mute_triangle": 80,
    "open_triangle": 81,
}

# Instrument ranges (MIDI note numbers: low, high)
INSTRUMENT_RANGES = {
    "piano": (21, 108),
    "violin": (55, 103),
    "viola": (48, 91),
    "cello": (36, 76),
    "contrabass": (28, 60),
    "flute": (60, 96),
    "oboe": (58, 91),
    "clarinet": (50, 94),
    "bassoon": (34, 75),
    "french_horn": (34, 77),
    "trumpet": (55, 82),
    "trombone": (40, 72),
    "tuba": (28, 58),
    "acoustic_guitar_nylon": (40, 84),
    "electric_guitar_clean": (40, 86),
    "acoustic_bass": (28, 55),
    "electric_bass_finger": (28, 60),
    "alto_sax": (56, 87),
    "tenor_sax": (49, 80),
    "soprano_sax": (60, 93),
    "baritone_sax": (44, 75),
    "harp": (24, 103),
    "celesta": (60, 108),
    "vibraphone": (53, 89),
    "marimba": (45, 96),
    "timpani": (40, 55),
}

# Dynamic markings to MIDI velocity
DYNAMICS = {
    "ppp": 16,
    "pp": 33,
    "p": 49,
    "mp": 64,
    "mf": 80,
    "f": 96,
    "ff": 112,
    "fff": 127,
}


def note_name_to_midi(name: str, octave: int = 4) -> int:
    """Convert note name + octave to MIDI number. e.g., 'C', 4 -> 60."""
    name = name.strip()
    if name in FLAT_TO_SHARP:
        name = FLAT_TO_SHARP[name]
    idx = NOTE_NAMES.index(name)
    return (octave + 1) * 12 + idx


def midi_to_note_name(midi_num: int) -> tuple[str, int]:
    """Convert MIDI number to (note_name, octave)."""
    octave = (midi_num // 12) - 1
    note = NOTE_NAMES[midi_num % 12]
    return note, octave
