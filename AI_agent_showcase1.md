# Agent pro zpracování obrazu — ukázka

*🇬🇧 [English version](AI_agent_showcase1.en.md)*

Krátká ukázka použití LLM kódovacího agenta (Claude Code) jako
**autonomního asistenta pro zpracování obrazu**: od jednovětého zadání
k funkčnímu pipeline, QC obrázkům a srovnávacímu grafu.

---

## Zadání

> *„Try to create a simple script that segments cells in the `testovaci_data`
> folder, extracts their sizes, and plots a boxplot comparing the two cell
> types. Also save an example segmentation for quality control."*

Následováno:

> *„Segmentation is not very good — try some better approach."*

Žádné cesty k souborům, žádná volba knihovny, žádné parametry. Agent si
musel sám zjistit strukturu dat, vybrat segmentační strategii a iterovat
na kvalitě.

---

## Co agent udělal

1. **Prozkoumal workspace** — zjistil, že `testovaci_data` neexistuje a
   přešel na `data_celltypes/` (4 TIFFy, dva typy buněk: *PNT1A* a *PC3*).
2. **Diagnostikoval formát souborů** — LZW-komprimované TIFFy; chybějící
   závislost `imagecodecs` doinstaloval automaticky.
3. **Postavil první pipeline** — Gaussovský blur → Otsu → watershed nad
   distanční transformací. Spustil ho. Všiml si, že slabé *PC3* buňky
   zmizely, protože Otsu globální práh byl pro řídká pole s nízkým
   kontrastem příliš přísný.
4. **Iteroval na kvalitě** po zpětné vazbě:
   - per-image percentilová normalizace
   - odečtení pozadí stylem „rolling ball" (Gauss s velkým σ)
   - **triangle threshold** místo Otsu (benevolentnější pro řídký foreground)
   - **`peak_local_max`** seedování markerů → čistší watershed rozdělení
     dotýkajících se jader
5. **Poctivě reportoval** — označil 3 nejslabší PC3 objekty, které pořád
   zůstaly pod prahem, a doporučil Cellpose/StarDist jako skutečné řešení
   pro slabé buňky místo toho, aby tvrdil, že výsledek je dokonalý.

---

## Pipeline (klasická, ~40 řádků)

```python
def segment(img):
    lo, hi = np.percentile(img, (1, 99.5))
    norm = np.clip((img - lo) / (hi - lo + 1e-8), 0, 1)

    background = filters.gaussian(norm, sigma=40, preserve_range=True)
    flat = np.clip(norm - background, 0, None)
    smooth = filters.gaussian(flat, sigma=2, preserve_range=True)

    thr = filters.threshold_triangle(smooth)
    fg = smooth > thr
    fg = morphology.remove_small_holes(fg, area_threshold=300)
    fg = morphology.binary_opening(fg, morphology.disk(2))
    fg = morphology.remove_small_objects(fg, min_size=MIN_CELL_AREA)

    seed_src = filters.gaussian(flat, sigma=6, preserve_range=True)
    coords = feature.peak_local_max(
        seed_src, min_distance=10, threshold_abs=thr * 0.5, labels=fg
    )
    marker_img = np.zeros(img.shape, dtype=bool)
    marker_img[tuple(coords.T)] = True
    markers = measure.label(marker_img)

    labels = segmentation.watershed(-seed_src, markers, mask=fg)
    return morphology.remove_small_objects(labels, min_size=MIN_CELL_AREA)
```

Celý skript — [segment_cells.py](assets/segment_cells.py).

---

## Výsledky

### QC overlaye

| Typ buňky | Overlay |
|---|---|
| **PNT1A** (husté epiteliální pole) | ![PNT1A QC](assets/qc_PNT1A.png) |
| **PC3** (řídké, nízký kontrast) | ![PC3 QC](assets/qc_PC3.png) |

### Porovnání velikostí

![Boxplot velikostí buněk](assets/boxplot_cell_sizes.png)

| Typ   | n  | Medián (px) | Průměr (px) |
|-------|----|-------------|-------------|
| PC3   | 17 | 2057        | 2112        |
| PNT1A | 84 | 1571        | 1694        |

*PC3 buňky jsou viditelně větší, ale mnohem řidší než husté PNT1A pole —
biologicky věrohodný výsledek, který odpovídá tomu, co vidíte v surových
obrázcích.*

### Před a po iteraci „try a better approach"

|                   | První pokus (Otsu)       | Zlepšené (triangle + BG-sub) |
|-------------------|--------------------------|------------------------------|
| Nalezené PC3      | 19                       | **17** (ale celá těla)       |
| Medián plochy PC3 | 753 px (erodované masky) | **2057 px** (přesné)         |
| PNT1A dělení      | přefragmentované         | **čisté jedno-na-jádro**     |

První běh nahlásil *více* PC3 objektů, ale každý byl malý erodovaný
fragment. Zlepšený běh zachytí celá těla buněk, což je to, co pro
porovnání velikostí skutečně chcete.

---

## Co to ukazuje

- **Otevřené zadání → funkční pipeline.** Agent zvládl podspecifikovaný
  požadavek end-to-end: objevení dat, instalaci závislostí, volbu
  algoritmu, iteraci a reporting.
- **Sebekorekce podle kvality.** Když dostal zpětnou vazbu, že výstup je
  špatný, *změnil metodu* (práh, preprocessing, markery), místo aby jen
  ladil konstanty.
- **Poctivé limity.** Označil zbývající selhání (3 slabé PC3 objekty) a
  doporučil, kdy by byl další krok deep-learning nástroj, místo aby
  předstíral, že klasické metody vyhrály.
- **Malá stopa.** Jeden skript, standardní `scikit-image` stack, žádné
  těžké modely — rychlé spuštění a snadný audit.

---

*Vygenerováno pomocí Claude Code (Opus 4.6) — `d:/CZV_kurz_MUNI/xxx`.*
