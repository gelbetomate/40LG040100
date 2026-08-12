#pragma once

#include "esphome/core/component.h"
#include "lg040100.h"
#include "lg040100_constants.h"
#include "lg040100_status_value_holder.h"
#include <vector>

namespace esphome
{
    namespace lg040100
    {
        class WR3223StatusControl
        {
        public:
            virtual void on_status(WR3223StatusValueHolder *holder) = 0;
        };

        class WR3223StatusComponent : public PollingComponent, public WR3223StartUpListener
        {
        public:
            WR3223StatusComponent(WR3223 *parent, uint32_t update_interval,
                                  WR3223StatusValueHolder *holder)
                : PollingComponent(update_interval), parent_(parent), holder_(holder) {}

            void setup() override;
            void update() override;

            void on_startup() override;

            /// @brief Expose the internally used value holder
            WR3223StatusValueHolder *get_holder() const { return holder_; }

            /// @brief Register a control that depends on the status bits
            void register_status_control(WR3223StatusControl *control) { controls_.push_back(control); }

            /// @brief Write the current holder status to the device
            void write_status();

            void set_rs_handshake_enabled(bool enabled) { rs_handshake_enabled_ = enabled; }
            bool is_rs_handshake_enabled() const { return rs_handshake_enabled_; }

        protected:
            void notify_controls();

        private:
            void request_status_readback_();
            void write_sw_status_();

            WR3223 *parent_;
            WR3223StatusValueHolder *holder_;
            std::vector<WR3223StatusControl *> controls_;
            bool rs_handshake_enabled_{false};
        };

        using LG040100StatusControl = WR3223StatusControl;
        using LG040100StatusComponent = WR3223StatusComponent;

    } // namespace lg040100
} // namespace esphome