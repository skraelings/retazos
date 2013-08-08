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

class Site(QGraphicsItem):

    def __init__(self, rect, weight, label_widget, color=(255, 46, 0, 128)):
        """
        Site's representation

        Parameters
        ----------
        rect : QRectF
            Keeps position and size
        weight : float
            Determines how much the site is allowed to move. Value in the range
            0-1. If 0, no movement.
        label_widget : QLabel
            When a site is selected, this label is used in the main dialog to
            display information about it (e.g. site's coordinates)
        color : tuple
            Site's color when not selected. The tuple's values represents red,
            green, blue and alpha channel.
        """
        super(Site, self).__init__()
        self.setFlags(QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemIsMovable |
                      QGraphicsItem.ItemIsFocusable)
        self.rect = rect
        self.weight = weight
        self.color = color
        self.label_widget = label_widget
        self.setFocus()

    def boundingRect(self):
        return self.rect

    # call by scene.update !!
    def paint(self, painter, option, widget=None):
        brush = QBrush(QColor(*self.color))
        self.label_widget.setText("")
        if option.state & QStyle.State_Selected:
            brush.setColor(QColor(100, 0, 32, 156))
            self.label_widget.setText("x:%i, y:%i" % (self.pos().x(),
                                                      self.pos().y()))
        painter.setPen(Qt.NoPen)
        painter.setBrush(brush)
        painter.drawEllipse(self.rect)

    # def mousePressEvent(self, event):
    #     view = self.scene().views()[0]
    #     print(view.mapFromScene(self.mapToScene(self.pos())))

class SiteDialog(QDialog):

    def __init__(self, parent=None):
        """Dialog to add a Site instance to the scene"""

        super(SiteDialog, self).__init__(parent)

        self.weight_label = QLabel("Weight: ")
        self.weight_spinbox = QDoubleSpinBox()
        self.weight_spinbox.setRange(0, 1)
        self.weight_spinbox.setSingleStep(0.01)
        self.weight_spinbox.setValue(random())

        ok_button = QPushButton("&Ok")
        cancel_button = QPushButton("Cancel")

        properties_layout = QHBoxLayout()
        properties_layout.addStretch()
        properties_layout.addWidget(self.weight_label)
        properties_layout.addWidget(self.weight_spinbox)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(properties_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.connect(ok_button, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancel_button, SIGNAL("clicked()"), self, SLOT("reject()"))
        self.setWindowTitle("Site Properties")

class MainForm(QDialog):
    SCENESIZE = (320, 240)

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, *self.SCENESIZE)
        self.view.setScene(self.scene)
        self.site_label = QLabel()

        # Layout contains buttons (e.g. "Add Site")
        button_layout = QVBoxLayout()
        for text, slot in (("Add &Site", self.add_site),):
            button = QPushButton(text)
            self.connect(button, SIGNAL("clicked()"), slot)
            button_layout.addWidget(button)
        button_layout.addStretch()

        # Layout contains a QGraphicsView. The QLabel displays information of a
        # selected Site
        display_layout = QVBoxLayout()
        display_layout.addWidget(self.view)
        display_layout.addWidget(self.site_label)

        # Main layout
        layout = QHBoxLayout()
        layout.addLayout(display_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_site(self):
        """Adds a new Site instance to the scene"""
        form = SiteDialog()
        rect = QRectF(random() * self.SCENESIZE[0],
                      random() * self.SCENESIZE[1],
                      64, 64)
        if form.exec_():
            weight = form.weight_spinbox.value()
            self.scene.addItem(Site(rect, weight, label_widget=self.site_label))
            self.scene.clearSelection()
            self.scene.update()

def main(args):
    app = QApplication(args)
    form = MainForm()
    form.showMaximized()
    app.exec_()

if __name__ == '__main__':
    main(sys.argv)
