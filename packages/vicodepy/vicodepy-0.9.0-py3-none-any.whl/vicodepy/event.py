# ViCodePy - A video coder for Experimental Psychology
#
# Copyright (C) 2024 Rafael Laboissière
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import (
    QColorDialog,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
)
from PySide6.QtGui import (
    QColor,
    QIcon,
)
from PySide6.QtWidgets import QStyle
from functools import partial
from .assets import Assets
from .utils import color_fg_from_bg


class Event:
    def __init__(
        self,
        name: str,
        color=None,
    ):
        """Initializes the annotation event"""
        self.name = name
        self.color = color


class ChooseEvent(QDialog):
    DEFAULT_COLOR = QColor(255, 255, 255)

    def __init__(self, timeline):
        super().__init__(timeline.time_pane)
        self.setWindowTitle("Choose Event")
        self.setStyleSheet(
            "QPushButton {"
            "    border: 1px solid gray;"
            "    border-radius: 5px;"
            "    padding: 5px"
            "}"
            "QPushButton:default {"
            "    border: 3px solid black;"
            "}"
        )
        self.timeline = timeline
        layout = QFormLayout(self)
        if len(timeline.events) > 0:
            event_buttons = QHBoxLayout()
            self.buttons = []
            for i, event in enumerate(timeline.events):
                button = QPushButton(event.name)
                button.setDefault(len(self.buttons) == 0)
                self.buttons.append(button)
                bg_color = event.color
                fg_color = color_fg_from_bg(bg_color)
                button.setStyleSheet(
                    "    background-color: qlineargradient("
                    "        x1:0, y1:0, x2:0, y2:1,"
                    f"       stop:0 {bg_color.name()},"
                    f"       stop:1 {bg_color.name()}"
                    "    );"
                    f"   color: {fg_color.name()};"
                )
                button.setAutoFillBackground(False)
                button.clicked.connect(partial(self.set_chosen, i))
                event_buttons.addWidget(button)
            layout.addRow(event_buttons)
        control_buttons = QHBoxLayout()
        assets = Assets()
        new_button = QPushButton(
            QIcon(assets.get("plus.png")),
            "New",
            self,
        )
        new_button.setDefault(False)
        new_button.clicked.connect(self.new_event)
        control_buttons.addWidget(new_button)
        finish_button = QPushButton(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_DialogCancelButton
            ),
            "Finish",
            self,
        )
        finish_button.setDefault(False)
        finish_button.clicked.connect(self.reject)
        control_buttons.addWidget(finish_button)
        layout.addRow(control_buttons)

    def set_chosen(self, val):
        self.chosen = val
        self.accept()

    def get_chosen(self):
        return self.chosen

    def new_event(self):
        event = Event("", self.DEFAULT_COLOR)
        dialog = ChangeEvent(event, self.timeline)
        dialog.exec()
        if dialog.result() == QMessageBox.DialogCode.Accepted:
            if event.name == "":
                QMessageBox.warning(
                    self, "Warning", "Event label cannot be empty"
                )
            else:
                if event.name in [x.name for x in self.timeline.events]:
                    QMessageBox.warning(
                        self,
                        "Warning",
                        f"Event with name {event.name} already exists",
                    )
                else:
                    self.timeline.add_event(event)
            for i, e in enumerate(self.timeline.events):
                if e.name == event.name:
                    self.set_chosen(i)


class ChangeEvent(QDialog):
    def __init__(self, event, timeline):
        super().__init__(timeline.time_pane)
        self.setWindowTitle("Change event")
        self.event = event
        self.color = event.color
        self.timeline = timeline
        layout = QFormLayout(self)
        widgetbox = QHBoxLayout()
        self.label_edit = QLineEdit(self)
        self.label_edit.setText(event.name)
        widgetbox.addWidget(self.label_edit)
        self.color_button = QPushButton("color")
        self.color_button.clicked.connect(self.choose_color)
        self.set_style()
        widgetbox.addWidget(self.color_button)
        layout.addRow("Name: ", widgetbox)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def accept(self):
        self.event.name = self.label_edit.text()
        for a in self.timeline.annotations:
            if a.event == self.event:
                a.set_event(self.event)
                a.update()
        super().accept()

    def choose_color(self):
        dialog = QColorDialog(self.color, self)
        dialog.exec()
        if dialog.result() == dialog.DialogCode.Accepted:
            self.event.color = dialog.currentColor()
            self.set_style()

    def set_style(self):
        bg_color = self.event.color
        fg_color = color_fg_from_bg(bg_color)
        self.color_button.setStyleSheet(
            "QPushButton {"
            "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
            f"   stop:0 {bg_color.name()}, stop:1 {bg_color.name()});"
            f" color: {fg_color.name()};"
            "border: 2px solid black;"
            "border-radius: 5px;"
            "padding: 6px"
            "}"
            "QPushButton:hover {"
            "    border: 3px solid black;"
            "}"
        )
