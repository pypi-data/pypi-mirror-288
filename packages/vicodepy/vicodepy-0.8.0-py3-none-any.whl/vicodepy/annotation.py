# ViCodePy - A video coder for Experimental Psychology
#
# Copyright (C) 2024 Esteban Milleret
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

from abc import abstractmethod

from PySide6.QtCore import (
    Qt,
    QRectF,
)
from PySide6.QtGui import (
    QColor,
    QPen,
)
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsItem,
    QMenu,
    QMessageBox,
)

from .utils import color_fg_from_bg
from .comment import AnnotationComment
from .event import ChooseEvent


class Annotation(QGraphicsRectItem):
    DEFAULT_PEN_COLOR = QColor(0, 0, 0, 255)
    DEFAULT_BG_COLOR = QColor(255, 48, 48, 128)
    DEFAULT_FONT_COLOR = QColor(0, 0, 0, 255)
    PEN_WIDTH_ON_CURSOR = 3
    PEN_WIDTH_OFF_CURSOR = 1

    def __init__(
        self,
        time_pane,
        timeline,
        start_time: int = None,
        end_time: int = None,
        lower_bound: int = None,
        upper_bound: int = None,
    ):
        """Initializes the Annotation widget"""
        super().__init__(timeline)
        self.brushColor = self.DEFAULT_BG_COLOR
        self.penColor = self.DEFAULT_PEN_COLOR
        self.penWidth = self.PEN_WIDTH_OFF_CURSOR
        self.fontColor = self.DEFAULT_FONT_COLOR
        self.event = None
        self.name = None
        self.time_pane = time_pane
        self.mfps = self.time_pane.video.mfps
        self.start_time = (
            start_time if start_time else time_pane.value - int(self.mfps / 2)
        )
        self.end_time = (
            end_time if end_time else time_pane.value + int(self.mfps / 2)
        )
        self.timeline = timeline
        self.start_x_position = int(
            self.start_time
            * self.time_pane.scene.width()
            / self.time_pane.duration
        )
        self.end_x_position = int(
            self.end_time
            * self.time_pane.scene.width()
            / self.time_pane.duration
        )
        self.set_default_rect()
        self.selected = False
        self.begin_handle: AnnotationHandle = None
        self.end_handle: AnnotationHandle = None

        self.setX(self.start_x_position)
        self.setY(self.timeline.label.FIXED_HEIGHT)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.comment: str = ""

    @staticmethod
    def can_be_initiated(annotations, value):
        """Check if the annotation can be initiated"""
        lower_bound = upper_bound = None
        valid = True
        annotation_under_cursor = None

        # Loop through the annotations of the selected timeline
        for a in annotations:
            if a.start_time <= value <= a.end_time:
                valid = False
                annotation_under_cursor = a
                break
            if not lower_bound:
                if a.end_time < value:
                    lower_bound = a.end_time + int(a.mfps / 2)
            else:
                if a.end_time < value:
                    if lower_bound < a.end_time:
                        lower_bound = a.end_time + int(a.mfps / 2)
            if not upper_bound:
                if a.start_time > value:
                    upper_bound = a.start_time - int(a.mfps / 2)
            else:
                if a.start_time > value:
                    if upper_bound > a.start_time:
                        upper_bound = a.start_time - int(a.mfps / 2)
        return valid, lower_bound, upper_bound, annotation_under_cursor

    def set_default_rect(self):
        self.setRect(
            QRectF(
                0,
                0,
                self.end_x_position - self.start_x_position,
                self.timeline.FIXED_HEIGHT - self.timeline.label.FIXED_HEIGHT,
            )
        )

    def mousePressEvent(self, event):
        return

    def mouseReleaseEvent(self, event):
        return

    def mouseDoubleClickEvent(self, event):
        if not self.time_pane.current_annotation:
            self.setSelected(True)
            self.calculateBounds()

    def focusOutEvent(self, event):
        self.setSelected(False)
        super().focusOutEvent(event)

    def contextMenuEvent(self, event):
        if not self.isSelected():
            super().contextMenuEvent(event)
            return
        can_merge_previous = False
        for annotation in self.timeline.annotations:
            if (
                annotation.end_time == self.start_time
                and self.name == annotation.name
            ):
                can_merge_previous = True
                break
        can_merge_next = False
        for annotation in self.timeline.annotations:
            if (
                self.end_time == annotation.start_time
                and self.name == annotation.name
            ):
                can_merge_next = True
                break
        menu = QMenu()
        menu.addAction("Delete annotation").triggered.connect(self.on_remove)
        menu.addAction("Change annotation label").triggered.connect(
            self.change_label
        )
        if can_merge_previous:
            menu.addAction("Merge with previous annotation").triggered.connect(
                self.merge_previous
            )
        if can_merge_next:
            menu.addAction("Merge with next annotation").triggered.connect(
                self.merge_next
            )
        menu.addAction("Comment annotation").triggered.connect(
            self.edit_comment
        )
        menu.exec(event.screenPos())

    def on_remove(self):
        answer = QMessageBox.question(
            self.time_pane,
            "Confirmation",
            "Do you want to remove the annotation?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.remove()

    def edit_comment(self):
        comment_dialog = AnnotationComment(self.comment)
        comment_dialog.exec()
        if comment_dialog.result() == QMessageBox.DialogCode.Accepted:
            self.comment = comment_dialog.get_text()

    def merge_previous(self):
        for annotation in self.timeline.annotations:
            if (
                self.start_time == annotation.end_time
                and self.name == annotation.name
            ):
                break
        self.start_time = annotation.start_time
        annotation.remove()
        self.update_rect()
        self.update()

    def merge_next(self):
        for annotation in self.timeline.annotations:
            if (
                self.end_time == annotation.start_time
                and self.name == annotation.name
            ):
                break
        self.end_time = annotation.end_time
        annotation.remove()
        self.update_rect()
        self.update()

    def change_label(self):
        events_dialog = ChooseEvent(
            self.timeline.events,
            "Select an event for the current annotation:",
        )
        events_dialog.exec()
        if events_dialog.result() == QMessageBox.DialogCode.Accepted:
            i = events_dialog.get_chosen()
            g = self.timeline.events[i]
            self.set_event(g)
            self.update()

    def remove(self):
        self.time_pane.scene.removeItem(self)
        if self in self.timeline.annotations:
            self.timeline.remove_annotation(self)
        if self.event:
            self.event.remove_annotation(self)
        del self

    def paint(self, painter, option, widget=...):
        # Draw the annotation rectangle
        self._draw_rect(painter)

        # Draw the name of the annotation in the annotation rectangle
        self._draw_name(painter)

        if self.isSelected():
            self.show_handles()
        else:
            self.hide_handles()

    def _draw_rect(self, painter):
        """Draw the annotation rectangle"""
        pen: QPen = QPen(self.penColor)
        pen.setWidth(self.penWidth)

        if self.isSelected():
            # Set border dotline if annotation is selected
            pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)
        painter.setBrush(self.brushColor)

        # Draw the rectangle
        painter.drawRect(self.rect())

    def _draw_name(self, painter):
        """Draws the name of the annotation"""
        if self.name:
            col = color_fg_from_bg(self.brushColor)
            painter.setPen(col)
            painter.setBrush(col)
            painter.drawText(
                self.rect(), Qt.AlignmentFlag.AlignCenter, self.name
            )

    def set_event(self, event=None):
        """Updates the event"""
        if event is None:
            self.event = None
            self.brushColor = self.DEFAULT_BG_COLOR
        else:
            self.event = event
            self.brushColor = event.color
            self.name = event.name
            self.setToolTip(self.name)
            if self.begin_handle:
                self.begin_handle.setBrush(event.color)
                self.end_handle.setBrush(event.color)

    def update_rect(self, new_rect: QRectF = None):
        new_rect = new_rect or self.time_pane.scene.sceneRect()
        # Calculate position to determine width
        self.start_x_position = (
            self.start_time * new_rect.width() / self.time_pane.duration
        )
        self.end_x_position = (
            self.end_time * new_rect.width() / self.time_pane.duration
        )
        self.setX(self.start_x_position)

        # Update the rectangle
        rect = self.rect()
        rect.setWidth(self.end_x_position - self.start_x_position)
        self.setRect(rect)

        if self.begin_handle:
            self.begin_handle.setX(self.rect().x())
            self.end_handle.setX(self.rect().width())

    def update_start_time(self, start_time: int):
        self.start_time = start_time
        self.update_rect()
        self.update()

    def update_end_time(self, end_time: int):
        """Updates the end time"""
        self.end_time = end_time
        self.update_rect()
        self.update()

    def update_selectable_flags(self):
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.update()

    def create_handles(self):
        self.begin_handle = AnnotationStartHandle(self)
        self.end_handle = AnnotationEndHandle(self)

    def ends_creation(self):
        """Ends the creation of the annotation"""
        self.update_selectable_flags()
        self.create_handles()

        # if start_time is greater than end_time then swap times
        if self.start_time > self.end_time:
            self.start_time, self.end_time = self.end_time, self.start_time
            self.update_rect()

        # Add this annotation to the annotation list of the timeline
        self.timeline.add_annotation(self)

        self.update()

    def show_handles(self):
        if self.begin_handle:
            self.begin_handle.setVisible(True)
        if self.end_handle:
            self.end_handle.setVisible(True)

    def hide_handles(self):
        if self.begin_handle:
            self.begin_handle.setVisible(False)
        if self.end_handle:
            self.end_handle.setVisible(False)

    def get_bounds(self):
        _, lower_bound, upper_bound, annotation = Annotation.can_be_initiated(
            list(filter(lambda x: x != self, self.timeline.annotations)),
            self.start_time,
        )
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def get_time_from_bounding_interval(self, time) -> int:
        if self.lower_bound and time < self.lower_bound:
            time = self.lower_bound
        elif self.upper_bound and time > self.upper_bound:
            time = self.upper_bound
            self.time_pane.video.mediaplayer.pause()
        return time


class AnnotationHandle(QGraphicsRectItem):
    PEN_WIDTH_ON = 3
    PEN_WIDTH_OFF = 1

    def __init__(self, annotation: Annotation, value: int, x: float):
        super().__init__(annotation)
        self.annotation = annotation
        self.value = value

        self.pen: QPen = QPen(self.annotation.penColor)
        self.pen.setWidth(self.PEN_WIDTH_OFF)
        self.setPen(self.pen)
        self.setBrush(self.annotation.brushColor)
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptDrops(True)

        width = 9
        self._height = annotation.rect().height() / 2
        self.setRect(QRectF(-4.5, 0, width, self._height))

        self.setX(x)
        self.setY(self._height / 2)

    @abstractmethod
    def change_time(self, new_time):
        self.value = new_time

    def focusInEvent(self, event):
        self.annotation.setSelected(True)
        self.annotation.time_pane.video.set_position(self.value)
        self.pen.setWidth(self.PEN_WIDTH_ON)
        self.setPen(self.pen)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.annotation.setSelected(False)
        self.pen.setWidth(self.PEN_WIDTH_OFF)
        self.setPen(self.pen)
        super().focusOutEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.setY(self._height / 2)

            # A la souris on déplace le X, il faut changer le temps
            time = int(
                event.scenePos().x()
                * self.annotation.time_pane.duration
                / self.annotation.time_pane.scene.width()
            )

            time = self.annotation.get_time_from_bounding_interval(time)

            self.annotation.time_pane.video.set_position(time)


class AnnotationStartHandle(AnnotationHandle):

    def __init__(self, annotation: Annotation):
        super().__init__(annotation, annotation.start_time, 0)

    def change_time(self, time):
        t = time - int(self.annotation.mfps / 2)
        super().change_time(t)
        self.annotation.update_start_time(t)


class AnnotationEndHandle(AnnotationHandle):
    def __init__(self, annotation: Annotation):
        super().__init__(
            annotation, annotation.end_time, annotation.rect().width()
        )

    def change_time(self, time):
        t = time + int(self.annotation.mfps / 2)
        super().change_time(t)
        self.annotation.update_end_time(t)
