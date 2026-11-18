# Pixling · Dino landing page

## Layout
- `index.html` – the built landing page (open in a browser; keep next to `boot_film_wedge_life.mp4`)
- `src/page/` – page source. Edit `src.html`, then `python3 src/page/build.py` to rebuild `index.html`
  - `fonts.css` (IBM Plex, inlined), `wedge.js` (Dino 128×64 face engine from the Wedge Sheet)
- `cad/stl/` – body, bezel, back plate (from the print files)
- `cad/render/` – Blender render pipeline
  - `render.py` – assembles the 3 parts, PLA material, lights, camera, screen face
  - `jobs/*.json` – one file per shot (colours, angle, face, resolution, samples)
  - `faces/` – screen bitmaps exported from the Wedge Sheet (`node export_faces.js`)
  - `render_all.sh` – renders every job into `assets/renders/`
- `assets/renders/` – output PNGs (transparent background)
- `references/` – brand language, wedge sheet, banner, reference layout, prototype photo

## Rendering on the Mac
1. Install Blender (free): `brew install --cask blender` or blender.org
2. From the project folder: `bash cad/render/render_all.sh` (or `bash cad/render/render_all.sh hero` for one shot)
GPU (Metal) is used automatically on Apple Silicon.
3. `python3 src/page/make_web_images.py` – web-sized WebP copies in `assets/web/` (needs Pillow)
4. `python3 src/page/build.py` – rebuild `index.html`

The page overlays the live screen on `dino_front_blank` at a fixed rectangle (`.prod .scr` in src.html).
If you change that job's camera, re-measure the rectangle (render.py prints SCREENRECT).

## Notes
- Back-plate rotation (`back_rot`) is a best guess from the outline; flip to 90 if the USB slot belongs at the top.
- Colours are matte PLA approximations; black is the current production colour.
