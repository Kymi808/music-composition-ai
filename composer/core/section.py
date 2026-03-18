"""Section - represents a song section (intro, verse, chorus, etc.)."""

from __future__ import annotations

from dataclasses import dataclass, field

from composer.core.track import Track


@dataclass
class Section:
    """A section of the composition (e.g., intro, verse, chorus)."""

    name: str  # intro, verse, chorus, bridge, outro, buildup, breakdown
    tracks: list[Track] = field(default_factory=list)
    duration_beats: float = 0.0
    intensity: float = 0.7  # 0-1

    @property
    def duration(self) -> float:
        if self.duration_beats > 0:
            return self.duration_beats
        if self.tracks:
            return max((t.duration for t in self.tracks), default=0)
        return 0

    def add_track(self, track: Track) -> None:
        self.tracks.append(track)

    def __repr__(self) -> str:
        return f"Section({self.name}, {len(self.tracks)} tracks, {self.duration:.1f} beats)"
