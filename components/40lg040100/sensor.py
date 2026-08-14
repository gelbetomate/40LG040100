import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    UNIT_CELSIUS,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_FREQUENCY,
    STATE_CLASS_MEASUREMENT,
    CONF_DEVICE_CLASS,
    CONF_NAME,
    CONF_SENSORS,
    CONF_FRIENDLY_NAME,
    CONF_UPDATE_INTERVAL,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_ACCURACY_DECIMALS,
)

# LG040100 Namespace holen (bereits in __init__.py definiert)
from . import LG040100, CONF_LG040100_ID, CONF_DEACTIVATE, lg040100_ns

# Sensor polling component (for all sensors)
LG040100SensorPollingComponent = lg040100_ns.class_("LG040100SensorPollingComponent", cg.PollingComponent)

# Supported sensor commands and defaults
SENSOR_COMMANDS = {
    # Temperatur-Sensoren
    "T1": ("Aussenluft - Verdampfertemperatur", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE),
    "T2": ("Zulufttemperatur", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE),
    "T3": ("Ablufttemperatur", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE),
    "T4": ("Fortlufttemperatur", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE),
    "T5": ("Nach Waermetauscher (Fortluft)", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE),
    "T6": ("Zulufttemperatur", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE),
    "T7": ("Nach Solevorerwaermung", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE),
    "T8": ("Nach Vorheizregister", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE),
    # Drehzahl-Sensoren
    "NA": ("V2-M2 Abluftventilator Drehzahl", "rpm", DEVICE_CLASS_FREQUENCY),
    "NZ": ("V1-M1 Zuluftventilator Drehzahl", "rpm", DEVICE_CLASS_FREQUENCY),
    # Weitere Messwerte
    "UA": ("Steuerspannung Abluft", "V", None),
    "UZ": ("Steuerspannung Zuluft", "V", None),
    "RA": ("Rueckwaermzahl", "%", None),
}

CONF_COMMAND = "command"
CONF_SENSOR_POLLING_COMPONENT_ID = "polling_component_id"
CONF_SENSORS_CUSTOM = "sensors_custom"
CONF_REFERENCE_PROFILE = "reference_profile"

REFERENCE_PROFILE_SENSORS_CUSTOM = {
    "lg150": [
        {CONF_COMMAND: "LS", CONF_NAME: "Ventilation Level", CONF_UNIT_OF_MEASUREMENT: "level"},
        {CONF_COMMAND: "L1", CONF_NAME: "Vent Level 1 Setpoint", CONF_UNIT_OF_MEASUREMENT: "%"},
        {CONF_COMMAND: "L2", CONF_NAME: "Vent Level 2 Setpoint", CONF_UNIT_OF_MEASUREMENT: "%"},
        {CONF_COMMAND: "L3", CONF_NAME: "Vent Level 3 Setpoint", CONF_UNIT_OF_MEASUREMENT: "%"},
    ],
    "lg250": [
        {CONF_COMMAND: "T1", CONF_NAME: "LG250 T1 Fortlufttemperatur (Fortluft FO)", CONF_UNIT_OF_MEASUREMENT: UNIT_CELSIUS, CONF_ACCURACY_DECIMALS: 1, CONF_UPDATE_INTERVAL: "30s"},
        {CONF_COMMAND: "T2", CONF_NAME: "LG250 T2 Zulufttemperatur (Zuluft ZU)", CONF_UNIT_OF_MEASUREMENT: UNIT_CELSIUS, CONF_ACCURACY_DECIMALS: 1, CONF_UPDATE_INTERVAL: "30s"},
        {CONF_COMMAND: "T3", CONF_NAME: "LG250 T3 Ablufttemperatur", CONF_UNIT_OF_MEASUREMENT: UNIT_CELSIUS, CONF_ACCURACY_DECIMALS: 1, CONF_UPDATE_INTERVAL: "30s"},
        {CONF_COMMAND: "T4", CONF_NAME: "LG250 T4 Fortlufttemperatur", CONF_UNIT_OF_MEASUREMENT: UNIT_CELSIUS, CONF_ACCURACY_DECIMALS: 1, CONF_UPDATE_INTERVAL: "30s"},
        {CONF_COMMAND: "T5", CONF_NAME: "LG250 T5 Nach Waermetauscher", CONF_UNIT_OF_MEASUREMENT: UNIT_CELSIUS, CONF_ACCURACY_DECIMALS: 1, CONF_UPDATE_INTERVAL: "30s"},
        {CONF_COMMAND: "NA", CONF_NAME: "LG250 V2-M2 Abluftventilator Drehzahl", CONF_UNIT_OF_MEASUREMENT: "rpm", CONF_ACCURACY_DECIMALS: 0, CONF_UPDATE_INTERVAL: "30s"},
        {CONF_COMMAND: "NZ", CONF_NAME: "LG250 V1-M1 Zuluftventilator Drehzahl", CONF_UNIT_OF_MEASUREMENT: "rpm", CONF_ACCURACY_DECIMALS: 0, CONF_UPDATE_INTERVAL: "30s"},
        {CONF_COMMAND: "UA", CONF_NAME: "LG250 Steuerspannung Abluft", CONF_UNIT_OF_MEASUREMENT: "V", CONF_ACCURACY_DECIMALS: 1, CONF_UPDATE_INTERVAL: "60s"},
        {CONF_COMMAND: "UZ", CONF_NAME: "LG250 Steuerspannung Zuluft", CONF_UNIT_OF_MEASUREMENT: "V", CONF_ACCURACY_DECIMALS: 1, CONF_UPDATE_INTERVAL: "60s"},
        {CONF_COMMAND: "RA", CONF_NAME: "LG250 Rueckwaermzahl", CONF_UNIT_OF_MEASUREMENT: "%", CONF_ACCURACY_DECIMALS: 1, CONF_UPDATE_INTERVAL: "60s"},
        {CONF_COMMAND: "L1", CONF_NAME: "LG250 L1-S1 Sollwert Lueftungsstufe 1", CONF_UNIT_OF_MEASUREMENT: "%", CONF_ACCURACY_DECIMALS: 0, CONF_UPDATE_INTERVAL: "2min"},
        {CONF_COMMAND: "L2", CONF_NAME: "LG250 L2-S2 Sollwert Lueftungsstufe 2", CONF_UNIT_OF_MEASUREMENT: "%", CONF_ACCURACY_DECIMALS: 0, CONF_UPDATE_INTERVAL: "2min"},
        {CONF_COMMAND: "L3", CONF_NAME: "LG250 L3-S3 Sollwert Lueftungsstufe 3", CONF_UNIT_OF_MEASUREMENT: "%", CONF_ACCURACY_DECIMALS: 0, CONF_UPDATE_INTERVAL: "2min"},
    ],
    "lg350": [
        {CONF_COMMAND: "LS", CONF_NAME: "Ventilation Level", CONF_UNIT_OF_MEASUREMENT: "level"},
        {CONF_COMMAND: "L1", CONF_NAME: "Vent Level 1 Setpoint", CONF_UNIT_OF_MEASUREMENT: "%"},
        {CONF_COMMAND: "L2", CONF_NAME: "Vent Level 2 Setpoint", CONF_UNIT_OF_MEASUREMENT: "%"},
        {CONF_COMMAND: "L3", CONF_NAME: "Vent Level 3 Setpoint", CONF_UNIT_OF_MEASUREMENT: "%"},
    ],
}


def validate_custom_command(value):
    """Validiert, dass benutzerdefinierte Kommandos genau 2 Zeichen haben."""
    value = cv.string(value)
    if not (len(value) == 2 and value.isalnum()):
        raise cv.Invalid(f"Custom command '{value}' must be exactly two alphanumeric characters long.")
    return value


_CUSTOM_SENSOR_SCHEMA = (
    sensor.sensor_schema(state_class=STATE_CLASS_MEASUREMENT)
    .extend(
        {
            cv.GenerateID(CONF_SENSOR_POLLING_COMPONENT_ID): cv.declare_id(LG040100SensorPollingComponent),
            cv.Required(CONF_COMMAND): cv.All(cv.string, validate_custom_command),
            cv.Required(CONF_NAME): cv._validate_entity_name,
            cv.Optional(CONF_UNIT_OF_MEASUREMENT): sensor.validate_unit_of_measurement,
            cv.Optional(CONF_DEVICE_CLASS): sensor.validate_device_class,
        }
    )
    .extend(cv.polling_component_schema("60s"))
)


def _apply_reference_profile(config):
    profile = config.get(CONF_REFERENCE_PROFILE, "none")
    if profile == "none":
        return config

    profile_entries = REFERENCE_PROFILE_SENSORS_CUSTOM.get(profile, [])
    existing_commands = set(config.get(CONF_SENSORS, {}).keys())
    existing_commands.update(
        item.get(CONF_COMMAND, "") for item in config.get(CONF_SENSORS_CUSTOM, [])
    )

    merged_custom = list(config.get(CONF_SENSORS_CUSTOM, []))
    for entry in profile_entries:
        command = entry[CONF_COMMAND]
        if command in existing_commands:
            continue
        merged_custom.append(_CUSTOM_SENSOR_SCHEMA(dict(entry)))

    config[CONF_SENSORS_CUSTOM] = merged_custom
    return config


# **Definition der einzelnen Temperatur-Sensoren**
CONFIG_SCHEMA = cv.All(cv.Schema(
    {
        cv.GenerateID(CONF_LG040100_ID): cv.use_id(LG040100),
        cv.Optional(CONF_REFERENCE_PROFILE, default="none"): cv.one_of("none", "lg150", "lg250", "lg350", lower=True),
        # **Standard-Sensoren mit IntelliSense (NUR vordefinierte Werte)**
        cv.Optional(CONF_SENSORS, default={}): cv.Schema(
            {
                cv.Optional(k): sensor.sensor_schema()
                .extend(
                    {
                        cv.GenerateID(CONF_SENSOR_POLLING_COMPONENT_ID): cv.declare_id(LG040100SensorPollingComponent),
                        cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,  # Sensor deaktivieren
                        cv.Optional(CONF_NAME, default=SENSOR_COMMANDS[k][0]): cv._validate_entity_name,
                        cv.Optional(CONF_UNIT_OF_MEASUREMENT, default=SENSOR_COMMANDS[k][1]): sensor.validate_unit_of_measurement,
                        **(
                            {cv.Optional(CONF_DEVICE_CLASS, default=SENSOR_COMMANDS[k][2]): sensor.validate_device_class}
                            if SENSOR_COMMANDS[k][2] is not None
                            else {}
                        ),
                    }
                )
                .extend(cv.polling_component_schema("60s"))
                for k in SENSOR_COMMANDS.keys()
            }
        ),
        # **Custom sensors (must be exactly 2 characters + required fields)**
        cv.Optional(CONF_SENSORS_CUSTOM, default=[]): cv.ensure_list(
            _CUSTOM_SENSOR_SCHEMA,
        ),
    }
).extend(cv.COMPONENT_SCHEMA), _apply_reference_profile)


async def generate_sensor_code(parent, sensor_config):
    """Generate code for one sensor."""

    command = sensor_config[CONF_COMMAND]
    sensor_config.setdefault(CONF_ACCURACY_DECIMALS, 1)

    sens = await sensor.new_sensor(sensor_config)

    var = cg.new_Pvariable(
        sensor_config[CONF_SENSOR_POLLING_COMPONENT_ID],
        parent,
        sensor_config[CONF_UPDATE_INTERVAL],
        sens,
        command,
    )

    await cg.register_component(var, sensor_config)


async def to_code(config):
    """ESPHome code generation for LG040100 sensors."""

    # LG040100 Hauptkomponente abrufen
    parent = await cg.get_variable(config[CONF_LG040100_ID])

    # Standard-Sensoren (Dictionary: {command: sensor_config})
    for command, sensor_config in config.get(CONF_SENSORS, {}).items():
        if sensor_config.get(CONF_DEACTIVATE, False):
            continue  # Sensor nicht erstellen, wenn deaktiviert

        sensor_config[CONF_COMMAND] = command
        sensor_config.setdefault(CONF_ACCURACY_DECIMALS, 1)

        await generate_sensor_code(parent, sensor_config)

    # Benutzerdefinierte Sensoren durchgehen
    for sensor_config in config.get(CONF_SENSORS_CUSTOM, []):
        await generate_sensor_code(parent, sensor_config)
