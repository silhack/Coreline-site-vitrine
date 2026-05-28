# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev       # Start dev server at http://localhost:5173
npm run build     # Production build to dist/
npm run preview   # Preview production build locally
npm run lint      # Run ESLint
```

## Architecture

**React 19 SPA** built with Vite, using React Router v7 for routing. No global state management — local `useState` only.

### Key Structure

- `src/main.jsx` — Entry point, sets up `HelmetProvider` and `BrowserRouter`
- `src/App.jsx` — Route definitions and layout wrapper (Navbar → Routes → Footer)
- `src/coreline.css` — **Single monolithic CSS file** (all styles here, no component-scoped CSS)
- `src/components/layout/` — `Navbar.jsx`, `Footer.jsx`
- `src/components/home/` — Section components composed in `src/pages/Home.jsx`
- `src/components/common/SEO.jsx` — Reusable Helmet wrapper for meta tags
- `src/pages/` — Full page components, each declares its own SEO meta tags

### CSS Conventions

All styles live in `coreline.css`. Uses CSS custom properties for theming:
- Primary: `#1b5798` (True Blue)
- Accent: `#cda141` (True Gold)
- Dark: `#061e63` (True Dark Blue)
- Font: Montserrat (Google Fonts)

Utility classes: `.container`, `.badge`, `.btn-primary`, `.btn-secondary`. Responsive via media queries.

### Animation Pattern

- **Framer Motion** for entrance animations (`initial`/`animate`/`transition` props)
- **React Intersection Observer** to trigger animations on scroll
- **React CountUp** for animated metrics in `ImpactMetrics.jsx`

### SEO Pattern

Every page uses the `SEO` component (`src/components/common/SEO.jsx`) to set page title, description, and Open Graph/Twitter Card meta tags.

### Backend Integration

Contact form (`src/pages/ContactPage.jsx`) POSTs to `{VITE_API_URL}/api/contact` (FastAPI backend). Uses native `fetch`, no HTTP client library. Includes honeypot field for spam detection.

Environment variable:
```
VITE_API_URL=http://localhost:8000
```
All env vars must be prefixed with `VITE_` to be accessible via `import.meta.env.VITE_*`.

### Security

`index.html` sets CSP, referrer policy, and permissions policy headers directly in `<meta>` tags. Do not loosen these without explicit intent.
