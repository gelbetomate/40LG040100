#include "lg040100_mode_select.h"
#include "esphome/core/log.h"
#include "lg040100_helper.h"

namespace esphome
{
    namespace lg040100
    {

        static const char *const TAG = "lg040100_mode_select";

        void WR3223ModeSelect::setup()
        {
            if (this->mode_ != nullptr)
            {
                this->mode_->register_mode_control(this);
                auto holder = this->mode_->get_holder();
                if (holder != nullptr)
                    this->on_mode(holder);
            }
        }

        void WR3223ModeSelect::control(const std::string &value)
        {
            ESP_LOGW(TAG, "Betriebsmodus '%s' ist ueber MD laut Hermes-PDF nur lesbar.", value.c_str());
        }

        void WR3223ModeSelect::on_mode(WR3223ModeValueHolder *holder)
        {
            if (holder == nullptr)
                return;

            int mode = holder->get_mode();
            const auto &options = this->traits.get_options();
            if (mode < 0 || mode >= static_cast<int>(options.size()))
                return;

            this->publish_state(options[mode]);
        }

    } // namespace lg040100
} // namespace esphome