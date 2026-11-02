# Family Tree Research

[English below](#english)

## Русский

**Навык для ИИ-агента, который помогает исследовать историю семьи и разобраться в родственных связях.** Он рассчитан прежде всего на поиск по бывшему СССР и Российской империи и работает с Claude Code, Codex и другими агентами, умеющими читать файлы и выполнять инструкции.

Это не отдельная программа для рисования дерева. Вы рассказываете агенту, что уже известно, даёте доступные материалы и задаёте вопрос. Навык помогает организовать поиск, проверить найденные сведения и сохранить понятное объяснение: что известно из документов, что сообщила семья и что пока остаётся предположением.

### Что он умеет

- Разбирать существующее древо, семейные рассказы, документы и GEDCOM-файлы; находить пробелы, противоречия и связи без источников.
- Подбирать архивы и другие источники по месту, времени и виду записи, учитывая старые названия, границы, приходы и варианты написания имён.
- Искать сведения в доступных метрических, военных, миграционных и репрессивных материалах, книгах, газетах и местных исторических ресурсах.
- Читать доступные документы и сканы, если агент поддерживает их просмотр, отмечать неясные места и отделять однофамильцев друг от друга.
- Вести учёт людей, источников и родственных связей, сохранять гипотезы и журнал поисков; готовить интерактивное дерево с отчётом в HTML и экспорт GEDCOM.

В комплекте — [региональный каталог](regional-archives/README.md) с 661 записью об учреждениях, отделениях и службах и [64 других источника](resources/README.md). Есть маршруты для всех 15 бывших союзных республик, Польши и Финляндии. **Покрытие частичное:** наличие ссылки не означает, что нужные записи сохранились или доступны онлайн. [Состояние каталога и пробелы](regional-archives/COVERAGE.md) указаны отдельно.

### Как начать

1. Скачайте и распакуйте репозиторий или склонируйте его. Сохраняйте всю папку: одного `SKILL.md` недостаточно.
2. Откройте папку в своём агенте и попросите его прочитать `SKILL.md`. Для установки в качестве постоянного навыка есть [короткая инструкция для разных агентов](guides/compatibility.md).
3. Расскажите, что знаете о семье и какие документы, фотографии или прежние исследования уже есть. Необязательно сразу заполнять всё дерево — начните с одного вопроса.

Например:

> Прочитай SKILL.md. Хочу выяснить, кем были родители моего прадеда. Помоги разобраться в имеющихся материалах, создай частное дело вне этой папки и выбери следующий полезный поиск. Отдельно показывай сведения из источников, семейные рассказы и гипотезы.

Агент заведёт отдельную папку исследования, сохранит источники и ход работы. В следующем сеансе попросите его продолжить это дело: журнал и список задач помогут не начинать заново.

Для новых онлайн-поисков агенту нужен доступ к веб-инструментам. Для работы со сканами — просмотр изображений или документов. Основные скрипты требуют Python 3.9+; без него агент может вести материалы вручную, но не должен утверждать, что выполнил автоматические проверки или экспорт. Все основные инструкции и шаблоны уже включены; отдельно устанавливать исходный навык не требуется.

### Что вы получите

Частное дело с источниками, журналом поисков, открытыми вопросами и следующими шагами. По запросу — **дерево и отчёт в одном файле `output/report.html`**, который открывается без интернета, и файл GEDCOM для переноса в генеалогическую программу. Ограничения экспорта описаны в [инструкции по результатам](guides/results.md).

Навык не гарантирует нахождение предка и не превращает совпадение имени в установленное родство. Если сведения расходятся или источник недоступен, это остаётся видимым в исследовании.

### Семейные данные и доступ

Храните настоящее дело **вне публичного репозитория**. По умолчанию готовые результаты исключают живых людей и людей с неизвестным жизненным статусом; для частного результата с ними нужно отдельное указание. Перед передачей файлов другим людям проверьте их содержание.

Агент работает с бесплатными публичными источниками и предоставленными материалами. Вход в аккаунты, CAPTCHA, оплату и отправку запросов учреждениям выполняет пользователь. Скрипты не публикуют результаты и не отправляют семейные файлы. Подробнее — в [правилах работы](guides/policy.md).

Навык построен на [ex-ussr-kinship-research](vendor/ex-ussr-kinship-research/SKILL.md) Дениса Ширяева и участников проекта. Используемая версия включена в репозиторий; лицензии — MIT.

---

<a id="english"></a>

## English

**An AI-agent skill for researching family history and understanding kinship.** It focuses on the former USSR and Russian Empire and works with Claude Code, Codex, and other agents that can read files and follow instructions.

This is not a separate tree-drawing application. You tell your agent what you know, provide available material, and ask a question. The skill helps organize the search, assess findings, and explain which details come from documents, which come from family accounts, and which remain uncertain.

### What it can do

- Examine existing trees, family accounts, documents, and GEDCOM files to identify gaps, contradictions, and unsupported relationships.
- Find promising archives and sources by place, period, and record type, accounting for historical names, boundaries, parishes, and name variants.
- Research accessible church, military, migration, and repression records, books, newspapers, and local-history resources.
- Read available documents and scans when the agent supports them, mark uncertain readings, and keep namesakes separate.
- Keep records of people, sources, claims, relationships, and searches; produce an interactive HTML tree/report and a GEDCOM export.

The package includes a [regional directory](regional-archives/README.md) with 661 institution, branch, and service entries, plus [64 other resources](resources/README.md). It provides research routes across all 15 former Soviet republics, Poland, and Finland. **Coverage is partial:** a link does not establish that particular records survive or are available online. See the [coverage notes and gaps](regional-archives/COVERAGE.md).

### Getting started

1. Download and extract the repository, or clone it. Keep the entire folder: `SKILL.md` alone is not enough.
2. Open the folder with your agent and ask it to read `SKILL.md`. For ongoing installation as a skill, follow the [host-specific instructions](guides/compatibility.md).
3. Describe what you know and which documents, photographs, or earlier research you have. Start with one useful question; you do not need a complete tree.

For example:

> Read SKILL.md. I want to find out who my great-grandfather's parents were. Help me examine the material I have, create a private case outside this folder, and choose the next useful search. Distinguish source statements, family accounts, and hypotheses.

The agent creates a separate case folder and records evidence and progress. In a later session, ask it to continue that case; the search log and task list help it pick up where you left off.

New online searches require the agent's web tools. Scans require image or document-reading capabilities. Core scripts need Python 3.9+; without it, the agent can maintain records manually but must not claim automated checks or exports ran. The main instructions and templates are bundled, so no separate installation of the upstream skill is needed.

### What you get

A private case with sources, search history, unanswered questions, and next steps. On request, you also get **the tree and report in one offline file, `output/report.html`**, and a GEDCOM file for transfer to genealogy software. See the [output guide](guides/results.md) for export limitations.

The skill cannot guarantee a discovery or establish kinship from a matching name. Conflicting details and inaccessible sources remain visible in the research.

### Family data and access

Keep real cases **outside the public repository**. Generated outputs exclude living people and people of unknown living status by default; including them in a private output requires an explicit request. Review files before sharing them.

The agent uses free public sources and supplied material. You handle sign-ins, CAPTCHAs, payments, and submitting institutional requests. The scripts do not publish results or send family files. See the [research policy](guides/policy.md).

Built on [ex-ussr-kinship-research](vendor/ex-ussr-kinship-research/SKILL.md) by Denis Shiryaev and contributors. The selected version is bundled; both projects use the MIT licence.
