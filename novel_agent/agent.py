"""Orchestration logic for the novel generation agent."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from .config import StoryConfig
from .llm import LLMClient
from .memory import StoryMemory
from .planner import OutlinePlanner


class NovelAgent:
    """Coordinates outlining and chapter generation."""

    def __init__(
        self,
        llm: LLMClient,
        config: StoryConfig,
        memory: Optional[StoryMemory] = None,
    ):
        self.llm = llm
        self.config = config
        self.memory = memory or StoryMemory()

    def plan(self) -> List[str]:
        """Plan the full story outline."""

        outline = OutlinePlanner(self.llm, self.config).build_outline()
        self.memory.record_outline(outline)
        return outline

    def write(self, output_dir: Path | str) -> List[Path]:
        """Generate all chapters to the target folder."""

        if not self.memory.outline:
            self.plan()
        target = Path(output_dir)
        target.mkdir(parents=True, exist_ok=True)

        files: List[Path] = []
        for idx, summary in enumerate(self.memory.outline, start=1):
            prompt = self.config.chapter_prompt(idx, summary, self.memory.continuity_summary())
            text = self.llm.generate(prompt, max_tokens=2000, temperature=0.95)
            self.memory.record_chapter(text)
            chapter_path = target / f"chapter-{idx:02d}.txt"
            chapter_path.write_text(text, encoding="utf-8")
            files.append(chapter_path)

        metadata_path = target / "story-config.json"
        metadata_path.write_text(self.config_json(), encoding="utf-8")
        files.append(metadata_path)
        return files

    def config_json(self) -> str:
        """Serialize the current configuration and outline to JSON."""

        from json import dumps

        payload = self.config.to_dict()
        payload["outline"] = self.memory.outline
        return dumps(payload, indent=2, ensure_ascii=False)

