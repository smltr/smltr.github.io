# My personal site

An Astro-powered portfolio and writing site, deployed to GitHub Pages.

## Work locally

```sh
npm install
npm run dev
```

Open the local URL printed in the terminal. Astro updates the page as files change.

The main editing surface is intentionally small:

- `src/pages/index.astro` — homepage words and links
- `src/styles/global.css` — type, color, spacing, and layout
- `src/content/blog/` — Markdown posts
- `src/layouts/BaseLayout.astro` — shared header, footer, and metadata

## Production build

```sh
npm run build
```

Pushing `main` deploys the generated site through GitHub Actions.
