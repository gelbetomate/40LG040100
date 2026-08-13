#include "lg040100_vent_speed_number.h"
#include "lg040100_helper.h"
#include "esphome/core/log.h"

namespace esphome
{
    namespace lg040100
    {

        static const char *const TAG = "lg040100_vent_speed_number";

        const char *WR3223VentSpeedNumber::get_command() const
        {
            if (!custom_command_.empty())
                return custom_command_.c_str();

            switch (level_)
            {
            case 1:
                return WR3223Commands::L1;
            case 2:
                return WR3223Commands::L2;
            case 3:
                return WR3223Commands::L3;
            default:
                return nullptr;
            }
        }

        void WR3223VentSpeedNumber::setup()
        {
            const char *cmd = get_command();
            if (cmd == nullptr || parent_ == nullptr || parent_->connector_ == nullptr)
                return;
            parent_->connector_->send_request(cmd, [this, cmd](char *resp, bool ok)
                                              {
                if (ok) {
                    int val = WR3223Helper::to_int(resp, true);
                    this->publish_state(val);
                } else {
                    ESP_LOGW(TAG, "Failed to read initial value for %s", cmd);
                } });
        }

        void WR3223VentSpeedNumber::control(float value)
        {
            const char *cmd = get_command();
            if (cmd == nullptr || parent_ == nullptr || parent_->connector_ == nullptr)
                return;

            if (!parent_->is_write_access_enabled())
            {
                ESP_LOGW(TAG, "Write access disabled (enable_unsafe_writes=false) - number write skipped.");
                return;
            }

            int val = static_cast<int>(value);
            std::string data = std::to_string(val);
            parent_->connector_->send_write_request(cmd, data, [this, val, cmd](char *, bool ok)
                                                    {
            ESP_LOGD(TAG, "Write %d result %d", val, ok);
            if (!ok)
                return;

            this->parent_->connector_->send_request(cmd, [this, val](char *response, bool read_ok)
                                                    {
                if (!read_ok) {
                    ESP_LOGW(TAG, "Write %d ACK, but %s readback failed", val, this->get_command());
                    return;
                }

                int readback = WR3223Helper::to_int(response, true);
                if (readback != val) {
                    ESP_LOGW(TAG, "Write %d ACK, but readback is %d", val, readback);
                    this->publish_state(readback);
                    return;
                }

                this->publish_state(readback);
            }); });
        }

    } // namespace lg040100
} // namespace esphome