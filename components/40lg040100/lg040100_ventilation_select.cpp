#include "lg040100_ventilation_select.h"
#include "esphome/core/log.h"
#include "lg040100_helper.h"

namespace esphome
{
    namespace lg040100
    {

        static const char *const TAG = "lg040100_vent_select";

        void WR3223VentilationLevelSelect::setup()
        {
            if (this->status_ != nullptr)
            {
                this->status_->register_status_control(this);
                auto holder = this->status_->get_holder();
                if (holder != nullptr)
                {
                    this->on_status(holder);
                }
            }
        }        

        void WR3223VentilationLevelSelect::control(const std::string &value)
        {
            ESP_LOGW(TAG, "Luftstufe '%s' ist ueber LS laut Hermes-PDF nur lesbar.", value.c_str());
        }

        void WR3223VentilationLevelSelect::on_status(WR3223StatusValueHolder *holder)
        {
            if (holder == nullptr)
                return;

            int level = holder->getVentilationLevel();
            const auto &options = this->traits.get_options();
            if (level < 0 || level >= static_cast<int>(options.size()))
                return;

            this->publish_state(options[level]);
        }

    } // namespace lg040100
} // namespace esphome