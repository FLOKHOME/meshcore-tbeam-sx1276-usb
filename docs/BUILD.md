# Build from source

The builder is deliberately simple and repeatable, not an upstream fork.

## 1. Prerequisites

- Python 3.11+ (Windows users can use `py`), Git, internet access.
- Python's `pip` available. PlatformIO 6.2.0 is installed if not found.
- Compatible hardware is **not required for compilation**; it is required for validation.

## 2. Run

```powershell
# Windows
powershell.exe -ExecutionPolicy Bypass -File .\build.ps1
```

```bash
# Linux/macOS
./build.sh
```

`python tools/build.py --help` shows `--work-dir`, `--output-dir`, `--ref`, `--no-install`, and `--skip-merged`.

Default source tag is `companion-v1.18.0` (upstream commit beginning `81dbae5`). The script:

1. Clones the exact MeshCore release tag into `.work/MeshCore-companion-v1.18.0` (only if missing).
2. Verifies the repository origin and required upstream files and conditional `ENABLE_USB_INTERFACE` code.
3. Writes a new `platformio.local.ini` overlay and **refuses to overwrite someone else's customized overlay**.
4. Builds `Tbeam_SX1276_companion_radio_usb` by inheriting the stock BLE target's source filters and libraries but replacing BLE build flags with USB flags.
5. Runs the upstream `mergebin` custom target to create the full flash image.
6. Copies application/merged images to `dist/`, recording hashes and source metadata.

No automatically generated firmware is committed to the source repository. The upstream sources remain separate from this repo.

## 3. Build environment

```ini
[env:Tbeam_SX1276_companion_radio_usb]
extends = env:Tbeam_SX1276_companion_radio_ble
build_flags =
  ${LilyGo_TBeam_SX1276.build_flags}
  -I examples/companion_radio/ui-new
  -D MAX_CONTACTS=160
  -D MAX_GROUP_CHANNELS=40
  -D OFFLINE_QUEUE_SIZE=128
  -D ENABLE_USB_INTERFACE
```

`extends = env:...` is essential: the base profile is a PlatformIO **environment**, not a plain configuration section. Using the wrong form can produce `UndefinedEnvPlatformError`.

The build uses the full upstream SX1276 pin mapping, including DIO0 26, DIO1 33, CS 18, RESET 23, SCLK 5, MISO 19 and MOSI 27. The custom overlay does not redefine those pins.

## 4. Updating upstream

Use `--ref companion-v1.18.0` to build a different MeshCore tag **at your own risk**. A new source tree is created per tag. If the upstream project changes its build flags, file structure or interface support, the builder stops instead of silently patching unknown code. New firmware versions need another hardware validation run.

## 5. Known errors

| Problem | Meaning / fix |
| --- | --- |
| `No module named platformio` | Use builder (auto-install) or `python -m pip install platformio==6.2.0` |
| `UndefinedEnvPlatformError` | Overlay must have `extends = env:Tbeam_SX1276_companion_radio_ble` |
| `firmware.bin` missing | Compilation failed; check full error output, not only the final file test |
| `platformio.local.ini exists` | Builder refuses to overwrite custom content; back it up or choose a new work area |
| `mergebin` missing | Upstream source changed, check tag and upstream build system |
| Serial connects but no protocol response | See `docs/TROUBLESHOOTING.md`, especially DTR/RTS |

## 6. CI

`.github/workflows/build.yml` executes offline Python unit tests followed by the same public builder. Github Actions publishes the output as a downloadable **workflow artifact**, not a signed / hardware-certified release.
