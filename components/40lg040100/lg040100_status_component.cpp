#include "lg040100_status_component.h"
#include "esphome/core/log.h"
#include "lg040100_helper.h"
#include "lg040100_connector.h"

namespace esphome
{
    namespace lg040100
    {

        static const char *const TAG = "lg040100_status_component";

        void WR3223StatusComponent::setup()
        {
            if (parent_ != nullptr)
                parent_->register_startup_listener(this);

            if (holder_ != nullptr)
                holder_->restore_state_sw();

            notify_controls();
        }

        void WR3223StatusComponent::update()
        {
            // Statuswerte werden nur durch eine explizite Benutzeraktion geschrieben.
        }

        void WR3223StatusComponent::on_startup()
        {
            if (controls_.empty())
                return;

            if (holder_ != nullptr)
            {
                holder_->restore_state_sw();
                notify_controls();
            }
        }

        void WR3223StatusComponent::write_status()
        {
            if (parent_ == nullptr || parent_->connector_ == nullptr ||
                holder_ == nullptr)
                return;

            if (!parent_->is_write_access_enabled())
            {
                ESP_LOGW(TAG, "Write access disabled (enable_unsafe_writes=false) - status write skipped.");
                request_status_readback_();
                return;
            }

            if (parent_->is_bedienteil_aktiv())
            {
                ESP_LOGW(TAG, "Bedienteil aktiv - Schreiben nicht moeglich, lese Status.");
                request_status_readback_();
                return;
            }

            if (rs_handshake_enabled_)
            {
                parent_->connector_->send_write_request(
                    WR3223Commands::RS,
                    "1",
                    [this](char *answer, bool success)
                    {
                        ESP_LOGD(TAG, "RS handshake response: %s success=%d", answer, success);
                        if (!success)
                            ESP_LOGW(TAG, "RS handshake failed - trying SW write anyway.");

                        write_sw_status_();
                    });
                return;
            }

            write_sw_status_();
        }

        void WR3223StatusComponent::request_status_readback_()
        {
            if (parent_ == nullptr || parent_->connector_ == nullptr || holder_ == nullptr)
                return;

            parent_->connector_->send_request(
                WR3223Commands::SW,
                [this](char *resp, bool ok)
                {
                    ESP_LOGD(TAG, "Status readback: %s success=%d", resp, ok);
                    if (ok && holder_->setSWStatus(resp))
                    {
                        notify_controls();
                    }
                });
        }

        void WR3223StatusComponent::write_sw_status_()
        {
            if (parent_ == nullptr || parent_->connector_ == nullptr || holder_ == nullptr)
                return;

            std::string data = std::to_string(holder_->getSwStatus());
            parent_->connector_->send_write_request(
                WR3223Commands::SW, data,
                [this](char *answer, bool success)
                {
                    ESP_LOGD(TAG, "Status write response: %s success=%d", answer, success);
                    if (!success) // bei misserfolg schreiben wir den echten Wert zurueck
                    {
                        request_status_readback_();
                    }
                    else
                    {
                        notify_controls();
                    }
                });
        }

        void WR3223StatusComponent::notify_controls()
        {
            for (auto *ctrl : controls_)
            {
                if (ctrl != nullptr)
                    ctrl->on_status(holder_);
            }
        }

    } // namespace lg040100
} // namespace esphome