# CZV course MUNI

*🇨🇿 [Česká verze](README.md)*

Materials and installation instructions for the image processing course (Fiji, Ilastik, Cellpose, CellProfiler).

## Data

Course data for download:

- [data.zip](data.zip)

## Course materials

- [Fiji basics](Fiji_basics.en.md) — a quick tour of basic operations and writing macros with AI help
- [AI agent showcase](AI_agent_showcase1.en.md) — cell segmentation and size comparison using an LLM coding agent

## Software installation

### Fiji

Download the archive, unpack it and run:

- <https://imagej.net/software/fiji/downloads>

### Ilastik

- <https://www.ilastik.org/download>

### Cellpose

The following procedure is for **Windows** (PowerShell). It uses [**uv**](https://docs.astral.sh/uv/) — a fast Python environment manager.

> **Alternative — let an AI agent do it.** If you use an AI coding agent (e.g. Claude Code, Cursor, Copilot), just give it the prompt:
>
> > *"Install cellpose using uv with GPU support if possible."*
>
> The agent will detect the GPU, create the environment and install the correct PyTorch variant automatically.

#### 1. Install uv

Open PowerShell and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. Create environment and install Cellpose

In the project directory:

```bash
uv venv cellpose_env
uv pip install --python cellpose_env/Scripts/python.exe "cellpose[gui]"
```

#### 3. Install PyTorch with NVIDIA GPU support (CUDA 12.1)

Requires an NVIDIA GPU and an up-to-date driver (CUDA 12.1+). Reinstalls the CPU torch build with the CUDA build:

```bash
uv pip install --python cellpose_env/Scripts/python.exe --reinstall torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

Verify that the GPU is available:

```bash
cellpose_env/Scripts/python.exe -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

#### 4. Launch Cellpose GUI

```bash
cellpose_env/Scripts/python.exe -m cellpose
```

More info: <https://github.com/MouseLand/cellpose>

## Online tutorials

### Cellpose

- <https://www.youtube.com/watch?v=5qANHWoubZU>

### Ilastik

- <https://www.youtube.com/watch?v=F6KbJ487iiU>

### Fiji

- <https://www.youtube.com/watch?v=mzS_Ay3VT5E>
- <https://www.youtube.com/watch?v=4URnGkrxXP0>
- <https://www.youtube.com/watch?v=smFso78veak>

### CellProfiler

- <https://www.youtube.com/watch?v=OgyfbJOMr70&list=PLXSm9cHbSZBBy7JkChB32_e3lURUcT3RL&index=5>
- <https://www.youtube.com/watch?v=8RGvnADDSkg>
