# IA-BigData: rules for Claude sessions

Repo of the Linkia FP specialization in AI and Big Data. It is PUBLIC on GitHub (`EzequielGaribotto/IA-BigData`). The user keeps everything here to study, but only his own work may be published.

## CORE RULE: educational support vs own content (never mix, never publish the first)

**Educational support** = anything the course provides or anything derived from it:
- Official documents: `IABD_*.pdf/.docx/.md` (unit documents, activity statements, capstone statements), `Clase N.pdf` (slides), `Programación de Inteligencia Artificial.pdf`, practice guides and activity sheets (for example `Actividades_RA1.pdf`, `Hadoop_Docker_Pràctica.pdf`, `Monitorización_Hadoop.pdf`).
- Course-provided code and config: class notebooks, teacher infra files (Hadoop `docker-compose.yml`, `Prometheus Docker/`), volunteer practice sheets, and notebooks handed out as templates (the agent notebooks `Agente1`/`Agent2` and their `.py`, `Distilbert`, `PyTorch`, the `RA1/T2/ipynbs` set, `Pandas_+_RedesCNN`). A file that arrives with someone else's API key inside is course-provided.
- Anything generated FROM those: `T0x_EXAMEN.md`, `T0x_DIFERENCIAS_PDF_ACTIVIDADES.md`, `T0x_TEMARIO_ACTIVIDADES_NUEVO.md`, any `.md`/`.pdf` converted from an academic PDF.

**Own content** = what the user wrote or produced: his notebooks and scripts, reports and PDFs exported from his notebooks with nbconvert, his notes, his configs, his summaries, his solved exercises and the visualizations he generates (`visual/` notebooks and images), all of which are published. Own PDFs and `.md` files ARE published: never add blanket `*.pdf` / `*.md` / `*.docx` ignores.

**Where educational material lives**: in a folder named `_educational/` in the SAME directory where the file would be. A directory that is entirely educational goes inside the `_educational/` folder of its parent. Examples:
- `M05_BigDataAplicado/RA1/IABD_M05_T01.pdf` -> `M05_BigDataAplicado/RA1/_educational/IABD_M05_T01.pdf`
- `M_ProyectoIABD/T1/` (all educational) -> `M_ProyectoIABD/_educational/T1/`

**`**/_educational/` is gitignored.** Never un-ignore it, never `git add -f` anything inside it, never copy its contents elsewhere in the tree.

**Never move a file into or out of `_educational/` unless the user asks.** If a file looks misplaced, say so and leave it where it is.

**New or unclassified file**: classify by evidence (official course names, text addressed to the student such as "trabajarás...", slides/Word/PowerPoint origin, notes derived from a course PDF). Do not guess silently when unsure: ask the user in batches (file name + one-line description), and until he answers do NOT stage or commit it. Default is not publishing. Remember: a PDF made with LaTeX is not proof that it is the user's (teachers use LaTeX too).

## Other rules
- Never commit secrets. Scan before any commit or push (`sk-`, `sk-or-`, `gsk_`, `AIza`, `hf_`, `ghp_`, `Bearer`, `api_key = "..."`). Read keys with `getpass` or environment variables; never paste a key into a cell. A key already pushed is leaked even if deleted later.
- Do not commit datasets, model weights, environments, logs or third-party binaries (the `.gitignore` covers them). `git status` before committing; ask before pushing.
- Before any commit, run `git status` and check that nothing under `_educational/` and nothing the user has not classified is staged.

## Notebooks
Every notebook that is delivered or exported to PDF follows `notebook_pdf/GUIDELINES.md` from its first cell. Read it before creating or editing one. Before calling a notebook done, restart and run it, then export it with `notebook_pdf/export.sh <notebook>`, fix every error and read the resulting PDF.

## Ideas queue (own work, no deadline, no priority until the user says so)
Capstone deliveries come first (2026-11-03 regression, 2026-12-01 clustering, 2027-01-08 final report). Offer an idea only when there is room; never start one unprompted.
- **MLflow + model card for the Ames house-price model** (`M03_ProgramacionDeIA/RA2/T4/ACT_OBL_04`, Random Forest/XGBoost with grid search, served by `ames_housing_flask_app.py`): log runs, parameters and metrics with MLflow, version the model, write a short model card (data, metrics, limits). Why: experiment tracking and reproducibility show up in junior AI/ML stacks. Effort: small. Own work, so it is published; it is not a CV line unless the user decides it is.
