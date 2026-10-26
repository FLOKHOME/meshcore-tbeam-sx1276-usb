# Home Assistant OS / Proxmox integration

This guide uses the T-Beam as a **USB/Serial Companion**, not a radio repeater. Home Assistant needs the [MeshCore integration](https://github.com/meshcore-dev/meshcore-ha).

## A. Proxmox host

Connect the T-Beam to the Proxmox host and identify it:

```bash
lsusb
ls -l /dev/serial/by-id/
```

The tested device appeared as `10c4:ea60 Silicon Labs CP210x` (CP2104) and a `/dev/serial/by-id/...` symlink. In **Proxmox → HAOS VM → Hardware → Add → USB Device**, select the corresponding CP210x device. If needed, completely power down and start the HAOS VM.

## B. Home Assistant OS

1. In HAOS, open **Settings → System → Hardware → All hardware** and locate `ttyUSB0` or `/dev/serial/by-id/...`.
2. Install the community **MeshCore integration** using HACS and restart HA if asked.
3. Go to **Settings → Devices & services → Add integration → MeshCore**.
4. Select **USB / Serial**, the serial path and `115200` baud if offered.
5. Check that the Companion's `Node Status` displays `Online` and radio frequency is as expected.

The integration did connect to the tested USB firmware running MeshCore v1.17.1 without custom changes to HAOS. If your integration cannot communicate, review the DTR/RTS caveats in the troubleshooting guide.

## C. Optional repeater monitoring

Configure your own repeater under the MeshCore integration options using **Add Repeater Station**, its authorized access credentials, and an appropriate telemetry interval (e.g. 1800–7200 seconds). Enabling neighbor telemetry may add considerable network overhead. Monitor only nodes you own or have permission to query.

Example entities, depending on integration version: Battery Voltage, Battery Percentage, Last RSSI/SNR, RX/TX Airtime, Uptime, Neighbor Count, Receive Errors, messages per minute.

Do not store passwords or MeshCore private keys in public dashboards or repository files. Avoid repeatedly polling a busy community mesh.

## D. What it is *not*

This is **not** an official Home Assistant add-on, and it does not make the ESP32 a USB-to-LoRaWAN adapter. It is a MeshCore Companion used by the Home Assistant integration.
