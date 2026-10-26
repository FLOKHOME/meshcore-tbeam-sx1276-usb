# MeshCore USB-Companion für den klassischen LilyGO T-Beam (SX1276)

**Inoffizielles Community-Projekt • Windows/Linux • USB-Serial • Home Assistant**

[English README](README.md) · [Build-Anleitung](docs/BUILD.md) · [Flash-Anleitung](docs/FLASHING.md) · [HAOS/Proxmox](docs/HOME_ASSISTANT.md)

## Worum geht es?

Ein älterer **LilyGO/TTGO T-Beam mit ESP32 und SX1276** lässt sich als **MeshCore USB-Companion** betreiben. Damit kann er am PC oder über **Proxmox USB-Passthrough an Home Assistant OS** angebunden werden.

Für diese Hardware wurde mit MeshCore **v1.17.1** eine eigene `companion_radio_usb`-Konfiguration kompiliert und erfolgreich getestet. Die offizielle Firmware-Auswahl bot für den klassischen T-Beam SX1276 bei diesem Release nur die BLE-Companion-Variante. Dieses Projekt baut deshalb aus den **unveränderten offiziellen MeshCore-Quellen** eine USB-Variante.

**Erprobt:** T22_V1.1, SX1276, CP2104, OLED, USB-Serial, MeshCore v1.17.1, Home Assistant 3.0.2 unter HAOS/Proxmox. Andere Platinenrevisionen sind nicht automatisch bestätigt.

### Voraussetzungen

- Board mit **ESP32 + SX1276**; keine SX1262-, T-Beam-S3- oder T-Beam-1W-Version.
- USB-Datenkabel und passende Antenne.
- Git und Python 3.11 oder neuer.
- Windows PowerShell oder Linux/macOS-Terminal.

### 1. Firmware erstellen

ZIP herunterladen, entpacken und im Projektordner starten:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\build.ps1
```

Unter Linux/macOS:

```bash
./build.sh
```

Das Skript installiert PlatformIO nur bei Bedarf und holt MeshCore `companion-v1.17.1` in `.work/`. Der Originalcode wird nicht verändert: Die zusätzlichen Build-Optionen landen in der lokalen `platformio.local.ini`.

Die fertige Firmware liegt in `dist/`:

- `*_merged-0x0.bin`: vollständiges Image, empfohlen für eine Erstinstallation.
- `*_app-0x10000.bin`: nur die Anwendung; **nur bei kompatibler vorhandener Partitionstabelle**.

Das Skript flasht **nicht automatisch**. Es prüft Build-Erfolg und Datei-Existenz und erzeugt SHA-256-Prüfsummen.

### 2. Flashen

Alte Konfiguration/Schlüssel ggf. vorher sichern. Antenne anschließen, alle seriellen Programme schließen, Port ermitteln und `esptool` installieren:

```powershell
py -m pip install "esptool>=4.8,<5"
py -m esptool --chip esp32 --port COM8 --baud 115200 write_flash 0x0 "dist\TBeam_SX1276_USB_companion-v1.17.1_merged-0x0.bin"
```

`COM8` ist nur ein Beispiel! Bei Bedarf IO0/BOOT halten, RST kurz drücken, BOOT loslassen und Flashvorgang neu starten. Siehe [FLASHING.md](docs/FLASHING.md).

### 3. USB-Verbindung testen

```powershell
py -m pip install meshcore-cli
meshcli -s "COM8:dtr=1,rts=0,baud=115200" infos
```

**Der DTR/RTS-Zusatz war beim getesteten CP2104 unter Windows entscheidend.** Eine `PermissionError`-Meldung kann auch bedeuten, dass PuTTY oder ein anderes Programm COM8 belegt. Der Companion reagiert nicht wie ein Repeater auf normale Textbefehle.

### 4. Proxmox und Home Assistant

Auf dem Proxmox-Host:

```bash
lsusb
ls -l /dev/serial/by-id/
```

CP210x (`10c4:ea60`) auswählen und über **VM → Hardware → Hinzufügen → USB-Gerät** an HAOS durchreichen. In HAOS `/dev/ttyUSB0` beziehungsweise bevorzugt den stabilen By-ID-Pfad prüfen. Die [MeshCore-Integration](https://github.com/meshcore-dev/meshcore-ha) per HACS installieren und den T-Beam als USB/Serial Companion hinzufügen.

Die Gerätedaten sollten anschließend auf `Online` wechseln. Dann sind Empfang von MeshCore-Nachrichten und das Monitoring ausgewählter Repeater möglich.

### Hinweise

- **GPS ist optional**; ein Wert von `0.0,0.0` belegt keinen Hardwaredefekt. Für stationären Einsatz kann man Positionen manuell setzen.
- Das OLED kann in den Stromsparmodus gehen; bei der getesteten Platine weckt kurzes Drücken von **IO0** das Display.
- Firmware-Updates für andere Quellversionen müssen erneut getestet werden.
- Funkfrequenz und Sendeleistung müssen zu deinem MeshCore-Netz und zu den geltenden Vorschriften passen.
- **Keine** privaten MeshCore-Schlüssel oder Repeater-Passwörter in öffentlichen Issues veröffentlichen.

**Dieses Projekt ist unabhängig von MeshCore und LILYGO, keine offizielle Firmware.** Siehe [LICENSE](LICENSE) und [NOTICE.md](NOTICE.md).
