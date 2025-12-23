from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analysis import analyze_text, format_metrics
from .book import BookProject, create_project
from .outline import build_outline, format_outline, research_prompts, style_guide


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="دستیار جامع نگارش کتاب فارسی",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_cmd = subparsers.add_parser("init", help="ایجاد پروژه کتاب")
    init_cmd.add_argument("path", type=Path, help="مسیر پوشه پروژه")
    init_cmd.add_argument("title", help="عنوان کتاب")
    init_cmd.add_argument("author", help="نام نویسنده")
    init_cmd.add_argument("genre", help="ژانر")
    init_cmd.add_argument("tone", help="لحن (رسمی، صمیمی و ...)")
    init_cmd.add_argument("target_length", type=int, help="تعداد واژه هدف")
    init_cmd.add_argument("--synopsis", default="", help="خلاصه کوتاه کتاب")
    init_cmd.add_argument("--audience", default="", help="مخاطب هدف")
    init_cmd.add_argument(
        "--guideline",
        action="append",
        default=[],
        help="دستورالعمل اختصاصی؛ می‌توانید چندین بار استفاده کنید",
    )

    add_cmd = subparsers.add_parser("add-chapter", help="افزودن فصل جدید")
    add_cmd.add_argument("path", type=Path, help="مسیر پوشه پروژه")
    add_cmd.add_argument("title", help="عنوان فصل")
    add_cmd.add_argument("--summary", default="", help="خلاصه فصل")
    add_cmd.add_argument("--goal", action="append", default=[], help="هدف فصل")

    outline_cmd = subparsers.add_parser("outline", help="تولید طرح کلی")
    outline_cmd.add_argument("path", type=Path, help="مسیر پوشه پروژه")
    outline_cmd.add_argument("--sections", type=int, default=8, help="تعداد فصل پیشنهادی")

    analyze_cmd = subparsers.add_parser("analyze", help="تحلیل متن")
    analyze_cmd.add_argument("file", type=Path, help="مسیر فایل متنی یا فصل")

    subparsers.add_parser("style-guide", help="نمایش شیوه‌نامه نگارش")

    prompts_cmd = subparsers.add_parser("prompts", help="پیشنهاد سوژه‌های پژوهشی")
    prompts_cmd.add_argument("path", type=Path, help="مسیر پوشه پروژه")

    return parser.parse_args(argv)


def cmd_init(args: argparse.Namespace) -> None:
    project = create_project(
        target=args.path,
        title=args.title,
        author=args.author,
        genre=args.genre,
        tone=args.tone,
        target_length_words=args.target_length,
        synopsis=args.synopsis,
        audience=args.audience,
        custom_guidelines=args.guideline,
    )
    outline = build_outline(project)
    (project.root / "outline.md").write_text(format_outline(outline), encoding="utf-8")
    print(f"پروژه ایجاد شد: {project.root}")
    print("فایل‌های کلیدی: book.json، guidelines.md، outline.md، پوشه chapters/")


def cmd_add_chapter(args: argparse.Namespace) -> None:
    project = BookProject.load(args.path)
    chapter = project.add_chapter(title=args.title, summary=args.summary, goals=args.goal)
    print(f"فصل ایجاد شد: chapters/{chapter.filename}")


def cmd_outline(args: argparse.Namespace) -> None:
    project = BookProject.load(args.path)
    outline = build_outline(project, major_sections=args.sections)
    print(format_outline(outline))


def cmd_analyze(args: argparse.Namespace) -> None:
    text = args.file.read_text(encoding="utf-8")
    metrics = analyze_text(text)
    print(format_metrics(metrics))


def cmd_style_guide() -> None:
    print(style_guide())


def cmd_prompts(args: argparse.Namespace) -> None:
    project = BookProject.load(args.path)
    print(research_prompts(project))


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.command == "init":
        cmd_init(args)
    elif args.command == "add-chapter":
        cmd_add_chapter(args)
    elif args.command == "outline":
        cmd_outline(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "style-guide":
        cmd_style_guide()
    elif args.command == "prompts":
        cmd_prompts(args)
    else:
        raise ValueError("unknown command")


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
