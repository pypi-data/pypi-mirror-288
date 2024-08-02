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

from PySide6.QtCore import (
    Signal,
    QPointF,
    QRectF,
    Qt,
)
from PySide6.QtGui import QPainter
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import (
    QAbstractSlider,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QMessageBox,
    QScrollBar,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QFontMetrics
from .annotation import (
    Annotation,
    AnnotationHandle,
)
from .cursor import Cursor
from .dialog import (
    ConfirmMessageBox,
    DialogCode,
    TimelineDialog,
)
from .event import (
    Event,
    EventDialog,
)
from .ticklocator import TickLocator
from .timeline import Timeline


class ZoomableGraphicsView(QGraphicsView):
    MARGIN_BOTTOM = 15.0

    def __init__(self, scene: QGraphicsScene, parent=None):
        super().__init__(scene, parent)
        self.zoom_factor = 1.0
        self.zoom_step = 1.2
        self.zoom_shift = None
        self.minimum_zoom_factor = 1.0

        vertical_scrollbar = QScrollBar(Qt.Orientation.Vertical, self)
        vertical_scrollbar.valueChanged.connect(
            self.on_vertical_scroll_value_changed
        )
        self.setVerticalScrollBar(vertical_scrollbar)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if not self.parent().video.media:
                return
            mouse_pos = self.mapToScene(event.position().toPoint()).x()
            if event.angleDelta().y() > 0:
                self.zoom_shift = mouse_pos * (1 - self.zoom_step)
                self.zoom_in()
            else:
                self.zoom_shift = mouse_pos * (1 - 1 / self.zoom_step)
                self.zoom_out()
            self.zoom_shift = None
        elif event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            if event.angleDelta().y() > 0:
                action = QAbstractSlider.SliderSingleStepAdd
            else:
                action = QAbstractSlider.SliderSingleStepSub
            self.horizontalScrollBar().triggerAction(action)
        else:
            super().wheelEvent(event)

    def on_vertical_scroll_value_changed(self, value):
        if self.parent().time_pane_scale:
            self.parent().time_pane_scale.setPos(0, value)

    def zoom_in(self):
        self.zoom_factor *= self.zoom_step
        self.update_scale()

    def zoom_out(self):
        if self.zoom_factor / self.zoom_step >= self.minimum_zoom_factor:
            self.zoom_factor /= self.zoom_step
            self.update_scale()

    def update_scale(self):
        # Update the size of the scene with zoom_factor
        self.scene().setSceneRect(
            0,
            0,
            self.width() * self.zoom_factor,
            self.scene().height(),
        )

        if self.zoom_shift:
            previous_anchor = self.transformationAnchor()
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.translate(self.zoom_shift, 0)
            self.setTransformationAnchor(previous_anchor)

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)

        # Get the position click from the scene
        map = self.mapToScene(self.scene().sceneRect().toRect())
        x = map.boundingRect().x()

        # Calculate the time of the position click
        time = int(
            (x + event.scenePosition().x())
            * self.parent().duration
            / self.scene().width()
        )

        self.parent().video.set_position(time)

    def set_position(self, time):
        # During the creation of a new annotation
        if self.parent().current_annotation:
            time = self.parent().current_annotation.get_time_from_bounding_interval(
                time
            )

        # Cope with selected annotation
        for i in self.parent().scene.selectedItems():
            if isinstance(i, Annotation):
                time = i.get_time_from_bounding_interval(time)
                break

        # Set time to the video player
        self.parent().video.mediaplayer.setPosition(int(time))

    def keyPressEvent(self, event):
        pass


class TimePane(QWidget):
    CSV_HEADERS = ["timeline", "label", "begin", "end", "duration", "comment"]
    valueChanged = Signal(int)
    durationChanged = Signal(int)

    def __init__(self, video=None):
        """Initializes the timeline widget"""
        super().__init__(video)
        self._duration = 0
        self._value = 0

        self.selected_timeline = None
        self.current_annotation: Annotation = None
        self.video = video
        self.scene = QGraphicsScene()
        self.scene.sceneRectChanged.connect(self.on_scene_changed)
        self.scene.selectionChanged.connect(self.on_selection_changed)
        self.timelines: list[Timeline] = []
        self.view = ZoomableGraphicsView(self.scene, self)
        self.cursor = None
        self.time_pane_scale = None

        self.view.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.view.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.setMouseTracking(True)
        self.scene.setSceneRect(0, 0, self.view.width(), self.view.height())

        self.valueChanged.connect(self.on_value_changed)
        self.durationChanged.connect(self.on_duration_changed)

        self.data_needs_save = False

    def on_scene_changed(self, rect):
        # Update annotations
        for timeline in self.timelines:
            timeline.update_rect_width(rect.width())
            for annotation in timeline.annotations:
                annotation.update_rect()

        if self.current_annotation:
            self.current_annotation.update_rect()

        # Update time_pane_scale display
        if self.time_pane_scale:
            # Update cursor
            if self.duration:
                self.time_pane_scale.cursor.setX(
                    self.value * rect.width() / self.duration
                )
            self.time_pane_scale.update_rect()

    def on_selection_changed(self):
        selected_items = self.scene.selectedItems()
        selected = None
        if len(selected_items) == 1:
            selected = selected_items[0]
            if isinstance(selected, Timeline):
                self.selected_timeline = selected
        for s in self.timelines:
            s.select = s == selected

    def select_cycle_timeline(self, delta, checked=False):
        i, n = self.find_selected_timeline()
        self.timelines[i].select = False
        if delta > 0:
            if i == n - 1:
                i = -1
        else:
            if i == 0:
                i = n
        i += delta
        self.select_timeline(self.timelines[i])

    def find_selected_timeline(self):
        n = len(self.timelines)
        for i in range(n):
            if self.timelines[i].select:
                break
        return i, n

    def select_timeline(self, line):
        line.select = True
        self.selected_timeline = line
        line.update()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != self._value:
            self._value = value
            self.valueChanged.emit(value)

    def on_value_changed(self, new_value):
        # First, update the current annotation, if it exists. If the cursor
        # value goes beyond the allowed bounds, bring it back and do not update
        # the other widgets.
        if self.current_annotation:
            if (
                self.current_annotation.lower_bound
                and new_value < self.current_annotation.lower_bound
            ):
                new_value = self.current_annotation.lower_bound
            elif (
                self.current_annotation.upper_bound
                and new_value > self.current_annotation.upper_bound
            ):
                new_value = self.current_annotation.upper_bound
                if (
                    self.video.mediaplayer.playbackState()
                    == QMediaPlayer.PlaybackState.PlayingState
                ):
                    self.video.mediaplayer.pause()
            start_time = self.current_annotation.start_time
            end_time = self.current_annotation.end_time
            mfps = self.video.mfps
            if start_time < end_time:
                if new_value >= start_time:
                    self.current_annotation.update_end_time(
                        new_value + int(mfps / 2)
                    )
                else:
                    self.current_annotation.update_start_time(end_time)
                    self.current_annotation.update_end_time(start_time - mfps)
            else:
                if new_value <= start_time:
                    self.current_annotation.update_end_time(
                        new_value - int(mfps / 2)
                    )
                else:
                    self.current_annotation.update_start_time(end_time)
                    self.current_annotation.update_end_time(start_time + mfps)

        # Cope with selected annotation
        for i in self.scene.selectedItems():
            if isinstance(i, Annotation):
                new_value = i.get_time_from_bounding_interval(new_value)
                break

        # Update cursor position
        if self.time_pane_scale and self.time_pane_scale.cursor:
            self.time_pane_scale.cursor.setX(
                new_value * self.scene.width() / self.duration
            )

        if isinstance(self.scene.focusItem(), AnnotationHandle):
            annotation_handle: AnnotationHandle = self.scene.focusItem()
            annotation_handle.change_time(new_value)

        # Change appearance of annotation under the cursor
        # (Brute force approach; this ought to be improved)
        if not self.current_annotation:
            for t in self.timelines:
                for a in t.annotations:
                    a.penWidth = Annotation.PEN_WIDTH_OFF_CURSOR
            if self.selected_timeline:
                for a in self.selected_timeline.annotations:
                    if a.start_time <= new_value and a.end_time >= new_value:
                        a.penWidth = Annotation.PEN_WIDTH_ON_CURSOR
                        break

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        if duration != self._duration:
            self._duration = duration
            self.durationChanged.emit(duration)

    def on_duration_changed(self, new_duration):
        # Update timeline Scale
        self.time_pane_scale = TimePaneScale(self)
        self.update()

    def load_common(self):
        # Recreate timeline
        self.time_pane_scale = TimePaneScale(self)

    def clear(self):
        # Clear timelineScene
        self.scene.clear()
        self.timelines = []

    def handle_annotation(self):
        """Handles the annotation"""
        if not self.selected_timeline:
            QMessageBox.warning(self, "Warning", "No timeline selected")
            return
        else:
            if self.current_annotation is None:
                can_be_initiate, lower_bound, upper_bound, annotation = (
                    Annotation.can_be_initiated(
                        self.selected_timeline.annotations, self.value
                    )
                )
                if can_be_initiate:
                    self.current_annotation = Annotation(
                        self,
                        self.selected_timeline,
                        None,
                        None,
                        lower_bound,
                        upper_bound,
                    )
                self.video.window.menu.add_annotation_action.setText(
                    "Finish annotation"
                )
                self.video.window.menu.abort_current_annotation_action.setEnabled(
                    True
                )
                if annotation:
                    annotation.setSelected(not annotation.isSelected())
                    annotation.get_bounds()

            else:
                # End the current annotation
                agd = EventDialog(self.current_annotation.timeline)
                agd.exec()

                if agd.result() == DialogCode.Accepted:
                    if agd.state == "create":
                        # When creating a new event, create the event and add the
                        # current annotation to it
                        event = Event(
                            len(self.current_annotation.timeline.events) + 1,
                            agd.event_name_text.text(),
                            agd.color,
                            self,
                        )
                        event.add_annotation(self.current_annotation)
                        self.current_annotation.timeline.add_event(event)
                    else:
                        # Otherwise, we are selecting an existing event, and will
                        # retrieve the event and add the annotation to it
                        event = agd.combo_box.currentData()
                        event.add_annotation(self.current_annotation)
                    self.current_annotation.ends_creation()
                    self.current_annotation = None
                    self.on_value_changed(self.value)
                elif agd.result() == DialogCode.Aborted:
                    self.current_annotation.remove()
                    self.current_annotation = None
                self.video.window.menu.add_annotation_action.setText(
                    "Start annotation"
                )
                self.video.window.menu.abort_current_annotation_action.setEnabled(
                    False
                )
                self.update()

    def handle_timeline(self):
        dialog = TimelineDialog(self)
        dialog.exec()
        if dialog.result() == DialogCode.Accepted:
            self.add_timeline(Timeline(dialog.get_text(), self))

    def resizeEvent(self, a0):
        if self.time_pane_scale:
            origin = self.view.mapToScene(0, 0).x()
            width_before = self.scene.width() / self.view.zoom_factor
            width_after = self.view.width()
            shift = origin * (1 - width_after / width_before)
            self.view.update_scale()
            previous_anchor = self.view.transformationAnchor()
            self.view.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.view.translate(shift, 0)
            self.view.setTransformationAnchor(previous_anchor)
        else:
            self.scene.setSceneRect(
                0,
                0,
                self.view.width(),
                TimePaneScale.FIXED_HEIGHT + Timeline.FIXED_HEIGHT,
            )

        self.update()

    def abort_current_annotation(self):
        if self.current_annotation is not None:
            confirm_box = ConfirmMessageBox(self)
            if confirm_box.result() == ConfirmMessageBox.DialogCode.Accepted:
                self.current_annotation.remove()
                self.current_annotation = None
                self.update()
                self.video.abort_current_annotation_action.setEnabled(False)

    def add_timeline(self, line):
        self.timelines.append(line)
        line.addToScene()

        # Calculate the new height of the scene
        new_height = (
            TimePaneScale.FIXED_HEIGHT
            + len(self.timelines) * Timeline.FIXED_HEIGHT
            + ZoomableGraphicsView.MARGIN_BOTTOM
        )
        scene_rect = self.scene.sceneRect()
        scene_rect.setHeight(new_height)
        self.scene.setSceneRect(scene_rect)

        # Set maximum height of the widget
        self.setMaximumHeight(int(new_height))

        # Select the new timeline
        for i in self.timelines:
            i.select = False
        line.select = True

    def get_timeline_by_name(self, name):
        """Get the timeline by name"""
        return next((x for x in self.timelines if x.name == name), None)

    def has_annotations(self) -> bool:
        return any(len(line.annotations) for line in self.timelines)

    def delete_annotation(self):
        for i in self.scene.selectedItems():
            if isinstance(i, Annotation):
                i.on_remove()
                break


class TimePaneScale(QGraphicsRectItem):

    FIXED_HEIGHT: float = 25.0

    def __init__(self, time_pane: TimePane):
        super().__init__()
        self.time_pane = time_pane
        self.time_pane.scene.addItem(self)
        self.cursor = Cursor(self)
        self.setRect(
            QRectF(0, 0, self.time_pane.scene.width(), self.FIXED_HEIGHT)
        )

    def paint(self, painter, option, widget=...):
        self._draw_rect(painter)

        if self.time_pane.duration != 0:
            self._draw_scale(painter)

    def update_rect(self):
        self.setRect(
            QRectF(0, 0, self.time_pane.scene.width(), self.FIXED_HEIGHT)
        )
        self.update()

    def _draw_rect(self, painter):
        """Draw the background rectangle of the timeline scale"""
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.lightGray)
        self.setRect(
            QRectF(0, 0, self.time_pane.scene.width(), self.FIXED_HEIGHT)
        )
        painter.drawRect(self.rect())

    def _draw_scale(self, painter):
        tl = TickLocator()
        min_gap = 0.05
        dur = self.time_pane.duration
        wid = self.time_pane.scene.width()
        font = painter.font()
        fm = QFontMetrics(font)
        loc = tl.find_locations(0, dur / 1000, wid, font, min_gap)
        # Calculate the height of the text
        font_height = painter.fontMetrics().height()
        line_height = 5
        y = self.rect().height()

        for p in loc:

            i = 1000 * (p[0] * wid / dur)

            # Calculate the position of the text
            text_width = fm.boundingRect(p[1]).width()
            text_position = QPointF(i - text_width / 2, font_height)

            # Draw the text
            painter.drawText(text_position, p[1])

            # Calculate the position of the line
            painter.drawLine(QPointF(i, y), QPointF(i, y - line_height))

    def mousePressEvent(self, event):
        return

    def mouseReleaseEvent(self, event):
        return
