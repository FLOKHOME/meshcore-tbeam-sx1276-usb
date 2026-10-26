"""Unit tests for overlay generation and defensive checks (network-free)."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build import OVERLAY, safe_ref, validate_upstream, write_overlay, ENVIRONMENT


class TestBuild(unittest.TestCase):
    def test_tags_restricted(self):
        self.assertEqual(safe_ref("companion-v1.17.1"), "companion-v1.17.1")
        for value in ("--upload", "../main", "a/b", "foo bar", "foo;rm", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_ref(value)

    def test_overlay_uses_environment_inheritance(self):
        self.assertIn("extends = env:Tbeam_SX1276_companion_radio_ble", OVERLAY)
        self.assertIn("-D ENABLE_USB_INTERFACE", OVERLAY)
        self.assertIn(f"[env:{ENVIRONMENT}]", OVERLAY)
        self.assertNotIn("-D BLE_PIN_CODE", OVERLAY)

    def test_overlay_does_not_overwrite_user_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            write_overlay(directory)
            self.assertEqual((directory / "platformio.local.ini").read_text(), OVERLAY)
            write_overlay(directory)  # idempotent
            (directory / "platformio.local.ini").write_text("[env:user]", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "Refusing to overwrite"):
                write_overlay(directory)

    def test_preflight_rejects_incompatible_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "variants/lilygo_tbeam_SX1276").mkdir(parents=True)
            (root / "examples/companion_radio").mkdir(parents=True)
            (root / "platformio.ini").write_text("extra_configs = variants/*/platformio.ini\n platformio.local.ini\n")
            (root / "variants/lilygo_tbeam_SX1276/platformio.ini").write_text("[env:Tbeam_SX1276_companion_radio_ble]\n")
            (root / "examples/companion_radio/main.cpp").write_text("#if defined(ENABLE_USB_INTERFACE)\n#endif\n")
            validate_upstream(root)
            (root / "examples/companion_radio/main.cpp").write_text("// changed")
            with self.assertRaisesRegex(RuntimeError, "ENABLE_USB_INTERFACE"):
                validate_upstream(root)


if __name__ == "__main__":
    unittest.main()
