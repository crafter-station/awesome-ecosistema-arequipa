"""Regenera README.md desde data/ecosistema_arequipa.json (miniaturas desde assets/covers/)."""
import json, pathlib, re
R = pathlib.Path(__file__).resolve().parents[1]
D = json.load(open(R / 'data/ecosistema_arequipa.json', encoding='utf-8'))
CATS = [  # (valor en data, título con emoji)
    ("universidad", "🎓 Universidades"),
    ("instituto/escuela técnica", "🛠️ Institutos y escuelas técnicas"),
    ("incubadora/aceleradora", "🚀 Incubadoras y aceleradoras"),
    ("comunidad tech", "👩‍💻 Comunidades tech"),
    ("espacio de innovación (hub/coworking/fablab)", "🏢 Espacios de innovación"),
    ("entidad pública/programa público", "🏛️ Estado y programas"),
    ("oficina universitaria de innovación/transferencia", "🔬 Oficinas de innovación universitaria"),
    ("fundación/ONG", "🤝 Fundaciones"),
    ("gremio/cámara", "🧾 Cámaras y gremios"),
    ("medio local", "📰 Medios"),
    ("fondo/inversión", "💰 Fondos e inversión"),
    ("evento recurrente", "📅 Eventos"),
    ("red", "🕸️ Redes"),
    ("startup", "🚀 Startups"),
]
EMPTY = {"fondo/inversión": "un fondo o red de inversión activa en Arequipa"}
def anchor(t):
    return '#' + re.sub(r'[^\w\- ]', '', t.lower(), flags=re.U).replace(' ', '-')  # estilo GitHub: emoji+espacio => '-'
def cell(s):
    return (s or '').replace('|', '\\|').replace('\n', ' ').strip()
def link(x):
    w = (x.get('web') or '').split(' ')[0]
    return f"[{cell(x['nombre'])}]({w})" if w.startswith('http') else f"**{cell(x['nombre'])}**"
n_cov = sum(1 for x in D if x.get('cover_path') and x.get('cover_kind', 'foto') == 'foto')
L = ['<p align="center"><img src="assets/header-arequipa-misti.jpg" alt="Volcán Misti y Catedral de Arequipa" width="100%"></p>', '',
     '<h1 align="center">Awesome Ecosistema Arequipa</h1>', '',
     '<p align="center"><a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a></p>', '',
     '> Lista curada de actores del ecosistema de innovación y tecnología de **Arequipa, Perú**: universidades, institutos, incubadoras, comunidades, espacios, Estado, gremios, medios, eventos recurrentes, redes y startups destacadas.', '',
     f'**{len(D)} actores** · **{n_cov}** con foto real · cada entrada enlaza a su **fuente pública**. Créditos de imágenes en [`assets/covers/SOURCES.md`](assets/covers/SOURCES.md).', '',
     '## Contenido', '']
for c, t in CATS:
    k = sum(1 for x in D if x['categoria'] == c)
    L.append(f"- [{t}]({anchor(t)}) ({k})")
L += ['- [Datos](#datos)', '- [Contribuir](#contribuir)', '']
for c, t in CATS:
    rows = sorted([x for x in D if x['categoria'] == c], key=lambda x: x['nombre'].lower())
    L += [f"## {t}", ""]
    if not rows:
        q = EMPTY.get(c, "un actor de esta categoría activo en Arequipa")
        L += [f"_Sin actores verificados aún. ¿Conoces {q}? Abre un issue con su fuente pública._", "", "[⬆ volver](#contenido)", ""]
        continue
    L += ["| | Actor | Descripción | Fuente |", "|:-:|---|---|:-:|"]
    for x in rows:
        thumb = f'<img src="{x["cover_path"]}" width="120" alt="">' if x.get('cover_path') else ''
        dist = f" <br><sub>📍 {cell(x['distrito'])}</sub>" if x.get('distrito') else ''
        src = f"[🔗]({x['fuente_url']})" if (x.get('fuente_url') or '').startswith('http') else ''
        L.append(f"| {thumb} | {link(x)}{dist} | {cell(x['descripcion_corta'])} | {src} |")
    L += ["", "[⬆ volver](#contenido)", ""]
L += ["## Datos", "",
      "- `data/ecosistema_arequipa.csv` / `.json`: directorio completo (`cover_path` = imagen en este repo, `cover_url` = imagen original, `cover_source_page`, `cover_kind` = foto | preview (imagen de vista previa/portada oficial) | logo, `lat`/`lng` cuando se conocen).",
      "- `data/pampam_import.csv`: spots para importar en PamPam.",
      "- `assets/covers/`: portadas 3:2 (≤1200 px) + `SOURCES.md` con créditos.", "",
      "Regenera este README con `python3 scripts/build_readme.py`.", "",
      "## Contribuir", "", "Abre un issue con el actor, una fuente pública y la fecha de verificación. Solo organizaciones; sin datos personales.", "",
      "## Licencia", "", "Datos y texto: ver [LICENSE](LICENSE). Las imágenes pertenecen a sus autores (ver `SOURCES.md`).", ""]
(R / 'README.md').write_text('\n'.join(L), encoding='utf-8')
print(len(D), 'entradas;', n_cov, 'con portada')
