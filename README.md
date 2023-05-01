[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

# Givenergy Patch Custom integration for Home Assistant
This integration patches the [givenergy-modbus](https://github.com/dewet22/givenergy-modbus) library used by the [GivEnergy Local](https://github.com/cdpuk/givenergy-local/) HACS custom component to recognise Gen2 inverters that have the new "EA" serial number prefix that is not recognised by the 0.10.1 version of givenergy-modbus that is the latest release at time of writing.

This integration is very heavily derived from the [Google Assistant SDK Custom integration](https://github.com/tronikos/google_assistant_sdk_custom) by @tronikos

Note: After a Home Assistant update the patch will be reapplied automatically but Home Assistant needs to be restarted manually.

# Installation

## HACS
1. [Add](http://homeassistant.local:8123/hacs/integrations) custom integrations repository: https://github.com/ScottyGuy/givenergy_patch
2. Select "Givenergy Patch" in the Integration tab and click download
3. Restart Home Assistant
4. Enable the integration

## Manual
1. Copy directory `custom_components/Givenergy Patch` to your `<config dir>/custom_components` directory
2. Restart Home-Assistant
3. Enable the integration

## Enable the integration
1. Go to [Settings / Devices & Services / Integrations](http://homeassistant.local:8123/config/integrations). Click **+ ADD INTEGRATION**
2. Search for "Givenergy Patch" and click on it
3. Restart Home Assistant
