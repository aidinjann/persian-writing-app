from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


PERSIAN_PUNCTUATION = "،؛؟!"
SENTENCE_ENDINGS = re.compile(r"[\.؟!！!]")
REPEATED_SPACES = re.compile(r"\s{2,}")


@dataclass
class TextMetrics:
    words: int
    sentences: int
    paragraphs: int
    average_sentence_length: float
    average_paragraph_length: float
    long_sentences: List[str]
    repeated_spaces: List[str]
    typography_alerts: List[str]


def analyze_text(text: str) -> TextMetrics:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    sentences = SENTENCE_ENDINGS.split(text)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = re.findall(r"\w+", text, flags=re.UNICODE)

    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    avg_paragraph_length = len(words) / len(paragraphs) if paragraphs else 0

    long_sentences = [s for s in sentences if len(s.split()) > 30]
    repeated_spaces = [m.group(0) for m in REPEATED_SPACES.finditer(text)]

    typography_alerts = []
    if " ," in text:
        typography_alerts.append("فاصله قبل از ویرگول را حذف کنید.")
    if " ;" in text:
        typography_alerts.append("فاصله قبل از نقطه ویرگول نباید باشد.")
    if "! !" in text:
        typography_alerts.append("از دو علامت تعجب پشت سر هم پرهیز کنید.")
    if "? ?" in text:
        typography_alerts.append("از چند علامت سوال پشت سر هم پرهیز کنید.")

    return TextMetrics(
        words=len(words),
        sentences=len(sentences),
        paragraphs=len(paragraphs),
        average_sentence_length=round(avg_sentence_length, 2),
        average_paragraph_length=round(avg_paragraph_length, 2),
        long_sentences=long_sentences,
        repeated_spaces=repeated_spaces,
        typography_alerts=typography_alerts,
    )


def format_metrics(metrics: TextMetrics) -> str:
    lines = [
        "## شاخص‌های متن\n",
        f"- تعداد واژه‌ها: {metrics.words}\n",
        f"- تعداد جمله‌ها: {metrics.sentences}\n",
        f"- تعداد پاراگراف‌ها: {metrics.paragraphs}\n",
        f"- میانگین طول جمله: {metrics.average_sentence_length} واژه\n",
        f"- میانگین طول پاراگراف: {metrics.average_paragraph_length} واژه\n",
        "\n",
    ]

    if metrics.long_sentences:
        lines.append("جمله‌های بلند (بیش از ۳۰ واژه):\n")
        for sentence in metrics.long_sentences:
            lines.append(f"- {sentence}\n")
        lines.append("\n")

    if metrics.repeated_spaces:
        lines.append("هشدار: فاصله‌های تکراری پیدا شد.\n")
    if metrics.typography_alerts:
        lines.append("هشدارهای ویرایشی:\n")
        for alert in metrics.typography_alerts:
            lines.append(f"- {alert}\n")

    return "".join(lines)
