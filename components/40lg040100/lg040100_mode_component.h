#pragma once

#include "esphome/core/component.h"
#include "lg040100.h"
#include "lg040100_constants.h"
#include "lg040100_mode_value_holder.h"
#include <vector>

namespace esphome
{
    namespace lg040100
    {

        class WR3223ModeControl
        {
        public:
            virtual void on_mode(WR3223ModeValueHolder *holder) = 0;
        };

        class WR3223ModeComponent : public PollingComponent, public WR3223StartUpListener
        {
        public:
            WR3223ModeComponent(WR3223 *parent, uint32_t update_interval,
                                WR3223ModeValueHolder *holder)
                : PollingComponent(update_interval), parent_(parent), holder_(holder) {}

            void setup() override;
            void update() override;

            void on_startup() override;

            WR3223ModeValueHolder *get_holder() const { return holder_; }

            void register_mode_control(WR3223ModeControl *control) { controls_.push_back(control); }

            void write_mode();

        protected:
            void notify_controls();

        private:
            WR3223 *parent_;
            WR3223ModeValueHolder *holder_;
            std::vector<WR3223ModeControl *> controls_;
        };

        using LG040100ModeControl = WR3223ModeControl;
        using LG040100ModeComponent = WR3223ModeComponent;

    } // namespace lg040100
} // namespace esphome