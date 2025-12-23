# Persian Writing App

ابزاری خط فرمان برای ایجاد و مدیریت پروژه‌های کتاب‌نویسی فارسی با تمرکز بر کتاب‌های حجیم و علمی.

## نصب
```
pip install -e .
```

## دستورها
- `persian-writer init <path> <title> <author> <genre> <tone> <target_length>`
  - گزینه‌های اضافی: `--synopsis`، `--audience`، `--guideline` (قابل تکرار)
- `persian-writer add-chapter <path> <title> [--summary ...] [--goal ...]`
- `persian-writer outline <path> [--sections N]`
- `persian-writer analyze <file>`
- `persian-writer style-guide`
- `persian-writer prompts <path>`

## نمونه جریان کار
```
persian-writer init book-project "تاریخ اندیشه" "نویسنده" "پژوهشی" "رسمی" 120000 --audience "دانشگاهی"
persian-writer add-chapter book-project "مقدمه" --summary "طرح کلی کتاب"
persian-writer analyze book-project/chapters/01-مقدمه.md
persian-writer outline book-project
persian-writer style-guide
```

پس از اجرای init فایل‌های `book.json`، `guidelines.md` و `outline.md` و پوشه `chapters/` ایجاد می‌شود.
