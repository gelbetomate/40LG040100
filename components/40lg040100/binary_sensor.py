import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_DEVICE_CLASS,
    CONF_ENTITY_CATEGORY,
    CONF_NAME,
    ENTITY_CATEGORY_DIAGNOSTIC,
)

# LG040100 Namespace holen (bereits in __init__.py definiert)
from . import (
    CONF_DEACTIVATE,
    CONF_LG040100_RELAIS_COMPONENT_ID,
    lg040100_ns,
)

LG040100RelaisComponent = lg040100_ns.class_("LG040100RelaisComponent", cg.PollingComponent)

CONF_RELAIS_SENSORS = "relais_sensors"
CONF_REFERENCE_PROFILE = "reference_profile"

# Definition of relay options as tuple (name, bit flag)
RELAIS_OPTIONS = {
    "kompressor": ("Kompressor", 1),
    "zusatzheizung": ("Zusatzheizung", 2),
    "erdwaermetauscher": ("Erdwaermetauscher", 4),
    "bypass": ("Bypass", 8),
    "vorheizregister": ("Vorheizregister", 16),
    "netzrelais_bypass": ("Netzrelais Bypass", 32),
    "bedienteil_aktiv": ("Bedienteil aktiv", 64),
    "bedienung_via_rs": (
        "Bedienung via RS-Schnittstelle",
        128,
    ),
    "luftstufe_vorhanden": ("Luftstufe Vorhanden", 256),
    "ww_nachheizregister": (
        "Warmwasser Nachheizregister",
        512,
    ),
    "magnetventil": ("Magnetventil", 2048),
    "vorheizen_aktiv": ("Vorheizen aktiv", 4096),
}

REFERENCE_PROFILE_RELAIS_SENSORS = {
    "lg150": {
        "kompressor": {CONF_NAME: "LG150 Kompressor"},
        "bypass": {CONF_NAME: "LG150 Bypass"},
        "bedienteil_aktiv": {CONF_NAME: "LG150 Bedienteil aktiv"},
        "bedienung_via_rs": {CONF_NAME: "LG150 Bedienung via RS"},
    },
    "lg250": {
        "kompressor": {CONF_NAME: "LG250 Kompressor"},
        "bypass": {CONF_NAME: "LG250 Bypass"},
        "vorheizregister": {CONF_NAME: "LG250 Vorheizregister"},
        "bedienteil_aktiv": {CONF_NAME: "LG250 Bedienteil aktiv"},
        "bedienung_via_rs": {CONF_NAME: "LG250 Bedienung via RS"},
        "ww_nachheizregister": {CONF_NAME: "LG250 Warmwasser Nachheizregister"},
        "magnetventil": {CONF_NAME: "LG250 Magnetventil"},
    },
    "lg350": {
        "kompressor": {CONF_NAME: "LG350 Kompressor"},
        "bypass": {CONF_NAME: "LG350 Bypass"},
        "bedienteil_aktiv": {CONF_NAME: "LG350 Bedienteil aktiv"},
        "bedienung_via_rs": {CONF_NAME: "LG350 Bedienung via RS"},
    },
}


def _binary_sensor_schema(default_name: str):
    return binary_sensor.binary_sensor_schema().extend(
        {
            cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,
            cv.Optional(CONF_NAME, default=default_name): cv._validate_entity_name,
        }
    )


def _apply_reference_profile(config):
    profile = config.get(CONF_REFERENCE_PROFILE, "none")
    if profile == "none":
        return config

    profile_entries = REFERENCE_PROFILE_RELAIS_SENSORS.get(profile, {})
    merged = dict(config.get(CONF_RELAIS_SENSORS, {}))

    for key, entry in profile_entries.items():
        if key in merged:
            continue
        merged[key] = _binary_sensor_schema(RELAIS_OPTIONS[key][0])(dict(entry))

    config[CONF_RELAIS_SENSORS] = merged
    return config

# Main schema for this component
CONFIG_SCHEMA = cv.All(cv.Schema(
    {
        cv.GenerateID(CONF_LG040100_RELAIS_COMPONENT_ID): cv.use_id(LG040100RelaisComponent),
        cv.Optional(CONF_REFERENCE_PROFILE, default="none"): cv.one_of("none", "lg150", "lg250", "lg350", lower=True),
        cv.Optional(CONF_RELAIS_SENSORS, default={}): cv.Schema(
            {
                cv.Optional(k): _binary_sensor_schema(RELAIS_OPTIONS[k][0])
                for k in RELAIS_OPTIONS.keys()
            }
        ),
    }
).extend(cv.COMPONENT_SCHEMA), _apply_reference_profile)


# Code-Generierung
async def to_code(config):
    # LG040100RelaisComponent abrufen
    var = await cg.get_variable(config[CONF_LG040100_RELAIS_COMPONENT_ID])

    relais_sensors = config.get(CONF_RELAIS_SENSORS, {})

    # Alle Relais aus RELAIS_OPTIONS durchgehen
    for key, (default_name, bit_flag) in RELAIS_OPTIONS.items():
        sensor_config = relais_sensors.get(key)

        if sensor_config is None:
            continue

        # Falls `skip: true`, den Sensor nicht erstellen
        if sensor_config.get(CONF_DEACTIVATE, False):
            continue
        # Falls keine `entity_category:` existiert, Standardwert setzen
        sensor_config.setdefault(CONF_ENTITY_CATEGORY, cv.entity_category(ENTITY_CATEGORY_DIAGNOSTIC))

        sensor = await binary_sensor.new_binary_sensor(sensor_config)

        cg.add(var.register_relais_sensor(bit_flag, sensor))
