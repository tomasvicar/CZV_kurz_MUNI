# CZV kurz MUNI

*🇬🇧 [English version](README.en.md)*

Materiály a instalační pokyny pro kurz zpracování obrazu (Fiji, Ilastik, Cellpose, CellProfiler).

## Data

Kurzovní data ke stažení:

- [FileSender CESNET — stáhnout data](https://filesender.cesnet.cz/?s=download&token=5f3ddd5d-bc29-4d98-b733-5825b8ae162d)

## Instalace softwaru

### Fiji

Stáhněte archiv, rozbalte a spusťte:

- <https://imagej.net/software/fiji/downloads>

### Ilastik

- <https://www.ilastik.org/download>

### Cellpose

Následující postup je pro **Windows** (PowerShell). Využívá [**uv**](https://docs.astral.sh/uv/) — rychlý správce Python prostředí.

> **Alternativa — nechte to udělat AI agenta.** Pokud používáte AI kódovacího agenta (např. Claude Code, Cursor, Copilot), stačí mu zadat prompt:
>
> > *„Nainstaluj mi cellpose pomocí uv včetně podpory GPU, pokud je to možné."*
>
> Agent detekuje GPU, vytvoří prostředí a nainstaluje správnou variantu PyTorch automaticky.

#### 1. Instalace uv

Otevřete PowerShell a spusťte:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. Vytvoření prostředí a instalace Cellpose

V adresáři projektu:

```bash
uv venv cellpose_env
uv pip install --python cellpose_env/Scripts/python.exe "cellpose[gui]"
```

#### 3. Instalace PyTorch s podporou NVIDIA GPU (CUDA 12.1)

Vyžaduje NVIDIA GPU a aktuální ovladač (CUDA 12.1+). Přeinstaluje CPU verzi torch za CUDA build:

```bash
uv pip install --python cellpose_env/Scripts/python.exe --reinstall torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

Ověření, že GPU je dostupné:

```bash
cellpose_env/Scripts/python.exe -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

#### 4. Spuštění Cellpose GUI

```bash
cellpose_env/Scripts/python.exe -m cellpose
```

Více informací: <https://github.com/MouseLand/cellpose>

## Online tutoriály

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
