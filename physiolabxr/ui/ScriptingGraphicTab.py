# This Python file uses the following encoding: utf-8

from PyQt6 import QtWidgets, uic

from physiolabxr.configs import config
from physiolabxr.configs.GlobalSignals import GlobalSignals
from physiolabxr.configs.configs import AppConfigs
from physiolabxr.presets.Presets import Presets
from physiolabxr.threadings.WaitThreads import start_wait_for_target_worker
from physiolabxr.ui.ScriptingWidget import ScriptingWidget




class ScriptingGraphicTab(QtWidgets.QWidget):
    """
    ScriptingTab receives data from streamwidget during the call of process_LSLStream_data
    ScriptingTab forward the data to the scriptingwidget that is actively running. ScriptingTab
    does so by calling the push_data function in scripting widget which forward the data
    through ZMQ to the scripting process

    """
    def __init__(self, parent):
        super().__init__()
        self.ui = uic.loadUi(AppConfigs()._ui_ScriptingGraphicTab, self)

        self.add_button.clicked.connect(self.add_script_clicked)

    def add_script_clicked(self):
        print("add script clicked")