import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from esphome.const import (
    CONF_NAME,
    CONF_UPDATE_INTERVAL,
)

from . import LG040100, CONF_LG040100_ID, CONF_DEACTIVATE
from .sensor import (
    CONF_COMMAND,
    CONF_SENSOR_POLLING_COMPONENT_ID,
    validate_custom_command,
    LG040100SensorPollingComponent,
)

CONF_TEXT_SENSORS_CUSTOM = "text_sensors_custom"
CONF_REFERENCE_PROFILE = "reference_profile"

REFERENCE_PROFILE_TEXT_SENSORS_CUSTOM = {
    "lg150": [
        {CONF_COMMAND: "ER", CONF_NAME: "Error Register Raw"},
        {CONF_COMMAND: "ST", CONF_NAME: "Status Register Raw"},
        {CONF_COMMAND: "MD", CONF_NAME: "Mode Register Raw"},
        {CONF_COMMAND: "SW", CONF_NAME: "Status Write Register Raw"},
        {CONF_COMMAND: "RL", CONF_NAME: "Relais Register Raw"},
    ],
    "lg250": [
        {CONF_COMMAND: "ER", CONF_NAME: "LG250 ER Fehler Register Roh"},
        {CONF_COMMAND: "LS", CONF_NAME: "LG250 LS Aktuelle Lueftungsstufe", CONF_UPDATE_INTERVAL: "30s"},
    ],
    "lg350": [
        {CONF_COMMAND: "ER", CONF_NAME: "Error Register Raw"},
        {CONF_COMMAND: "ST", CONF_NAME: "Status Register Raw"},
        {CONF_COMMAND: "MD", CONF_NAME: "Mode Register Raw"},
        {CONF_COMMAND: "SW", CONF_NAME: "Status Write Register Raw"},
        {CONF_COMMAND: "RL", CONF_NAME: "Relais Register Raw"},
    ],
}


def _text_sensor_schema(default_name: str = "Register Value"):
    return (
        text_sensor.text_sensor_schema()
        .extend(
            {
                cv.GenerateID(CONF_SENSOR_POLLING_COMPONENT_ID): cv.declare_id(
                    LG040100SensorPollingComponent
                ),
                cv.Required(CONF_COMMAND): cv.All(cv.string, validate_custom_command),
                cv.Optional(CONF_NAME, default=default_name): cv.string_strict,
                cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,
            }
        )
        .extend(cv.polling_component_schema("60s"))
    )


def _apply_reference_profile(config):
    profile = config.get(CONF_REFERENCE_PROFILE, "none")
    if profile == "none":
        return config

    profile_entries = REFERENCE_PROFILE_TEXT_SENSORS_CUSTOM.get(profile, [])
    existing_commands = set(
        item.get(CONF_COMMAND, "") for item in config.get(CONF_TEXT_SENSORS_CUSTOM, [])
    )

    merged = list(config.get(CONF_TEXT_SENSORS_CUSTOM, []))
    for entry in profile_entries:
        command = entry[CONF_COMMAND]
        if command in existing_commands:
            continue
        merged.append(_text_sensor_schema()(dict(entry)))

    config[CONF_TEXT_SENSORS_CUSTOM] = merged
    return config


CONFIG_SCHEMA = cv.All(cv.Schema(
    {
        cv.GenerateID(CONF_LG040100_ID): cv.use_id(LG040100),
        cv.Optional(CONF_REFERENCE_PROFILE, default="none"): cv.one_of("none", "lg150", "lg250", "lg350", lower=True),
        cv.Optional(CONF_TEXT_SENSORS_CUSTOM, default=[]): cv.ensure_list(
            _text_sensor_schema()
        ),
    }
).extend(cv.COMPONENT_SCHEMA), _apply_reference_profile)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_LG040100_ID])

    for sensor_config in config.get(CONF_TEXT_SENSORS_CUSTOM, []):
        if sensor_config.get(CONF_DEACTIVATE, False):
            continue

        command = sensor_config[CONF_COMMAND]
        txt = await text_sensor.new_text_sensor(sensor_config)

        var = cg.new_Pvariable(
            sensor_config[CONF_SENSOR_POLLING_COMPONENT_ID],
            parent,
            sensor_config[CONF_UPDATE_INTERVAL],
            txt,
            command,
        )
        await cg.register_component(var, sensor_config)
