#pragma once

#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "lg040100_connector.h"
#include <vector>

namespace esphome
{
    namespace lg040100
    {

        class WR3223RelaisComponent; // forward declaration

        class WR3223StartUpListener
        {
        public:
            virtual void on_startup() = 0;
        };

        class WR3223 : public PollingComponent
        {
        public:
            WR3223(uart::UARTComponent *parent, uint32_t update_interval = 5000)
                : PollingComponent(update_interval) {}

            void setup() override;
            void update() override;
            void dump_config() override;

            void set_connector(WR3223Connector *connector) { connector_ = connector; }
            void set_relais_component(WR3223RelaisComponent *component) { relais_component_ = component; }

            void register_startup_listener(WR3223StartUpListener *listener) { startup_listeners_.push_back(listener); }

            void on_relais_update();

            void set_max_restore_attempts(uint8_t attempts) { max_restore_attempts_ = attempts; }
            void set_write_access_enabled(bool enabled) { write_access_enabled_ = enabled; }
            bool is_write_access_enabled() const { return write_access_enabled_; }

            bool is_bedienteil_aktiv();

            /// @brief liefert ob der Statup Prozess abgeschlossen wurde
            /// @return
            bool is_startup_completed() { return fresh_start_ == false; }

            WR3223Connector *connector_{nullptr};
            WR3223RelaisComponent *relais_component_{nullptr};

        private:
            /// @brief nach einem stromausfall oder aehnlichem, verhalten wir uns anders im
            /// ersten Update
            bool fresh_start_{true};
            uint8_t startup_counter_{0};
            uint8_t max_restore_attempts_{4};
            bool write_access_enabled_{false};
            std::vector<WR3223StartUpListener *> startup_listeners_{};
        };

        using LG040100StartUpListener = WR3223StartUpListener;
        using LG040100 = WR3223;
        using LG040100RelaisComponent = WR3223RelaisComponent;

    } // namespace lg040100
#ifndef ESPHOME_LG040100_NAMESPACE_ALIAS_DEFINED
#define ESPHOME_LG040100_NAMESPACE_ALIAS_DEFINED
    namespace wr3223 = lg040100;
#endif
} // namespace esphome
