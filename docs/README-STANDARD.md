# Directory README standard

`README.md` is the public directory of the Arequipa innovation and technology ecosystem. **Do not hand-edit it.** Change `scripts/build_readme.py` and regenerate:

```bash
python3 scripts/build_readme.py
```

The header must follow this contract so the page stays discoverable and consistent.

## 1. H1 with keywords

First heading, exactly:

```markdown
# Awesome Ecosistema de Innovación y Tecnología de Arequipa, Perú
```

Defined as `H1` in the generator. Keep the location keywords (Arequipa, Perú) and the topic keywords (ecosistema, innovación, tecnología).

## 2. Links block

Immediately under the H1 (after the existing Awesome badge), render every entry of the `LINKS` dict at the top of `scripts/build_readme.py`. Do not scatter these URLs elsewhere in the script. Use HTML anchors inside the centered `<p>` (`<a href="...">Web</a> · …`): GFM does not process markdown `[label](url)` inside an inline HTML block.

| Label | Surface |
|---|---|
| Web | Public directory site |
| Guía | How-to / guide |
| Notion | Source directory |
| Mapa PamPam | Map |
| Ranking TierMaker | Category ranking |

Add or rename a surface by editing `LINKS` only, then regenerating.

## 3. Data-derived intro

A short Spanish paragraph (2–4 sentences) with natural discovery wording: ecosistema de innovación, startups, comunidades tech, universidades, incubadoras, eventos, Arequipa, Perú.

Every figure (actor count, category count, per-category counts, photo count) is computed from `data/ecosistema_arequipa.json` at build time. Do not hardcode numbers or invent facts that are not in the dataset.

## 4. Body

Table of contents, category tables, Datos, Contribuir, and Licencia stay generated from the same data and templates. Header/intro changes should not alter list content.

## 5. Check

`tests/test_readme_header.py` (and `assert_header` in the generator) require the H1 and all five `LINKS` URLs to be present in the generated README:

```bash
python3 tests/test_readme_header.py
```
