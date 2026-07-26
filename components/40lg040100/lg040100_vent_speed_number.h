#pragma once

#include "esphome/components/number/number.h"
#include "esphome/core/component.h"
#include "lg040100.h"
#include "lg040100_constants.h"
#include <string>

namespace esphome
{
    namespace lg040100
    {

        class WR3223VentSpeedNumber : public number::Number, public Component
        {
        public:
            WR3223VentSpeedNumber(WR3223 *parent, int level) : parent_(parent), level_(level) {}
            WR3223VentSpeedNumber(WR3223 *parent, const std::string &command)
                : parent_(parent), level_(0), custom_command_(command) {}

            void setup() override;
            float get_setup_priority() const override { return setup_priority::DATA; }

        protected:
            void control(float value) override;
            const char *get_command() const;

            WR3223 *parent_;
            int level_;
            std::string custom_command_{};
        };

        using LG040100VentSpeedNumber = WR3223VentSpeedNumber;

    } // namespace lg040100
} // namespace esphome