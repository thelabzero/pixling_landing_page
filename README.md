# Pixling · Dino landing page

Static site, deployed on Vercel straight from `public/`. No framework, no build step on Vercel.

## Layout
- `public/` – **everything that gets deployed** (`index.html`, `assets/*.webp`, `boot_film_wedge_life.mp4`)
- `src/page/` – landing page source. Edit `src.html`, then `python3 src/build.py` writes `public/index.html`
- `src/site/` – subpages (`about`, `faq`, `privacy`, `404`): `pages/*.html` content, `layout.html`, `site.css`, `site.js`, `faq.json`, `site.json`. Same build command also writes `robots.txt` and `sitemap.xml`
  - `fonts.css` (IBM Plex, inlined), `wedge.js` (Dino 128×64 face engine from the Wedge Sheet)
- `assets/renders/` – Blender output PNGs (source for the web images)
- `cad/` – STLs, Blender render pipeline, `requirements.txt` (only for rendering)
- `tools/` – `assembly_tool.html` (3D assembly viewer, not deployed)
- `references/` – brand language, wedge sheet, banner, reference layout, prototype photo
- `archive/` – old v2 page, kept for reference
- `vercel.json` – output directory `public`, no build/install, cache + security headers

## Everyday workflow
1. Edit `src/page/src.html`
2. `python3 src/build.py` (builds the landing page and all subpages)
3. Preview: `python3 -m http.server -d public 8000`
4. Commit `public/` together with the source and push; Vercel redeploys on push to `main`

## Adding a page
1. Create `src/site/pages/<slug>.html`. First line is a metadata comment (`slug`, `title`, `description`, `eyebrow`, `h1`, `lead`, optional `nav`, `art`, `schema`, `cta`); the rest is the body. Reuse classes from `site.css` (`blk`, `prose`, `cards`, `specs`, `step`).
2. Add the slug to `NAV`/`FOOT` and to the sitemap list in `src/site/build.py`.
3. `python3 src/build.py`. Links between pages are relative (`faq`, not `/faq`) so GitHub Pages and Vercel both work.
Brand: stepped corners (never rounded), night/cream/teal, IBM Plex, mono eyebrows. Only state facts we have confirmed; write "coming soon" for price, shipping and battery life until they are real.
`src/site/site.json` holds the base URL and `contact_email` (shown on the privacy page; fill it in).

## GitHub Pages
`.github/workflows/pages.yml` publishes `public/` on every push to `main` (repo Settings > Pages > Source = GitHub Actions).
Live at https://thelabzero.github.io/pixling_landing_page/

## Vercel
Import the repo; leave Framework Preset as "Other". `vercel.json` sets everything.
Do not put `requirements.txt`, `pyproject.toml` or `app.py`/`main.py` in the repo root: Vercel will treat the project as Python and fail with `PYTHON_ENTRYPOINT_NOT_FOUND`.

## Rendering on the Mac
1. Install Blender (free): `brew install --cask blender` or blender.org
2. From the project folder: `bash cad/render/render_all.sh` (or `bash cad/render/render_all.sh hero` for one shot)
GPU (Metal) is used automatically on Apple Silicon.
3. `python3 src/page/make_web_images.py` – web-sized WebP copies in `public/assets/` (needs Pillow)
4. `python3 src/page/build.py` – rebuild `public/index.html`

The page overlays the live screen on `dino_front_blank` at a fixed rectangle (`.prod .scr` in src.html).
If you change that job's camera, re-measure the rectangle (render.py prints SCREENRECT).

## Notes
- Back-plate rotation (`back_rot`) is a best guess from the outline; flip to 90 if the USB slot belongs at the top.
- Colours are matte PLA approximations; black is the current production colour.
