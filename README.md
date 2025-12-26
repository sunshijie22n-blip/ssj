# ssj novel agent

A compact Python toolkit for running an **unrestricted long-form novel generation agent**. The agent plans a chapter outline, keeps continuity memory, and writes chapters using a pluggable language model backend.

## Features
- Structured `StoryConfig` with genre, tone, POV, and fearless writer directives.
- Outline planner plus continuity-aware chapter writer.
- Swappable LLM client interface; ships with an offline-friendly template generator for quick demos.
- Simple CLI that saves chapters and configuration metadata to disk.

## Quickstart
1. Ensure Python 3.11+ is available.
2. Run the CLI with defaults:
   ```bash
   python -m novel_agent.cli --output ./novel_output
   ```
3. Use a custom JSON config for a richer run:
   ```bash
   python -m novel_agent.cli --config ./examples/story_config.json --output ./graviton_noir
   ```

Chapters and the serialized configuration will be written to the chosen output directory.

## Customizing the agent
- Edit `examples/story_config.json` or create your own; all fields align with the `StoryConfig` dataclass.
- Swap in a real model by implementing `LLMClient.generate`—for example, wrapping an OpenAI or HuggingFace client—and pass it to `NovelAgent` instead of the default `LocalTemplateLLM`.
- Adjust `writer_directives` to emphasize tone, pacing, or thematic boundaries; the agent inlines them into prompts to keep output intense and unconstrained.

## Project layout
- `novel_agent/config.py` – configuration dataclasses and prompt templates.
- `novel_agent/llm.py` – LLM interface plus the offline template generator.
- `novel_agent/memory.py` – continuity memory across chapters.
- `novel_agent/planner.py` – outline generation logic.
- `novel_agent/agent.py` – orchestration that plans then writes chapters.
- `novel_agent/cli.py` – command-line interface for running the agent end to end.
- `examples/story_config.json` – sample fearless story configuration.

