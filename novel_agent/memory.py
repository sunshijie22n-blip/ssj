"""Story memory and continuity helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class StoryMemory:
    """Captures evolving story state for better continuity."""

    outline: List[str] = field(default_factory=list)
    chapters: List[str] = field(default_factory=list)

    def record_outline(self, outline: List[str]) -> None:
        """Store the outline for later reference."""

        self.outline = outline

    def record_chapter(self, chapter_text: str) -> None:
        """Append a new chapter to the timeline."""

        self.chapters.append(chapter_text)

    def continuity_summary(self) -> str:
        """Summarize prior chapters to remind the model of what happened."""

        if not self.chapters:
            return "No previous chapters; open with a gripping hook."

        summary_lines = []
        for idx, chapter in enumerate(self.chapters, start=1):
            condensed = " ".join(chapter.split())
            condensed = condensed[:320] + ("…" if len(condensed) > 320 else "")
            summary_lines.append(f"Chapter {idx}: {condensed}")
        return "\n".join(summary_lines)

