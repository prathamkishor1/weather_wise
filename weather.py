import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("🌤️ Weather App", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Check Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.resize(500, 600)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Title Label
        self.city_label.setAlignment(Qt.AlignCenter)

        # Input & Button Layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.get_weather_button)

        # Weather Display Card
        card = QVBoxLayout()
        card.setSpacing(10)
        card.addWidget(self.temperature_label)
        card.addWidget(self.emoji_label)
        card.addWidget(self.description_label)

        card_frame = QFrame()
        card_frame.setLayout(card)
        card_frame.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 20px;
            padding: 20px;
        """)

        # Add widgets to main layout
        main_layout.addWidget(self.city_label)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(card_frame)

        self.setLayout(main_layout)

        # Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #e6f2ff;
                font-family: calibri;
            }
            QLabel#city_label {
                font-size: 45px;
                font-weight: bold;
                color: #003366;
            }
            QLineEdit {
                font-size: 20px;
                padding: 8px;
                border: 2px solid #3399ff;
                border-radius: 10px;
            }
            QPushButton {
                font-size: 20px;
                padding: 10px 20px;
                background-color: #3399ff;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #267dcc;
            }
            QLabel#temperature_label {
                font-size: 70px;
                color: #003366;
            }
            QLabel#emoji_label {
                font-size: 90px;
                font-family: Segoe UI Emoji;
            }
            QLabel#description_label {
                font-size: 30px;
                color: #333333;
            }
        """)

        # Set Object Names
        self.city_label.setObjectName("city_label")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Button click action
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "f1d576dfcde4ae917844dda7001dab4e"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nCheck your input.")
                case 401:
                    self.display_error("Invalid API Key.")
                case 404:
                    self.display_error("City not found.")
                case _:
                    self.display_error(f"HTTP Error:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error.\nCheck internet.")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out.")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Error:\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setText("")
        self.emoji_label.setText("❌")
        self.description_label.setText(message)

    def display_weather(self, data):
        temperature_k = data["main"]["temp"]
        temperature_f = (temperature_k * 9 / 5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"].capitalize()

        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return "🌈"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
