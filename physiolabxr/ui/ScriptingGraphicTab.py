# This Python file uses the following encoding: utf-8

from PyQt6 import QtWidgets, uic
from physiolabxr.ui.ScriptingGraphicWidget import ScriptingGraphicWidget
from physiolabxr.configs.configs import AppConfigs
from physiolabxr.configs import config
from physiolabxr.configs.GlobalSignals import GlobalSignals
from physiolabxr.presets.Presets import Presets
from physiolabxr.threadings.WaitThreads import start_wait_for_target_worker

class ScriptingGraphicTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = uic.loadUi(AppConfigs()._ui_ScriptingGraphicTab, self)
        self.parent = parent

        self.AddScriptBtn.clicked.connect(self.add_gscript_clicked)

        self.scriptingWidgetsContainer = self.ui.findChild(QtWidgets.QWidget, "ScriptingWidgetScrollContent")
        self.GraphicScriptingWidgetsLayout = self.scriptingWidgetsContainer.layout()

        self.gscript_widgets = {}

    def add_gscript_clicked(self):
        self.add_gscript_widget()

    def add_gscript_widget(self, gscript_preset=None):
        port = config.scripting_port + 4 * len(self.gscript_widgets)
        gscript_widget = ScriptingGraphicWidget(
            parent_widget=self.scriptingWidgetsContainer,
            main_window=self.parent,
            port=port,
            gscript_preset=gscript_preset
        )

        self.GraphicScriptingWidgetsLayout.addWidget(gscript_widget)

        widget_id = len(self.gscript_widgets)
        self.gscript_widgets[widget_id] = gscript_widget