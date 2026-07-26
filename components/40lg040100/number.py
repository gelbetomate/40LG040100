import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import (
    CONF_ID,
    CONF_NAME,
    CONF_MIN_VALUE,
    CONF_MAX_VALUE,
    CONF_STEP,
    CONF_ENTITY_CATEGORY,
    ENTITY_CATEGORY_CONFIG,
)

from . import LG040100, lg040100_ns, CONF_LG040100_ID, CONF_DEACTIVATE

LG040100VentSpeedNumber = lg040100_ns.class_(
    "LG040100VentSpeedNumber", number.Number, cg.Component
)

CONF_NUMBERS = "numbers"
CONF_VENT_LEVEL_1_SPEED = "vent_level_1_speed"
CONF_VENT_LEVEL_2_SPEED = "vent_level_2_speed"
CONF_VENT_LEVEL_3_SPEED = "vent_level_3_speed"
CONF_SUPPLY_AIR_SETPOINT = "supply_air_setpoint"
CONF_SUPPLY_AIR_TARGET = "supply_air_target"
CONF_ROOM_TARGET = "room_target"
CONF_SUPPLY_FAN_TRIM = "supply_fan_trim"
CONF_EXHAUST_FAN_TRIM = "exhaust_fan_trim"
CONF_EWT_PRESENT = "ewt_present"
CONF_ADDITIONAL_HEATING_RELEASE = "additional_heating_release"
CONF_ADDITIONAL_HEATING_ENABLE = "additional_heating_enable"
CONF_HEAT_PUMP_RELEASE = "heat_pump_release"
CONF_DEFROST_ON_TEMP = "defrost_on_temp"
CONF_DEFROST_OFF_TEMP = "defrost_off_temp"
CONF_DEFROST_SUPPLY = "defrost_supply"
CONF_DEFROST_EXHAUST = "defrost_exhaust"
CONF_FROST_OFF_TEMP = "frost_off_temp"
CONF_FROST_ON_TEMP = "frost_on_temp"
CONF_DEFROST_PAUSE = "defrost_pause"
CONF_DEFROST_RUNON = "defrost_runon"
CONF_EWT_SUMMER_STOP = "ewt_summer_stop"
CONF_EWT_SUMMER = "ewt_summer"
CONF_EWT_WINTER = "ewt_winter"
CONF_BRINE_PUMP_ON = "brine_pump_on"
CONF_BRINE_PUMP_OFF = "brine_pump_off"
CONF_SPEED_LIMIT = "speed_limit"
CONF_MAX_CONDENSATION_TEMP = "max_condensation_temp"
CONF_PRESSURE_EQUALIZATION_PAUSE = "pressure_equalization_pause"
CONF_DELTA_N1 = "delta_n1"
CONF_DELTA_N2 = "delta_n2"
CONF_DELTA_N3 = "delta_n3"
CONF_EWT_BOOST_STAGE_1 = "ewt_boost_stage_1"
CONF_EWT_BOOST_STAGE_2 = "ewt_boost_stage_2"
CONF_EWT_BOOST_STAGE_3 = "ewt_boost_stage_3"
CONF_AIR_REDUCTION_TEMP = "air_reduction_temp"
CONF_WATER_SETPOINT = "water_setpoint"

REGISTER_NUMBER_DEFINITIONS = {
    CONF_EWT_PRESENT: ("Erdwaermetauscher vorhanden (EC)", "EC", "state", "mdi:check-decagram", 0, 1, 1),
    CONF_ADDITIONAL_HEATING_RELEASE: ("Zusatzheizung frei (ZH)", "ZH", "state", "mdi:radiator", 0, 1, 1),
    CONF_ADDITIONAL_HEATING_ENABLE: ("Zusatzheizung ein (ZE)", "ZE", "state", "mdi:radiator-disabled", 0, 1, 1),
    CONF_HEAT_PUMP_RELEASE: ("Waermepumpe frei (WP)", "WP", "state", "mdi:heat-pump", 0, 1, 1),
    CONF_DEFROST_ON_TEMP: ("Abtau ein Temperatur (AE)", "AE", "°C", "mdi:snowflake-melt", -30, 30, 1),
    CONF_DEFROST_OFF_TEMP: ("Abtau aus Temperatur (AA)", "AA", "°C", "mdi:snowflake-off", -30, 30, 1),
    CONF_DEFROST_SUPPLY: ("Abtau Zuluft (Az)", "Az", "°C", "mdi:thermometer-chevron-up", -30, 30, 1),
    CONF_DEFROST_EXHAUST: ("Abtauluft (Aa)", "Aa", "°C", "mdi:thermometer-chevron-down", -30, 30, 1),
    CONF_FROST_OFF_TEMP: ("Frost aus (AR)", "AR", "°C", "mdi:snowflake-off", -30, 30, 1),
    CONF_FROST_ON_TEMP: ("Frost an (AZ)", "AZ", "°C", "mdi:snowflake", -30, 30, 1),
    CONF_DEFROST_PAUSE: ("Abtaupause (AP)", "AP", "min", "mdi:timer-pause", 0, 240, 1),
    CONF_DEFROST_RUNON: ("Abtaunachlauf (AN)", "AN", "min", "mdi:timer-play", 0, 240, 1),
    CONF_EWT_SUMMER_STOP: ("Schaltpunkt Sommer-Stopp (Es)", "Es", "°C", "mdi:sun-thermometer", -20, 40, 1),
    CONF_EWT_SUMMER: ("Schaltpunkt EWT Sommer (ES)", "ES", "°C", "mdi:thermometer-high", -20, 40, 1),
    CONF_EWT_WINTER: ("Schaltpunkt EWT Winter (EW)", "EW", "°C", "mdi:thermometer-low", -30, 20, 1),
    CONF_BRINE_PUMP_ON: ("Schaltpunkt Solepumpe Ein (EE)", "EE", "°C", "mdi:pump", -20, 40, 1),
    CONF_BRINE_PUMP_OFF: ("Schaltpunkt Solepumpe Aus (EA)", "EA", "°C", "mdi:pump-off", -20, 40, 1),
    CONF_SPEED_LIMIT: ("Grenzdrehzahl (NM)", "NM", "%", "mdi:speedometer", 0, 100, 1),
    CONF_MAX_CONDENSATION_TEMP: ("Max. Kondensationstemp. (KM)", "KM", "°C", "mdi:thermometer-alert", 0, 90, 1),
    CONF_PRESSURE_EQUALIZATION_PAUSE: ("Pausezeit Druckabbau (PA)", "PA", "s", "mdi:timer-sand", 0, 300, 1),
    CONF_DELTA_N1: ("Delta n1 max (D1)", "D1", "%", "mdi:fan", 0, 100, 1),
    CONF_DELTA_N2: ("Delta n2 max (D2)", "D2", "%", "mdi:fan", 0, 100, 1),
    CONF_DELTA_N3: ("Delta n3 max (D3)", "D3", "%", "mdi:fan", 0, 100, 1),
    CONF_EWT_BOOST_STAGE_1: ("EWT Boost Stufe 1 (E1)", "E1", "%", "mdi:fan-plus", 0, 40, 1),
    CONF_EWT_BOOST_STAGE_2: ("EWT Boost Stufe 2 (E2)", "E2", "%", "mdi:fan-plus", 0, 40, 1),
    CONF_EWT_BOOST_STAGE_3: ("EWT Boost Stufe 3 (E3)", "E3", "%", "mdi:fan-plus", 0, 40, 1),
    CONF_AIR_REDUCTION_TEMP: ("Luftreduktion Temp. (LR)", "LR", "°C", "mdi:thermometer-minus", -20, 10, 1),
    CONF_WATER_SETPOINT: ("Warmwasser Sollwert (WS)", "WS", "°C", "mdi:water-thermometer", 20, 70, 1),
}


def _speed_schema(default_name: str):
    return (
        number.number_schema(
            LG040100VentSpeedNumber,
            unit_of_measurement="%",
            icon="mdi:fan",
        )
        .extend(
            {
                cv.Optional(CONF_NAME, default=default_name): cv.string_strict,
                cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,
                cv.Optional(CONF_MIN_VALUE, default=40): cv.int_,
                cv.Optional(CONF_MAX_VALUE, default=100): cv.int_,
                cv.Optional(CONF_STEP, default=1): cv.int_,
                cv.Optional(CONF_ENTITY_CATEGORY, default=ENTITY_CATEGORY_CONFIG): cv.entity_category,
            }
        )
        .extend(cv.COMPONENT_SCHEMA)
    )


def _register_number_schema(default_name: str, default_unit: str, default_icon: str, default_min: int, default_max: int, default_step: int = 1):
    return (
        number.number_schema(
            LG040100VentSpeedNumber,
            unit_of_measurement=default_unit,
            icon=default_icon,
        )
        .extend(
            {
                cv.Optional(CONF_NAME, default=default_name): cv.string_strict,
                cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,
                cv.Optional(CONF_MIN_VALUE, default=default_min): cv.int_,
                cv.Optional(CONF_MAX_VALUE, default=default_max): cv.int_,
                cv.Optional(CONF_STEP, default=default_step): cv.int_,
                cv.Optional(CONF_ENTITY_CATEGORY, default=ENTITY_CATEGORY_CONFIG): cv.entity_category,
            }
        )
        .extend(cv.COMPONENT_SCHEMA)
    )


CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_LG040100_ID): cv.use_id(LG040100),
        cv.Optional(CONF_NUMBERS, default={}): cv.Schema(
            {
                cv.Optional(CONF_VENT_LEVEL_1_SPEED, default={}): _speed_schema(
                    "Luftstufe 1 Geschwindigkeit"
                ),
                cv.Optional(CONF_VENT_LEVEL_2_SPEED, default={}): _speed_schema(
                    "Luftstufe 2 Geschwindigkeit"
                ),
                cv.Optional(CONF_VENT_LEVEL_3_SPEED, default={}): _speed_schema(
                    "Luftstufe 3 Geschwindigkeit"
                ),
                cv.Optional(CONF_SUPPLY_AIR_SETPOINT, default={}): _register_number_schema(
                    "Zuluftsolltemperatur (SP)", "°C", "mdi:thermometer", 10, 35
                ),
                cv.Optional(CONF_SUPPLY_AIR_TARGET, default={}): _register_number_schema(
                    "Zulufttemperatur Sollwert (Re)", "°C", "mdi:thermometer-lines", 10, 35
                ),
                cv.Optional(CONF_ROOM_TARGET, default={}): _register_number_schema(
                    "Raumsollwert (Rd)", "°C", "mdi:home-thermometer", 10, 30
                ),
                cv.Optional(CONF_SUPPLY_FAN_TRIM, default={}): _register_number_schema(
                    "Zuluft +/- (LD)", "%", "mdi:fan-plus", -40, 40
                ),
                cv.Optional(CONF_EXHAUST_FAN_TRIM, default={}): _register_number_schema(
                    "Abluft +/- (Ld)", "%", "mdi:fan-minus", -40, 40
                ),
                **{
                    cv.Optional(key, default={}): _register_number_schema(
                        definition[0],
                        definition[2],
                        definition[3],
                        definition[4],
                        definition[5],
                        definition[6],
                    )
                    for key, definition in REGISTER_NUMBER_DEFINITIONS.items()
                },
            }
        ),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_LG040100_ID])
    numbers_conf = config.get(CONF_NUMBERS, {})

    async def build(key: str, level: int):
        conf = numbers_conf.get(key)
        if conf is None or conf.get(CONF_DEACTIVATE):
            return
        var = cg.new_Pvariable(conf[CONF_ID], parent, level)
        await cg.register_component(var, conf)
        await number.register_number(
            var,
            conf,
            min_value=conf.get(CONF_MIN_VALUE, 40),
            max_value=conf.get(CONF_MAX_VALUE, 100),
            step=conf.get(CONF_STEP, 1),
        )

    async def build_register(key: str, command: str, fallback_min: int, fallback_max: int, fallback_step: int = 1):
        conf = numbers_conf.get(key)
        if conf is None or conf.get(CONF_DEACTIVATE):
            return
        var = cg.new_Pvariable(conf[CONF_ID], parent, command)
        await cg.register_component(var, conf)
        await number.register_number(
            var,
            conf,
            min_value=conf.get(CONF_MIN_VALUE, fallback_min),
            max_value=conf.get(CONF_MAX_VALUE, fallback_max),
            step=conf.get(CONF_STEP, fallback_step),
        )

    await build(CONF_VENT_LEVEL_1_SPEED, 1)
    await build(CONF_VENT_LEVEL_2_SPEED, 2)
    await build(CONF_VENT_LEVEL_3_SPEED, 3)
    await build_register(CONF_SUPPLY_AIR_SETPOINT, "SP", 10, 35)
    await build_register(CONF_SUPPLY_AIR_TARGET, "Re", 10, 35)
    await build_register(CONF_ROOM_TARGET, "Rd", 10, 30)
    await build_register(CONF_SUPPLY_FAN_TRIM, "LD", -40, 40)
    await build_register(CONF_EXHAUST_FAN_TRIM, "Ld", -40, 40)
    for key, definition in REGISTER_NUMBER_DEFINITIONS.items():
        await build_register(key, definition[1], definition[4], definition[5], definition[6])
