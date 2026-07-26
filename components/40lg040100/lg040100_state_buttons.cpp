#include "lg040100_state_buttons.h"
#include "esphome/core/log.h"

namespace esphome
{
    namespace lg040100
    {
        static const char *TAG = "lg040100_state_button";

        void WR3223SaveStateButton::dump_config()
        {
            LOG_BUTTON("", "LG040100 Save State Button", this);
        }

        void WR3223SaveStateButton::press_action()
        {
            ESP_LOGD(TAG, "Saving state to NVS");
            if (mode_ != nullptr && mode_->get_holder() != nullptr)
                mode_->get_holder()->save_state();
            if (status_ != nullptr && status_->get_holder() != nullptr)
                status_->get_holder()->save_state_sw();
        }

        void WR3223RestoreStateButton::dump_config()
        {
            LOG_BUTTON("", "LG040100 Restore State Button", this);
        }

        void WR3223RestoreStateButton::press_action()
        {
            ESP_LOGD(TAG, "Restoring state from NVS");
            if (mode_ != nullptr && mode_->get_holder() != nullptr)
            {
                mode_->get_holder()->restore_state();
                mode_->write_mode();
            }
            if (status_ != nullptr && status_->get_holder() != nullptr)
            {
                status_->get_holder()->restore_state_sw();
                status_->write_status();
            }
        }

    } // namespace lg040100
} // namespace esphome