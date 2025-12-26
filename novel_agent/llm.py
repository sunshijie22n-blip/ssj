"""LLM interface and a lightweight local template implementation."""

from __future__ import annotations

import random
from typing import Protocol


class LLMClient(Protocol):
    """Interface for language model backends."""

    def generate(self, prompt: str, *, max_tokens: int = 512, temperature: float = 0.7) -> str:
        """Generate text for the given prompt."""


class LocalTemplateLLM:
    """A deterministic, offline-friendly stand-in for a real model.

    This class exists so the agent can run without external dependencies. It
    stitches together high-impact narrative fragments to simulate a model
    response while keeping the API surface similar to a production LLM.
    """

    def __init__(self, seed: int | None = None):
        self.random = random.Random(seed)

    def generate(self, prompt: str, *, max_tokens: int = 512, temperature: float = 0.7) -> str:
        """Return a pseudo-random response composed of curated fragments."""

        _ = max_tokens  # Max tokens intentionally unused by the template engine.
        del temperature

        opening = self.random.choice(
            [
                "Neon rain slicked the steelbones of the city, every drop an impatient metronome.",
                "The desert sky bruised purple as engines howled awake beyond the dunes.",
                "Towers leaned into the wind like conspirators as the night market lit its lanterns.",
            ]
        )
        heartbeat = self.random.choice(
            [
                "Somewhere deep underground, an old oath stirred.",
                "Between breaths, the world kept a secret just for the bold.",
                "Every sensor blinked amber as fate rerouted in real time.",
            ]
        )
        escalation = self.random.choice(
            [
                "Allies blurred into adversaries and back again in the same sentence.",
                "The plan bent, never quite breaking, fed by stubborn hope.",
                "Each step forward rewrote the rules no one dared to speak aloud.",
            ]
        )
        finish = self.random.choice(
            [
                "By dawn, nothing sacred remained untouched—exactly as promised.",
                "The chapter closed on a vow sharper than any blade.",
                "In the silence after the storm, the next rebellion inhaled.",
            ]
        )
        return " ".join([opening, heartbeat, escalation, finish])

