# This Python file uses the following encoding: utf-8
import json
import os
import uuid
from typing import List

import numpy as np
import psutil
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QThread, QTimer
from PyQt6.QtGui import QMovie

from PyQt6.QtWidgets import QFileDialog, QLayout

from physiolabxr.configs.GlobalSignals import GlobalSignals
from physiolabxr.configs.configs import AppConfigs
from physiolabxr.exceptions.exceptions import MissingPresetError, UnsupportedLSLDataTypeError, RenaError
from physiolabxr.configs.config import SCRIPTING_UPDATE_REFRESH_INTERVAL
from physiolabxr.presets.PresetEnums import DataType, PresetType
from physiolabxr.presets.Presets import Presets
from physiolabxr.presets.ScriptPresets import ScriptPreset, ScriptOutput
from physiolabxr.scripting.RenaScript import RenaScript
from physiolabxr.scripting.script_utils import start_rena_script, get_target_class_name
from physiolabxr.scripting.scripting_enums import ParamChange, ParamType
from physiolabxr.configs.shared import SCRIPT_STOP_SUCCESS, SCRIPT_PARAM_CHANGE, SCRIPT_STOP_REQUEST
from physiolabxr.sub_process.TCPInterface import RenaTCPInterface
from physiolabxr.threadings import workers
from physiolabxr.threadings.WaitThreads import start_wait_for_response
from physiolabxr.ui.PoppableWidget import Poppable
from physiolabxr.ui.ScriptConsoleLog import ScriptConsoleLog
from physiolabxr.ui.ScriptingInputWidget import ScriptingInputWidget
from physiolabxr.ui.ScriptingOutputWidget import ScriptingOutputWidget
from physiolabxr.ui.ParamWidget import ParamWidget
from physiolabxr.ui.ui_shared import script_realtime_info_text
from physiolabxr.utils.Validators import NoCommaIntValidator
from physiolabxr.utils.buffers import DataBuffer, click_on_file
from physiolabxr.utils.networking_utils import send_data_dict
from physiolabxr.presets.presets_utils import get_stream_preset_names, get_experiment_preset_streams, \
    get_experiment_preset_names, get_stream_preset_info, is_stream_name_in_presets, remove_script_from_settings

from physiolabxr.utils.ui_utils import add_presets_to_combobox, \
    another_window, update_presets_to_combobox, validate_script_path, show_label_movie, get_int_from_line_edit
from physiolabxr.ui.dialogs import dialog_popup

class ScriptingGraphicWidget(QtWidgets.QWidget):
    def __init__(self, parent_widget: QtWidgets.QWidget, main_window, port, gscript_preset: ScriptPreset):
        super().__init__(parent_widget)
        self.ui = uic.loadUi(AppConfigs()._ui_ScriptingGraphicWidget, self)

        self.parent = parent_widget
        self.port = port
        self.script = None
        self.input_widgets = []
        self.output_widgets = []
        self.param_widgets = []
        self.main_window = main_window

        self.ui.addNewStateButton.clicked.connect(self.add_new_state_widget)

        self.state_widgets = []

    def add_new_state_widget(self):
        state_widget_ui = uic.loadUi(AppConfigs()._ui_ScriptingState)
        scroll_area_layout = self.ui.scrollAreaWidgetContents2.layout()
        position_to_insert = scroll_area_layout.count() - 1
        scroll_area_layout.insertWidget(position_to_insert, state_widget_ui)