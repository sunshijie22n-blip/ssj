"""Outline planning for the novel agent."""

from __future__ import annotations

from typing import List

from .config import StoryConfig
from .llm import LLMClient


class OutlinePlanner:
    """Create a high-impact outline using an LLM backend."""

    def __init__(self, llm: LLMClient, config: StoryConfig):
        self.llm = llm
        self.config = config

    def build_outline(self) -> List[str]:
        """Generate a chapter-by-chapter plan."""

        prompt = self.config.outline_prompt()
        raw_outline = self.llm.generate(prompt, max_tokens=800, temperature=0.6)
        return self._postprocess(raw_outline)

    def _postprocess(self, raw_outline: str) -> List[str]:
        """Turn free-form text into a list of chapter beats."""

        lines = [line.strip("- ") for line in raw_outline.splitlines() if line.strip()]
        if not lines:
            lines = self._fallback_outline()

        while len(lines) < self.config.chapter_count:
            chapter_num = len(lines) + 1
            lines.append(
                f"Chapter {chapter_num}: push relationships to the edge and reveal a new layer of threat."
            )
        return lines[: self.config.chapter_count]

    def _fallback_outline(self) -> List[str]:
        """Provide a resilient default outline."""

        return [
            "Introduce the protagonist with a disruptive choice and a sharp hook.",
            "Escalate tensions between allies and rivals while the world frays.",
            "Deliver a midpoint reversal that forces a new objective.",
            "Tear down safety nets and expose the true antagonist strategy.",
            "Stage a penultimate clash that costs the hero dearly.",
            "Resolve the central conflict with irreversible change.",
        ]

