from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent
from typing import List

from .book import BookProject


@dataclass
class OutlineItem:
    title: str
    summary: str
    word_target: int


def build_outline(project: BookProject, major_sections: int = 8) -> List[OutlineItem]:
    avg_chapter_words = max(project.target_length_words // max(major_sections, 1), 1500)
    outline = []
    for idx in range(1, major_sections + 1):
        outline.append(
            OutlineItem(
                title=f"فصل {idx}",
                summary=f"گسترش خط روایی در بخش {idx} با تاکید بر مخاطب {project.audience or 'عمومی'}.",
                word_target=avg_chapter_words,
            )
        )
    return outline


def format_outline(outline: List[OutlineItem]) -> str:
    lines = ["## طرح کلی پیشنهادی\n"]
    for item in outline:
        lines.append(f"### {item.title}\n")
        lines.append(f"- خلاصه: {item.summary}\n")
        lines.append(f"- هدف واژگانی: {item.word_target}\n\n")
    return "".join(lines)


def style_guide() -> str:
    return dedent(
        """
        # شیوه‌نامه نگارش فارسی برای کتاب‌های حجیم

        - از نیم‌فاصله‌ در ترکیب‌های رایج («می‌رود»، «ها‌ی») استفاده کنید.
        - پاراگراف‌های طولانی را به بخش‌های کوتاه‌تر تقسیم کنید تا خوانایی حفظ شود.
        - تیترها را با اعداد و ساختار سلسله‌مراتبی مشخص کنید (۱، ۱.۱، ۱.۱.۱).
        - نقل‌قول‌های طولانی را در قالب بلاک‌کوت با منبع دقیق بیاورید.
        - برای آمار و داده‌ها جدول بسازید و واحد اندازه‌گیری را ذکر کنید.
        - در پایان هر فصل، «خلاصه و درس‌های کلیدی» و «پرسش برای مطالعه بیشتر» اضافه کنید.
        - ارجاعات درون‌متنی را با شیوه‌نامه ثابت (APA یا شبیه آن) هماهنگ کنید.
        - برای واژگان تخصصی، واژه‌نامه پایانی بسازید و همه مدخل‌ها را به‌روزرسانی کنید.
        - هنگام استفاده از اشعار و متون کهن، اعراب‌گذاری و منبع را ذکر کنید.
        - در متن از اعداد فارسی استفاده کنید مگر در کد یا URL.
        """
    ).strip() + "\n"


def research_prompts(project: BookProject) -> str:
    prompts = [
        "تحلیل روند تاریخی موضوع و تاثیر آن بر وضعیت امروز",
        "گفت‌وگو با متخصصان و نقل نظر آنان",
        "مطالعه موردی از یک نمونه موفق ایرانی یا بین‌المللی",
        "مقایسه تطبیقی با آثار مشابه و بررسی تمایز کتاب شما",
        "ارجاع به منابع دانشگاهی و مقالات علمی برای استحکام استدلال",
        "گردآوری واژگان تخصصی و ساخت واژه‌نامه پایانی",
    ]
    lines = ["## فهرست موضوعات پژوهشی و مصاحبه\n"]
    for prompt in prompts:
        lines.append(f"- {prompt}\n")
    return "".join(lines)
