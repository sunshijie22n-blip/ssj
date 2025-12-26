"""Command-line entry point for the novel agent."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from .agent import NovelAgent
from .config import StoryConfig
from .llm import LocalTemplateLLM
from .memory import StoryMemory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a long-form novel with an agent.")
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a JSON configuration file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("./novel_output"),
        help="Directory where chapters will be written.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for deterministic local generation.",
    )
    return parser


def load_config(path: Optional[Path]) -> StoryConfig:
    if path:
        return StoryConfig.from_json(path)
    return StoryConfig()


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    config = load_config(args.config)
    llm = LocalTemplateLLM(seed=args.seed)
    memory = StoryMemory()

    agent = NovelAgent(llm=llm, config=config, memory=memory)
    outline = agent.plan()
    files = agent.write(args.output)

    print("Generated outline:")
    for idx, beat in enumerate(outline, start=1):
        print(f"  {idx}. {beat}")
    print("\nChapters saved to:")
    for file in files:
        print(f"- {file}")


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()

