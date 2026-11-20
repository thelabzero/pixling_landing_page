"""Build the Pixling subpages (dino, about, faq, privacy, 404), shared CSS/JS, fonts, robots and sitemap into public/.
Run: python3 src/site/build.py   (or python3 src/build.py to build the landing page too)"""
import os, re, json, html, datetime
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(H, '..', '..')); PUB = os.path.join(ROOT, 'public')
rd = lambda *p: open(os.path.join(*p), encoding='utf-8').read()
def wr(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True); open(path, 'w', encoding='utf-8').write(s)
cfg = json.loads(rd(H, 'site.json')); BASE = cfg['base_url'].rstrip('/')
TODAY = datetime.date.today().isoformat()
esc = lambda s: html.escape(s, quote=True)
strip = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()

# ---- shared assets ----
steps = 12; pts = ['0 100%', '0 0']
for i in range(1, steps + 1):
    x = f'{i/steps*100:.2f}%'; pts += [f'{x} {(i-1)/steps*70:.2f}%', f'{x} {i/steps*70:.2f}%']
pts.append('100% 100%')
wr(os.path.join(PUB, 'assets', 'site.css'), rd(H, 'site.css').replace('/*STAIRS*/', 'polygon(' + ','.join(pts) + ')'))
src = rd(ROOT, 'src', 'page', 'src.html').splitlines()
want = ('const WORD=', 'const DOT=', 'const SEQ=', 'const ARROW=', 'const HEART=', 'function wordBits', 'function drawRows', 'function wordmark')
brand = [l for l in src if l.startswith(want)]
# wordmark() spans 3 lines in the source
i = next(k for k, l in enumerate(src) if l.startswith('function wordmark')); brand = [l for l in brand if not l.startswith('function wordmark')]
brand += src[i:i + 3]
assert len(brand) == 10, len(brand)
wr(os.path.join(PUB, 'assets', 'site.js'), rd(H, 'site.js').replace('/*BRAND*/', '\n'.join(brand)))
wr(os.path.join(PUB, 'assets', 'fonts.css'), rd(ROOT, 'src', 'page', 'fonts.css'))

# ---- pages ----
NAV = [('about', 'about')]
def navleft(cur, root): return ''.join(f'<a class="lnk{" on" if s == cur else ""}" href="{root}{s}">{t}</a>' for s, t in NAV)
FOOT = [('about', 'about'), ('faq', 'faq'), ('privacy', 'privacy')]
def footnav(root): return f'<a href="{root}">home</a>' + ''.join(f'<a href="{root}{s}">{t}</a>' for s, t in FOOT)
ARROW = '<span class="arr step sm"><canvas class="px-arrow" width="7" height="7" style="width:14px;height:14px"></canvas></span>'
def cta(root): return (f'<div class="cta2 step lg"><div><div class="eyebrow">pre-order · dino by pixling</div><h2>Bring Dino home<span class="sp">.</span></h2>'
    f'<p>Reserve yours and we will write the moment pre-orders open, with the price and shipping date. Nothing to pay today.</p></div>'
    f'<a class="btn step sm" href="{root or "./"}#preorder">reserve mine {ARROW}</a></div>')
contact = (f'To ask us anything about your data, write to <a href="mailto:{esc(cfg["contact_email"])}">{esc(cfg["contact_email"])}</a>.' if cfg.get('contact_email')
           else 'Our contact address for data requests will be published here before pre-orders open.')

faq = json.load(open(os.path.join(H, 'faq.json'), encoding='utf-8'))
def crumbs(slug, name):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Pixling", "item": BASE + '/'},
        {"@type": "ListItem", "position": 2, "name": name, "item": f'{BASE}/{slug}'}]}

pages = []
for fn in sorted(os.listdir(os.path.join(H, 'pages'))):
    raw = rd(H, 'pages', fn); m = re.match(r'<!--meta (.*?) -->\n', raw, re.S); meta = json.loads(m.group(1)); body = raw[m.end():]
    slug = meta['slug']
    body = body.replace('{{updated}}', meta.get('updated', '')).replace('{{contact}}', contact).replace('{{email}}', esc(cfg.get('contact_email', '')))
    graph = [crumbs(slug, meta['h1'])]
    if meta.get('schema') == 'faq':
        body = body.replace('<!--FAQ-->', '\n'.join(f'      <details class="step sm"><summary>{esc(q)}</summary><div class="a">{a}</div></details>' for q, a in faq))
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in faq]})
    if meta.get('schema') == 'product':
        graph.append({"@type": "Product", "name": "Dino", "brand": {"@type": "Organization", "name": "Pixling", "url": BASE + '/'},
                      "description": meta['description'], "image": BASE + '/assets/og-image.png', "url": f'{BASE}/{slug}'})
    art = f'<div class="art"><img src="{meta["art"]}" alt="Dino, the first Pixling" width="1100" height="1100" loading="eager"></div>' if meta.get('art') else ''
    out = rd(H, 'layout.html')
    for k, v in {'title': esc(meta['title']), 'description': esc(meta['description']), 'robots': 'index,follow,max-image-preview:large', 'root': '', 'home': './',
                 'canonical': f'<link rel="canonical" href="{BASE}/{slug}">', 'ogurl': f'<meta property="og:url" content="{BASE}/{slug}">', 'base': BASE,
                 'jsonld': '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + '</script>',
                 'navleft': navleft(meta.get('nav'), ''), 'eyebrow': esc(meta['eyebrow']), 'h1': esc(meta['h1']), 'lead': esc(meta['lead']), 'art': art,
                 'body': body, 'cta': cta('') if meta.get('cta', True) else '', 'footnav': footnav('')}.items():
        out = out.replace('{{' + k + '}}', v)
    wr(os.path.join(PUB, slug + '.html'), out); pages.append(slug)

# remove stale generated pages (a deleted page must not linger in public/)
for f in os.listdir(PUB):
    if f.endswith('.html') and f not in ('index.html', '404.html') and f[:-5] not in pages:
        os.remove(os.path.join(PUB, f))

# ---- 404 (absolute asset paths: it can be served from any URL) ----
out = rd(H, 'layout.html')
for k, v in {'home': '/', 'title': 'Page not found · Pixling', 'description': 'This page wandered off.', 'robots': 'noindex', 'root': '/', 'canonical': '', 'ogurl': '', 'base': BASE, 'jsonld': '',
             'navleft': navleft(None, '/'), 'eyebrow': '404 · not found', 'h1': 'This page wandered off', 'lead': 'Dino looked everywhere. Try the home page, or ask the FAQ.', 'art': '',
             'body': f'<section class="blk"><div class="wrap"><a class="btn dark step sm" href="/">back home {ARROW}</a> <a class="link" style="margin-left:18px;font-family:var(--mono);font-size:14px" href="/faq">read the faq</a></div></section>',
             'cta': '', 'footnav': footnav('/')}.items():
    out = out.replace('{{' + k + '}}', v)
wr(os.path.join(PUB, '404.html'), out)

# ---- robots + sitemap ----
wr(os.path.join(PUB, 'robots.txt'), f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n')
urls = [BASE + '/'] + [f'{BASE}/{s}' for s in ('about', 'faq', 'privacy')]
wr(os.path.join(PUB, 'sitemap.xml'), '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
   ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n')
print('built', pages, '+ 404, site.css, site.js, fonts.css, robots, sitemap')
