import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import select
from esphome.const import CONF_ID, CONF_OPTIONS, CONF_NAME

from . import (
    LG040100,
    LG040100StatusComponent,
    LG040100ModeComponent,
    lg040100_ns,
    CONF_LG040100_ID,
    CONF_LG040100_STATUS_COMPONENT_ID,
    CONF_LG040100_MODE_COMPONENT_ID,
    CONF_DEACTIVATE,
)

LG040100VentilationLevelSelect = lg040100_ns.class_(
    "LG040100VentilationLevelSelect", select.Select, cg.Component
)
LG040100ModeSelect = lg040100_ns.class_("LG040100ModeSelect", select.Select, cg.Component)

DEFAULT_VENTILATION_LEVEL_OPTIONS = ["AUS", "Luftstufe 1", "Luftstufe 2", "Luftstufe 3"]
DEFAULT_MODE_OPTIONS = [
    "AUS",
    "Sommerbetrieb",
    "Sommer-Abluftbetrieb",
    "Winterbetrieb",
    "Handbetrieb",
]

CONF_SELECTS = "selects"
CONF_VENTILATION_LEVEL = "ventilation_level"
CONF_OPERATION_MODE = "operation_mode"

VENTILATION_LEVEL_SCHEMA = (
    select.select_schema(LG040100VentilationLevelSelect, icon="mdi:fan")
    .extend(
        {
            cv.Optional(CONF_NAME, default="Lueftungsstufe"): cv.string_strict,
            cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,
            cv.Optional(
                CONF_OPTIONS, default=DEFAULT_VENTILATION_LEVEL_OPTIONS
            ): cv.All(cv.ensure_list(cv.string_strict), cv.Length(min=4, max=4)),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)

MODE_SELECT_SCHEMA = (
    select.select_schema(LG040100ModeSelect, icon="mdi:format-list-bulleted")
    .extend(
        {
            cv.Optional(CONF_NAME, default="Betriebsmodus"): cv.string_strict,
            cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,
            cv.Optional(CONF_OPTIONS, default=DEFAULT_MODE_OPTIONS): cv.All(
                cv.ensure_list(cv.string_strict), cv.Length(min=5, max=5)
            ),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_LG040100_ID): cv.use_id(LG040100),
        cv.GenerateID(CONF_LG040100_STATUS_COMPONENT_ID): cv.use_id(
            LG040100StatusComponent
        ),
        cv.GenerateID(CONF_LG040100_MODE_COMPONENT_ID): cv.use_id(LG040100ModeComponent),
        cv.Optional(CONF_SELECTS, default={CONF_VENTILATION_LEVEL: {}}): cv.Schema(
            {
                cv.Optional(
                    CONF_VENTILATION_LEVEL, default={}
                ): VENTILATION_LEVEL_SCHEMA,
                cv.Optional(CONF_OPERATION_MODE, default={}): MODE_SELECT_SCHEMA,
            }
        ),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_LG040100_ID])
    status_comp = await cg.get_variable(config[CONF_LG040100_STATUS_COMPONENT_ID])
    mode_comp = await cg.get_variable(config[CONF_LG040100_MODE_COMPONENT_ID])

    selects_conf = config.get(CONF_SELECTS, {})

    vent_conf = selects_conf.get(CONF_VENTILATION_LEVEL, {})
    if not vent_conf.get(CONF_DEACTIVATE):
        var = cg.new_Pvariable(vent_conf[CONF_ID], parent, status_comp)
        await cg.register_component(var, vent_conf)
        await select.register_select(
            var,
            vent_conf,
            options=vent_conf.get(CONF_OPTIONS, DEFAULT_VENTILATION_LEVEL_OPTIONS),
        )

    mode_conf = selects_conf.get(CONF_OPERATION_MODE, {})
    if not mode_conf.get(CONF_DEACTIVATE):
        mode_var = cg.new_Pvariable(mode_conf[CONF_ID], parent, mode_comp)
        await cg.register_component(mode_var, mode_conf)
        await select.register_select(
            mode_var,
            mode_conf,
            options=mode_conf.get(CONF_OPTIONS, DEFAULT_MODE_OPTIONS),
        )
