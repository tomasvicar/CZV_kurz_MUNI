# Fiji basics — from a single click to an AI-assisted macro

*🇨🇿 [Česká verze](Fiji_basics.md)*

A guided tour of Fiji aimed at people who have never used it, ending with
an AI-assisted macro that generalizes a click-through workflow into a
reproducible script.

We use the course dataset [testovaci_data/](testovaci_data/) — the same
PNT1A / PC3 TIFFs used in the [AI agent showcase](AI_agent_showcase1.en.md),
so you can compare a classical Fiji workflow against an AI-driven pipeline.

> **Note.** Fiji can do an enormous amount of things — 3D rendering,
> deconvolution, tracking, registration, deep-learning segmentation,
> colocalization, and much more. This page is just a quick tour of a few
> basic operations to get you started; it is nowhere near an exhaustive
> overview.

---

## 1. Opening images and file formats

File → Open handles common formats directly (TIFF, PNG, JPEG).
For microscopy formats (`.lif`, `.czi`, `.nd2`, `.ome.tiff`, …) Fiji ships
with **Bio-Formats**, which detects the format, reads metadata (pixel size,
channels, time) and opens the image as a hyperstack.

> Drag-and-drop works too — just drop the file onto the Fiji toolbar.

![Drag-and-drop to open a file](assets/fiji/drag_and_drop.png)

---

## 2. Navigating an image

Zoom: `+` / `-` or scroll wheel. Pan: hold space.
Multi-dimensional images expose sliders at the bottom: **c** (channel),
**z** (slice), **t** (time).

Image → Properties shows the pixel size and units — **always check this
before measuring**, otherwise every size you report is in pixels.

---

## 3. Brightness, contrast and LUTs

Image → Adjust → **Brightness/Contrast** changes how the image is
*displayed* — the underlying pixel values are untouched. This is the single
most common source of confusion for newcomers: stretching the histogram
does **not** alter the data used for measurements.

LUTs (Image → Lookup Tables) assign colors to intensities — useful for
single-channel fluorescence (Fire, Grays, Green, …).

![Brightness/Contrast dialog](assets/fiji/brightness.png)

---

## 4. ROIs and measurements

Use the toolbar (rectangle, ellipse, polygon, freehand, line) to draw a
region of interest. Open **Analyze → Tools → ROI Manager** and press `t`
to store the selection — the ROI Manager lets you reuse, rename, save and
batch-apply regions.

Pick the quantities you want with **Analyze → Set Measurements** (area,
mean, integrated density, bounding box, …), then **Analyze → Measure**
(`m`) produces a Results table.

![ROI Manager with stored selections](assets/fiji/roi.png)

---

## 5. Intensity line profile

Draw a straight line across a feature and run **Analyze → Plot Profile**
(`k`). You get intensity along the line — the fastest sanity check for
contrast, background level and whether an edge is real or a compression
artifact.

![Line profile across a cell](assets/fiji/profile.png)

---

## 6. Filtering and background correction

Process → Filters offers the standard kit: Gaussian Blur (denoise),
Median (salt-and-pepper removal), Unsharp Mask (sharpen).

Process → **Subtract Background** (rolling ball) flattens uneven
illumination — crucial before thresholding, otherwise the threshold picks
up the gradient instead of the cells.

![Gaussian blur filter](assets/fiji/gaussian_blur.png)

---

## 7. Thresholding and particle analysis

Image → Adjust → **Threshold** opens a histogram-based binarizer. Try
different methods in the dropdown (Otsu, Triangle, Li, …) — there is no
universally correct one, it depends on the image.

Once you have a mask, **Analyze → Analyze Particles** counts connected
components and measures each one, filtering by size and circularity.
Output: a labeled image, an overlay, and a Results table.

![Threshold dialog](assets/fiji/threshold.png)

---

## 8. Finding commands — the command finder

Fiji has *hundreds* of commands. Press **`L`** to open the command finder
and start typing — it's the fastest way to navigate without memorizing
menus. **Help → Search…** searches the ImageJ docs and forum.

> If you only remember one shortcut, remember `L`.

![Command finder with a search query](assets/fiji/shearch.png)

---

## 9. Plugins and update sites

Help → Update… → **Manage update sites** gives you one-click access to
community toolboxes:

- **MorphoLibJ** — advanced morphology, watershed, label-map operations
- **BioVoxxel** — image analysis utilities and extended particle analysis
- **3D ImageJ Suite** — 3D segmentation and measurement
- **StarDist**, **CSBDeep** — deep-learning segmentation

Tick the site, click Apply Changes, restart Fiji. The plugin shows up in
the menu.

---

## 10. Recording a macro

Plugins → Macros → **Record…** opens a recorder window. Every click,
every dialog, every parameter you touch is captured as an ImageJ macro
line. Run your workflow once, then File → Save As → `.ijm`.

This turns a one-off click-through into a reproducible script — and it
is also how you learn the macro API: just do the thing and read what
Record wrote.

![Macro recorder capturing a workflow](assets/fiji/macro.png)

---

## 11. Letting an AI write the macro

Record is perfect for *capturing* a sequence, but the captured script is
often verbose, hard-coded to one image, and clumsy to generalize. This is
where an LLM coding agent helps:

- **Describe the goal, not the clicks.** *"For every .tif in this folder,
  subtract background (rolling ball 50), threshold with Triangle, run
  Analyze Particles with area 50–5000, and append results to one CSV."*
- **Hand it the Record output as a starting point.** The agent sees the
  exact API calls you need and generalizes them into a loop.
- **Ask for a specific dialect.** Say *"ImageJ macro language (.ijm), not
  Groovy"* — Fiji supports several scripting languages and models sometimes
  mix them up.
- **Verify by running.** Treat the generated macro as a draft. Fiji is
  forgiving — run it on one image first, then scale up.

Limits worth knowing: LLMs sometimes hallucinate between ImageJ 1 and
ImageJ 2 APIs, or mix macro syntax with Jython/Groovy. If a line looks
suspicious, cross-check it by recording the same action manually.

---

## What to take away

- Fiji is a **visual prototyping environment** — click until the workflow
  works, then turn it into a macro.
- **Brightness/contrast changes display, not data.** Measure on the raw
  pixels.
- **Always check pixel size** before reporting measurements.
- `L` finds any command. Update sites give you the rest.
- **Record + AI** is the production loop: one click-through becomes a
  reproducible, generalizable script in minutes.
