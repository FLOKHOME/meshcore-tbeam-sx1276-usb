# Flashing guide — classic ESP32 T-Beam SX1276

> Flashing is optional and explicit. Do not flash the wrong chip, and do not erase a device until its current keys/settings have been backed up if needed.

## Preflight

1. Confirm that your hardware contains an **SX1276**, **not SX1262**.
2. Confirm ESP32 classic / T-Beam board, not T-Beam S3 Supreme or T-Beam 1W.
3. Attach a suitable antenna before using radio functionality.
4. Backup any current TTN Mapper / Meshtastic / MeshCore data that matters. The supplied image is **not** a backup.
5. Use a known USB data cable; close PuTTY and all applications accessing the serial port.
6. Obtain the exact `*_merged-0x0.bin` from a successful build; validate SHA-256 from `SHA256SUMS.txt` if distributing it.

## Flashing with esptool 4.x

```bash
python -m pip install 'esptool>=4.8,<5'
```

**Windows:** substitute your detected COM port, e.g. `COM8`:

```powershell
py -m esptool --chip esp32 --port COM8 --baud 115200 write_flash 0x0 "dist\TBeam_SX1276_USB_companion-v1.17.1_merged-0x0.bin"
```

**Linux:** use the actual serial path (for example `/dev/ttyUSB0`):

```bash
python3 -m esptool --chip esp32 --port /dev/ttyUSB0 --baud 115200 write_flash 0x0 dist/TBeam_SX1276_USB_companion-v1.17.1_merged-0x0.bin
```

**Warning:** `0x0` is only correct for the **merged** image. If intentionally updating just the app on an already-compatible bootloader/partition layout, use the **`*_app-0x10000.bin`** file at `0x10000`, not `0x0`. First-time users should use the merged image.

If automatic upload mode fails: hold **IO0 / BOOT**, briefly press **RST**, release RST and then release IO0 after the bootloader is ready. Retry the flash. **PWR is the power button**, not the download-mode key. Board key labels can vary.

## After flashing

Reboot or reconnect USB. The OLED can go dark after its power-save timeout; short-pressing **IO0** wakes it on the tested T22 V1.1 board. That behavior does not indicate failure.

The Companion's serial stream is **binary**, not a text command terminal. Validate it through `meshcore-cli`:

```bash
python -m pip install meshcore-cli
meshcli -s 'COM8:dtr=1,rts=0,baud=115200' infos
```

For the tested CP2104 device the `dtr=1,rts=0` combination was necessary under Windows; your port and line states may vary. Check that you see a `Connected to ... running on a ... fw` response and the configured radio settings.

GPS is optional, and a missing GPS fix indoors is not a USB or LoRa failure.
