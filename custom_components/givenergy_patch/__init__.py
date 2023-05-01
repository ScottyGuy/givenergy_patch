"""The Givenergy Patch integration."""
from __future__ import annotations

import logging
import os
from os import listdir
from os.path import isdir, join
import subprocess
import sys

import homeassistant.components.givenergy_patch as givenergy_patch
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.start import async_at_start

_LOGGER = logging.getLogger(__name__)
PATCH_FILE = os.path.dirname(os.path.realpath(__file__)) + "/givenergy_modbus.patch"
CWD = os.path.dirname(os.path.realpath(givenergy_patch.__file__))
GIT_APPLY_CMD = "git apply"
MODULE_NAME = "givenergy_modbus"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Givenergy Patch from a config entry."""

    modpath = find_module()
    if modpath == None:
        _LOGGER.error(f"Cannot find {MODULE_NAME}")
        return False
    
    _LOGGER.info(f"Found module at path {modpath}")
    os.chdir(modpath)

    if run_command(f"{GIT_APPLY_CMD} --reverse --check {PATCH_FILE}", should_log_error=False):
        _LOGGER.info("Already patched, enjoy :)")
        return True

    _LOGGER.info("Applying patch")
    if run_command(f"{GIT_APPLY_CMD} -- {PATCH_FILE}"):
        _LOGGER.warning("Patched, enjoy :)")
        _LOGGER.warning("Restart Home Assistant to use the patch")
        return True

    _LOGGER.error("Failed to apply patch :(")
    return False



async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Reversing patch")
    if run_command(f"{GIT_APPLY_CMD} --reverse {PATCH_FILE}"):
        _LOGGER.info("Reversed patch")
    else:
        _LOGGER.warning("Failed to reverse patch")
    return True


def find_module() -> str:
    for libpath in sys.path:
        if "/" not in libpath:
            continue
        if not isdir(libpath):
            continue
        for f in listdir(libpath):
            fullpath = join(libpath, f)
            if f == MODULE_NAME and isdir(fullpath):
                return(fullpath)
    return(None)


def run_command(cmd: str, should_log_error: bool = True) -> bool:
    """Call subprocess.run. Returns true iff successful."""
    _LOGGER.debug("Running: %s", cmd)
    ret = subprocess.run(cmd, shell=True, capture_output=True, check=False, cwd=CWD)
    if ret.returncode and should_log_error:
        _LOGGER.error(
            "Error running command: %s - stderr:%s, stdout:%s",
            cmd,
            ret.stderr,
            ret.stdout,
        )
    return not ret.returncode
