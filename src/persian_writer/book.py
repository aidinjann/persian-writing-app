from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Chapter:
    """Represents a single chapter in the book project."""

    title: str
    filename: str
    summary: str = ""
    goals: List[str] = field(default_factory=list)
    draft_status: str = "not-started"


@dataclass
class BookProject:
    """Encapsulates metadata and file operations for a book project."""

    root: Path
    title: str
    author: str
    genre: str
    tone: str
    target_length_words: int
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    synopsis: str = ""
    audience: str = ""
    language: str = "fa"
    chapters: List[Chapter] = field(default_factory=list)
    custom_guidelines: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "root": str(self.root),
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "tone": self.tone,
            "target_length_words": self.target_length_words,
            "created_at": self.created_at,
            "synopsis": self.synopsis,
            "audience": self.audience,
            "language": self.language,
            "custom_guidelines": self.custom_guidelines,
            "chapters": [chapter.__dict__ for chapter in self.chapters],
        }

    def save(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "chapters").mkdir(exist_ok=True)
        with open(self.root / "book.json", "w", encoding="utf-8") as fp:
            json.dump(self.to_dict(), fp, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, root: Path) -> "BookProject":
        with open(root / "book.json", "r", encoding="utf-8") as fp:
            data = json.load(fp)
        chapters = [Chapter(**chapter) for chapter in data.get("chapters", [])]
        return cls(
            root=Path(data["root"]),
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
            tone=data.get("tone", ""),
            target_length_words=int(data.get("target_length_words", 0)),
            created_at=data.get("created_at", ""),
            synopsis=data.get("synopsis", ""),
            audience=data.get("audience", ""),
            language=data.get("language", "fa"),
            custom_guidelines=data.get("custom_guidelines", []),
            chapters=chapters,
        )

    def add_chapter(self, title: str, summary: str = "", goals: Optional[List[str]] = None) -> Chapter:
        goals = goals or []
        index = len(self.chapters) + 1
        filename = f"{index:02d}-{self._slugify(title)}.md"
        chapter = Chapter(title=title, filename=filename, summary=summary, goals=goals)
        self.chapters.append(chapter)
        self.save()
        self._write_chapter_template(chapter)
        return chapter

    def _write_chapter_template(self, chapter: Chapter) -> None:
        template = self._chapter_template(chapter)
        chapter_path = self.root / "chapters" / chapter.filename
        chapter_path.write_text(template, encoding="utf-8")

    def _chapter_template(self, chapter: Chapter) -> str:
        lines = [
            f"# {chapter.title}\n",
            "\n",
            "خلاصه:\n",
            f"{chapter.summary}\n\n" if chapter.summary else "(اینجا خلاصه فصل را بنویسید)\n\n",
            "اهداف فصل:\n",
        ]
        goals = chapter.goals or [
            "با معرفی مسئله یا سوال اصلی شروع کنید.",
            "از روایت‌ها و مثال‌های ملموس فارسی استفاده کنید.",
            "از نقل قول‌های معتبر برای تقویت استدلال بهره بگیرید.",
        ]
        for goal in goals:
            lines.append(f"- {goal}\n")
        lines.extend(
            [
                "\n",
                "## ساختار پیشنهادی\n",
                "1. مقدمه و طرح پرسش\n",
                "2. ارائه زمینه و پیش‌فرض‌ها\n",
                "3. بسط ایده‌ها با نمونه‌های مستند\n",
                "4. جمع‌بندی موقت و طرح پرسش بعدی\n",
                "5. یادداشت‌های پژوهشی و منابع\n",
                "\n",
                "## بدنه فصل\n",
                "(اینجا پیش‌نویس کامل فصل را بنویسید)\n",
                "\n",
                "## بازنویسی و ویرایش\n",
                "- وضوح جملات را بررسی کنید.\n",
                "- لحن را با لحن کلی کتاب هماهنگ نگه دارید.\n",
                "- اطمینان از پیوستگی منطقی بخش‌ها.\n",
                "\n",
                "## فهرست منابع فصل\n",
                "- نویسنده، «عنوان»، ناشر، سال.\n",
            ]
        )
        return "".join(lines)

    @staticmethod
    def _slugify(text: str) -> str:
        normalized = text.strip().replace(" ", "-")
        for bad in "\u200c\t\n\r،؟؛!؛؛":
            normalized = normalized.replace(bad, "-")
        return normalized.lower()


def create_project(
    target: Path,
    title: str,
    author: str,
    genre: str,
    tone: str,
    target_length_words: int,
    synopsis: str = "",
    audience: str = "",
    custom_guidelines: Optional[List[str]] = None,
) -> BookProject:
    custom_guidelines = custom_guidelines or []
    project = BookProject(
        root=target,
        title=title,
        author=author,
        genre=genre,
        tone=tone,
        target_length_words=target_length_words,
        synopsis=synopsis,
        audience=audience,
        custom_guidelines=custom_guidelines,
    )
    project.save()
    _write_guidelines(project)
    return project


def _write_guidelines(project: BookProject) -> None:
    guideline_lines = [
        f"# راهنمای نگارش برای «{project.title}»\n\n",
        "## مشخصات کلی\n",
        f"- نویسنده: {project.author}\n",
        f"- ژانر: {project.genre}\n",
        f"- لحن: {project.tone}\n",
        f"- طول هدف: {project.target_length_words} واژه\n\n",
        "## مخاطب و هدف\n",
        f"- مخاطب اصلی: {project.audience or 'مشخص نشده'}\n",
        f"- خلاصه/سیلوپیس: {project.synopsis or 'هنوز نوشته نشده است'}\n\n",
        "## اصول نگارش پیشنهادی\n",
        "- انسجام پاراگراف‌ها و پیوستگی موضوعی حفظ شود.\n",
        "- از علائم سجاوندی فارسی شامل «،» و «؛» درست استفاده کنید.\n",
        "- از واژگان هم‌معنی برای پرهیز از تکرار استفاده کنید.\n",
        "- ارجاع به منابع مطابق شیوه‌نامه انتخابی (مثل APA) نوشته شود.\n",
        "- نقل قول‌ها دقیق و با ذکر صفحه ثبت شوند.\n\n",
        "## دستورالعمل‌های اختصاصی\n",
    ]
    guideline_lines.extend([f"- {rule}\n" for rule in project.custom_guidelines])
    guideline_lines.append("\nموفق باشید!\n")
    (project.root / "guidelines.md").write_text("".join(guideline_lines), encoding="utf-8")
