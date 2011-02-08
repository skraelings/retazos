#!/usr/bin/python2
# -*- coding: utf-8 -*-
"""
2011 (c) Reynaldo Baquerizo <reynaldomic001@gmail.com>
"""
from __future__ import print_function
import sys
from random import random

from PyQt4.QtGui import *
from PyQt4.QtCore import *

SCENESIZE = (320, 240)

class Site(QGraphicsItem):

    def __init__(self, rect, weight):
        super(Site, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsFocusable)
        self.rect = rect
        self.weight = weight            # Controls how much the Site is allowed
                                        # to move. Range is 0-1. If 0, no movemente.
        self.setFocus()

    def boundingRect(self):
        return self.rect

    # call by scene.update !!
    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(Qt.blue))
        painter.drawRect(self.rect)

class SiteDialog(QDialog):

    def __init__(self, parent=None):
        super(SiteDialog, self).__init__(parent)

        self.weight_label = QLabel("Weight: ")
        self.weight_spinbox = QDoubleSpinBox()
        self.weight_spinbox.setRange(0, 1)
        self.weight_spinbox.setSingleStep(0.01)

        ok_button = QPushButton("&Ok")
        cancel_button = QPushButton("Cancel")

        properties_layout = QHBoxLayout()
        # properties_layout.addStretch()
        properties_layout.addWidget(self.weight_label)
        properties_layout.addWidget(self.weight_spinbox)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        layout = QVBoxLayout()
        layout.addLayout(properties_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.connect(ok_button, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancel_button, SIGNAL("clicked()"), self, SLOT("reject()"))
        self.setWindowTitle("Site Properties")

class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, *SCENESIZE)
        self.view.setScene(self.scene)

        self.siteLabel = QLabel("Site: ")

        button_layout = QVBoxLayout()
        for text, slot in (("Add &Site", self.add_site),):
            button = QPushButton(text)
            self.connect(button, SIGNAL("clicked()"), slot)
            button_layout.addWidget(button)
        button_layout.addStretch()

        display_layout = QVBoxLayout()
        display_layout.addWidget(self.view)
        display_layout.addWidget(self.siteLabel)
        display_layout.addStretch()

        layout = QHBoxLayout()
        layout.addLayout(display_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_site(self):
        form = SiteDialog()
        if form.exec_():
            weight = form.weight_spinbox.value()
            self.scene.addItem(Site(QRectF(random() * SCENESIZE[0],
                                           random() * SCENESIZE[1],
                                           8, 8), weight))
            self.scene.update()

def main():
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
