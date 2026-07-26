import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, binary_sensor as esphome_binary_sensor, text_sensor as esphome_text_sensor
from esphome.components.binary_sensor import new_binary_sensor
from esphome.const import(    
    CONF_UART_ID,
    CONF_UPDATE_INTERVAL,
    CONF_NAME,
    CONF_DEVICE_CLASS, 
    CONF_ENTITY_CATEGORY, 
    DEVICE_CLASS_PROBLEM,
    ENTITY_CATEGORY_DIAGNOSTIC
)

# Use lg040100 as the external namespace name.
# C++ keeps backward compatibility via namespace aliases in headers.
lg040100_ns = cg.esphome_ns.namespace("lg040100")

# Main classes in Python use LG040100 names, mapped to existing C++ class names.
LG040100 = lg040100_ns.class_("LG040100", cg.PollingComponent)
LG040100Connector = lg040100_ns.class_("LG040100Connector", cg.Component)
LG040100ErrorComponent = lg040100_ns.class_("LG040100ErrorComponent", cg.PollingComponent)
LG040100StatusValueHolder = lg040100_ns.class_("LG040100StatusValueHolder")
LG040100StatusComponent = lg040100_ns.class_("LG040100StatusComponent", cg.PollingComponent)
LG040100ModeValueHolder = lg040100_ns.class_("LG040100ModeValueHolder")
LG040100ModeComponent = lg040100_ns.class_("LG040100ModeComponent", cg.PollingComponent)
LG040100RelaisComponent = lg040100_ns.class_("LG040100RelaisComponent", cg.PollingComponent)


# Automatisches Laden der Module
AUTO_LOAD = ["uart", "text_sensor", "binary_sensor", "switch", "select", "number", "button"]

CONF_LG040100_ID = "lg040100_id"
CONF_LG040100_CONNECTOR_ID = "lg040100_connector_id"
CONF_LG040100_ERROR_COMPONENT_ID = "lg040100_error_component_id"
CONF_LG040100_STATUS_COMPONENT_ID = "lg040100_status_component_id"
CONF_LG040100_STATUS_HOLDER_ID = "lg040100_status_holder_id"
CONF_LG040100_MODE_COMPONENT_ID = "lg040100_mode_component_id"
CONF_LG040100_MODE_HOLDER_ID = "lg040100_mode_holder_id"
CONF_LG040100_RELAIS_COMPONENT_ID = "lg040100_relais_component_id"
CONF_DEACTIVATE = "deactivate"
CONF_ERROR_POLLING = "error_polling"
CONF_ERROR_STATUS = "error_status_sensor"
CONF_ERROR_TEXT = "error_text_sensor"
CONF_STATUS_UPDATE_INTERVAL = "status_update_interval"
CONF_MODE_UPDATE_INTERVAL = "mode_update_interval"
CONF_RELAIS_UPDATE_INTERVAL = "relais_update_interval"
CONF_RESTORE_ATTEMPTS = "restore_attempts"
CONF_ENABLE_UNSAFE_WRITES = "enable_unsafe_writes"
CONF_REFERENCE_PROFILE = "reference_profile"

def validate_status_interval(value):
    value = cv.update_interval(value)
    if value.total_milliseconds > 20000:
        raise cv.Invalid("Status update interval must not exceed 20s")
    return value

# YAML validation for ESPHome
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_LG040100_ID): cv.declare_id(LG040100),    
    cv.GenerateID(CONF_LG040100_CONNECTOR_ID): cv.declare_id(LG040100Connector),
    cv.GenerateID(CONF_LG040100_ERROR_COMPONENT_ID): cv.declare_id(LG040100ErrorComponent),
    cv.GenerateID(CONF_LG040100_STATUS_COMPONENT_ID): cv.declare_id(LG040100StatusComponent),
    cv.GenerateID(CONF_LG040100_STATUS_HOLDER_ID): cv.declare_id(LG040100StatusValueHolder),
    cv.GenerateID(CONF_LG040100_MODE_COMPONENT_ID): cv.declare_id(LG040100ModeComponent),
    cv.GenerateID(CONF_LG040100_MODE_HOLDER_ID): cv.declare_id(LG040100ModeValueHolder),
    cv.GenerateID(CONF_LG040100_RELAIS_COMPONENT_ID): cv.declare_id(LG040100RelaisComponent),
    cv.Optional(CONF_STATUS_UPDATE_INTERVAL, default="10s"): validate_status_interval,
    cv.Optional(CONF_MODE_UPDATE_INTERVAL, default="60s"): cv.update_interval,
    cv.Optional(CONF_RELAIS_UPDATE_INTERVAL, default="60s"): cv.update_interval,
     cv.Optional(CONF_RESTORE_ATTEMPTS, default=4): cv.int_,
    cv.Optional(CONF_ENABLE_UNSAFE_WRITES, default=False): cv.boolean,
    cv.Optional(CONF_REFERENCE_PROFILE, default="none"): cv.one_of("none", "lg150", "lg250", "lg350", lower=True),
    cv.Required(CONF_UART_ID): cv.use_id(uart.UARTComponent),
    cv.Optional(CONF_ERROR_POLLING, default={}): cv.Schema({
        cv.Optional(CONF_UPDATE_INTERVAL, default="60s"): cv.update_interval,
        cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,  # Option zum Deaktivieren
        cv.Optional(CONF_ERROR_STATUS, default={
            CONF_NAME: "FEHLER", 
            CONF_DEVICE_CLASS: DEVICE_CLASS_PROBLEM, 
            CONF_ENTITY_CATEGORY: ENTITY_CATEGORY_DIAGNOSTIC,
            }): esphome_binary_sensor.binary_sensor_schema().extend({
                cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,  # Option zum Deaktivieren
        }),
        cv.Optional(CONF_ERROR_TEXT, default={
            CONF_NAME: "FEHLER Text",            
            CONF_ENTITY_CATEGORY: ENTITY_CATEGORY_DIAGNOSTIC
        }): esphome_text_sensor.text_sensor_schema().extend({
            cv.Optional(CONF_DEACTIVATE, default=False): cv.boolean,  # Option zum Deaktivieren
        }), 
    }),
}).extend(cv.COMPONENT_SCHEMA).extend(cv.polling_component_schema("30s"))

# Code generation for ESPHome
async def to_code(config):
    # Hauptkomponente erzeugen
    var = cg.new_Pvariable(config[CONF_LG040100_ID], await cg.get_variable(config[CONF_UART_ID]))    
    await cg.register_component(var, config)
    cg.add(var.set_max_restore_attempts(config.get(CONF_RESTORE_ATTEMPTS, 4)))
    cg.add(var.set_write_access_enabled(config.get(CONF_ENABLE_UNSAFE_WRITES, False)))

    # LG040100Connector als eigene Komponente registrieren
    connector = cg.new_Pvariable(
        config[CONF_LG040100_CONNECTOR_ID], 
        await cg.get_variable(config[CONF_UART_ID])
    )    
    await cg.register_component(connector, {})
    cg.add(var.set_connector(connector))  # Verbinde den Connector mit LG040100    

    # Relais component wird nun immer gebaut, damit andere module das nutzen koennen
    relais_component = cg.new_Pvariable(
        config[CONF_LG040100_RELAIS_COMPONENT_ID],
        var,
        config[CONF_RELAIS_UPDATE_INTERVAL],
    )
    await cg.register_component(relais_component, {})
    cg.add(var.set_relais_component(relais_component)) # Verbinde die RelaisComponent mit LG040100

    holder = cg.new_Pvariable(config[CONF_LG040100_STATUS_HOLDER_ID])
    status_component = cg.new_Pvariable(
        config[CONF_LG040100_STATUS_COMPONENT_ID],
        var,
        config[CONF_STATUS_UPDATE_INTERVAL],
        holder,
    )
    await cg.register_component(status_component, {})

    mode_holder = cg.new_Pvariable(config[CONF_LG040100_MODE_HOLDER_ID])
    mode_component = cg.new_Pvariable(
        config[CONF_LG040100_MODE_COMPONENT_ID],
        var,
        config[CONF_MODE_UPDATE_INTERVAL],
        mode_holder,
    )
    await cg.register_component(mode_component, {})

    

    error_polling = config.get(CONF_ERROR_POLLING)        
    
    if error_polling.get(CONF_DEACTIVATE) != True: # build error component by default
        
        error_status_config = error_polling.get(CONF_ERROR_STATUS)
        error_text_config = error_polling.get(CONF_ERROR_TEXT)

        if(error_status_config.get(CONF_DEACTIVATE) != True or error_text_config.get(CONF_DEACTIVATE) != True):
            # LG040100ErrorComponent instanziieren und registrieren
            error_component = cg.new_Pvariable(config[CONF_LG040100_ERROR_COMPONENT_ID], var, error_polling.get(CONF_UPDATE_INTERVAL, cv.update_interval("60s")))
            await cg.register_component(error_component, config)
            
            if error_status_config.get(CONF_DEACTIVATE) != True:
                sensor_error_status = await new_binary_sensor(error_status_config)
                cg.add(error_component.register_status_sensor(sensor_error_status))
    
            if error_text_config.get(CONF_DEACTIVATE) != True:
                sensor_error_text = await esphome_text_sensor.new_text_sensor(error_text_config)
                cg.add(error_component.register_text_sensor(sensor_error_text))
