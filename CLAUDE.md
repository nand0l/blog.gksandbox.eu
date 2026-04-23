# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```powershell
npm start          # Start dev server on port 4505
npm run build      # Build static output to /build
npm run serve      # Serve the built output locally
npm run typecheck  # TypeScript type checking (tsc)
npm run clear      # Clear Docusaurus cache
```

```powershell
# Blog post builder (Streamlit UI)
streamlit run .python/blog_post_builder.py
```

Deployment is handled automatically via AWS Amplify (`amplify.yaml`) on push to the `main` branch.

## Architecture

This is a **Docusaurus 3.x** site (TypeScript) configured in **blog-only mode**. The blog is served at `/` (root). Docs are disabled (`docs: false`). Color mode switching is disabled (light mode only).

- **`/blog/`** — All blog posts (`.md` or `.mdx`). Filename format: `YYYY-MM-DD-slug.md`
- **`/blog/authors.yml`** — Author profiles. Currently only `nlu` (Nando Lutgerink).
- **`/blog/tags.yml`** — Canonical tag definitions (label, permalink, description). Tags used in posts must be registered here, or the build will warn.
- **`/src/css/custom.css`** — Global CSS overrides
- **`/static/`** — Static assets served at root
- **`/.python/blog_post_builder.py`** — Streamlit app that generates blog post files and auto-updates `tags.yml` for new tags

`tsconfig.json` uses inline compiler options instead of `extends: "@docusaurus/tsconfig"` — the package had a version mismatch with the installed Docusaurus (3.10.0 vs 3.9.2 in devDependencies).

## Blog post front matter

```md
---
slug: my-post           # optional — defaults to filename slug
title: My Post Title
authors: [nlu]          # must match a key in blog/authors.yml
tags: [aws, howto]      # must match keys in blog/tags.yml
---
```

Use `<!-- truncate -->` in `.md` files and `{/* truncate */}` in `.mdx` files to split the listing preview from the full post body.

Use `.mdx` instead of `.md` only when you need React components (e.g. `<Tabs>`).

## Linting

`.markdownlint.yaml` disables heading-increment (MD001), enforces a 1200-char line limit (MD013), and allows duplicate headings (MD024), unordered list numbering (MD029), inline HTML (MD033), and emphasis used as heading (MD036).
