#include "lg040100_sensor_polling.h"
#include "esphome/core/log.h"
#include <cerrno>
#include <cstdlib>
#include <cctype>
#include <string>

namespace esphome
{
    namespace lg040100
    {

        static const char *const TAG = "lg040100_sensor_polling";

        static std::string trim_response(const char *response)
        {
            if (response == nullptr)
                return "";

            std::string value(response);
            size_t start = 0;
            while (start < value.size() && std::isspace(static_cast<unsigned char>(value[start])))
                ++start;

            size_t end = value.size();
            while (end > start && std::isspace(static_cast<unsigned char>(value[end - 1])))
                --end;

            return value.substr(start, end - start);
        }

        static bool is_integer_with_trailing_dot(const std::string &value)
        {
            if (value.size() < 2 || value.back() != '.')
                return false;

            size_t index = (value[0] == '-' || value[0] == '+') ? 1 : 0;
            if (index >= value.size() - 1)
                return false;

            for (; index < value.size() - 1; ++index)
            {
                if (!std::isdigit(static_cast<unsigned char>(value[index])))
                    return false;
            }

            return true;
        }

        void WR3223SensorPollingComponent::update()
        {
            ESP_LOGD(TAG, "Sende Anfrage fuer Kommando: %s", command_);

            this->parent_->connector_->send_request(command_, [this](char *response, bool success)
                                                    {
        if (success)
            this->process_response(response);
        else
            ESP_LOGW(TAG, "Command %s: Timeout", command_); });
        }

        void WR3223SensorPollingComponent::process_response(char *response)
        {
            if (!response || strlen(response) == 0)
            {
                ESP_LOGW(TAG, "Command %s: Keine Antwort vom WR3223 erhalten.", command_);
                return;
            }

            ESP_LOGI(TAG, "Command %s: Antwort = %s", command_, response);

            if (sensor_)
            {
                errno = 0;
                char *endptr = nullptr;
                float value = strtof(response, &endptr);

                while (endptr != nullptr && *endptr != '\0' && std::isspace(static_cast<unsigned char>(*endptr)))
                    ++endptr;

                if (endptr == response || errno == ERANGE || (endptr != nullptr && *endptr != '\0'))
                {
                    ESP_LOGW(TAG, "Command %s: Ungueltige numerische Antwort '%s' - Wert wird verworfen.", command_, response);
                    return;
                }

                ESP_LOGD(TAG, "Sensorwert fuer %s: %f", command_, value);
                sensor_->publish_state(value);
            }
            else if (binary_sensor_)
            {
                bool state = (strcmp(response, "1") == 0);
                ESP_LOGD(TAG, "BinarySensor fuer %s: %d", command_, state);
                binary_sensor_->publish_state(state);
            }
            else if (text_sensor_)
            {
                std::string text_value = trim_response(response);
                if (is_integer_with_trailing_dot(text_value))
                    text_value.pop_back();

                ESP_LOGD(TAG, "TextSensor fuer %s: %s", command_, text_value.c_str());
                text_sensor_->publish_state(text_value);
            }
        }

    } // namespace lg040100
} // namespace esphome
