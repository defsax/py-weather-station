import yaml
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox


class DropDown(QWidget):
  def __init__(self):
    super(DropDown, self).__init__()
    
    combobox = QComboBox()
    self.config = yaml.safe_load(open("/home/pi/code/python/py-weather-station/settings.yml"))
    for i, item in enumerate(self.config['mission_ids']):
        print(item)
        combobox.addItem(item)
    
    # Connect signals to the methods.
    combobox.activated.connect(self.activated)
    combobox.currentTextChanged.connect(self.text_changed)
    combobox.currentIndexChanged.connect(self.index_changed)
    
    
    layout = QHBoxLayout()
    layout.addWidget(combobox)
    self.setLayout(layout)

  def handleButton(self):
    print("settings button")  

  def activated(Self, index):
    print("Activated index:", index)

  def text_changed(self, s):
    print("Text changed:", s)

  def index_changed(self, index):
    print("Index changed", index)
