# Publishing the repository to GitHub

This ZIP is a complete Git repository **working tree**, not an already published GitHub URL. Use a new public repository, e.g. `meshcore-tbeam-sx1276-usb`.

## Option A: GitHub website

1. Open https://github.com/new and create an empty public repository named `meshcore-tbeam-sx1276-usb`. **Do not** add a README, license or `.gitignore` on GitHub (they are already in this ZIP).
2. Extract the ZIP to a local folder, open a terminal in the folder and run:

   ```bash
   git init
   git add .
   git commit -m "Initial community MeshCore USB build for classic T-Beam SX1276"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/meshcore-tbeam-sx1276-usb.git
   git push -u origin main
   ```

3. Replace `YOUR-USERNAME` with your own GitHub username. GitHub authentication is required.
4. Open the **Actions** tab and check the `Build T-Beam SX1276 USB` workflow. Its successful artifacts contain both `.bin` files and SHA-256 checksums.
5. Hardware-test the CI-generated firmware before making a public GitHub Release.

## Option B: GitHub CLI

After running `git init`, `git add .`, `git commit -m ...` as above:

```bash
gh auth login
gh repo create meshcore-tbeam-sx1276-usb --public --source=. --remote=origin --push
```

## Suggested GitHub About

> Community USB/Serial Companion firmware builder for the classic ESP32 LilyGO T-Beam SX1276 using upstream MeshCore. Windows, Linux, Proxmox and Home Assistant.

**Topics:** `meshcore`, `lilygo`, `t-beam`, `sx1276`, `esp32`, `lora`, `home-assistant`, `platformio`, `usb-serial`, `proxmox`

Do not commit `dist/`, `.work/`, private keys, admin credentials or user-specific Home Assistant configuration. Both directories are ignored by `.gitignore`.
