"""Lightweight movie summary & sentiment recap module.

Provides a placeholder abstraction for integrating an external LLM (e.g.,
Gemma / Google generative APIs). For environments without network access
or API credentials, falls back to a deterministic extractive style
summary so the UI still shows a meaningful block.
"""
from __future__ import annotations

from typing import List, Dict, Tuple
import re

try:  # Optional import pattern – real integration can be added later
    import google.generativeai as genai  # type: ignore
except Exception:  # pragma: no cover
    genai = None  # type: ignore

import os

GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")  # document in .env.example

SYSTEM_PROMPT = (
    "You are an assistant that composes concise, neutral movie review summaries in natural, flowing prose. "
    "Blend audience sentiment context with a spoiler‑safe synopsis. Avoid headings, labels, or bullet points. "
    "Write 2–4 sentences and keep it under 120 words."
)


def _extract_likes_dislikes(sentiments: Dict[str, int]) -> Tuple[str, str]:
    """Produce brief phrases about what viewers liked vs. disliked.

    This is heuristic in the fallback path (no LLM). We infer overall tone
    and craft generic but tailored phrasing. Real implementation could
    leverage keyword polarity aggregation.
    """
    pos = sentiments.get("positive", 0)
    neg = sentiments.get("negative", 0)
    total = max(1, sum(sentiments.values()))
    pos_ratio = pos / total
    neg_ratio = neg / total
    if pos_ratio >= 0.65:
        likes = "People praise its direction and emotional resonance."
    elif pos_ratio >= 0.5:
        likes = "People generally enjoy the performances and pacing."
    else:
        likes = "Positive comments highlight a handful of strong moments."

    if neg_ratio >= 0.45:
        dislikes = "Some point to uneven storytelling and tonal shifts."
    elif neg_ratio >= 0.3:
        dislikes = "Others mention pacing issues and predictable turns."
    else:
        dislikes = "A few note some familiar genre beats."
    return likes, dislikes


_SPOILER_CLEAN_PAT = re.compile(r"(kills?|dies|death|betrayal|murder|twist|identity|secret|culprit|final battle)", re.IGNORECASE)


def _sanitize_plot(plot: str | None) -> str:
    if not plot:
        return "Plot details unavailable."
    # Take first 1-2 sentences, neutralize potential spoilers by redacting trigger terms.
    sentences = re.split(r"(?<=[.!?])\s+", plot.strip())
    core = " ".join(sentences[:2])
    return _SPOILER_CLEAN_PAT.sub("[spoiler removed]", core)


def _fallback_summary(movie_title: str, plot: str | None, sentiments: Dict[str, int]) -> str:
    total = max(1, sum(sentiments.values()))
    pos_pct = round(sentiments.get("positive", 0) / total * 100)
    neu_pct = round(sentiments.get("neutral", 0) / total * 100)
    neg_pct = round(sentiments.get("negative", 0) / total * 100)
    likes, dislikes = _extract_likes_dislikes(sentiments)
    plot_part = _sanitize_plot(plot)
    lead = (
        f"Early reactions to '{movie_title}' lean positive (about {pos_pct}%), "
        f"with {neu_pct}% mixed and {neg_pct}% negative."
    )
    # Compose 2–4 natural sentences total
    return f"{lead} {likes} {dislikes} In short, {plot_part}"


def generate_summary(movie_title: str, plot: str | None, sentiments: Dict[str, int]) -> str:
    """Produce a human‑readable summary using Gemma if configured, else fallback.

    Parameters
    ----------
    movie_title: Title of the movie.
    plot: Optional plot text from metadata.
    sentiments: Dict with keys positive/neutral/negative counts.
    """
    if not GEMMA_API_KEY or not genai:  # no API configured
        return _fallback_summary(movie_title, plot, sentiments)

    try:  # pragma: no cover - external network
        genai.configure(api_key=GEMMA_API_KEY)
        model = genai.GenerativeModel("gemma-7b-it")
        prompt = (
            f"Movie: {movie_title}\n"
            f"Sentiment counts: {sentiments}.\n"
            f"Plot: {plot}\n"
            "Write 2–4 sentences of natural prose (no headings or lists). Start with the overall audience tilt using the counts, "
            "then briefly mention what people are liking and disliking, and end with a spoiler‑safe synopsis (avoid late‑act reveals). "
            "Keep it under 110 words."
        )
        resp = model.generate_content([SYSTEM_PROMPT, prompt])
        text = getattr(resp, "text", None) or "".join(getattr(resp, "candidates", []))
        cleaned = text.strip()
        # Light post-clean: ensure no obvious spoiler trigger words appear
        safe = _SPOILER_CLEAN_PAT.sub("[spoiler removed]", cleaned)
        return safe or _fallback_summary(movie_title, plot, sentiments)
    except Exception:
        return _fallback_summary(movie_title, plot, sentiments)
