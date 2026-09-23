# File Processing Toolkit

A safe, dependency-free Python toolkit for file inventory, hashing, duplicate detection, and deterministic bulk-rename planning.

> English first · العربية أدناه

## English

### Overview
File Processing Toolkit turns common filesystem inspection tasks into one consistent CLI and Python API. It is designed for local automation where predictable behavior, useful validation, and safe defaults matter more than a large dependency stack.

### Why it exists
Small file jobs often become unrelated one-off scripts. This project provides tested primitives that can be reused in terminals, scripts, and CI without uploading filenames or file contents anywhere.

### Features
- Recursive or flat file inventory with extension and minimum-size filters.
- Streaming SHA-256 hashing by default; other algorithms exposed by Python `hashlib` are supported.
- Duplicate detection that groups by size first, then verifies file content by cryptographic hash.
- Deterministic bulk rename planning with extension preservation and collision checks.
- **Safe by default:** rename is preview-only until `--apply` is explicitly supplied.
- JSON output for inventory and duplicate groups.
- UTF-8 / Arabic filenames, Windows, macOS and Linux support.
- Python API with no runtime third-party dependencies.

### Preview
```text
$ file-toolkit rename ./incoming --prefix photo-
IMG_0042.jpg -> photo-001.jpg
IMG_0088.jpg -> photo-002.jpg
Preview only. Add --apply to perform these renames.
```
For repository screenshots, capture the preview command above against non-sensitive sample files; do not commit personal filenames merely for a screenshot.

### Requirements & installation
- Python 3.10+

```bash
git clone https://github.com/rad03i2/file-processing-toolkit.git
cd file-processing-toolkit
python -m pip install -e .
file-toolkit --version
```

### Usage
```bash
# Inventory
file-toolkit scan ./data
file-toolkit scan ./data --extension pdf --min-size 1000000 --json
file-toolkit scan ./data --flat

# Hash one file
file-toolkit hash ./archive.zip
file-toolkit hash ./archive.zip --algorithm sha512

# Find exact duplicate contents (never deletes)
file-toolkit duplicates ./photos
file-toolkit duplicates ./photos --json

# Preview, then explicitly apply a rename plan
file-toolkit rename ./incoming --prefix scan- --width 4
file-toolkit rename ./incoming --prefix scan- --width 4 --apply
```
Module execution also works: `python -m file_processing_toolkit ...`.

### Python API
```python
from file_processing_toolkit import scan, find_duplicates, plan_rename

files = scan("./data", extension=".pdf")
duplicates = find_duplicates("./data")
plan = plan_rename("./incoming", prefix="document-")  # no changes yet
```
`apply_rename(plan)` performs a planned rename. It uses temporary names to handle swaps safely and attempts rollback when staging fails.

### Configuration
There is no configuration file, account, environment variable, API key, network service, or telemetry. Options are explicit CLI flags or Python arguments.

### Project structure
```text
src/file_processing_toolkit/  package, core operations, CLI
tests/                        unit and CLI tests
.github/workflows/ci.yml      cross-platform CI
bash/                         legacy standalone rename-preview helper
csharp/                       legacy standalone hashing example
python/                       legacy standalone report example
```
The legacy examples are retained for reference; the supported product is the packaged Python implementation under `src/`.

### Testing
```bash
python -m pip install -e .
python -m compileall -q src tests
python -m unittest discover -s tests -v
```
CI runs these checks on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

### Security & privacy
All processing is local. Scanning skips symbolic links. Hashing streams files rather than loading them entirely into memory. Duplicate detection is read-only. Rename requires explicit `--apply`; review the preview and keep backups for important files. See [SECURITY.md](SECURITY.md).

### Limitations
- Duplicate detection finds byte-identical files, not visually or semantically similar content.
- Large duplicate sets require reading candidate files to hash them and can be I/O intensive.
- Rename operates on files directly inside one directory, not recursively.
- Concurrent external changes during a rename can still cause filesystem errors; this is not a transactional filesystem.
- Permissions and locked files are governed by the host OS.

### Optional roadmap
Optional future work may include checksum manifests, copy/move planning, and richer machine-readable reports. These are not current features.

### Contributing & license
See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the [MIT License](LICENSE).

### Author
**Radwan Abdulhadi Ahmed** · **رضوان عبدالهادي أحمد** · GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**File Processing Toolkit** حزمة Python محلية وآمنة لجرد الملفات، وحساب البصمات، واكتشاف النسخ المتطابقة، والتخطيط لإعادة تسمية الملفات بصورة جماعية ومنظمة. توفر واجهة أوامر وواجهة Python واحدة بدل الاعتماد على سكربتات متفرقة.

### لماذا أُنشئ المشروع؟
مهام الملفات الصغيرة تتحول بسهولة إلى سكربتات منفصلة يصعب اختبارها وإعادة استخدامها. يجمع هذا المشروع العمليات الأساسية في أدوات واضحة ومختبرة، من دون رفع أسماء الملفات أو محتوياتها إلى أي خدمة خارجية.

### الميزات
- جرد تكراري أو لمجلد واحد مع التصفية حسب الامتداد والحد الأدنى للحجم.
- SHA-256 افتراضيًا مع دعم خوارزميات `hashlib` الأخرى.
- كشف الملفات المتطابقة فعليًا عبر تجميع الحجم ثم التحقق بالبصمة.
- خطة إعادة تسمية حتمية تحفظ الامتداد وتتحقق من تعارض الأسماء.
- إعادة التسمية **معاينة فقط افتراضيًا** ولا تُنفذ إلا بإضافة `--apply`.
- مخرجات JSON للجرد والمكررات.
- دعم أسماء الملفات العربية وUTF-8 والعمل على Windows وmacOS وLinux.
- لا توجد تبعيات تشغيل خارجية.

### المعاينة
```text
file-toolkit rename ./incoming --prefix photo-
IMG_0042.jpg -> photo-001.jpg
IMG_0088.jpg -> photo-002.jpg
Preview only. Add --apply to perform these renames.
```
يمكن أخذ لقطة شاشة لهذا الأمر باستخدام ملفات تجريبية غير حساسة عند الحاجة إلى صورة للمستودع.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث:
```bash
git clone https://github.com/rad03i2/file-processing-toolkit.git
cd file-processing-toolkit
python -m pip install -e .
file-toolkit --version
```

### الاستخدام
```bash
file-toolkit scan ./data --extension pdf --json
file-toolkit hash ./archive.zip
file-toolkit duplicates ./photos
file-toolkit rename ./incoming --prefix scan- --width 4
file-toolkit rename ./incoming --prefix scan- --width 4 --apply
```
ويمكن التشغيل أيضًا عبر `python -m file_processing_toolkit`.

### واجهة Python
```python
from file_processing_toolkit import scan, find_duplicates, plan_rename
files = scan("./data", extension="pdf")
duplicates = find_duplicates("./data")
plan = plan_rename("./incoming", prefix="document-")
```
لا تغير `plan_rename` أي ملف؛ التنفيذ الفعلي يتم فقط باستدعاء `apply_rename(plan)`.

### الإعداد
لا يحتاج المشروع ملف إعداد أو حسابًا أو متغيرات بيئة أو مفاتيح API، ولا يتصل بخدمة شبكة ولا يرسل telemetry. جميع الخيارات تمرر صراحة عبر CLI أو Python API.

### بنية المشروع
```text
src/file_processing_toolkit/  الحزمة والعمليات وواجهة الأوامر
tests/                        الاختبارات
.github/workflows/ci.yml      التكامل المستمر متعدد الأنظمة
bash/ csharp/ python/         أمثلة قديمة مستقلة محفوظة للمرجعية
```

### الاختبارات
```bash
python -m pip install -e .
python -m compileall -q src tests
python -m unittest discover -s tests -v
```
ويشغّل CI الفحوص على Ubuntu وWindows وmacOS مع عدة إصدارات من Python.

### الأمان والخصوصية
المعالجة محلية بالكامل، ويتم تجاهل الروابط الرمزية أثناء المسح. قراءة الملفات للبصمة تتم على أجزاء، وكشف المكررات لا يحذف أي شيء. إعادة التسمية تتطلب `--apply` صراحة. راجع [SECURITY.md](SECURITY.md) واحتفظ بنسخة احتياطية للبيانات المهمة.

### القيود
- الكشف يحدد الملفات المتطابقة بايتًا ببايت وليس الصور أو المستندات المتشابهة معنويًا.
- فحص مجموعات كبيرة قد يستهلك عمليات إدخال/إخراج كثيرة.
- إعادة التسمية تخص الملفات الموجودة مباشرة داخل مجلد واحد وليست تكرارية.
- تغيّر الملفات بالتزامن مع التنفيذ أو الملفات المقفلة قد يؤدي إلى أخطاء نظام الملفات.

### تطوير اختياري مستقبلًا
قد تضاف لاحقًا manifests للبصمات وخطط النسخ/النقل وتقارير آلية أغنى؛ وهي ليست ميزات حالية.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md). المشروع مرخص وفق [MIT](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed** · **رضوان عبدالهادي أحمد** · GitHub: **@rad03i2**
