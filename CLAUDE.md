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

Deployment is handled automatically via AWS Amplify (`amplify.yaml`) on push to the main branch.

## Architecture

This is a **Docusaurus 3.x** site (TypeScript) configured in **blog-only mode**. The blog is served at `/` (root).

- **`/blog/`** — All blog posts (MDX/MD). This is the only content section.
- **`/src/css/custom.css`** — Global CSS overrides
- **`/static/`** — Static assets served at root

Docs and the courses plugin are disabled. Color mode switching is disabled (light mode only).

`tsconfig.json` uses inline compiler options instead of `extends: "@docusaurus/tsconfig"` — the package had a version mismatch with the installed Docusaurus (3.10.0 vs 3.9.2 in devDependencies).
