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
            auto idx = this->index_of(value);
            if (!idx.has_value())
            {
                ESP_LOGW(TAG, "Unknown ventilation option: %s", value.c_str());
                return;
            }
            int level = *idx;

            auto write_ls = [this, level]() {
                if (this->parent_ == nullptr || this->parent_->connector_ == nullptr)
                    return;

                this->parent_->connector_->send_write_request(
                    WR3223Commands::LS, std::to_string(level),
                    [this, level](char *answer, bool success)
                    {
                        ESP_LOGD(TAG, "LS write level=%d success=%d answer=%s", level, success, answer ? answer : "<null>");
                        if (success)
                        {
                            if (this->status_ != nullptr)
                            {
                                auto *holder = this->status_->get_holder();
                                if (holder != nullptr)
                                    holder->setVentilationLevel(level);
                            }
                        }
                    });
            };

            if (this->status_ != nullptr && this->status_->is_rs_handshake_enabled())
            {
                if (this->parent_ != nullptr && this->parent_->connector_ != nullptr)
                {
                    this->parent_->connector_->send_write_request(
                        WR3223Commands::RS, "1",
                        [this, write_ls](char *answer, bool success)
                        {
                            ESP_LOGD(TAG, "RS handshake for LS write success=%d answer=%s", success, answer ? answer : "<null>");
                            if (success)
                                write_ls();
                        });
                    this->publish_state(value);
                    return;
                }
            }

            write_ls();
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