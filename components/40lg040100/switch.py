import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID, CONF_NAME

from . import (
    LG040100StatusComponent,
    lg040100_ns,
    CONF_LG040100_STATUS_COMPONENT_ID,
    CONF_DEACTIVATE,
)

LG040100StatusSwitch = lg040100_ns.class_("LG040100StatusSwitch", switch.Switch, cg.Component)
LG040100HeatPumpSwitch = lg040100_ns.class_("LG040100HeatPumpSwitch", LG040100StatusSwitch)
LG040100AdditionalHeatingSwitch = lg040100_ns.class_(
    "LG040100AdditionalHeatingSwitch", LG040100StatusSwitch
)
LG040100CoolingSwitch = lg040100_ns.class_("LG040100CoolingSwitch", LG040100StatusSwitch)

CONF_SWITCHES = "switches"
CONF_HEAT_PUMP = "heat_pump"
CONF_ADDITIONAL_HEATING = "additional_heating"
CONF_COOLING = "cooling"


def _switch_schema(class_, default_name: str, default_icon: str):
    return (
        switch.switch_schema(class_, icon=default_icon)
        .extend({cv.Optional(CONF_NAME, default=default_name): cv.string_strict})
        .extend({cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean})
        .extend(cv.COMPONENT_SCHEMA)
    )


CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_LG040100_STATUS_COMPONENT_ID): cv.use_id(
            LG040100StatusComponent
        ),
        cv.Optional(CONF_SWITCHES, default={}): cv.Schema(
            {
                cv.Optional(CONF_HEAT_PUMP, default={}): _switch_schema(
                    LG040100HeatPumpSwitch,
                    "Waermepumpe",
                    "mdi:heat-pump-outline",
                ),
                cv.Optional(CONF_ADDITIONAL_HEATING, default={}): _switch_schema(
                    LG040100AdditionalHeatingSwitch,
                    "Zusatzheizung",
                    "mdi:heat-wave",
                ),
                cv.Optional(CONF_COOLING, default={}): _switch_schema(
                    LG040100CoolingSwitch,
                    "Kuehlung",
                    "mdi:snowflake",
                ),
            }
        ),
    }
)


async def to_code(config):
    status_comp = await cg.get_variable(config[CONF_LG040100_STATUS_COMPONENT_ID])
    switches_conf = config.get(CONF_SWITCHES, {})

    async def build(key, class_):
        conf = switches_conf.get(key, {})
        if conf.get(CONF_DEACTIVATE):
            return
        var = await switch.new_switch(conf)
        await cg.register_component(var, conf)
        cg.add(var.set_status_component(status_comp))

    await build(CONF_HEAT_PUMP, LG040100HeatPumpSwitch)
    await build(CONF_ADDITIONAL_HEATING, LG040100AdditionalHeatingSwitch)
    await build(CONF_COOLING, LG040100CoolingSwitch)
