"""Análisis exploratorio por municipio; no mezcla unidades entre contaminantes."""
import argparse
import json
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from urllib.parse import urlencode
from urllib.request import urlopen
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

URL = "https://www.datos.gov.co/resource/kekd-7v7h.json"


def normalizar(value):
    return "".join(c for c in unicodedata.normalize("NFKD", str(value)).lower()
                   if not unicodedata.combining(c)).strip()


def descargar(page_size=1000):
    rows = []
    offset = 0
    while True:
        query = urlencode({"$limit": page_size, "$offset": offset, "$order": ":id"})
        with urlopen(URL + "?" + query, timeout=60) as response:
            page = json.load(response)
        if not isinstance(page, list):
            raise ValueError("La API no devolvió una lista de registros")
        rows.extend(page)
        if len(page) < page_size:
            break
        offset += len(page)
    return pd.DataFrame(rows)


def limpiar(df, municipio):
    required = ["nombre_del_municipio", "estaci_n", "variable", "unidades", "a_o", "promedio"]
    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")
    selected = df.loc[df["nombre_del_municipio"].map(normalizar) == normalizar(municipio)].copy()
    selected = selected.rename(columns={"estaci_n": "estacion", "variable": "contaminante",
                                        "a_o": "anio", "nombre_del_municipio": "municipio"})
    selected["promedio"] = pd.to_numeric(selected["promedio"], errors="coerce")
    selected["anio"] = pd.to_numeric(selected["anio"], errors="coerce")
    selected = selected.dropna(subset=["promedio", "anio", "estacion", "contaminante", "unidades"])
    selected = selected.loc[selected["anio"].mod(1).eq(0)].copy()
    selected["anio"] = selected["anio"].astype(int)
    if selected.empty:
        raise ValueError(f"No hay registros válidos para {municipio}; no se generan resultados")
    return selected


def ejecutar(df, municipio, out):
    clean = limpiar(df, municipio)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    clean.to_csv(out / "datos_filtrados.csv", index=False)
    summary = clean.groupby(["contaminante", "unidades", "estacion"], as_index=False).agg(
        promedio_de_registros=("promedio", "mean"), registros=("promedio", "size"),
        primer_anio=("anio", "min"), ultimo_anio=("anio", "max"))
    summary.to_csv(out / "resumen.csv", index=False)
    metadata = {"source": URL, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                "municipio": municipio, "source_records": len(df), "valid_records": len(clean),
                "first_year": int(clean.anio.min()), "last_year": int(clean.anio.max()),
                "note": "Promedios exploratorios de registros publicados; no estimaciones de exposición ni mediciones diarias."}
    (out / "cobertura.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    for i, ((contaminante, unidad), group) in enumerate(summary.groupby(["contaminante", "unidades"]), 1):
        fig, ax = plt.subplots(figsize=(10, max(4, len(group) * 0.3)))
        ax.barh(group["estacion"], group["promedio_de_registros"])
        ax.set(xlabel=f"Promedio de registros ({unidad})", title=f"{municipio} · {contaminante}")
        fig.tight_layout()
        fig.savefig(out / f"contaminante_{i:02d}.png", dpi=150)
        plt.close(fig)
    return metadata


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--municipio", default="Medellín")
    parser.add_argument("--input", help="CSV local con columnas originales; omite la descarga")
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()
    raw = pd.read_csv(args.input) if args.input else descargar()
    print(json.dumps(ejecutar(raw, args.municipio, args.out), ensure_ascii=False, indent=2))
