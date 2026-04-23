# Contributing to Platform Prepared — Widget Development Guide

Welcome. This repo powers [platformprepared.com](https://platformprepared.com) and its free tool suite. Each widget is a standalone HTML file — no build pipeline, no framework setup, no npm install. Just open a file and start building.

---

## Tech Stack

Every widget uses the same three CDN libraries. Copy this into your `<head>`:

```html
<script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script src="https://cdn.tailwindcss.com"></script>
```

All React code goes inside `<script type="text/babel">` tags. No imports, no modules — just `const { useState, useEffect } = React;` at the top and you're off.

---

## Design System

Use these colors in your Tailwind config and inline styles so everything looks native to the site:

```js
tailwind.config = {
  theme: {
    extend: {
      colors: {
        navy:   '#0D1B2A',   // primary dark background
        forest: '#1A5C3A',   // primary green (buttons, accents)
        mint:   '#6DC99A',   // light green (highlights, chips)
        gold:   '#D4AF37',   // use sparingly — confidence badges, alerts
      }
    }
  }
}
```

**Typography:** Inter (sans) + Instrument Serif for headings. Add this to `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
```

**General rules:**
- Navy (`#0D1B2A`) for dark sections and the email gate background
- Forest (`#1A5C3A`) for primary buttons and key UI elements
- Mint (`#6DC99A`) for chips, badges, and interactive highlights
- White backgrounds for cards and content areas
- `gray-50` / `gray-100` for subtle section backgrounds

---

## File Structure

Each widget is **one self-contained `.html` file** at the root of the repo:

```
hvac-fix-finder.html    ← existing example — study this first
[your-widget-name].html ← your new file
index.html              ← main site (don't touch unless discussed)
firebase.json           ← routing config (Nathan updates this)
```

**Naming convention:** `[industry]-[what-it-does].html`
Examples: `plumbing-leak-finder.html`, `electrical-load-calculator.html`, `roofing-estimate-tool.html`

---

## Email Gate (Required)

Every widget must have an email gate — this is how Platform Prepared captures leads. Copy this component exactly and drop it at the top of your app:

```jsx
function EmailGate({ onAccess }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const emailValid = v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

  const handleSubmit = async () => {
    if (!name.trim()) { setError('Please enter your first name.'); return; }
    if (!emailValid(email)) { setError('Please enter a valid email address.'); return; }
    setError('');
    setSubmitting(true);
    localStorage.setItem('hvacgate_name', name.trim());
    localStorage.setItem('hvacgate_email', email.trim());
    try {
      const formData = new FormData();
      formData.append('name', name.trim());
      formData.append('email', email.trim());
      formData.append('source', 'YOUR WIDGET NAME — platformprepared.com');
      formData.append('submitted_at', new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles' }) + ' PT');
      formData.append('_subject', 'New Lead — ' + name.trim());
      formData.append('_replyto', email.trim());
      formData.append('_captcha', 'false');
      await fetch('https://formsubmit.co/nate@gardpartners.com', {
        method: 'POST',
        body: formData
      });
    } catch (e) {
      console.warn('Lead capture failed:', e);
    }
    setSubmitting(false);
    onAccess(name.trim());
  };

  // UI — match the navy gate screen from hvac-fix-finder.html
}
```

Update the `source` field to match your widget name. The email always goes to `nate@gardpartners.com` — do not change that.

---

## Widget Structure

A widget has three sections. Keep them in this order:

### 1. Landing / Hero
- Explain what the tool does and who it's for
- Show 3–5 feature bullets
- Show 2–3 example scenarios so users know what to expect
- End with a CTA that opens the tool

### 2. The Tool Itself
- Input form (dropdowns, text, chips — whatever fits)
- A "Diagnose" or "Calculate" or "Analyze" button
- Clear loading state

### 3. Results Panel
- Lead with the most important finding
- Break into 2–4 expandable cause/recommendation cards
- Include a confidence level: **High / Medium / Low**
- Add a safety alert if anything involves risk (electrical, gas, water, etc.)
- Always include a disclaimer at the bottom
- "Check Another Issue" or "Start Over" reset button

---

## Local Testing

No server needed — just open the file in Chrome:

```
File → Open File → [your-widget].html
```

Or if you want to test the email gate submission (requires a web server), run:

```bash
npx serve .
```

Then open `http://localhost:3000/your-widget.html`

---

## Submitting Your Widget

1. **Never push directly to `main`**
2. Create a branch: `git checkout -b widget/plumbing-leak-finder`
3. Build your widget, test it locally
4. `git add your-widget.html`
5. `git commit -m "Add plumbing leak finder widget"`
6. `git push origin widget/plumbing-leak-finder`
7. Open a **Pull Request** on GitHub — describe what the tool does and who it's for
8. Nathan reviews, approves, and handles deployment to Firebase

---

## Checklist Before Submitting a PR

- [ ] File is self-contained — no external dependencies beyond the 4 CDN scripts
- [ ] Email gate is included and `source` field updated with widget name
- [ ] Colors match the design system (navy, forest, mint)
- [ ] Mobile-first — tested at 375px width (iPhone SE)
- [ ] Results panel has confidence levels on each card
- [ ] Safety alerts present if tool involves anything hazardous
- [ ] Disclaimer footer included
- [ ] "Start Over" / reset button works
- [ ] No hardcoded emails, API keys, or credentials in the file

---

## Questions

Reach out to Nathan at nate@gardpartners.com or open a GitHub Issue on this repo.
