# MeshCore USB Companion for the classic LilyGO T-Beam (SX1276)

**Unofficial community build • Windows / Linux • USB serial • Home Assistant ready**

[Deutsche Anleitung](README.de.md) · [Build guide](docs/BUILD.md) · [Flash guide](docs/FLASHING.md) · [Home Assistant](docs/HOME_ASSISTANT.md) · [Troubleshooting](docs/TROUBLESHOOTING.md)

> Turn a classic **LilyGO / TTGO T-Beam with ESP32 and SX1276** into a **MeshCore USB Companion**, for example as a LoRa-to-Home Assistant gateway via Proxmox USB passthrough.
>
> This is **not** an official MeshCore firmware release, and it is **not** a standalone LoRaWAN/TTN mapper.

## Why this repository exists

MeshCore provides a `Tbeam_SX1276_companion_radio_ble` profile, but the upstream release we tested does **not** publish the matching `companion_radio_usb` firmware for this classic board. This small project supplies a **non-invasive PlatformIO overlay** that builds the existing MeshCore companion application with `ENABLE_USB_INTERFACE` and without Bluetooth. It **does not fork or replace** upstream MeshCore code.

The overlay is based on a real working setup: a **T22_V1.1** board, **CP2104 USB serial**, **SX1276 / 868 MHz**, **OLED**, running **MeshCore v1.18.0**. The device successfully answered `meshcli infos` via USB and was connected to Home Assistant OS running under Proxmox, with live MeshCore data and repeater monitoring. **These observations do not establish compatibility with every T-Beam revision.**

## Hardware checklist

| Requirement | Status |
| --- | --- |
| Classic T-Beam ESP32 / **SX1276** (868/915 MHz radio module) | Target hardware |
| Board marked **T22_V1.1** | Reported working setup |
| Older/newer classic V1.x with SX1276 | Candidates — verify individual revision |
| T-Beam **SX1262**, **S3 Supreme**, T-Beam **1W**, LoRa32 | **Not supported by this build** |
| USB data cable / CP210x driver | Required |
| 868 MHz antenna for EU setup | Attach **before transmitting** |
| GPS fix / 18650 battery | Optional; not needed for Home Assistant |

**Be sure about the radio chip.** A board label such as “T-Beam 1.1” is not enough to infer SX1276 vs SX1262. This project intentionally builds **SX1276 only**.

## Quick start — build

Install [Python 3.11+](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads) (Git for Windows on Windows). The script installs **PlatformIO 6.2.0** if missing, clones the **MeshCore `companion-v1.18.0`** source tag, creates a local overlay, compiles the USB Companion, and generates checksums.

**Windows (PowerShell):**

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\build.ps1
```

**Linux / macOS:**

```bash
./build.sh
```

Successful builds create two files in `dist/`:

| File suffix | Flash address | When to use |
| --- | --- | --- |
| `*_merged-0x0.bin` | `0x0` | **Recommended** for a first install; includes bootloader/partition images |
| `*_app-0x10000.bin` | `0x10000` | Existing compatible ESP32 partition layout **only** |

The exact upstream commit, build environment and SHA-256 hashes are recorded in `dist/manifest.json` and `dist/SHA256SUMS.txt`.

**Build success is not proof of hardware compatibility.** Review the flashing guide first. No firmware is flashed automatically by this project.

## Flash — example

> **Back up any previous identity/settings first** if you intend to keep them. Flashing can replace the existing firmware and erase settings. Never flash an SX1276 build onto an SX1262 device. Connect a suitable antenna.

Install the Espressif flashing tool:

```bash
python -m pip install 'esptool>=4.8,<5'
```

Then close PuTTY, browser serial consoles, and any other program holding the serial device.

```bash
# Windows example: change COM8 to your own port and substitute the exact file
python -m esptool --chip esp32 --port COM8 --baud 115200 write_flash 0x0 dist/TBeam_SX1276_USB_companion-v1.18.0_merged-0x0.bin
```

On Linux, use a device such as `/dev/serial/by-id/...`. **Do not** use `0x0` with the `*_app-0x10000.bin` file. See [Flash guide](docs/FLASHING.md) for more.

## Test USB protocol

The device may not respond to text commands in PuTTY: the **Companion uses a binary protocol**. Install the CLI and query the Companion:

```bash
python -m pip install meshcore-cli
meshcli -s 'COM8:dtr=1,rts=0,baud=115200' infos
```

On the reported CP2104 T-Beam, setting **`dtr=1,rts=0`** was needed for the Windows CLI. Other devices may work with default control lines; Linux/HAOS device paths will be different. Expected: `Connected to ... running on ... fw` plus radio settings.

## Home Assistant / Proxmox

```mermaid
flowchart LR
    A[MeshCore radio network] <-->|868 MHz LoRa| B[T-Beam SX1276 USB Companion]
    B <-->|USB passthrough| C[Proxmox host]
    C --> D[Home Assistant OS VM]
    D --> E[MeshCore HA integration]
```

- Proxmox: identify CP210x with `lsusb` and `/dev/serial/by-id`, then add the USB device to the HAOS VM.
- HAOS: verify `/dev/ttyUSB0` (or preferably `/dev/serial/by-id/...`).
- Install [meshcore-ha](https://github.com/meshcore-dev/meshcore-ha) via HACS; add a **USB/Serial Companion** with baud rate `115200` if requested.
- When connected, you can receive public messages and monitor selected repeaters, depending on the integration version and network permissions.

Details: [Home Assistant guide](docs/HOME_ASSISTANT.md).

## Features and boundaries

- **USB serial Companion** (not a repeater firmware, not a TTN gateway).
- Preserves upstream board pin settings for SX1276, OLED button and GPS provider.
- **IO0** briefly wakes the OLED on the reported board; a blank OLED can be normal power saving.
- The presence of GPS code **does not guarantee a GPS fix**; location can be manually configured.
- Radio defaults come from the selected upstream tag; check local regulations and network presets.
- **Does not** ship vendor binaries, user credentials, device keys, or a clone of upstream source code.
- **No automatic flashing**, no automatic erase.

## CI / downloads

GitHub Actions compiles the firmware and makes the `.bin` files available under **Actions → Build T-Beam SX1276 USB → Artifacts** after the workflow completes. Workflow artifacts are **community builds**, not official MeshCore releases. A maintainer should verify an artifact on real hardware before publishing it as a GitHub Release.

## Upgrading MeshCore

The **default is the hardware-verified source tag** `companion-v1.18.0`. You can experiment with another upstream tag:

```bash
python tools/build.py --ref companion-v1.18.0
```

That creates a separate source directory and **does not claim that the newer source is compatible**. For a release, build, flash and run tests on real hardware again. If upstream adds a native T-Beam SX1276 USB configuration, prefer the official one.

## Contributing / reporting issues

See [CONTRIBUTING.md](CONTRIBUTING.md). Include board revision, radio chip, CP210x model, build output, and firmware tag; do **not** post private keys, Wi-Fi passwords, repeater admin passwords, or precise home coordinates.

## Licensing and credits

This repository's original scripts and documentation are under the [MIT License](LICENSE). MeshCore is developed separately by [meshcore-dev](https://github.com/meshcore-dev/MeshCore) and is MIT-licensed; its license and credit remain with the upstream project. See [NOTICE.md](NOTICE.md).
