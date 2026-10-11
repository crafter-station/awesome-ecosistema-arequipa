"""Regenera README.md desde data/ecosistema_arequipa.json (miniaturas desde assets/covers/)."""
import json, pathlib, re

R = pathlib.Path(__file__).resolve().parents[1]

# Canonical public surfaces — keep URLs here, not scattered in the template.
H1 = "Awesome Ecosistema de Innovación y Tecnología de Arequipa, Perú"
LINKS = {
    "Web": "https://arequipa-sillar-connect.lovable.app",
    "Guía": "https://arequipa-sillar-connect.lovable.app/guia",
    "Notion": "https://ignacio-velasquez.notion.site/Directorio-Ecosistema-Arequipa-3f2da2435b468151bbadd79211050be0",
    "Mapa PamPam": "https://www.pampam.city/ecosistema-de-innovacion-de-arequipa-5cJmBIAEiXBQ0yQw4bfp",
    "Ranking TierMaker": "https://tiermaker.com/list/technology/ecosistema-de-innovacin-de-arequipa-19907354/6679308",
}

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

# Count keys used in the intro (labels in Spanish, only emitted when count > 0).
INTRO_FEATURED = [
    ("universidad", "universidades"),
    ("instituto/escuela técnica", "institutos"),
    ("incubadora/aceleradora", "incubadoras y aceleradoras"),
    ("comunidad tech", "comunidades tech"),
    ("espacio de innovación (hub/coworking/fablab)", "espacios de innovación"),
    ("startup", "startups"),
    ("evento recurrente", "eventos recurrentes"),
]
INTRO_ALSO = [
    ("entidad pública/programa público", "entidades públicas"),
    ("oficina universitaria de innovación/transferencia", "oficinas universitarias de innovación"),
    ("fundación/ONG", "fundaciones"),
    ("gremio/cámara", "gremios"),
    ("medio local", "medios"),
    ("red", "redes"),
]


def load_data():
    return json.load(open(R / "data/ecosistema_arequipa.json", encoding="utf-8"))


def cat_counts(data):
    return {c: sum(1 for x in data if x["categoria"] == c) for c, _ in CATS}


def photo_count(data):
    return sum(1 for x in data if x.get("cover_path") and x.get("cover_kind", "foto") == "foto")


def intro_paragraph(data):
    """2–4 Spanish sentences; every number comes from the dataset."""
    n = len(data)
    by_cat = cat_counts(data)
    n_cats = sum(1 for v in by_cat.values() if v)
    n_cov = photo_count(data)
    featured = [f"**{by_cat[c]}** {label}" for c, label in INTRO_FEATURED if by_cat[c]]
    also = [label for c, label in INTRO_ALSO if by_cat[c]]
    featured_txt = ", ".join(featured[:-1]) + f" y {featured[-1]}" if len(featured) > 1 else (featured[0] if featured else "")
    also_txt = ", ".join(also[:-1]) + f" y {also[-1]}" if len(also) > 1 else (also[0] if also else "")
    return (
        f"Directorio curado del **ecosistema de innovación** y tecnología de **Arequipa, Perú**. "
        f"Reúne **{n} actores** en **{n_cats} categorías** — universidades, incubadoras, "
        f"comunidades tech, espacios de innovación, startups, eventos y más. "
        f"Incluye {featured_txt}"
        + (f", además de {also_txt}" if also_txt else "")
        + f". **{n_cov}** entradas tienen foto real; cada ficha enlaza a su fuente pública."
    )


def links_block():
    items = " · ".join(f"[{label}]({url})" for label, url in LINKS.items())
    return f'<p align="center">{items}</p>'


def anchor(t):
    return "#" + re.sub(r"[^\w\- ]", "", t.lower(), flags=re.U).replace(" ", "-")  # estilo GitHub: emoji+espacio => '-'


def cell(s):
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def link(x):
    w = (x.get("web") or "").split(" ")[0]
    return f"[{cell(x['nombre'])}]({w})" if w.startswith("http") else f"**{cell(x['nombre'])}**"


def assert_header(text):
    assert f"# {H1}" in text, "README missing keyword H1"
    for url in LINKS.values():
        assert url in text, f"README missing link {url}"


def build_readme(data=None):
    D = data if data is not None else load_data()
    n_cov = photo_count(D)
    L = [
        '<p align="center"><img src="assets/header-arequipa-misti.jpg" alt="Volcán Misti y Catedral de Arequipa" width="100%"></p>',
        "",
        f"# {H1}",
        "",
        '<p align="center"><a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a></p>',
        "",
        links_block(),
        "",
        intro_paragraph(D),
        "",
        f"**{len(D)} actores** · **{n_cov}** con foto real · cada entrada enlaza a su **fuente pública**. Créditos de imágenes en [`assets/covers/SOURCES.md`](assets/covers/SOURCES.md).",
        "",
        "## Contenido",
        "",
    ]
    for c, t in CATS:
        k = sum(1 for x in D if x["categoria"] == c)
        L.append(f"- [{t}]({anchor(t)}) ({k})")
    L += ["- [Datos](#datos)", "- [Contribuir](#contribuir)", ""]
    for c, t in CATS:
        rows = sorted([x for x in D if x["categoria"] == c], key=lambda x: x["nombre"].lower())
        L += [f"## {t}", ""]
        if not rows:
            q = EMPTY.get(c, "un actor de esta categoría activo en Arequipa")
            L += [f"_Sin actores verificados aún. ¿Conoces {q}? Abre un issue con su fuente pública._", "", "[⬆ volver](#contenido)", ""]
            continue
        L += ["| | Actor | Descripción | Fuente |", "|:-:|---|---|:-:|"]
        for x in rows:
            thumb = f'<img src="{x["cover_path"]}" width="120" alt="">' if x.get("cover_path") else ""
            dist = f" <br><sub>📍 {cell(x['distrito'])}</sub>" if x.get("distrito") else ""
            src = f"[🔗]({x['fuente_url']})" if (x.get("fuente_url") or "").startswith("http") else ""
            L.append(f"| {thumb} | {link(x)}{dist} | {cell(x['descripcion_corta'])} | {src} |")
        L += ["", "[⬆ volver](#contenido)", ""]
    L += [
        "## Datos",
        "",
        "- `data/ecosistema_arequipa.csv` / `.json`: directorio completo (`cover_path` = imagen en este repo, `cover_url` = imagen original, `cover_source_page`, `cover_kind` = foto | preview (imagen de vista previa/portada oficial) | logo, `lat`/`lng` cuando se conocen).",
        "- `data/pampam_import.csv`: spots para importar en PamPam.",
        "- `assets/covers/`: portadas 3:2 (≤1200 px) + `SOURCES.md` con créditos.",
        "",
        "Regenera este README con `python3 scripts/build_readme.py`.",
        "",
        "## Contribuir",
        "",
        "Abre un issue con el actor, una fuente pública y la fecha de verificación. Solo organizaciones; sin datos personales.",
        "",
        "## Licencia",
        "",
        "Datos y texto: ver [LICENSE](LICENSE). Las imágenes pertenecen a sus autores (ver `SOURCES.md`).",
        "",
    ]
    text = "\n".join(L)
    assert_header(text)
    return text


def main():
    D = load_data()
    text = build_readme(D)
    (R / "README.md").write_text(text, encoding="utf-8")
    n_cov = photo_count(D)
    print(len(D), "entradas;", n_cov, "con portada")


if __name__ == "__main__":
    main()
