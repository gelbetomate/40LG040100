#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "lg040100.h"

namespace esphome {
namespace lg040100 {

class WR3223SensorPollingComponent : public PollingComponent {
public:
    WR3223SensorPollingComponent(WR3223 *parent, uint32_t update_interval, sensor::Sensor *sensor, const char *command)
        : PollingComponent(update_interval), parent_(parent), command_(command), sensor_(sensor), binary_sensor_(nullptr), text_sensor_(nullptr) {}

    WR3223SensorPollingComponent(WR3223 *parent, uint32_t update_interval, binary_sensor::BinarySensor *binary_sensor, const char *command)
        : PollingComponent(update_interval), parent_(parent), command_(command), sensor_(nullptr), binary_sensor_(binary_sensor), text_sensor_(nullptr) {}

    WR3223SensorPollingComponent(WR3223 *parent, uint32_t update_interval, text_sensor::TextSensor *text_sensor, const char *command)
        : PollingComponent(update_interval), parent_(parent), command_(command), sensor_(nullptr), binary_sensor_(nullptr), text_sensor_(text_sensor) {}

    void update() override;

private:
    WR3223 *parent_;
    const char *command_;
    sensor::Sensor *sensor_;
    binary_sensor::BinarySensor *binary_sensor_;
    text_sensor::TextSensor *text_sensor_;

    void process_response(char *response);
};

using LG040100SensorPollingComponent = WR3223SensorPollingComponent;

} // namespace lg040100
} // namespace esphome

