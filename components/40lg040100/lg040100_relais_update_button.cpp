#include "lg040100_relais_update_button.h"
#include "esphome/core/log.h"

namespace esphome
{
    namespace lg040100
    {

        static const char *TAG = "lg040100_relais_button";

        void WR3223RelaisUpdateButton::dump_config()
        {
            LOG_BUTTON("", "LG040100 Relais Update Button", this);
        }

        void WR3223RelaisUpdateButton::press_action()
        {
            if (relais_ != nullptr)
            {
                ESP_LOGD(TAG, "Manuelle Relaisaktualisierung ausgeloest");
                relais_->update();
            }
        }

    } // namespace lg040100
} // namespace esphome