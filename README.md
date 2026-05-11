# Platform Prepared

Static marketing site for Platform Prepared's electrical revenue recovery offer. The site is a single self-contained HTML page hosted from the repo root with Firebase Hosting.

## What This Site Covers

The homepage presents Platform Prepared's Electrical Revenue Recovery System for electrical contractors:

- Missed call text-back and follow-up.
- Review automation.
- Estimate follow-up and lead reactivation.
- CRM pipeline setup and monthly reporting.

The content source of truth is `PLANS.md`. Styling follows the navy, forest, mint, and white visual system described in `CONTRIBUTING.md`.

## Repo Structure

```text
index.html       Public static homepage
firebase.json    Firebase Hosting config and fallback route
PLANS.md         Offer positioning and content source of truth
CONTRIBUTING.md  Static-site conventions and design guidance
```

There is no package manager, framework, build step, or compiled asset pipeline.

## Local Hosting

Open the site directly in a browser:

```text
File -> Open File -> index.html
```

Or run a local static server from the repo root:

```bash
python3 -m http.server 8000
```

Then visit:

```text
http://127.0.0.1:8000/
```

To test Firebase Hosting rewrites locally, use the Firebase CLI if it is installed:

```bash
firebase emulators:start --only hosting
```

## Testing Checklist

- Confirm `index.html` opens without console errors.
- Check desktop and mobile widths, especially the hero, pillar cards, pricing section, and mobile menu.
- Confirm CTA links point to Calendly, phone, and `nate@gardpartners.com`.
- Validate Firebase config with:

```bash
python3 -m json.tool firebase.json
```

- Confirm the current offer copy is present with:

```bash
rg "Electrical Revenue Recovery|missed-call|review automation" index.html
```
