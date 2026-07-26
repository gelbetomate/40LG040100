#pragma once

#include "esphome/components/button/button.h"
#include "esphome/core/component.h"
#include "lg040100_relais_component.h"

namespace esphome
{
    namespace lg040100
    {

        class WR3223RelaisUpdateButton : public button::Button, public Component
        {
        public:
            explicit WR3223RelaisUpdateButton(WR3223RelaisComponent *relais)
                : relais_(relais) {}

            void dump_config() override;

        protected:
            void press_action() override;
            WR3223RelaisComponent *relais_{nullptr};
        };

        using LG040100RelaisUpdateButton = WR3223RelaisUpdateButton;

    } // namespace lg040100
} // namespace esphome