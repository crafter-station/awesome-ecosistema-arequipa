#!/usr/bin/env python3
"""Regenera data/*.csv, data/*.json y README.md desde la base Notion 'Directorio' (fuente de verdad).
Uso: NOTION_TOKEN=secret_xxx NOTION_DIRECTORIO_DB=<db_id> python3 scripts/export_from_notion.py
Requiere: pip install requests. Solo lectura sobre Notion. Nombres de propiedades según notion_mapping.md.
"""
import os, csv, json, sys, requests
TOKEN=os.environ.get("NOTION_TOKEN"); DB=os.environ.get("NOTION_DIRECTORIO_DB","fb90c3816e0d4adf90f894bbc782cba0")
if not TOKEN or DB.startswith("<"): sys.exit("Define NOTION_TOKEN y NOTION_DIRECTORIO_DB")
H={"Authorization":f"Bearer {TOKEN}","Notion-Version":"2022-06-28","Content-Type":"application/json"}
COLS=["nombre","categoria","descripcion_corta","distrito","direccion","lat","lng","web","redes","actividad_reciente","fuente_url","fecha_verificacion","fuente_coords"]
PROP={"nombre":"Nombre","categoria":"Categoría","descripcion_corta":"Descripción","distrito":"Distrito","direccion":"Dirección","lat":"Lat","lng":"Lng","web":"Web","redes":"Redes","actividad_reciente":"Detalle actividad","fuente_url":"Fuente URL","fecha_verificacion":"Fecha verificación","fuente_coords":"Fuente coords"}
def val(p):
    if p is None: return ""
    t=p["type"]; v=p[t]
    if t in("title","rich_text"): return "".join(x["plain_text"] for x in v)
    if t=="select": return v["name"] if v else ""
    if t=="multi_select": return ", ".join(x["name"] for x in v)
    if t=="number": return "" if v is None else str(v)
    if t=="url": return v or ""
    if t=="date": return (v or {}).get("start","")
    if t=="checkbox": return "sí" if v else "no"
    return ""
rows=[]; cursor=None
while True:
    body={"page_size":100, **({"start_cursor":cursor} if cursor else {}),
          "filter":{"property":"Estado","select":{"equals":"Publicado"}}}  # solo filas aprobadas (A3)
    r=requests.post(f"https://api.notion.com/v1/databases/{DB}/query",headers=H,json=body); r.raise_for_status(); d=r.json()
    for pg in d["results"]:
        rows.append({c:val(pg["properties"].get(PROP[c])) for c in COLS})
    if not d.get("has_more"): break
    cursor=d["next_cursor"]
os.makedirs("data",exist_ok=True)
with open("data/ecosistema_arequipa.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(rows)
json.dump(rows,open("data/ecosistema_arequipa.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
spots=[x for x in rows if x["lat"] and x["lng"]]
with open("data/pampam_spots.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["Title","Address","Coordinates","Description","Links","Section"])
    for x in spots: w.writerow([x["nombre"],f'{x["direccion"]}, Arequipa, Perú' if x["direccion"] else "Arequipa, Perú",f'{x["lat"]}, {x["lng"]}',x["descripcion_corta"],x["web"],x["categoria"]])
print(f"{len(rows)} filas exportadas, {len(spots)} con coordenadas. Regenera README con la misma lógica del borrador.")
