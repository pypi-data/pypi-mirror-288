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

import csv
import os
import re
import tempfile
import zipfile
import yaml

from PySide6.QtCore import QUrl
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QStyle,
    QVBoxLayout,
)
from PySide6.QtMultimedia import QMediaFormat
from .annotation import Annotation
from .coders import Coders
from .config import Config
from .dialog import DialogCode
from .exceptions import LoadProjectError
from .event import Event
from .format import FORMAT, format_ok
from .timeline import Timeline
from .timepane import TimePane


class Files:

    def __init__(self, window):

        self.window = window
        self.data_to_load = None
        self.csv_delimiter = ","
        self.config_file_name = "config.yml"
        self.data_file_name = "metadata.yml"

        # Search for supported video file formats
        self.video_file_extensions = []
        for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
            mime_type = QMediaFormat(f).mimeType()
            name = mime_type.name()
            if re.search("^video/", name):
                self.video_file_extensions.extend(mime_type.suffixes())
        self.file_name_filters = [
            f"Video Files ({' '.join(['*.' + x for x in self.video_file_extensions])})",
            "All Files (*.*)",
        ]

        self.project_file_filters = [
            f"Zip files ({' '.join(['*.zip'])})",
            "All Files (*.*)",
        ]

    def open_video(self, widget=None):
        """Open a video file in a MediaPlayer"""
        dialog_txt = "Open Video File"
        file_dialog = QFileDialog(widget) if widget else QFileDialog()
        file_dialog.setWindowTitle(dialog_txt)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilters(self.file_name_filters)
        file_dialog.exec()
        if file_dialog.result() == DialogCode.Accepted:
            # Load only the first of the selected file
            try:
                filename = file_dialog.selectedFiles()[0]
                self.load_video_file(filename)
                self.load_config_file()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"{e}")

    def open_project(self, widget=None):
        """Open a project file"""
        dialog_txt = "Open Project File"
        project_dialog = QFileDialog(widget) if widget else QFileDialog()
        project_dialog.setWindowTitle(dialog_txt)
        project_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        project_dialog.setNameFilters(self.project_file_filters)
        project_dialog.exec()
        if project_dialog.result() == DialogCode.Accepted:
            try:
                filename = project_dialog.selectedFiles()[0]
                self.load_project_file(filename)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"{e}")

    def load_file(self, filename):
        try:
            if os.path.splitext(filename)[1] in [
                "." + ext for ext in self.video_file_extensions
            ]:
                self.load_video_file(filename)
                self.load_config_file()
            elif os.path.splitext(filename)[1] == ".zip":
                self.load_project_file(filename)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{e}")

    def load_video_file(self, filename):
        """Load video file"""
        if not os.path.exists(filename) or not os.path.isfile(filename):
            raise FileNotFoundError(
                f"FileNotFoundError : {filename} doesn't exist"
            )

        # getOpenFileName returns a tuple, so use only the actual file name
        self.media = QUrl.fromLocalFile(filename)
        self.window.video.media = self.media

        # Enable the buttons
        self.window.video.playbutton.setEnabled(True)
        self.window.video.stopbutton.setEnabled(True)

        # Put the media in the media player
        self.window.video.mediaplayer.setSource(self.media)

        # Set the title of the track as window title
        self.window.setWindowTitle(os.path.basename(filename))

        # Show first frame
        self.window.video.mediaplayer.play()
        self.window.video.mediaplayer.pause()

        # Clear the time_pane
        if bool(self.media):
            self.window.time_pane.clear()
        self.window.time_pane.load_common()

    def load_project_file(self, filename):
        """Load project file"""
        if not os.path.exists(filename) or not os.path.isfile(filename):
            raise FileNotFoundError(f"FileNotFoundError : {filename} not found")

        # filename is a zip file
        self.project_file_path = filename

        with zipfile.ZipFile(filename, "r") as zip_file:
            # Create temp dir
            temp_dir = tempfile.TemporaryDirectory()

            # Load data from metadata.yml
            with zip_file.open(self.data_file_name) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                if not format_ok(data["format"]):
                    raise LoadProjectError("Format problem")
                files = zip_file.namelist()

                # Search for video in temp dir
                video_file = data["video"]
                if video_file not in files:
                    raise LoadProjectError("Failed to load video file")

                # Search for config.yml in temp dir
                if self.config_file_name not in files:
                    raise LoadProjectError("Failed to load config file")

                # Search for csv file in temp dir
                data_file = os.path.splitext(video_file)[0] + ".csv"
                if data_file not in files:
                    raise LoadProjectError("Failed to load CSV file")

                # Extract all files in temp dir
                zip_file.extractall(temp_dir.name)

                # Load video file from temp dir
                self.load_video_file(os.path.join(temp_dir.name, video_file))

                # Load config file from in temp dir
                self.load_config_file(
                    os.path.join(temp_dir.name, self.config_file_name)
                )

                # Load csv data file from in temp dir
                self.data_to_load = os.path.join(temp_dir.name, data_file)

            self.temp_dir = temp_dir

    def load_config_file(self, filename=None):
        """load presets from config.yml file"""
        # Read the YAML file
        config = Config() if filename is None else Config(filename)

        # Access the values
        if "timelines" in config:
            # Loop over timelines from the config file
            for i, timeline in enumerate(config["timelines"]):
                # Create timeline
                line = Timeline(timeline["name"], self.window.time_pane)

                # Add the timeline to the TimePane
                self.window.time_pane.add_timeline(line)

                # Loop over events of the timeline
                events = timeline["events"]
                for i, event in enumerate(events):
                    line.events.append(
                        Event(
                            i, str(event["name"]), QColor(event["color"]), line
                        )
                    )

        if "csv-delimiter" in config:
            self.csv_delimiter = config["csv-delimiter"]

        if "coders" in config:
            self.coders = Coders(config["coders"])

    def load_data_file(self, filename=None):
        """load csv file"""
        if os.path.isfile(filename):
            with open(filename, newline="") as data_file:
                dialect = csv.Sniffer().sniff(data_file.read())
                data_file.seek(0)
                csv_reader = csv.DictReader(data_file, dialect=dialect)
                for row in csv_reader:
                    # Search for timeline
                    timeline = self.window.time_pane.get_timeline_by_name(
                        row["timeline"]
                    )

                    # If timeline from csv doesn't exist in TimePane,
                    # escape row
                    if not timeline:
                        continue

                    # Search for event
                    event = timeline.get_event_by_name(row["label"])

                    # If event from csv doesn't exist in timeline,
                    # then add it
                    if not event:
                        continue

                    annotation = Annotation(
                        self.window.time_pane,
                        timeline,
                        int(row["begin"]),
                        int(row["end"]),
                    )

                    event.add_annotation(annotation)
                    annotation.ends_creation()
        else:
            QMessageBox.critical(
                self,
                "Error",
                "The file you tried to load does not exist.",
            )

        self.data_to_load = None

    def save_project(self) -> bool:
        """Save project file"""
        temp_dir = tempfile.TemporaryDirectory()

        # Construct the default file name from the QUrl of the video file
        target_directory = self.media.path()
        target_file_name = os.path.splitext(
            os.path.basename(self.media.path())
        )[0]
        data_file_name = target_file_name + ".csv"
        if self.project_file_path:
            target_directory = self.project_file_path
            target_file_name = os.path.splitext(
                os.path.basename(self.project_file_path)
            )[0]

        target_directory = (
            os.path.dirname(target_directory) + "/" + target_file_name + ".zip"
        )

        # 1. Create config file from information of time_pane in
        # tmp directory
        if self.coders:
            if not self.coders.current:
                self.coders.set_current()
        else:
            self.coders = Coders({})
            self.coders.set_current()
        self.coders.current.set_date_now()

        config_file_path = os.path.join(temp_dir.name, self.config_file_name)
        self.export_config_file(config_file_path)

        # 2. Create CSV file "data.csv" from information of time_pane in
        # tmp directory
        data_file_path = os.path.join(temp_dir.name, data_file_name)
        self.export_data_file(data_file_path)

        data_file_path = os.path.join(temp_dir.name, self.data_file_name)
        with open(data_file_path, "w") as f:
            yaml.safe_dump(
                {
                    "video": os.path.basename(self.media.path()),
                    "format": FORMAT,
                },
                f,
            )

        # Open FileDialog
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save project",
            target_directory,
            "Zip Files (*.zip);;All Files (*)",
        )
        if path:
            with zipfile.ZipFile(path, "w") as zip_file:
                zip_file.write(data_file_path, self.data_file_name)
                zip_file.write(config_file_path, self.config_file_name)
                zip_file.write(data_file_path, data_file_name)
                zip_file.write(
                    self.media.toLocalFile(),
                    os.path.basename(self.media.path()),
                )
            self.window.time_pane.data_needs_save = False
            return True
        return False

    def export_data_file(self, target_path=None) -> bool:
        """Export data in CSV file"""
        if not target_path:
            if not self.is_exportable():
                QMessageBox.warning(
                    self, "No Data", "There is no data to save to CSV."
                )
                return False

            # Construct the default file name from the QUrl of the video file
            default_target_path = (
                os.path.dirname(self.media.path())
                + "/"
                + os.path.splitext(os.path.basename(self.media.path()))[0]
                + ".csv"
            )

            target_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save CSV",
                default_target_path,
                "CSV Files (*.csv);;All Files (*)",
            )
        if target_path:
            with open(target_path, "w", newline="") as f:
                writer = csv.writer(f, delimiter=self.csv_delimiter)
                # Write headers
                writer.writerow(header for header in TimePane.CSV_HEADERS)

                # Write data
                for timeline in sorted(
                    self.window.time_pane.timelines, key=lambda x: x.name
                ):
                    for annotation in timeline.annotations:
                        comment = annotation.comment.replace('"', '\\"')
                        row = [
                            timeline.name,
                            annotation.event.name,
                            annotation.start_time,
                            annotation.end_time,
                            annotation.end_time - annotation.start_time,
                            comment,
                        ]
                        writer.writerow(row)
            self.window.time_pane.data_needs_save = False
            return True
        return False

    def is_exportable(self) -> bool:
        """Return true if the media file is exportable"""
        return (
            self.window.video.mediaplayer is not None
            and self.window.time_pane is not None
            and self.window.time_pane.timelines
            and self.has_annotations()
        )

    def export_config_file(self, target_path=None):
        config = Config(target_path)

        config["timelines"] = [
            {
                "name": timeline.name,
                "events": [
                    {"name": event.name, "color": event.color.name()}
                    for event in timeline.events
                ],
            }
            for timeline in self.window.time_pane.timelines
        ]

        if self.coders:
            config["coders"] = self.coders.to_list()

        # Write data
        config.save()

    def no_video_loaded(self):
        dialog = OpenProjectDialog(self.window)
        dialog.exec()


class OpenProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open a project")

        self.layout = QVBoxLayout(self)

        self.open_video_btn = QPushButton(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "Open video",
            self,
        )
        self.open_project_btn = QPushButton(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon),
            "Open project",
            self,
        )

        self.buttons = QDialogButtonBox(self)
        self.buttons.addButton(
            self.open_video_btn, QDialogButtonBox.ButtonRole.AcceptRole
        )
        self.buttons.addButton(
            self.open_project_btn, QDialogButtonBox.ButtonRole.AcceptRole
        )
        self.buttons.addButton(QDialogButtonBox.StandardButton.Cancel)

        self.buttons.clicked.connect(self.perform_action)
        self.buttons.rejected.connect(self.reject)

        self.layout.addWidget(
            QLabel("Choose a video or a project file to start coding")
        )
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)

    def perform_action(self, button):
        if button == self.open_video_btn:
            self.parent().files.open_video(self)
        elif button == self.open_project_btn:
            self.parent().files.open_project(self)
        self.accept()
