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
            int level = 0;

            if (value == "Aus")
                level = 0;
            else if (value == "Luftstufe 1")
                level = 1;
            else if (value == "Luftstufe 2")
                level = 2;
            else if (value == "Luftstufe 3")
                level = 3;
            else if (value == "Automatik")
                level = 4;
            else
            {
                auto idx = this->index_of(value);
                if (!idx.has_value())
                {
                    ESP_LOGW(TAG, "Unknown ventilation option: %s", value.c_str());
                    return;
                }
                level = static_cast<int>(*idx);
            }

            if (this->status_ != nullptr)
            {
                auto *holder = this->status_->get_holder();
                if (holder != nullptr)
                {
                    holder->setVentilationLevel(level);
                    this->status_->write_status();
                }
            }

            this->publish_state(value);
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