# Troubleshooting

## The serial port opens but MeshCore CLI reports no response

- Close PuTTY, serial monitor browser tabs, and any other client using the serial device.
- The Companion uses a **binary protocol**. `ver`, `help`, and other raw text commands are not a reliable firmware test.
- On the tested CP2104 T-Beam / Windows, this succeeded:

  ```text
  meshcli -s COM8:dtr=1,rts=0,baud=115200 infos
  ```

- Try the device's actual port, not the example `COM8`.
- Be mindful that toggling DTR/RTS may cause an ESP32 reset.
- If a tool crashes before closing its serial handle, unplug/replug USB after closing the tool.

## `PermissionError(13, 'Access is denied')`

Another program may have the COM port open, or a CLI may have attempted to reopen the same port while switching DTR. Close the serial terminal and browser serial windows; check that the current port number did not change after reconnection.

## Display goes blank

The OLED can turn off for power saving. On the tested board, short **IO0** press wakes it. This does not necessarily indicate a crash. **RST** reboots the ESP32; **PWR** controls board power.

## GPS stays at 0.0, 0.0

GPS is optional. Indoors, a NEO-6M can fail to achieve a fix. Also, the Companion may not expose live GNSS status. Do not interpret a zero stored coordinate as evidence of a failed radio. Use a manual static location if appropriate.

## Device visible in Proxmox but not Home Assistant

Check Proxmox USB passthrough, VM power cycle, and HAOS hardware list. Prefer `/dev/serial/by-id/...` for a stable name if available.

## Firmware compiles but fails to communicate

A successful build only proves source compatibility. Confirm that you built the **USB profile**, used an **SX1276** board and the correct `merged` vs `app` flash address. Use the hardware-tested default upstream tag first. If problems persist, capture the build log, board marking, radio module identification, and serial output *without exposing secrets*.

## Security and regulatory notes

Do not publicly post your public/home coordinates if privacy matters; never publish private keys or repeater passwords. Use the applicable radio preset and comply with local radio rules. Do not transmit without an antenna.
