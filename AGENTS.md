# Agent Instructions

These instructions apply to the entire repository.

## Project Context

This repository is the static website for Platform Prepared. It is currently a single-page, Firebase-hosted marketing site for the Electrical Revenue Recovery System.

Read these files before making substantial changes:

- `README.md` for current project structure, local hosting, and validation commands.
- `PLANS.md` for offer positioning, target customer, pricing, integrations, and copy source of truth.
- `CONTRIBUTING.md` for static-site conventions, visual system, and widget guidance.
- `firebase.json` before changing routes, hosting behavior, cache headers, or public files.

If `CONTRIBUTING.md` and `README.md` appear to conflict, prefer `README.md` for the current repository shape. Use `CONTRIBUTING.md` for the design system and static-file conventions unless the task is explicitly about adding a standalone widget.

## Repository Shape

- `index.html` is the public homepage and contains the site HTML, CSS, and JavaScript.
- `firebase.json` configures Firebase Hosting with the repo root as the public directory and rewrites all routes to `index.html`.
- `PLANS.md` is the source of truth for product/service claims and offer copy.
- `CONTRIBUTING.md` documents visual conventions and widget requirements.
- There is no package manager, framework, build step, or compiled asset pipeline.

## Development Rules

- Preserve the no-build static-site model unless the user explicitly asks for a framework or build pipeline.
- Keep assets and behavior self-contained where practical.
- Do not add npm, pnpm, yarn, bundlers, generated lockfiles, or framework scaffolding without explicit approval.
- Match the existing visual language: navy `#0D1B2A`, forest `#1A5C3A`, mint `#6DC99A`, white cards, Inter body text, and Instrument Serif headings.
- Keep copy aligned with `PLANS.md`. Do not invent pricing, guarantees, integrations, or capabilities beyond that file unless instructed.
- Preserve existing CTA intent: Calendly booking, phone contact, and `nate@gardpartners.com`.
- Treat Firebase Hosting config carefully. Markdown files are ignored by deployment via `firebase.json`.

## Local Validation

Use the lightweight checks from `README.md`:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://127.0.0.1:8000/
```

Validate Firebase config:

```bash
python3 -m json.tool firebase.json
```

Confirm key current-offer copy is still present:

```bash
rg "Electrical Revenue Recovery|missed-call|review automation" index.html
```

Also manually check desktop and mobile widths, especially the hero, pillar cards, pricing section, and mobile menu.

## Standalone Widgets

Only use the widget workflow in `CONTRIBUTING.md` when the task is specifically to create or edit a standalone tool/widget. In that case:

- Add each widget as a self-contained root-level `.html` file.
- Use the required CDN scripts and no module imports.
- Include the required email gate and update its `source` field.
- Follow the checklist in `CONTRIBUTING.md` before submission.

## Change Hygiene

- Keep changes focused on the user request.
- Do not rewrite unrelated sections of `index.html`.
- Do not push directly to `main`.
- Do not commit unless the user asks.
- Avoid secrets, API keys, or credentials in any file.
