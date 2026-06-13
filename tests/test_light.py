"""Tests for the Govee light entity."""

from types import SimpleNamespace

from homeassistant.components.light import ColorMode

from custom_components.govee.light import GoveeLightEntity


def _device(**overrides):
    data = {
        "support_color": False,
        "support_color_tem": False,
        "support_brightness": False,
        "device": "aa:bb:cc:dd",
        "device_name": "Test Light",
        "model": "H0000",
        "power_state": False,
        "source": None,
        "online": True,
        "color": (255, 255, 255),
        "brightness": 0,
        "color_temp": 4000,
    }
    data.update(overrides)
    return SimpleNamespace(**data)


def test_color_mode_for_rgb_light():
    """RGB-capable devices should expose HS as current mode."""
    entity = GoveeLightEntity(None, "govee", None, _device(support_color=True))

    assert entity.supported_color_modes == {ColorMode.HS}
    assert entity.color_mode == ColorMode.HS


def test_color_mode_for_color_temp_light():
    """CT-only devices should expose color temperature mode."""
    entity = GoveeLightEntity(None, "govee", None, _device(support_color_tem=True))

    assert entity.supported_color_modes == {ColorMode.COLOR_TEMP}
    assert entity.color_mode == ColorMode.COLOR_TEMP


def test_color_mode_for_brightness_only_light():
    """Brightness-only devices should expose brightness mode."""
    entity = GoveeLightEntity(None, "govee", None, _device(support_brightness=True))

    assert entity.supported_color_modes == {ColorMode.BRIGHTNESS}
    assert entity.color_mode == ColorMode.BRIGHTNESS


def test_color_mode_for_switch_like_light():
    """On/off-only devices should expose on/off mode."""
    entity = GoveeLightEntity(None, "govee", None, _device())

    assert entity.supported_color_modes == {ColorMode.ONOFF}
    assert entity.color_mode == ColorMode.ONOFF
