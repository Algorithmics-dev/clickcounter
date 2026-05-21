import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush


class NeonPanel(QFrame):
    def __init__(self, border_color):
        super().__init__()

        self.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(10, 25, 55, 220);
                border: 4px solid {border_color};
                border-radius: 24px;
            }}
        """)


class ClickCounterGame(QWidget):
    def __init__(self):
        super().__init__()

        self.clicks = 0
        self.time_left = 10
        self.game_active = False

        # BIGGER WINDOW
        self.setWindowTitle("Button Frenzy Arena")
        self.setFixedSize(1200, 1000)

        self.setStyleSheet("""
            QWidget {
                background-color: #070b1f;
                color: white;
                font-family: Arial;
            }
        """)

        # TITLE
        self.title = QLabel("⚡ BUTTON FRENZY ARENA ⚡")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 56px;
            font-weight: 900;
            color: #ffd32a;
            background: transparent;
        """)

        # SUBTITLE
        self.subtitle = QLabel(
            "Click as fast as you can before the arena timer explodes!"
        )
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            background: transparent;
        """)

        # TIMER NUMBER
        self.timer_big = QLabel("10")
        self.timer_big.setAlignment(Qt.AlignCenter)
        self.timer_big.setStyleSheet("""
            font-size: 64px;
            font-weight: 900;
            color: white;
            background: transparent;
        """)

        # SCORE NUMBER
        self.score_big = QLabel("0")
        self.score_big.setAlignment(Qt.AlignCenter)
        self.score_big.setStyleSheet("""
            font-size: 64px;
            font-weight: 900;
            color: white;
            background: transparent;
        """)

        # TIMER TITLE
        timer_title = QLabel("⏱ Time Left")
        timer_title.setAlignment(Qt.AlignCenter)
        timer_title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00d2ff;
            background: transparent;
        """)

        # SCORE TITLE
        score_title = QLabel("🎯 Total Clicks")
        score_title.setAlignment(Qt.AlignCenter)
        score_title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2ed573;
            background: transparent;
        """)

        # TIMER PANEL
        timer_panel = NeonPanel("#00d2ff")
        timer_panel.setMinimumHeight(180)

        timer_layout = QVBoxLayout()
        timer_layout.setContentsMargins(25, 20, 25, 20)
        timer_layout.setSpacing(12)

        timer_layout.addWidget(timer_title)
        timer_layout.addWidget(self.timer_big)

        timer_panel.setLayout(timer_layout)

        # SCORE PANEL
        score_panel = NeonPanel("#2ed573")
        score_panel.setMinimumHeight(180)

        score_layout = QVBoxLayout()
        score_layout.setContentsMargins(25, 20, 25, 20)
        score_layout.setSpacing(12)

        score_layout.addWidget(score_title)
        score_layout.addWidget(self.score_big)

        score_panel.setLayout(score_layout)

        # STATS LAYOUT
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(40)

        stats_layout.addWidget(timer_panel)
        stats_layout.addWidget(score_panel)

        # MESSAGE LABEL
        self.message_label = QLabel("🏁 Press START ARENA to begin!")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setMinimumHeight(120)

        self.message_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: white;
                background-color: rgba(10, 20, 45, 220);
                border: 4px dashed #ffd32a;
                border-radius: 24px;
                padding: 20px;
            }
        """)

        # CLICK BUTTON
        self.click_button = QPushButton("⚡ CLICK ME! ⚡")
        self.click_button.setEnabled(False)
        self.click_button.setMinimumHeight(220)

        self.click_button.setStyleSheet("""
            QPushButton {
                font-size: 62px;
                font-weight: 900;
                color: white;
                background-color: #ff2e1f;
                border: 8px solid #ffd32a;
                border-radius: 42px;
            }

            QPushButton:hover {
                background-color: #ff512f;
                border: 8px solid white;
            }

            QPushButton:pressed {
                background-color: #ffd32a;
                color: black;
                border: 8px solid #ff3838;
            }

            QPushButton:disabled {
                background-color: #555555;
                color: #dddddd;
                border: 8px solid #888888;
            }
        """)

        self.click_button.clicked.connect(self.add_click)

        # START BUTTON
        self.start_button = QPushButton("START ARENA")
        self.start_button.setMinimumHeight(95)

        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 36px;
                font-weight: 900;
                color: white;
                background-color: #16c93a;
                border: 6px solid #a8ffb5;
                border-radius: 26px;
            }

            QPushButton:hover {
                background-color: #2ed573;
                color: black;
            }

            QPushButton:pressed {
                background-color: #ffd32a;
                color: black;
            }

            QPushButton:disabled {
                background-color: #555555;
                color: #bbbbbb;
                border: 6px solid #777777;
            }
        """)

        self.start_button.clicked.connect(self.start_game)

        # MAIN LAYOUT
        main_layout = QVBoxLayout()

        # BIGGER SPACING
        main_layout.setContentsMargins(70, 55, 70, 55)
        main_layout.setSpacing(48)

        main_layout.addWidget(self.title)
        main_layout.addWidget(self.subtitle)
        main_layout.addLayout(stats_layout)
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.click_button)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.start_button)

        self.setLayout(main_layout)

        # TIMER
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    # BACKGROUND EFFECTS
    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(QColor("#070b1f")))
        painter.drawRect(self.rect())

        pen_colors = [
            "#ff3838",
            "#ffd32a",
            "#00d2ff",
            "#2ed573",
            "#ff4dff"
        ]

        for i in range(40):
            color = QColor(pen_colors[i % len(pen_colors)])

            painter.setPen(QPen(color, 4))

            x = 20 + (i * 53) % 1080
            y = 80 + (i * 71) % 760

            painter.drawLine(x, y, x + 28, y + 8)

        painter.end()

    # START GAME
    def start_game(self):
        self.clicks = 0
        self.time_left = 10
        self.game_active = True

        self.score_big.setText("0")
        self.timer_big.setText("10")

        self.message_label.setText(
            "🔥 GO GO GO! The arena is watching!"
        )

        self.click_button.setEnabled(True)

        self.start_button.setEnabled(False)
        self.start_button.setText("GAME RUNNING...")

        self.timer.start(1000)

    # ADD CLICK
    def add_click(self):
        if self.game_active:

            self.clicks += 1

            self.score_big.setText(str(self.clicks))

            if self.clicks == 10:
                self.message_label.setText("⚡ Warm-up complete!")

            elif self.clicks == 25:
                self.message_label.setText("🔥 Combo energy rising!")

            elif self.clicks == 50:
                self.message_label.setText("💀 The button is panicking!")

            elif self.clicks == 80:
                self.message_label.setText("👑 Mythic energy detected!")

    # UPDATE TIMER
    def update_timer(self):

        self.time_left -= 1

        self.timer_big.setText(str(self.time_left))

        if self.time_left <= 3 and self.game_active:
            self.message_label.setText(
                "🚨 FINAL SECONDS! CLICK LIKE A LEGEND!"
            )

        if self.time_left <= 0:
            self.end_game()

    # END GAME
    def end_game(self):

        self.timer.stop()

        self.game_active = False

        self.click_button.setEnabled(False)

        self.start_button.setEnabled(True)
        self.start_button.setText("↻ PLAY AGAIN")

        rank = self.get_rank()

        self.message_label.setText(
            f"🏁 Final Score: {self.clicks} clicks\n"
            f"🏆 Rank Unlocked: {rank}"
        )

    # RANK SYSTEM
    def get_rank(self):

        if self.clicks < 20:
            return "Rookie Clicker 🐣"

        elif self.clicks < 40:
            return "Explorer Tapper 🧭"

        elif self.clicks < 70:
            return "Innovator Button Breaker 🔧"

        elif self.clicks < 100:
            return "Elite Click Machine ⚡"

        else:
            return "MYTHIC BUTTON DESTROYER 👑"


# RUN GAME
app = QApplication(sys.argv)

window = ClickCounterGame()

window.show()

sys.exit(app.exec_())