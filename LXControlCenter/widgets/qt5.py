#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
#  lx-control-center
#
#       Copyright 2016 (c) Julien Lavergne <gilir@ubuntu.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from functools import partial
import sys

import logging

# For access settings
import os
import os.path

from LXControlCenter.base import Base

class Qt5App(Base):
    def __init__(self):
        Base.__init__(self)

    def draw_ui(self):
        logging.info("Qt5.draw_ui: enter function")
        if (self.mode == "main-UI"):
            if (self.standalone_module == None):
                self.icon_view_button.setEnabled(False)
                self.edit_view_button.setEnabled(True)
                self.pref_view_button.setEnabled(True)
            self.build_icon_view()
        elif (self.mode == "edit-UI"):
            if (self.standalone_module == None):
                self.icon_view_button.setEnabled(True)
                self.edit_view_button.setEnabled(False)
                self.pref_view_button.setEnabled(True)
            self.build_edit_view()
        elif (self.mode == "pref-UI"):
            if (self.standalone_module == None):
                self.icon_view_button.setEnabled(True)
                self.edit_view_button.setEnabled(True)
                self.pref_view_button.setEnabled(False)
            self.build_pref_view()
        elif (self.mode == "module-UI"):
            if (self.standalone_module == None):
                self.icon_view_button.setEnabled(True)
                self.edit_view_button.setEnabled(True)
                self.pref_view_button.setEnabled(True)
            self.build_module_view()
        elif (self.mode == "edit-item-UI"):
            if (self.standalone_module == None):
                self.icon_view_button.setEnabled(True)
                self.edit_view_button.setEnabled(True)
                self.pref_view_button.setEnabled(True)
        self.window.show()

    def build_toolbar(self):
        # Header
        # Icon view - Edit View - Preferences - Search
        self.header_box = QHBoxLayout()
        self.layout.addLayout(self.header_box)

        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.on_search)
        self.header_box.insertWidget(3, self.search_box, 0, Qt.AlignRight)

        self.icon_view_button = QPushButton("Icon")
        self.icon_view_button.clicked.connect(self.on_icons_mode_menu_click)
        self.header_box.insertWidget(0, self.icon_view_button, 0, Qt.AlignLeft)

        self.edit_view_button = QPushButton("Edit")
        self.edit_view_button.clicked.connect(self.on_edit_mode_menu_click)
        #TODO Implement edit view
        #self.header_box.insertWidget(1, self.edit_view_button, 0, Qt.AlignLeft)

        self.pref_view_button = QPushButton("Preferences")
        self.pref_view_button.clicked.connect(self.on_pref_mode_menu_click)
        #TODO Implement pref view
        #self.header_box.insertWidget(2, self.pref_view_button, 0, Qt.AlignLeft)

    def clean_main_view(self):
        for i in reversed(range(self.content_ui_vbox.count())): 
            self.content_ui_vbox.itemAt(i).widget().setParent(None)

    def build_pref_view(self):
        #TODO
        self.clean_main_view()

    def build_generic_icon_view(self, type_view):
        logging.info("Qt5.build_generic_icon_view: enter function")
        items_to_draw = self.items_visible_by_categories

        if (type_view == "all"):
            items_to_draw = self.items_by_categories

        row = 0
        for category in items_to_draw:
            groupBox = QGroupBox(category)
            groupGrid = QGridLayout()
            groupGrid.setAlignment(Qt.AlignCenter)
            groupBox.setLayout(groupGrid)
            self.content_ui_vbox.addWidget(groupBox, row, 0)
            row = row + 1
            groupCol = 0
            groupRow = 0
# Need Qt 5.7 https://woboq.com/blog/qicon-reads-gtk-icon-cache-in-qt57.html
            for i in items_to_draw[category]:
                if (i.icon_type == "fix"):
                    pixbuf = QIcon(i.icon)
                elif (i.icon_type == "themed"):
                    pixbuf = QIcon.fromTheme(i.icon, QIcon.fromTheme(self.icon_fallback))
                else:
                    pixbuf = QIcon.fromTheme(self.icon_fallback)

                # Add icon button
                image = QToolButton()
                image.setIcon(pixbuf)
                image.setIconSize(QSize(self.icon_view_icons_size, self.icon_view_icons_size))

                if (self.mode == "main-UI"):
                    image.clicked.connect(partial(self.on_item_activated, i))
                else:
                    image.clicked.connect(partial(self.on_item_edit_activated, i))

                # Add text for icon
                text = QLabel()
                text.setText(i.name)
                text.setWordWrap(True)
                text.setAlignment(Qt.AlignCenter)

                if (groupCol > self.icon_view_columns):
                    groupCol = 0
                    groupRow = groupRow + 1

                iconview = QWidget()
                vbox = QVBoxLayout()
                vbox.addWidget(image, Qt.AlignCenter, Qt.AlignCenter)
                vbox.addWidget(text, Qt.AlignCenter, Qt.AlignCenter)
                iconview.setLayout(vbox)

                groupGrid.addWidget(iconview, groupRow, groupCol, Qt.AlignLeft, Qt.AlignLeft)
                groupCol = groupCol + 1

    def activate_module_view(self):
        self.content_ui_vbox.addWidget(self.module_class.main_box)

    def on_item_activated(self, item):
        logging.debug("Qt5.on_item_activated: click activated")
        logging.debug("Qt5.on_item_activated: path = %s" % item.path)
        self.on_item_activated_common(item.path)

    def on_item_edit_activated(self, item):
        logging.debug("Qt5.on_item_edit_activated: click activated")
        logging.debug("Qt5.on_item_edit_activated: path = %s" % item.path)
        self.build_edit_item_view(item.path)

    def build_edit_item_view(self, path):
        # TODO
        self.clean_main_view()
        self.mode = "edit-item-UI"
        self.draw_ui()

    def on_resize(self):
        #TODO
        # Since Qt doesn t have a resize signal ...
        #Find a better ay that subclassing indo : https://stackoverflow.com/questions/43126721/pyqt-detect-resizing-in-widget-window-resized-signal
        pass

    def on_search(self, text):
        logging.info("Qt5.on_search: enter function")
        self.search_string = text
        self.draw_ui()

    def destroy(self, widget, data=None):
        #TODO Since Qt doesn t have a close signal ...
        self.util.save_object("keyfile", self.keyfile_settings, os.path.join("lx-control-center", "settings.conf"))

    def main(self):
        self.app = QApplication(sys.argv)

        # Main WIndow
        self.window = QWidget()
        self.layout = QVBoxLayout(self.window)
        self.scroll = QScrollArea()
        self.window.setWindowTitle(self.window_title)
        self.window.setWindowIcon(QIcon.fromTheme(self.window_icon))
        self.window.resize(self.window_size_w, self.window_size_h)

        # Content UI
        self.widget = QWidget()
        self.content_ui_vbox = QGridLayout()
        self.vbox1 = QVBoxLayout()
        self.vbox1.addLayout(self.content_ui_vbox)
        self.widget.setLayout(self.vbox1)
        self.widget.show()

        if (self.standalone_module == None):
            self.build_toolbar()

        #Function to launch at startup
        self.init()
        self.generate_view()
        self.draw_ui()

        # Add content Widget to ScrollArea, and ScrollArea to window layout
        self.scroll.setWidget(self.widget)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll) 

        sys.exit(self.app.exec_())
