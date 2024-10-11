"""Platform for sensor integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import CONF_ADDRESS, CONF_NAME, UnitOfTemperature, PERCENTAGE
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType, StateType

from . import IQstove

stove = IQstove.IQstove("192.168.1.158")

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([temperatureSensor(), phaseSensor(), performanceSensor(), heatingUpSensor()])

class temperatureSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = f"stove{stove.serial}+{_attr_name}"

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        self._attr_native_value = stove.temperature

class phaseSensor(SensorEntity):
    _attr_name = "Phase"
    #_attr_state_class = SensorStateClass.MEASUREMENT
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["idle", "heating up", "burning", "add wood", "don't add wood"]
    _attr_unique_id = f"stove{stove.serial}+{_attr_name}"

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        phase = stove.phase
        self._attr_native_value = self._attr_options[int(phase)]
        if (int(phase) == 0):
            self._attr_icon = "mdi:fireplace-off"
        else:
            self._attr_icon = "mdi:fireplace"


class performanceSensor(SensorEntity):
    """Performance Sensor."""

    _attr_name = "Performance"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = f"stove{stove.serial}+{_attr_name}"
    _attr_icon = "mdi:gauge"

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        self._attr_native_value = stove.performance

class heatingUpSensor(SensorEntity):
    """Performance Sensor."""

    _attr_name = "Heating Up"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_unique_id = f"stove{stove.serial}+{_attr_name}"
    _attr_icon = "mdi:elevation-rise"

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        self._attr_native_value = stove.heatingPercentage

