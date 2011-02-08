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

class Site(QGraphicsEllipseItem):

    def __init__(self, rect, weight):
        super(Site, self).__init__(rect)
        self.setFlags(QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsFocusable)
        self.rect = rect
        self.weight = weight            # Controls how much the Site is allowed
                                        # to move
        self.setFocus()

class SiteDialog(QDialog):

    def __init__(self, parent=None):
        super(SiteDialog, self).__init__(parent)

        self.weightSpinBox = QDoubleSpinBox()
        self.weightSpinBox.setRange(0, 1)
        self.weightSpinBox.setSingleStep(0.01)

        okButton = QPushButton("&Ok")
        cancelButton = QPushButton("Cancel")

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        layout = QVBoxLayout()
        layout.addWidget(self.weightSpinBox)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancelButton, SIGNAL("clicked()"), self, SLOT("reject()"))
        self.setWindowTitle("Site Properties")

class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, *SCENESIZE)
        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setScene(self.scene)

        self.siteLabel = QLabel("Site: ")

        buttonLayout = QVBoxLayout()
        for text, slot in (("Add &Site", self.add_site),):
            button = QPushButton(text)
            self.connect(button, SIGNAL("clicked()"), slot)
            buttonLayout.addWidget(button)
        buttonLayout.addStretch()

        displayLayout = QVBoxLayout()
        displayLayout.addWidget(self.view)
        displayLayout.addWidget(self.siteLabel)
        displayLayout.addStretch()

        layout = QHBoxLayout()
        layout.addLayout(displayLayout)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def add_site(self):
        form = SiteDialog()
        if form.exec_():
            weight = form.weightSpinBox.value()
            self.scene.addItem(Site(QRectF(random() * SCENESIZE[0],
                                           random() * SCENESIZE[1],
                                           8, 8), weight))

def main():
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
