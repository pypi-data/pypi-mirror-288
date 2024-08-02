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
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)
from PySide6.QtGui import QColor
from functools import partial
from dialog import (
    ConfirmMessageBox,
    DialogCode,
)
from .utils import color_fg_from_bg


class Event:
    def __init__(
        self,
        id: int,
        name: str,
        color=None,
        timeline=None,
    ):
        """Initializes the annotation event"""
        self.id = id
        self.name = name
        self.color = color
        self.timeline = timeline
        self.annotations = []

    def add_annotation(self, annotation):
        annotation.name = self.name
        annotation.set_event(self)
        self.annotations.append(annotation)
        self.annotations.sort(key=lambda x: x.start_time)

    def remove_annotation(self, annotation):
        annotation.name = None
        annotation.set_event(None)
        self.annotations.remove(annotation)


class EventDialog(QDialog):
    DEFAULT_COLOR = QColor(255, 255, 255)
    """Dialog to select or create a new annotation event"""

    def __init__(self, timeline=None):
        super().__init__(timeline.time_pane)
        self.setWindowTitle("New annotation")

        self.color = self.DEFAULT_COLOR
        self.combo_box = QComboBox()
        self.labels = [x.name for x in timeline.events]
        for event in timeline.events:
            self.combo_box.addItem(event.name, event)
        self.combo_box.setEditable(True)

        self.label_2 = QLabel("New label")
        self.event_name_text = QLineEdit()

        self.button_color_2 = QPushButton("Color")
        self.button_color_2.clicked.connect(self.on_button_color_2_clicked)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        self.abort_button = QPushButton("Abort")
        self.abort_button.clicked.connect(self.abort)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)

        # Create layout for contents
        layout = QHBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.label_2)
        layout.addWidget(self.event_name_text)
        layout.addWidget(self.button_color_2)

        # Create layout for main buttons
        main_button_layout = QHBoxLayout()
        main_button_layout.addWidget(self.cancel_button)
        main_button_layout.addWidget(self.abort_button)
        main_button_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(main_button_layout)

        self.setLayout(main_layout)

        if timeline.events:
            self.state = "choose"
        else:
            self.state = "create"

        self.set_visibility()

    def accept(self):
        if self.state == "choose" and (
            self.combo_box.currentText() not in self.labels
        ):
            self.state = "create"
            self.event_name_text.setText(self.combo_box.currentText())
            self.set_visibility()
            self.event_name_text.setFocus()
        else:
            super().accept()

    def abort(self):
        confirm_box = ConfirmMessageBox(
            self,
            "Are you sure to abort the creation of this annotation ?",
        )
        if confirm_box.result() == QMessageBox.DialogCode.Accepted:
            self.done(DialogCode.Aborted)

    def on_button_color_2_clicked(self):
        dialog = QColorDialog(self.color, self)
        dialog.exec()
        if dialog.result() == dialog.DialogCode.Accepted:
            self.color = dialog.currentColor()

    def set_visibility(self):
        if self.state == "choose":
            self.combo_box.setVisible(True)
            self.label_2.setVisible(False)
            self.event_name_text.setVisible(False)
            self.button_color_2.setVisible(False)
        else:
            self.combo_box.setVisible(False)
            self.label_2.setVisible(True)
            self.event_name_text.setVisible(True)
            self.button_color_2.setVisible(True)
        self.save_button.setDefault(True)


class ChooseEvent(QDialog):
    def __init__(self, events, info):
        super().__init__()
        self.setWindowTitle("Choose event")
        layout = QFormLayout(self)
        info = QLabel(info)
        layout.addRow(info)
        eventbox = QHBoxLayout()
        for i, event in enumerate(events):
            button = QPushButton(event.name)
            bg_color = event.color
            fg_color = color_fg_from_bg(bg_color)
            button.setAutoFillBackground(False)
            button.setStyleSheet(
                "QPushButton {"
                "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
                f"   stop:0 {bg_color.name()}, stop:1 {bg_color.name()});"
                f" color: {fg_color.name()};"
                "border: 2px solid black;"
                "border-radius: 5px"
                "}"
                "QPushButton:hover {"
                "    border: 3px solid black;"
                "}"
            )
            button.clicked.connect(partial(self.set_chosen, i))
            eventbox.addWidget(button)
        layout.addRow(eventbox)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def set_chosen(self, val):
        self.chosen = val
        self.accept()

    def get_chosen(self):
        return self.chosen


class ChangeEvent(QDialog):
    def __init__(self, event, timeline):
        super().__init__()
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
        layout.addRow(widgetbox)
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
