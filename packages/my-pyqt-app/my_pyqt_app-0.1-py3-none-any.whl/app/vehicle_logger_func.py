#!/usr/bin/env python3.8
"""
Functions called by widgets on main GUI are here.

"""

import os
import re
import h5py
import yaml
import ping3
import subprocess
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import can
import cantools
import pytest
from time import sleep
# from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from zipfile import ZipFile
from artifactory import ArtifactoryPath
from shutil import copytree, rmtree, make_archive
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QGuiApplication, QPixmap, QColor, QBrush, QDesktopServices, QIcon
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QListWidgetItem, QDialog, \
    QTableWidget, QVBoxLayout, QDialogButtonBox, QTableWidgetItem, QInputDialog, QMessageBox, QLineEdit, QLabel
from _resources.local_keywords import *
import _resources.ssh_keywords as ssh_keywords
from _resources.get_vehicle_logs import *
from _resources.exception_handling import *
from vehicle_logger_logic import vehicle_log_gui_logic
from gui_workers import Worker_for_fetch_topics, Worker_for_get_vehicle_logs, \
    Worker_for_hostlog_start_logging, Worker_for_progressbar, \
    Worker_for_xcp_domain_controller, Worker_for_run_bundle_script, \
    Worker_for_run_tracelogger_script
from importlib import util
from _resources.decoder import decode_flcw_images_module

if util.find_spec("xcplib"):
    from xcplib import Xcp


class vehicle_logger_func(metaclass=CombinedMeta):
    def __init__(self) -> None:
        self.ui = vehicle_log_gui_logic()
        # Set up the user interface from Designer.
        self.ui.setupUi(self)
        self.DCF_PATH = ""
        self.DCF_TDF_PATH = ""
        self.DCF_BIN_PATH = ""
        self.TIMER = 0
        self.ui.set_initial_btn_state()
        self.dcf_watcher = None
        self.load_yaml_file()
        self.latest_hostlog_ver = self.get_latest_hostlog_version()

    def load_yaml_file(self, *args, **kwargs):
        with open("gui_parameters.yaml", "r") as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
            self.DCF_PATH = self.data["dcf_configuration"]["execution_path"]
            self.WINSCP_PATH = self.data["winscp_path"]
            self.vehicle_test = ssh_keywords.ssh_keywords(self.WINSCP_PATH)
            self.CAN_LOGS_PATH = self.data["dcf_configuration"]["log_path"]["can_mri_logs_path"]
            self.IMAGE_DECODED_PATH = self.data["dcf_configuration"]["log_path"]["image_decoded_dcf"]
            self.DLT_LOG_PATH = self.data["dcf_configuration"]["log_path"]["dlt_logs_path"]
            self.COLLECTED_DLT_DCF_CAN_LOGS = self.data["dcf_configuration"]["log_path"]["collected_dlt_dcf_can_logs"]
            self.DCF_HDF5_PATH = self.data["dcf_configuration"]["log_path"]["hdf5_logs_path"]
            self.A2L_S19_BASE_FOLDER = self.data["xcp_paths"]["adas_domain_controller"]
            self.DCF_BASE_PATH = os.getcwd()
            self.DCF_LOG_DESTINATION_FOLDER = self.DCF_BASE_PATH
            self.DCF_BIN_PATH = f"{self.DCF_BASE_PATH}\\bin"
            self.DCF_TDF_PATH = f"{self.DCF_BASE_PATH}\\tdf"
            self.ZEN_DECODED_PATH = f"{self.DCF_BASE_PATH}\\decoded_Zenseact"
            self.VCC_DECODED_PATH = f"{self.DCF_BASE_PATH}\\decoded_VCC"
            self.TOPICS_TO_BE_LOGGED = self.data["dcf_configuration"]["topics_to_adas"]
            self.VEHICLE_LOG_COMMENT = self.data["dcf_configuration"]["log_path"]['vehilog_comment']
            self.OSB_PATH = self.data["osb_paths"]["execution_path"]
            self.LOG_FILES_PATH = self.data["dcf_configuration"]["log_path"]["log_files_folder"]
            self.ARA_USER_NAME = self.data["dcf_configuration"]["artifactory_user"]
            self.ARA_PWD = self.data["dcf_configuration"]["ara_api"]
            self.LOG_SET_LIST = [self.DCF_TDF_PATH, self.DCF_BIN_PATH, self.CAN_LOGS_PATH,
                                 self.VCC_DECODED_PATH, self.ZEN_DECODED_PATH, self.DLT_LOG_PATH,
                                 self.VEHICLE_LOG_COMMENT, self.LOG_FILES_PATH]
            self.CS_MANIFEST = f"{self.DCF_BASE_PATH}\\log_files\\cs-manifest.yml"
            self.ARA_DCF_URL = self.data["dcf_configuration"]["ara_url_dcf"]
            self.FAULT_MATRIX = self.data["fault_matrix"]
            self.CAM_REC_INDEX = self.data["dcf_configuration"]["camera_index"]
            self.HEALTH_MONITOR = self.data["health_monitor_output_system_fault"]
            self.CHANGE_LOG = f"{self.DCF_PATH}\\docs\\CHANGELOG.md"
            self.check_hostlog_version()

            # Sets up base folders
            self.set_up_log_folders()
            self.OPERATION_STATUS = False
            self.fill_tdf_list(self.data)
            self.get_ip_address()
            self.sga2hpa()
            # check if aca is available
            self.check_aca(self.ZEN_DECODED_PATH)

        if self.DCF_PATH != "":
            self.ui.status_lbl.setText(
                f"Configuration loaded.\nTDF is set to limited scope as default.\n{self.TOPICS_TO_BE_LOGGED}")
            self.ui.start_logging_btn.setEnabled(True)
            self.ui.fetch_tdf_btn.setEnabled(True)
            self.ui.deploy_btn.setEnabled(True)
            self.ui.decode_btn.setEnabled(True)
            self.ui.aeb_analysis_btn.setEnabled(True)
            self.ui.ms_signal_analysis_btn.setEnabled(True)
            # self.ui.aam_signal_analysis_btn.setEnabled(True)
            self.ui.domain_controller_signal_analysis_btn.setEnabled(True)
            self.ui.fault_matrix_btn.setEnabled(True)
            self.ui.health_monitor_fault_btn.setEnabled(True)
            self.ui.can_check_btn.setEnabled(True)
            self.ui.generate_report_btn.setEnabled(True)
            self.ui.aeb_pytest_btn.setEnabled(True)
            self.ui.lat_pytest_btn.setEnabled(True)
            self.ui.rsi_pytest_btn.setEnabled(True)
            self.ui.ddaw_pytest_btn.setEnabled(True)
            self.ui.pa_pytest_btn.setEnabled(True)
            self.ui.pap_pytest_btn.setEnabled(True)
        else:
            self.ui.status_lbl.setText("check Config file")
        self.ui.progressBar.setProperty("value", 100)
        self.ui.set_waiting_for_request_state()

        @QtCore.pyqtSlot(str)
        def file_changed():
            print('gui_parameters file changed. Updating loaded config.')
            self.load_yaml_file()

        if not self.dcf_watcher:
            dcf_config_file = f"{self.DCF_BASE_PATH}/{file.name}"
            self.dcf_watcher = QtCore.QFileSystemWatcher([dcf_config_file])
            self.dcf_watcher.fileChanged.connect(file_changed)

    # return a fig contains all necessary signals for aeb analysis
    def signals_aeb_analysis_necessary(self, *args, **kwargs):
        fig, ax = plt.subplots(5, 1, figsize=(18, 12), sharex=True)

        hdf5_file1 = f"{self.get_latest_folder_in_directory(self.ZEN_DECODED_PATH)}/zen_qm_feature_a.hdf5"
        hdf5_file2 = f"{self.get_latest_folder_in_directory(self.ZEN_DECODED_PATH)}/zen_asil_feature_a.hdf5"
        vcc_decoded_file = glob(f"{self.VCC_DECODED_PATH}/*.hdf5")
        latest_vcc_decoded_file = max(vcc_decoded_file, key=os.path.getmtime)
        hdf5_file3 = latest_vcc_decoded_file

        with h5py.File(hdf5_file1, 'r') as file1, h5py.File(hdf5_file2, 'r') as file2, h5py.File(hdf5_file3,
                                                                                                 'r') as file3:
            # Axis 0
            aeb_dataset = \
            file1["zen_qm_feature_a"]["emergency_brake_request"]["data"]["emergency_braking_request"]["unitless"][
                "value"]
            aeb_timestamp_dataset = file1["zen_qm_feature_a"]["emergency_brake_request"]["zeader"]["timestamp_ns"]
            aeb_signal = aeb_dataset[:]
            aeb_timestamp = aeb_timestamp_dataset[:]

            fcw_dataset = file1["zen_qm_feature_a"]["warning_request_from_cw"]["data"]["request"]["unitless"]["value"]
            fcw_timestamp_dataset = file1["zen_qm_feature_a"]["warning_request_from_cw"]["zeader"]["timestamp_ns"]
            fcw_timestamp = fcw_timestamp_dataset[:]
            fcw_signal = fcw_dataset[:]

            ms_t1_signal_data = file3["hostlog"]["channel_26"]["topic_1"]["data"]["brake_request_v1"][
                "deceleration_enable_"]
            ms_t1_signal_timestamp_data = file3["hostlog"]["channel_26"]["topic_1"]["timestamp"]
            ms_t1_signal = ms_t1_signal_data[:]
            ms_t1_signal_timestamp = ms_t1_signal_timestamp_data[:]

            asil_thread_validator_dataset = \
            file2["zen_asil_feature_a"]["threat_validator_output"]["data"]["validated_acceleration_request"][
                "acceleration_request"]["emergency_acceleration_request"]["unitless"]["value"]
            asil_thread_validator_timestamp_dataset = file2["zen_asil_feature_a"]["threat_validator_output"]["zeader"][
                "timestamp_ns"]
            asil_thread_validator_signal = asil_thread_validator_dataset[:]
            asil_thread_validator_timestamp = asil_thread_validator_timestamp_dataset[:]

            ax[0].plot(aeb_timestamp, aeb_signal,
                       label="zen_qm_feature_a.emergency_brake_request.data.emergency_braking_request.unitless.value")
            ax[0].plot(fcw_timestamp, fcw_signal,
                       label="zen_qm_feature_a.warning_request_from_cw.data.request.unitless.value")
            ax[0].plot(ms_t1_signal_timestamp, ms_t1_signal,
                       label="[Incoming ManagerSafe app] hostlog.channel_26.topic_1.data.brake_request_v1.deceleration_enable_")
            ax[0].plot(asil_thread_validator_timestamp, asil_thread_validator_signal,
                       label="zen_asil_feature_a.threat_validator_output.data.validated_acceleration_request.acceleration_request.emergency_acceleration_request.unitless.value")
            ax[0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[0].set_ylabel('enable_signals')
            ax[0].set_facecolor('black')
            ax[0].legend()

            # Axis 1
            aam_enable_signal_dataset = file3["hostlog"]["channel_84"]["topic_0"]["data"][
                "emergency_braking_state_is_enable"]
            aam_enable_signal_timestamp_dataset = file3["hostlog"]["channel_84"]["topic_0"]["timestamp"]
            aam_enable_signal = aam_enable_signal_dataset[:]
            aam_enable_signal_timestamp = aam_enable_signal_timestamp_dataset[:]

            ms_t2_signal_data = file3["hostlog"]["channel_26"]["topic_2"]["data"]["deceleration_request_enable"]
            ms_t2_signal_timestamp_data = file3["hostlog"]["channel_26"]["topic_2"]["timestamp"]
            ms_t2_signal = ms_t2_signal_data[:]
            ms_t2_signal_timestamp = ms_t2_signal_timestamp_data[:]

            ax[1].plot(ms_t2_signal_timestamp, ms_t2_signal,
                       label="[Outgoing ManagerSafe app]hostlog.channel_26.topic_2.data.deceleration_request_enable")
            ax[1].plot(aam_enable_signal_timestamp, aam_enable_signal,
                       label="[AAM]hostlog.channel_84.topic_0.data.emergency_braking_state_is_enable")
            ax[1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[1].set_ylabel('enable_signals')
            ax[1].set_facecolor('black')
            ax[1].legend()

            # Axis 2
            ms_brake_request_dataset = file3["hostlog"]["channel_26"]["topic_1"]["data"]["brake_request_v1"][
                "deceleration_request_"]
            ms_brake_request_timestamp_dataset = file3["hostlog"]["channel_26"]["topic_1"]["timestamp"]

            ms_brake_request_signal = ms_brake_request_dataset[:]
            ms_brake_request_timestamp = ms_brake_request_timestamp_dataset[:]

            aam_acceleration_level_dataset = file3["hostlog"]["channel_83"]["topic_0"]["data"]["braking_request"][
                "deceleration_request_"]
            aam_acceleration_level_timestamp_dataset = file3["hostlog"]["channel_83"]["topic_0"]["timestamp"]

            aam_acceleration_level_signal = aam_acceleration_level_dataset[:]
            aam_acceleration_level_timestamp = aam_acceleration_level_timestamp_dataset[:]

            asil_speed_reduction_monitor_dataset = \
            file2["zen_asil_feature_a"]["speed_reduction_monitor_output"]["data"]["validated_acceleration_request"][
                "maximum_acceleration_limit"]["meters_per_second2"]["value"]
            asil_speed_reduction_monitor_timestamp_dataset = \
            file2["zen_asil_feature_a"]["speed_reduction_monitor_output"]["zeader"]["timestamp_ns"]

            asil_speed_reduction_monitor_signal = abs(asil_speed_reduction_monitor_dataset[:])
            asil_speed_reduction_monitor_timestamp = asil_speed_reduction_monitor_timestamp_dataset[:]

            ax[2].plot(ms_brake_request_timestamp, ms_brake_request_signal,
                       label="[Incoming ManagerSafe app] hostlog.channel_26.topic_1.data.brake_request_v1.deceleration_request_")
            ax[2].plot(aam_acceleration_level_timestamp, aam_acceleration_level_signal,
                       label="[AAM]hostlog.channel_83.topic_0.data.braking_request.deceleration_request_")
            ax[2].plot(asil_speed_reduction_monitor_timestamp, asil_speed_reduction_monitor_signal,
                       label="zen_asil_feature_a.speed_reduction_monitor_output.data.validated_acceleration_request.maximum_acceleration_limit.meters_per_second2.value")
            ax[2].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[2].set_ylabel('deceleration_request_signals')
            ax[2].set_facecolor('black')
            ax[2].legend()

            # Axis 3
            ms_deceleration_request_dataset = file3["hostlog"]["channel_26"]["topic_2"]["data"][
                "deceleration_request_value"]
            ms_deceleration_request_timestamp_dataset = file3["hostlog"]["channel_26"]["topic_2"]["timestamp"]

            ms_deceleration_request_signal = ms_deceleration_request_dataset[:]
            ms_deceleration_request_timestamp = ms_deceleration_request_timestamp_dataset[:]

            aeb_decel_req_dataset = \
            file1["zen_qm_feature_a"]["emergency_brake_request"]["data"]["requested_deceleration"][
                "meters_per_second2"]["value"]
            aeb_decel_req_timestamp_dataset = file1["zen_qm_feature_a"]["emergency_brake_request"]["zeader"][
                "timestamp_ns"]
            aeb_decel_req_signal = aeb_decel_req_dataset[:]
            aeb_decel_req_timestamp = aeb_decel_req_timestamp_dataset[:]

            ax[3].plot(ms_deceleration_request_timestamp, ms_deceleration_request_signal,
                       label="[Outgoing ManagerSafe app]hostlog.channel_26.topic_2.data.deceleration_request_value")
            ax[3].plot(aeb_decel_req_timestamp, aeb_decel_req_signal,
                       label="zen_qm_feature_a.emergency_brake_request.data.requested_deceleration.meters_per_second2.value")
            ax[3].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[3].set_ylabel('deceleration_request_signals')
            ax[3].set_facecolor('black')
            ax[3].legend()

            # Axis 4
            asil_threat_validated_debug_dataset = \
            file2["zen_asil_feature_a"]["threat_validator_debug"]["data"]["confirmed_threat"]["unitless"]["value"]
            asil_threat_validated_debug_timestamp_dataset = \
            file2["zen_asil_feature_a"]["threat_validator_debug"]["zeader"]["timestamp_ns"]

            asil_threat_validated_debug_signal = asil_threat_validated_debug_dataset[:]
            asil_threat_validated_debug_timestamp = asil_threat_validated_debug_timestamp_dataset[:]

            zen_qm_threat_assessment_dataset = \
            file1["zen_qm_feature_a"]["ca_long_qm_debug"]["data"]["debug_longitudinal_threat_assessment"][
                "intervention_condition"]["primary_target_for_intervention"]["object_attributes"]["id"]["unitless"][
                "value"]
            zen_qm_threat_assessment_timestamp_dataset = file1["zen_qm_feature_a"]["ca_long_qm_debug"]["zeader"][
                "timestamp_ns"]

            zen_qm_threat_assessment_signal = zen_qm_threat_assessment_dataset[:]
            zen_qm_threat_assessment_timestamp = zen_qm_threat_assessment_timestamp_dataset[:]

            ax[4].plot(asil_threat_validated_debug_timestamp, asil_threat_validated_debug_signal,
                       label="zen_asil_feature_a.threat_validator_debug.data.confirmed_threat.unitless.value")
            ax[4].plot(zen_qm_threat_assessment_timestamp, zen_qm_threat_assessment_signal,
                       label="zen_qm_feature_a.ca_long_qm_debug.data.debug_longitudinal_threat_assessment.intervention_condition.primary_target_for_intervention.object_attributes.id.unitless.value")
            ax[4].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[4].set_facecolor('black')
            ax[4].set_ylabel('threat_validator')
            ax[4].legend()

        plt.suptitle('All necessary signals for AEB analysis', fontsize=16)
        plt.tight_layout()
        return fig

    # plot signals for aeb analysis
    def plot_aeb_analysis_necessary_signals(self, *args, **kwargs):
        self.signals_aeb_analysis_necessary().show()

    # return a fig contains all necessary signals for manager safe
    def signals_from_manager_safe(self, *args, **kwargs):
        vcc_decoded_file = glob(f"{self.VCC_DECODED_PATH}/*.hdf5")
        latest_vcc_decoded_file = max(vcc_decoded_file, key=os.path.getmtime)
        hdf5_file = latest_vcc_decoded_file

        with h5py.File(hdf5_file, 'r') as file:
            fig, ax = plt.subplots(5, 1, figsize=(18, 12), sharex=True)

            # Axis 0
            signal_1_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["brake_request_v1"][
                "deceleration_request_"]
            long_velocity_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["velocity_longitudinal"]["nominal_"][
                "value_"]
            signal_1 = signal_1_data[:]
            long_velocity = long_velocity_data[:]

            ax[0].plot(signal_1, label="[MS-input]hostlog.topic_1.data.brake_request_v1.deceleration_request_")
            ax[0].plot(long_velocity, label="hostlog.topic_1.data.velocity_longitudinal.nominal_.value_")
            ax[0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[0].set_facecolor('black')
            ax[0].set_ylabel('MS topic 1 data')
            ax[0].legend()

            # Axis 1
            signal_1_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["brake_request_v1"]["deceleration_enable_"]
            signal_1 = signal_1_data[:]

            ax[1].plot(signal_1, label="[MS-input]hostlog.topic_1.data.brake_request_v1.deceleration_enable_")
            ax[1].set_ylabel('MS topic 1 data')
            ax[1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[1].set_facecolor('black')
            ax[1].legend()

            # Axis 2
            signal_1_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["collision_threat"]["value_"]
            signal_1 = signal_1_data[:]

            ax[2].plot(signal_1, label="[MS-input]hostlog.topic_1.data.collision_threat.value_")
            ax[2].set_ylabel('MS topic 1 data')
            ax[2].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[2].set_facecolor('black')
            ax[2].legend()

            # Axis 3
            signal_1_data = file["hostlog"]["channel_26"]["topic_2"]["data"]["deceleration_request_enable"]
            signal_2_data = file["hostlog"]["channel_26"]["topic_2"]["data"]["deceleration_request_value"]

            signal_1 = signal_1_data[:]
            signal_2 = signal_2_data[:]

            ax[3].plot(signal_1, label="[MS-output]hostlog.topic_2.data.deceleration_request_enable")
            ax[3].plot(signal_2, label="[MS-output]hostlog.topic_2.data.deceleration_request_value")
            ax[3].set_ylabel('MS topic 2 data')
            ax[3].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[3].set_facecolor('black')
            ax[3].legend()

            # Axis 4
            signal_1_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["override_by_throttle"]
            signal_2_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["override_by_throttle_e2e_ok"]

            signal_1 = signal_1_data[:]
            signal_2 = signal_2_data[:]

            ax[4].plot(signal_1, label="[MS-input]hostlog.topic_1.data.override_by_throttle")
            ax[4].plot(signal_2, label="[MS-input]hostlog.topic_1.data.override_by_throttle_e2e_ok")
            ax[4].set_ylabel('MS topic 1 data')
            ax[4].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[4].set_facecolor('black')
            ax[4].legend()

            # Add labels, legend, and title
            plt.xlabel('Time')
            plt.suptitle('Multiple Signals from adas-manager-safe', fontsize=16)
            plt.tight_layout()
            return fig

    # plot signals for manager safe
    def plot_signals_from_manager_safe(self, *args, **kwargs):
        self.signals_from_manager_safe().show()

    # return a fig contains all necessary signals for actuation arbitration manager
    def signals_from_adas_actuation_arbitration_manager(self, *args, **kwargs):
        vcc_decoded_file = glob(f"{self.VCC_DECODED_PATH}/*.hdf5")
        latest_vcc_decoded_file = max(vcc_decoded_file, key=os.path.getmtime)
        hdf5_file = latest_vcc_decoded_file

        with h5py.File(hdf5_file, 'r') as file:
            fig, ax = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

            # Axis 0
            signal_1_data = file["hostlog"]["channel_83"]["topic_0"]["data"]["accel_pedal_percentage"]["position_"]
            # signal_2_data = file["hostlog"]["channel_83"]["topic_0"]["data"]["accel_pedal_percentage"]["pressed_qm_"]
            signal_3_data = file["hostlog"]["channel_83"]["topic_0"]["data"]["braking_request"]["deceleration_request_"]

            signal_1 = signal_1_data[:]
            # signal_2 = signal_2_data[:]
            signal_3 = signal_3_data[:]

            ax[0].plot(signal_1, label="hostlog.topic_0.data.accel_pedal_percentage.position_")
            # ax[0].plot(signal_2, label="hostlog.topic_0.data.accel_pedal_percentage.pressed_qm_")
            ax[0].plot(signal_3, label="hostlog.topic_0.data.braking_request.deceleration_request_")
            ax[0].set_ylabel('AAAM input-channel:83')
            ax[0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[0].set_facecolor('black')
            ax[0].legend()

            # Axis 1
            signal_1_data = file["hostlog"]["channel_84"]["topic_0"]["data"]["emergency_braking_state_is_enable"]
            signal_1 = signal_1_data[:]
            ax[1].plot(signal_1, label="hostlog.topic_0.data.emergency_braking_state_is_enable.")
            ax[1].set_ylabel('AAAM output-channel:84')
            ax[1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[1].set_facecolor('black')
            ax[1].legend()

            # Add labels, legend, and title
            plt.xlabel('Time')
            plt.suptitle('Multiple Signals from adas-actuation-arbitration-manager', fontsize=16)
            plt.tight_layout()
            plt.show()
            return fig

    def plot_signals_from_aca_long(self, *args, **kwargs):
        latest_post_aca_file = f'{self.get_latest_folder_in_directory(self.ZEN_DECODED_PATH)}\\post_aca.hdf5'
        hdf5_file = latest_post_aca_file

        with h5py.File(hdf5_file, 'r') as file:
            fig, ax = plt.subplots(3, 1, figsize=(16, 10), sharex=True)

            # Axis 0
            signal_1_data = file["post_aca"]["adas_actuation_arbitration_status"]["data"]["brake_noticeable"]
            signal_2_data = file["post_aca"]["adas_actuation_arbitration_status"]["data"]["brake_gain_noticeable"]
            signal_3_data = file["post_aca"]["adas_actuation_arbitration_status"]["data"][
                "brake_request_confirmation_mode"]

            signal_1 = signal_1_data[:]
            signal_2 = signal_2_data[:]
            signal_3 = signal_3_data[:]

            ax[0].plot(signal_1, label="brake_noticeable")
            ax[0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[0].set_facecolor('black')
            ax[0].legend()

            ax[1].plot(signal_2, label="brake_gain_noticeable")
            ax[1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[1].set_facecolor('black')
            ax[1].legend()

            ax[2].plot(signal_3, label="brake_request_confirmation_mode")
            ax[2].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[2].set_facecolor('black')
            ax[2].legend()

            # Add labels, legend, and title
            plt.xlabel('Time')
            plt.suptitle('post_aca brake arbitration', fontsize=16)
            plt.tight_layout()
            plt.show()
            return fig

    def plot_signals_from_aca_lat(self, *args, **kwargs):
        latest_post_aca_file = f'{self.get_latest_folder_in_directory(self.ZEN_DECODED_PATH)}\\post_aca.hdf5'
        hdf5_file = latest_post_aca_file

        with h5py.File(hdf5_file, 'r') as file:
            fig, ax = plt.subplots(6, 1, figsize=(16, 10), sharex=True)

            # Axis 0
            signal_1_data = file["post_aca"]["adas_actuation_arbitration_status"]["data"][
                "lateral_control_arbitration_mode"]
            signal_2_data = file["post_aca"]["adas_function_arbitration_external"]["data"]["lateral_control_mode"]
            signal_3_data = file["post_aca"]["adas_function_arbitration_external"]["data"][
                "lateral_control_path_selection"]
            signal_4_data = file["post_aca"]["adas_function_arbitration_external"]["data"][
                "zen_lateral_control_path_selection"]
            signal_5_data = file["post_aca"]["haptic_steering_warning"]["data"]["value"]["unitless"]["value"]
            signal_6_data = file["post_aca"]["lateral_feature_type_input"]["data"]["type"]

            signal_1 = signal_1_data[:]
            signal_2 = signal_2_data[:]
            signal_3 = signal_3_data[:]
            signal_4 = signal_4_data[:]
            signal_5 = signal_5_data[:]
            signal_6 = signal_6_data[:]

            ax[0].plot(signal_1, label="arbitration_status-lateral_control_arbitration_mode")
            ax[0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[0].set_facecolor('black')
            ax[0].legend()

            ax[1].plot(signal_2, label="arbitration_external-lateral_control_mode")
            ax[1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[1].set_facecolor('black')
            ax[1].legend()

            ax[2].plot(signal_3, label="arbitration_external-lateral_control_path_selection")
            ax[2].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[2].set_facecolor('black')
            ax[2].legend()

            ax[3].plot(signal_4, label="arbitration_external-zen_lateral_control_path_selection")
            ax[3].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[3].set_facecolor('black')
            ax[3].legend()

            ax[4].plot(signal_5, label="haptic_steering_warning")
            ax[4].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[4].set_facecolor('black')
            ax[4].legend()

            ax[5].plot(signal_6, label="lateral_feature_type_input")
            ax[5].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[5].set_facecolor('black')
            ax[5].legend()

            # Add labels, legend, and title
            plt.xlabel('Time')
            plt.suptitle('post_aca brake arbitration', fontsize=16)
            plt.tight_layout()
            plt.show()
            return fig

    # plot signals for actuation arbitration manager
    def plot_signals_from_adas_actuation_arbitration_manager(self, *args, **kwargs):
        self.signals_from_adas_actuation_arbitration_manager().show()

    # return a fig contains all necessary signals for domain controller
    def signals_from_domain_controller(self, *args, **kwargs):
        vcc_decoded_file = glob(f"{self.VCC_DECODED_PATH}/*.hdf5")
        latest_vcc_decoded_file = max(vcc_decoded_file, key=os.path.getmtime)
        hdf5_file = latest_vcc_decoded_file

        with h5py.File(hdf5_file, 'r') as file:
            fig, ax = plt.subplots(2, 1, figsize=(18, 10), sharex=True)
            # Axis 0
            sensor_blockage_fc_dataset = \
            file["hostlog"]["channel_97"]["topic_0"]["data"]["configuration_interface_"]["sensor_blockage_"][
                "front_camera_"]
            sensor_blockage_fc_timestamp_dataset = file["hostlog"]["channel_97"]["topic_0"]["timestamp"]
            sensor_blockage_flr_dataset = \
            file["hostlog"]["channel_97"]["topic_0"]["data"]["configuration_interface_"]["sensor_blockage_"][
                "front_looking_radar_"]
            sensor_blockage_flr_timestamp_dataset = file["hostlog"]["channel_97"]["topic_0"]["timestamp"]

            sensor_blockage_fc = sensor_blockage_fc_dataset[:]
            sensor_blockage_fc_timestamp = sensor_blockage_fc_timestamp_dataset[:]
            sensor_blockage_flr = sensor_blockage_flr_dataset[:]
            sensor_blockage_flr_timestamp = sensor_blockage_flr_timestamp_dataset[:]

            ax[0].plot(sensor_blockage_fc_timestamp, sensor_blockage_fc,
                       label="hostlog.channel_97.topic_0.data.configuration_interface_.sensor_blockage_.front_camera_")
            ax[0].plot(sensor_blockage_flr_timestamp, sensor_blockage_flr,
                       label="hostlog.channel_97.topic_0.data.configuration_interface_.sensor_blockage_.front_looking_radar_")
            ax[0].set_ylabel('DC Sensor blockage')
            ax[0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[0].set_facecolor('black')
            ax[0].legend()

            # Axis 1
            sensor_calibration_fc_dataset = \
            file["hostlog"]["channel_97"]["topic_0"]["data"]["configuration_interface_"]["sensor_calibration_"][
                "front_camera_"]
            sensor_calibration_fc_timestamp_dataset = file["hostlog"]["channel_97"]["topic_0"]["timestamp"]
            sensor_calibration_flr_dataset = \
            file["hostlog"]["channel_97"]["topic_0"]["data"]["configuration_interface_"]["sensor_calibration_"][
                "front_looking_radar_"]
            sensor_calibration_flr_timestamp_dataset = file["hostlog"]["channel_97"]["topic_0"]["timestamp"]

            sensor_calibration_fc = sensor_calibration_fc_dataset[:]
            sensor_calibration_fc_timestamp = sensor_calibration_fc_timestamp_dataset[:]
            sensor_calibration_flr = sensor_calibration_flr_dataset[:]
            sensor_calibration_flr_timestamp = sensor_calibration_flr_timestamp_dataset[:]

            ax[1].plot(sensor_calibration_fc_timestamp, sensor_calibration_fc,
                       label="hostlog.channel_97.topic_0.data.configuration_interface_.sensor_calibration_.front_camera_")
            ax[1].plot(sensor_calibration_flr_timestamp, sensor_calibration_flr,
                       label="hostlog.channel_97.topic_0.data.configuration_interface_.sensor_calibration_.front_looking_radar_")
            ax[1].set_ylabel('DC Sensor calibration')
            ax[1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[1].set_facecolor('black')
            ax[1].legend()

            # Add labels, legend, and title
            plt.xlabel('Time')
            plt.suptitle('Multiple Signals from domain controller', fontsize=16)
            plt.tight_layout()
            return fig

    # plot signals for domain controller
    def plot_signals_from_domain_controller(self, *args, **kwargs):
        self.signals_from_domain_controller().show()

    def check_fault_matrix(self, *args, **kwargs):
        # get vcc hdf5 file
        vcc_decoded_file = glob(f"{self.VCC_DECODED_PATH}\\*\\*.hdf5")
        latest_vcc_decoded_file = max(vcc_decoded_file, key=os.path.getmtime)
        # generate fault matrix dict
        with h5py.File(latest_vcc_decoded_file, 'r') as file:
            try:
                fault_matrix = file["hostlog"]["channel_95"]["topic_0"]["data"]["fault_categories_"][:]
                row_len = len(fault_matrix)
                colu_len = len(fault_matrix[0])
            except Exception:
                print("Probably there is no Channel 95 recorded in hostlog.")
            headers = ['Index', 'Description', 'Result']
            fault_matrix_dict = {'Index': [], 'Description': [], 'Result': []}
            result_by_row = []
            for row in range(row_len):
                result_by_row = fault_matrix[row]
            for i in range(len(fault_matrix[0])):
                fault_matrix_dict['Index'].append(i)
                fault_matrix_dict['Description'].append(self.FAULT_MATRIX[i])
                fault_matrix_dict['Result'].append(result_by_row[i])
            # generate heatmap
            self.tableDialog_fault_matrix_hm = HeatmapDialog(fault_matrix, f"Domain Controller Fault Matrix - {os.path.basename(latest_vcc_decoded_file)}", list(fault_matrix_dict['Description']))
            self.tableDialog_fault_matrix_hm.exec_()

    def get_latest_hostlog_version(self, *args, **kwargs):
        file = 'hostlog-portable/'
        try:
            hostlog_artifacts = ArtifactoryPath(f'{self.ARA_DCF_URL}/{file}', auth=(
                self.data["dcf_configuration"]["artifactory_user"], self.data["dcf_configuration"]["ara_api"]))
            # assume that the version follows the rule largest number comes last
            major, minor, patch = [0, 0, 0]
            self.ui.hostlog_ver.clear()
            for folder in hostlog_artifacts.stat().children:
                if folder.count('.') == 2:
                    if int(folder.split('.')[1]) < 4:  # skip to display versions below 4
                        continue
                    self.ui.hostlog_ver.addItem(folder)
                    ma, mi, pa = map(int, folder.split('.'))
                    if ma > major:
                        major, minor, patch = ma, mi, pa
                    elif ma == major:
                        if mi > minor:
                            minor, patch = mi, pa
                        elif mi == minor:
                            patch = max(patch, pa)
            latest_hostlog_version = '.'.join(map(str, [major, minor, patch]))
            self.ui.hostlog_ver.setCurrentText(latest_hostlog_version)
            self.ui.status_lbl.setText(f"Latest Hostlog Client in Aratifactory: {latest_hostlog_version}")
        except Exception:
            latest_hostlog_version = "Failed to fetch from Ara"
            self.ui.status_lbl.setText("Failed to fetch Hostlog Client info from Artifactory. \
                Do you have internet and are the Artifactory credentials correct in gui_parameters.yaml?")

        return latest_hostlog_version

    def download_hostlog_client(self, *args, **kwargs):
        chosen_hostlog_ver = self.ui.hostlog_ver.currentText()
        file = 'hostlog-portable/'
        hostlog_artifacts = ArtifactoryPath(
            f'{self.ARA_DCF_URL}/{file}/{chosen_hostlog_ver}/hostlog-portable-{chosen_hostlog_ver}.zip', auth=(
                self.data["dcf_configuration"]["artifactory_user"], self.data["dcf_configuration"]["ara_api"]))
        out_path = r"C:\hostlog"
        if not os.path.isdir(out_path):
            os.mkdir(out_path)
        # download hostlog client zipfile
        hostlog_zip_path = f'{out_path}\\hostlog-portable-{chosen_hostlog_ver}.zip'
        with hostlog_artifacts.open() as host, open(hostlog_zip_path, 'wb') as out:
            out.write(host.read())
        # unzip hostlog client zipfile
        with ZipFile(hostlog_zip_path, 'r') as zip_ref:
            zip_ref.extractall(out_path)
        self.check_hostlog_version()

    def check_hostlog_version(self, *args, **kwargs):
        self.hostlog_ver = self.get_hostlog_client_version()
        self.hostlog_ver_str = f"{self.hostlog_ver[0]}.{self.hostlog_ver[1]}.{self.hostlog_ver[2]}"
        if self.hostlog_ver[1] > 3:
            self.ui.status_lbl.setText(
                f'<b <br>dcf_config_file loaded. TDF is set to all topics as default.<br>Current Hostlog-Client version: {self.hostlog_ver_str}</b>')
            self.ui.download_hostlog_btn.setStyleSheet("QPushButton {background-color: None;}")
        else:
            self.ui.status_lbl.setText(
                f'<b <br>dcf_config_file loaded. TDF is set to all topics as default.<br>Current Hostlog-Client version: {self.hostlog_ver_str}<br></b><b style="color: red;">Hostlog-client version 0.4.x is available. Please download it by clicking the download hostlog button in red.</b>')
            self.ui.download_hostlog_btn.setStyleSheet("QPushButton {background-color: red;}")

    def get_ip_address(self, *args, **kwargs):
        if self.ui.SGA_IP_address.isChecked():
            self.IP_address = "169.254.4.10"
            self.vehicle_test.update_IP(self.IP_address)
        elif self.ui.HPA_IP_address.isChecked():
            self.IP_address = "198.19.4.1"
            self.vehicle_test.update_IP(self.IP_address)
        elif self.ui.custom_IP_address_radio_button.isChecked():
            self.IP_address = self.ui.custom_IP_address_line_edit.text()
            self.vehicle_test.update_IP(self.IP_address)

        ip_regex = re.compile(r'\b(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'
                              r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'
                              r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'
                              r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b')
        if ip_regex.findall(self.IP_address):
            print("Current chosen node IP address: ", self.IP_address)
        else:
            print(f"{self.IP_address} is not a valid IP address, please recheck.")

    def set_up_log_folders(self, *args, **kwargs):
        for folder in self.LOG_SET_LIST:
            os.makedirs(folder, exist_ok=True)

    def get_latest_folder_in_directory(_, directory, *args, **kwargs):
        latest_diretory = max(glob(f"{directory}\\*"), key=os.path.getmtime)
        return latest_diretory

    def get_latest_file_w_pattern_in_directory(_, directory, pattern_match: str):
        files = list(glob(f"{directory}/{pattern_match}"))
        if len(files) < 1:
            if 'dbc' in pattern_match:
                print(f"Could not find .dbc file in {directory}")
                return None
            elif 'asc' in pattern_match:
                print(f"Could not find .asc file in {directory}")
                return None
            else:
                raise FileNotFoundError(f'No files with pattern {pattern_match} found in {directory}.')
        file_path = max([f for f in files], key=os.path.getmtime) # returns latest file
        return file_path

    def get_latest_tdf_folder_in_directory(self, *args, **kwargs):
        if not (os.path.exists(self.DCF_TDF_PATH) and os.listdir(self.DCF_TDF_PATH)):
            print("Failed to find a tdf folder, attempting to download new tdf:s..")
            self.hostlog_fetch_topics_threading()
            self.worker1.wait()
            # TODO fix behaviour that the progress bar is updated from two places

        return self.get_latest_folder_in_directory(self.DCF_TDF_PATH)

    def hostlog_fetch_topics_threading(self, *args, **kwargs):
        self.ui.status_lbl.setText("Fetching TDF files!")
        self.worker1 = Worker_for_fetch_topics(self.hostlog_fetch_topics, self.DCF_BASE_PATH, self.DCF_PATH)
        self.worker2 = Worker_for_progressbar()
        self.worker2.change_value.connect(self.setProgressVal)
        self.worker2.duration = 0.35  # takes around 35 seconds to fetch topics
        self.worker1.finished.connect(self.task1_finished)
        self.worker2.finished.connect(self.task2_finished)
        self.worker1.start()
        self.worker2.start()
        self.ui.set_function_is_active_state()

    def hostlog_fetch_topics(self, parm_1_dcf_base_path, parm_2_dcf_path, *args, **kwargs):
        tdf_path = parm_1_dcf_base_path
        os.makedirs(tdf_path, exist_ok=True)
        bat_path = parm_2_dcf_path

        connected_node_ip = self.IP_address

        fetch_arguments = f" online fetch-tdf --host {connected_node_ip} --output {tdf_path}"
        fetch_cmd = f"{bat_path}\\set_path.bat && {bat_path}\\hostlog.bat{fetch_arguments}"
        print(f"fetch_cmd: {fetch_cmd}")
        currrent_dir = os.getcwd()
        os.chdir(bat_path)
        print(f"Moving to hostlog directory ->  {os.getcwd()}. This is to be able to run DCF")

        os.system(f'start /wait cmd /c {fetch_cmd}')
        os.chdir(currrent_dir)

    def hostlog_start_logging_threading(self, *args, **kwargs):
        if hasattr(self, 'worker1') and self.worker1.isRunning():
            os.system(r'wmic process where ExecutablePath="C:\\hostlog\\hostlog-client\\python.exe" delete')
            self.ui.start_logging_btn.setText("Start DCF Logging")
            self.ui.set_waiting_for_request_state()
            return

        if self.TOPICS_TO_BE_LOGGED == "":
            ret = QMessageBox.warning(self, 'All topics?',
                                      'Are you sure that you want to log ALL topics? It will increase the CPU load signficantly, so it is recommended to limit the topics. You can limit the topics by selecting predefined topic sets in the top right corner and then press "Update TDF" (in gui_parameters.yaml you can add your own topic sets).',
                                      QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
            if ret == QMessageBox.Cancel:
                return

        self.ui.status_lbl.setText("Hostlog started!!!")

        self.worker1 = Worker_for_hostlog_start_logging(self.hostlog_start_logging,
                                                        self.DCF_TDF_PATH,
                                                        self.DCF_PATH,
                                                        self.DCF_LOG_DESTINATION_FOLDER,
                                                        self.ui.spinBox_log_duration.value(),
                                                        self.TOPICS_TO_BE_LOGGED)
        self.worker2 = Worker_for_progressbar()
        self.worker2.change_value.connect(self.setProgressVal)
        self.worker2.duration = self.ui.spinBox_log_duration.value() / 100
        self.worker1.finished.connect(self.task1_finished)
        self.worker2.finished.connect(self.task_start_logging_finished)
        self.worker1.start()
        self.worker2.start()
        self.ui.set_function_is_active_state(hostlog_active=True)
        self.ui.start_logging_btn.setText("Stop Logging")

    def hostlog_start_logging(self,
                              parm_1_dcf_tdf_path,
                              parm_2_dcf_path,
                              parm_3_dcf_log_destination_folder,
                              parm_4_dcf_log_duration,
                              parm_5_topics_to_be_logged, *args, **kwargs):
        tdf_path = parm_1_dcf_tdf_path
        bat_path = parm_2_dcf_path
        log_dst_path = parm_3_dcf_log_destination_folder
        log_duration = parm_4_dcf_log_duration
        topics_to_be_logged = parm_5_topics_to_be_logged
        camera_elapse_time = 0

        print(f"\n\nTOPICS to be LOGGED {topics_to_be_logged}\n\n")
        os.makedirs(tdf_path, exist_ok=True)
        tdf_folder = self.get_latest_tdf_folder_in_directory()

        print("Cleaning Unnamed TDF files.")
        found_unnamed_tdfs = []
        for item in os.listdir(tdf_folder):
            full_path = os.path.join(tdf_folder, item)
            if os.path.isfile(full_path) and item.startswith("tdf_unnamed"):
                found_unnamed_tdfs.append(full_path)
        if found_unnamed_tdfs:
            for unnamed_tdf in found_unnamed_tdfs:
                try:
                    os.remove(unnamed_tdf)
                    print(f"Removed unnamed tdf file: {unnamed_tdf}")
                except OSError as e:
                    print(f"Error occurs when removing unnamed tdf file: {unnamed_tdf} : {e.strerror}")
        else:
            print("No unnamed tdf file exists.")

        connected_node_ip = self.IP_address
        print(f"Connected to {connected_node_ip}")

        if self.ui.camera_rec_checkBox.isChecked():
            datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            start_recording_cmd = f"python camera_recorder.py " \
                                  f"--file_path bin/scenario_{datetime_str}.avi " \
                                  f"--duration {log_duration} " \
                                  f"--camera_index {self.CAM_REC_INDEX}"
            # Run process in the background
            subprocess.Popen(start_recording_cmd.split())
            # Give some time for camera to start recording
            sleep(3)
            camera_elapse_time = 3

        if self.hostlog_ver[1] > 4:
            appconfig = "--appconfig output.files.binary_capture_split_megabytes=10000"
        elif self.hostlog_ver[1] == 4:
            appconfig = "--appconfig client.binary_capture_split_megabytes=10000"
        else:
            appconfig = ''
        if topics_to_be_logged == "":
                arguments = f"online start-logging --no-decode --to-binary --host {connected_node_ip} " \
                            f"--output {log_dst_path} --definitions {tdf_folder} " \
                            f"--max-time-s {str(log_duration + camera_elapse_time)} --topics all " \
                            f"{appconfig}"
        else:
                arguments = f"online start-logging --no-decode --to-binary --host {connected_node_ip} " \
                            f"--output {log_dst_path} --definitions {tdf_folder} " \
                            f"--max-time-s {str(log_duration + camera_elapse_time)} --topics {topics_to_be_logged} " \
                            f"{appconfig}"

        logging_cmd = f"{bat_path}\\set_path.bat && {bat_path}\\hostlog.bat {arguments}"
        print(f"logging_cmd: {logging_cmd}")
        currrent_dir = os.getcwd()
        os.chdir(bat_path)
        print(f"Moving to hostlog directory ->  {os.getcwd()}. This is to be able to run DCF")
        # Start hostlog
        os.system(f'start /wait cmd /c {logging_cmd}')
        os.chdir(currrent_dir)
        print(f"Moving back to script directory {os.getcwd()}")

        self.ui.start_logging_btn.setText("Start DCF Logging")

    def get_vcu_logs_thread(self, *args, **kwargs):
        if self.is_host_responsive():
            ret = QMessageBox.warning(self, 'VCU logs', 'Are you sure you want to collect the VCU logs?\nNOTE: '
                                                        'All files in log_files will be erased',
                                      QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

            if ret == QMessageBox.Yes:
                self.ui.status_lbl.setText(f"Fetching VCU logs!")
                self.worker1 = Worker_for_get_vehicle_logs(self.vehicle_test)
                self.worker2 = Worker_for_progressbar()
                self.worker2.change_value.connect(self.setProgressVal)
                self.worker2.duration = 10
                self.worker1.finished.connect(self.task1_finished)
                self.worker2.finished.connect(self.task_get_vcu_logs_finished)
                self.worker1.start()
                self.worker2.start()
                self.ui.set_function_is_active_state()
        else:
            self.ui.status_lbl.setText(f"Host {self.IP_address} not responsive.")

    def run_cpu_load_bundle_script(self, *args, **kwargs):
        if self.is_host_responsive():
            ret = QMessageBox.warning(self, 'Bundle Script', 'Are you sure you want '
                                                             'to run Bundle Script? It takes 10 minutes.',
                                      QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

            if ret == QMessageBox.Yes:
                self.ui.status_lbl.setText(f"Running make_bundle.sh. It takes 10-15 minutes")
                self.worker1 = Worker_for_run_bundle_script(self.vehicle_test)
                self.worker2 = Worker_for_progressbar()
                self.worker2.change_value.connect(self.setProgressVal)
                self.worker2.duration = 10
                self.worker1.finished.connect(self.task1_finished)
                self.worker2.finished.connect(self.task_get_vcu_logs_finished)
                self.worker1.start()
                self.worker2.start()
                self.ui.set_function_is_active_state()
        else:
            self.ui.status_lbl.setText(f"Host {self.IP_address} not responsive.")

    def run_cpu_load_tracelogger_script(self, *args, **kwargs):
        if self.is_host_responsive():
            ret = QMessageBox.warning(self, 'Tracebuffer Script', 'Are you sure you want '
                                                                  'to run the Tracebuffer Script? It takes 5 minutes.',
                                      QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

            if ret == QMessageBox.Yes:
                self.ui.status_lbl.setText(f"Running make_tracebuffer.sh. It takes 10-15 minutes")
                self.worker1 = Worker_for_run_tracelogger_script(self.vehicle_test)
                self.worker2 = Worker_for_progressbar()
                self.worker2.change_value.connect(self.setProgressVal)
                self.worker2.duration = 10
                self.worker1.finished.connect(self.task1_finished)
                self.worker2.finished.connect(self.task_get_vcu_logs_finished)
                self.worker1.start()
                self.worker2.start()
                self.ui.set_function_is_active_state()
        else:
            self.ui.status_lbl.setText(f"Host {self.IP_address} not responsive.")

    def task1_finished(self, result, *args, **kwargs):
        print(result)
        self.worker2.stop()

    def task2_finished(self, result, *args, **kwargs):
        print(result)
        self.ui.status_lbl.setText(f"Fetching DONE!!!\nCheck log_files folder")
        QApplication.processEvents()
        self.ui.set_waiting_for_request_state()

    def task_get_vcu_logs_finished(self, result, *args, **kwargs):
        print(result)
        self.ui.status_lbl.setText(f"DONE!!!\nCheck log_files folder")
        QApplication.processEvents()
        self.worker2.stop()
        self.ui.set_waiting_for_request_state()

    def task_start_logging_finished(self, result, *args, **kwargs):
        print(result)
        self.ui.status_lbl.setText(f"Logging DONE!!!\nCheck BIN folder")
        QApplication.processEvents()
        self.worker2.stop()
        self.ui.set_waiting_for_request_state()

    def setProgressVal(self, val, *args, **kwargs):
        self.ui.progressBar.setProperty("value", val)

    def deploy_logs(self, *args, **kwargs):
        self.ui.status_lbl.setText("Deploying logs to ARA-Artifactory")
        sleep(1)
        QGuiApplication.processEvents()
        self.ui.progressBar.setProperty("value", 25)
        deploy_logs_to_artifactory(self.ui.artifactory_dropdown.currentText(), self.vehicle_test)
        sleep(1)
        QGuiApplication.processEvents()
        self.ui.progressBar.setProperty("value", 75)
        self.ui.status_lbl.setText("Logs deployed")
        move_zip_files_from_base_folder()
        self.ui.progressBar.setProperty("value", 100)
        QGuiApplication.processEvents()

    def get_sw_info(self, *args, **kwargs):
        if self.is_host_responsive():
            print("Downloading CS-manifest file.")
            self.ui.status_lbl.setText("Trying to download cs-maifest file and \n"
                                       "read out sw part number + DTCs")
            self.ui.progressBar.setProperty("value", 50)
            QGuiApplication.processEvents()
            get_cs_manifest_btn_action(self.vehicle_test)
            self.update_comment_panel()
            read_out_sw_part_numbers(self.OSB_PATH, self.VEHICLE_LOG_COMMENT, self.IP_address)
            read_out_camera_status_hia(self.OSB_PATH, self.VEHICLE_LOG_COMMENT, self.IP_address)
            if os.path.isfile(self.CS_MANIFEST):
                self.ui.status_lbl.setText(f"Success - {self.CS_MANIFEST}")
            else:
                self.ui.status_lbl.setText("Something went wrong - \nMake sure you connected to The VCU?")
        else:
            print("Failed to ping SGA")
            self.ui.status_lbl.setText("Get_sw_info \nMake sure you connected to The VCU?")
        self.ui.progressBar.setProperty("value", 100)
        QGuiApplication.processEvents()

    def is_host_responsive(self, *args, **kwargs):
        host = self.IP_address
        try:
            response_time = ping3.ping(host, timeout=2)  # Set a timeout for the ping
            if response_time is not None:
                return True
        except (TimeoutError, OSError) as e:
            pass
        return False

    def generate_app_state_dict(self, app_state_yaml, *args, **kwargs):
        apps_state_dict = {'Index': [], 'Apps': [], 'States': []}
        with open(app_state_yaml, "r") as file:
            apps_state = yaml.load(file, Loader=yaml.FullLoader)['apps']
            for idx, app in enumerate(sorted(apps_state)):
                apps_state_dict['Index'].append(idx)
                apps_state_dict['Apps'].append(app)
                apps_state_dict['States'].append(apps_state[app]['state'])
        return apps_state_dict

    def get_em_control_app_state(self, *args, **kwargs):
        if self.is_host_responsive():
            print("Running em_control -l and saving it to yaml file")
            self.ui.status_lbl.setText("Running em_control -l and saving it to yaml file.")
            self.ui.progressBar.setProperty("value", 50)
            QGuiApplication.processEvents()
            app_state_file = get_app_state_as_yaml_file(self.vehicle_test)
            if app_state_file:
                em_control_app_state_file = f"{self.DCF_BASE_PATH}\\log_files\\{app_state_file}"
                self.ui.progressBar.setProperty("value", 100)
                apps_state_dict = self.generate_app_state_dict(em_control_app_state_file)
                self.tableDialog_app_state = TableDialog(apps_state_dict, ['Index', 'Apps', 'States'], "App State")
                self.tableDialog_app_state.exec_()
            else:
                self.ui.status_lbl.setText("Something went wrong on app_state_datetime.yml")
                return
            if os.path.isfile(em_control_app_state_file):
                self.ui.status_lbl.setText(f"Success - {em_control_app_state_file}")
            else:
                self.ui.status_lbl.setText("Something went wrong")
        else:
            em_control_app_state_file = get_latest_file_w_pattern_in_directory(f"{self.DCF_BASE_PATH}\\log_files", "app_state_*.yml")
            self.ui.status_lbl.setText(f"Host {self.IP_address} not responsive.\nWill show app stats info from {em_control_app_state_file}")
            apps_state_dict = self.generate_app_state_dict(em_control_app_state_file)
            self.ui.progressBar.setProperty("value", 100)
            self.tableDialog_app_state = TableDialog(apps_state_dict, ['Index', 'Apps', 'States'], f"App State - {os.path.basename(em_control_app_state_file)}")
            self.tableDialog_app_state.exec_()

    def decode_dcf(self, *args, **kwargs):
        self.ui.status_lbl.setText("Starting decoding")
        self.ui.progressBar.setProperty("value", 10)
        QGuiApplication.processEvents()

        if self.ui.checkBox_vcc.isChecked():
            print('******* Decoding VCC started *******')
            decode_dcf_log_vcc(self)
            print('******* Decoding VCC finished *******')
            self.ui.progressBar.setProperty("value", 25)
            self.ui.status_lbl.setText(f"{self.ui.status_lbl.text()}\nVCC decoding finished")
            QGuiApplication.processEvents()

        if self.ui.checkBox_zen.isChecked():
            if "finished" in self.ui.status_lbl.text():
                self.ui.status_lbl.setText(f'{self.ui.status_lbl.text()}, continuing with Zenseact decoding')
                QGuiApplication.processEvents()
            else:
                self.ui.status_lbl.setText("Zenseact decoding started")
                QGuiApplication.processEvents()

            print('******* Decoding Zenseact started *******')
            decode_dcf_log_zenseact(self)
            print('******* Decoding Zenseact finished *******')
            self.ui.progressBar.setProperty("value", 70)

        if self.ui.checkBox_flcw.isChecked():
            if "finished" in self.ui.status_lbl.text():
                self.ui.status_lbl.setText('Only FLCW image decoding left!')
                QGuiApplication.processEvents()
            QGuiApplication.processEvents()
            print('******* Decoding FLCW images started *******')
            binary_file_path = get_latest_file_w_pattern_in_directory(self.DCF_BIN_PATH, '*.bin')
            tdf_path = get_latest_folder_in_directory(self.DCF_TDF_PATH)
            self.ui.status_lbl.setText(f"{self.ui.status_lbl.text()}\nLatest binary file : {binary_file_path}")
            out_path = f"{self.IMAGE_DECODED_PATH}/{os.path.basename(binary_file_path).split('.')[0]}"
            try:
                decode_flcw_images_module(binary_file_path, tdf_path, out_path)
            except shutil.Error:
                self.ui.status_lbl.setText(f"{self.ui.status_lbl.text()}\n The same decoded FLCW images already exist.")
            self.ui.status_lbl.setText(
                f"{self.ui.status_lbl.text()}\nLatest decoded FLCW images : {self.IMAGE_DECODED_PATH}")
            print('******* Decoding FLCW images *******')

        self.ui.status_lbl.setText(f"{self.ui.status_lbl.text()}\nDecoding done - Check folders for files")
        print("Decoding done - Check folders for files")
        self.ui.progressBar.setProperty("value", 100)
        # check if aca is available
        self.check_aca(self.ZEN_DECODED_PATH)

    def zip_dlt_can_dct_log(self, *args, **kwargs):
        # Prompts the user to modify the comment file before it gets saved and zipped
        plainTextEdit_text = self.ui.plainTextEdit.toPlainText()
        text_from_window, ok = QInputDialog.getMultiLineText(self, 'Comment file',
                                                             'Make sure that the comment file is updated',
                                                             text=plainTextEdit_text)

        if ok:
            self.ui.plainTextEdit.setPlainText(text_from_window)
            self.save_comment()

        self.ui.status_lbl.setText("Zipping log files!")
        os.makedirs(self.COLLECTED_DLT_DCF_CAN_LOGS, exist_ok=True)
        try:
            # copy log files
            for folder in self.LOG_SET_LIST:
                print(f"Copying -> {folder}")
                copytree(folder, str(self.COLLECTED_DLT_DCF_CAN_LOGS), dirs_exist_ok=True)

            # clean log folder's but keep tdf & log_files
            for folder in self.LOG_SET_LIST:
                if "tdf" not in str(folder) and "log_files" not in str(folder):
                    print(f"Removing files in folder -> {folder}")
                    rmtree(folder)
                else:
                    print(f"Those files will be kept -> {folder}")

            now = datetime.now()
            # convert to string
            dt = now.strftime("%Y-%m-%d_%H-%M-%S")
            result_file = f"{self.DCF_BASE_PATH}/DLT_DCF_CAN_LOGS_{dt}"

            # zip folder
            make_archive(result_file, 'zip', self.COLLECTED_DLT_DCF_CAN_LOGS)
            if self.DCF_HDF5_PATH.exists():
                rmtree(self.DCF_HDF5_PATH)
            if self.COLLECTED_DLT_DCF_CAN_LOGS:
                rmtree(self.COLLECTED_DLT_DCF_CAN_LOGS)
            # set up empty folder's
            self.set_up_log_folders()
            self.ui.status_lbl.setText(f"Logs compressed - {result_file}")
            self.ui.progressBar.setProperty("value", 100)
        except:
            print("It was not possible to copy the files."
                  "\nClose all files before performing this action")
            self.ui.status_lbl.setText("!!!!!!!!!! It was not possible to copy the files."
                                       f"\nClose all files before performing this action "
                                       f"!!!!!!!!!!!")

    def save_comment(self, *args, **kwargs):
        print("Saving comments")
        text = self.ui.plainTextEdit.toPlainText()
        vehicle_log_destination = f"{self.VEHICLE_LOG_COMMENT}/Vehilog_comments.txt"
        try:
            with open(vehicle_log_destination, "w") as data:
                data.write(text)
                print(f'Comment saved in {vehicle_log_destination}')
        except Exception as err:
            print(f'FAILED TO SAVE THE COMMENT FILE: {err}')

    def aeb_check(self, *args, **kwargs):
        hdf5_path = f"{self.get_latest_folder_in_directory(self.ZEN_DECODED_PATH)}/zen_qm_feature_a.hdf5"
        try:
            with h5py.File(hdf5_path, 'r') as h:
                aeb_signal = \
                h["zen_qm_feature_a"]["aeb_brake_request"]["data"]["emergency_braking_request"]["unitless"]["value"]
                aeb_trigger = 1 in list(aeb_signal)
                if aeb_trigger:
                    msg = "AEB IS TRIGGERED!"
                else:
                    msg = "AEB is NOT triggered."
                self.ui.status_lbl.setText(msg)
                # save and plot image in QGraphicsView
                png_path = "aeb_trigger.png"
                plt.figure()
                plt.plot(aeb_signal[:])
                plt.savefig(png_path)
                scene = QGraphicsScene()
                pixmap = QPixmap(png_path)
                scene.addPixmap(pixmap)
                self.ui.graphicsView.setScene(scene)
                self.ui.graphicsView.fitInView(scene.sceneRect(), QtCore.Qt.IgnoreAspectRatio)

                return aeb_trigger
        except Exception as e:
            err = repr(e).split("(")[0]
            err_msg = re.findall("error message = '(.*?)',", repr(e))
            self.ui.status_lbl.setText(f"Failed to check AEB.\n{err}: {err_msg[0]}")
            return False

    def can_check(self, *args, **kwargs):
        # Run pytest on BCMA
        db, asc_file = self.load_dbc_asc()
        # Get the message and signal
        message = db.get_message_by_name('Dp2Bcma2CANFrame01')
        decel_req = 'SftyDecelGroupSafeToBrk1AsySftyDecelReq'
        decel_ena = 'SftyDecelGroupSafeToBrk1AsySftyEnaDecel'
        brake_gain_ena = 'SftyGainGroupSafe1AsyBrkGainEna'
        brake_gain_decel = 'SftyGainGroupSafe1AsyBrkGainMaxDecel'
        brake_gain_req = 'SftyGainGroupSafe1AsyBrkGainReq'
        for signal in message.signals:
            if signal.name == decel_req:
                signal_decel_req = signal
            if signal.name == decel_ena:
                signal_decel_ena = signal
            if signal.name == brake_gain_ena:
                signal_brake_gain_ena = signal
            if signal.name == brake_gain_decel:
                signal_brake_gain_decel = signal
            if signal.name == brake_gain_req:
                signal_brake_gain_req = signal

        message2 = db.get_message_by_name('BcmaBcma2CANFrame02')
        decel_ackd = 'AsyBrkEnaAckdAsySftyEnaDecelAckd'
        inhibit = 'InhbOfAsySftyDecelByVehDyn'
        brake_allwd = 'AsySftyDecelEnadByVehDyn'
        brake_gain_ackd = 'AsyBrkEnaAckdAsyBrkGainEnaAckd'
        for signal in message2.signals:
            if signal.name == decel_ackd:
                signal_decel_ackd = signal
            if signal.name == inhibit:
                signal_inhibit = signal
            if signal.name == brake_allwd:
                signal_brake_allwd = signal
            if signal.name == brake_gain_ackd:
                signal_brake_gain_ackd = signal

        message3 = db.get_message_by_name('Dp2HIBBcma2CANFrame01')
        post_impact = 'PostImpctBrkgReqGrpPostImpctBrkgDecel'
        for signal in message3.signals:
            if signal.name == post_impact:
                signal_post_impact = signal

        message4 = db.get_message_by_name('BcmaBcma2CANDp2AndDp2HIBFrame01')
        vehicle_speed = 'VehSpdLgt3VehSpdLgt'
        for signal in message4.signals:
            if signal.name == vehicle_speed:
                signal_vehicle_speed = signal

        can_decel_req = []
        can_decel_ena = []
        can_decel_ackd = []
        can_post_impact = []
        can_inhibit = []
        can_brake_allwd = []
        can_brake_gain_ena = []
        can_brake_gain_decel = []
        can_brake_gain_ackd = []
        can_brake_gain_req = []
        can_vehicle_speed = []

        with can.io.ASCReader(asc_file) as reader:
            for msg in reader:
                # Check if this message has the same ID as the one we're interested in
                if msg.arbitration_id == message.frame_id:
                    # Decode the message
                    decoded_message = db.decode_message(msg.arbitration_id, msg.data)
                    can_decel_req.append(decoded_message[signal_decel_req.name])
                    can_decel_ena.append(decoded_message[signal_decel_ena.name])
                    can_brake_gain_ena.append(decoded_message[signal_brake_gain_ena.name])
                    can_brake_gain_decel.append(decoded_message[signal_brake_gain_decel.name])
                    can_brake_gain_req.append(decoded_message[signal_brake_gain_req.name])

                if msg.arbitration_id == message2.frame_id:
                    decoded_message2 = db.decode_message(msg.arbitration_id, msg.data)
                    can_decel_ackd.append(decoded_message2[signal_decel_ackd.name])
                    can_inhibit.append(decoded_message2[signal_inhibit.name])
                    can_brake_allwd.append(decoded_message2[signal_brake_allwd.name])
                    can_brake_gain_ackd.append(decoded_message2[signal_brake_gain_ackd.name])
                if msg.arbitration_id == message3.frame_id:
                    decoded_message3 = db.decode_message(msg.arbitration_id, msg.data)
                    can_post_impact.append(decoded_message3[signal_post_impact.name])
                if msg.arbitration_id == message4.frame_id:
                    decoded_message4 = db.decode_message(msg.arbitration_id, msg.data)
                    can_vehicle_speed.append(decoded_message4[signal_vehicle_speed.name])

        numeric_can_decel_ena = [0 if x == 'OnOff1_Off' else 1 for x in can_decel_ena]
        numeric_can_decel_ackd = [0 if x == 'OnOff1_Off' else 1 for x in can_decel_ackd]
        numeric_can_inhibit = [0 if x == 'InhbOfAsySftyDecelByVehDyn1_AsySftyBrkgDendByBrk' else 1 for x in can_inhibit]
        numeric_can_brake_allwd = [0 if x == 'AsySftyDecelEnadByVehDyn1_AsyBrkgAllwd' else 1 for x in can_brake_allwd]
        numeric_can_brake_gain_ackd = [0 if x == 'OnOff1_Off' else 1 for x in can_brake_gain_ackd]
        numeric_can_brake_gain_ena = [0 if x == 'OnOff1_Off' else 1 for x in can_brake_gain_ena]
        # save and plot image in QGraphicsView
        png_path = "can_trigger.png"
        fig, ax = plt.subplots(5, 1, figsize=(16, 10), sharex=True)
        # axis 0 - AEB
        ax[0].plot(can_decel_req, label=decel_req)
        ax[0].plot(numeric_can_decel_ena, label=decel_ena)
        ax[0].plot(can_post_impact, label=post_impact)
        ax[0].plot(numeric_can_decel_ackd, label=decel_ackd)
        ax[0].grid(True, color='white', linestyle='--', linewidth=0.4)
        ax[0].set_facecolor('black')
        ax[0].set_ylabel('AEB')
        ax[0].legend()
        # axis 1 - Inhibit
        ax[1].plot(numeric_can_inhibit, label=inhibit)
        ax[1].plot(numeric_can_brake_allwd, label=brake_allwd)
        ax[1].set_ylabel('Inhibit')
        ax[1].grid(True, color='white', linestyle='--', linewidth=0.4)
        ax[1].set_facecolor('black')
        ax[1].legend()
        # axis 2 - BrakeGain
        ax[2].plot(numeric_can_brake_gain_ackd, label=brake_gain_ackd)
        ax[2].plot(numeric_can_brake_gain_ena, label=brake_gain_ena)
        ax[2].set_ylabel('Brakegain')
        ax[2].grid(True, color='white', linestyle='--', linewidth=0.4)
        ax[2].set_facecolor('black')
        ax[2].legend()
        # axis 3 - BrakeGain
        ax[3].plot(can_brake_gain_decel, label=brake_gain_decel)
        ax[3].plot(can_brake_gain_req, label=brake_gain_req)
        ax[3].set_ylabel('Brakegain')
        ax[3].grid(True, color='white', linestyle='--', linewidth=0.4)
        ax[3].set_facecolor('black')
        ax[3].legend()
        # axis 4 - Vehicle speed
        ax[4].plot(can_vehicle_speed, label=vehicle_speed)
        ax[4].set_ylabel('Vehicle speed')
        ax[4].grid(True, color='white', linestyle='--', linewidth=0.4)
        ax[4].set_facecolor('black')
        ax[4].legend()

        plt.xlabel('Frame')
        plt.suptitle('CAN signals', fontsize=16)
        plt.tight_layout()
        plt.savefig(png_path)
        plt.show()

        return None

    def pscm_can_check(self, *args, **kwargs):
        # Run pytest on PSCM
        db, asc_file = self.load_dbc_asc()
        latmodcfmd = 'SteerLatCtrlModReqCfmd'
        latmod = 'SteerLatCtrlModReqLatCtrlModReq'
        rackpos = 'RackPositionReqSafeSteerRackPosReq'
        steerovrlyactvreq = 'SteerOvrlyActvReq'
        steerovrlyactvcmfd = 'SteerOvrlyActvCmfd'
        steerassitmodreq = 'SteerAssistModReq'

        Lat_mod_dict = {'LatCtrlMod5_NoReq': 0, 'LatCtrlMod5_Mode1': 1, 'LatCtrlMod5_Mode2': 2, 'LatCtrlMod5_Mode3': 3,
                        'LatCtrlMod5_Mode4': 4, 'LatCtrlMod5_Mode5': 5, 'LatCtrlMod5_Mode6': 6, 'LatCtrlMod5_Mode7': 7,
                        'LatCtrlMod5_Mode8': 8, 'LatCtrlMod5_Mode9': 9, 'LatCtrlMod5_Mode10': 10}
        reversed_Lat_mod_dict = {value: key for key, value in Lat_mod_dict.items()}

        steer_tq_ovrlyactv_dict = {'SteerOvrlyActvReq_NoReq': 0, 'SteerOvrlyActvReq_OvrlyMotTqActv': 1,
                                   'SteerOvrlyActvReq_SteerWhlOvrlyTqActv': 2,
                                   'SteerOvrlyActvReq_OvrlyMotTrqActvWithWd': 3, 'SteerOvrlyActvReq_spare4': 4,
                                   'SteerOvrlyActvReq_spare5': 5,
                                   'SteerOvrlyActvReq_spare6': 6, 'SteerOvrlyActvReq_spare7': 7}
        reversed_steer_tq_ovrlyactv_dict = {value: key for key, value in steer_tq_ovrlyactv_dict.items()}

        steer_assit_mod_req_dict = {'SteerAssistMod2_Off': 0, 'SteerAssistMod2_Standby': 1,
                                    'SteerAssistMod2_FullAssist': 2, 'SteerAssistMod2_Unused0': 3,
                                    'SteerAssistMod2_Unused1': 4, 'SteerAssistMod2_Unused2': 5,
                                    'SteerAssistMod2_Unused3': 6, 'SteerAssistMod2_Unused4': 7,
                                    'SteerAssistMod2_FltOperStandby': 8, 'SteerAssistMod2_FltOperIntFlt': 9,
                                    'SteerAssistMod2_FltOperLimpHome': 10, 'SteerAssistMod2_FltOperLimpAside': 11,
                                    'SteerAssistMod2_FltOperUnused1': 12, 'SteerAssistMod2_FltOperUnused2': 13,
                                    'SteerAssistMod2_FltOperUnused3': 14, 'SteerAssistMod2_Inoperable': 15}
        reversed_steer_assit_mod_req_dict = {value: key for key, value in steer_assit_mod_req_dict.items()}

        numerical_latmodcfmd = self.can_signal_converter(latmodcfmd, 'PscmPscm1CanFrame12_05', db, asc_file, str,
                                                         Lat_mod_dict)
        numerical_latmodrq = self.can_signal_converter(latmod, 'PscmdpHIAPscmHIA1CanFrame04_5', db, asc_file, str,
                                                       Lat_mod_dict)
        numerical_rackpos = self.can_signal_converter(rackpos, 'PscmdpHIAPscmHIA1CanFrame04_5', db, asc_file, float)
        numerical_steertq = self.can_signal_converter(steerovrlyactvreq, 'PscmdpPscm1CanFrame05_20', db, asc_file, str,
                                                      steer_tq_ovrlyactv_dict)
        numerical_steerovrlyactvcmfd = self.can_signal_converter(steerovrlyactvcmfd, 'PscmPscm1CanFrame02_10', db,
                                                                 asc_file, str, steer_tq_ovrlyactv_dict)
        numerical_steerassitmodreq = self.can_signal_converter(steerassitmodreq, 'PscmdpPscm1CanFrame03_100', db,
                                                               asc_file, str, steer_assit_mod_req_dict)

        # save and plot image in QGraphicsView
        png_path = "can_lka_trigger.png"
        fig, (ax_cfmd, ax_rq, ax_rack_pos, ax_steer_tq_req, ax_steerovrlyactvcmfd, ax_steerassitmodreq) = plt.subplots(
            6, 1, figsize=(16, 10))
        # ax_cfmd - LKA mode confirmed
        ax_cfmd.plot(numerical_latmodrq)
        ax_cfmd.grid(True, color='white', linestyle='--', linewidth=0.4)
        ax_cfmd.set_facecolor('black')
        tick_values, tick_labels = list(zip(*((val, reversed_Lat_mod_dict[val]) for val in set(numerical_latmodrq))))
        ax_cfmd.set_yticks(tick_values, tick_labels)
        ax_cfmd.set_title('PscmdpHIAPscmHIA1CanFrame04_5.SteerLatCtrlModReqLatCtrlModReq')

        ax_rq.plot(numerical_latmodcfmd)
        ax_rq.grid(True, color='white', linestyle='--', linewidth=0.4)
        ax_rq.set_facecolor('black')
        tick_values, tick_labels = list(zip(*((val, reversed_Lat_mod_dict[val]) for val in set(numerical_latmodcfmd))))
        ax_rq.set_yticks(tick_values, tick_labels)
        ax_rq.set_title('PscmPscm1CanFrame12_05.SteerLatCtrlModReqCfmd')

        ax_rack_pos.plot(numerical_rackpos)
        ax_rack_pos.grid(True, color='white', linestyle='--', linewidth=0.4)
        ax_rack_pos.set_facecolor('black')
        ax_rack_pos.set_title('PscmdpHIAPscmHIA1CanFrame04_5.RackPositionReqSafeSteerRackPosReq')

        ax_steer_tq_req.plot(numerical_steertq)
        ax_steer_tq_req.grid(True, color='white', linestyle='--', linewidth=0.4)
        ax_steer_tq_req.set_facecolor('black')
        tick_values, tick_labels = list(
            zip(*((val, reversed_steer_tq_ovrlyactv_dict[val]) for val in set(numerical_steertq))))
        ax_steer_tq_req.set_yticks(tick_values, tick_labels)
        ax_steer_tq_req.set_title('PscmdpPscm1CanFrame05_20.SteerOvrlyActvReq')

        ax_steerovrlyactvcmfd.plot(numerical_steerovrlyactvcmfd)
        ax_steerovrlyactvcmfd.grid(True, color='white', linestyle='--', linewidth=0.4)
        ax_steerovrlyactvcmfd.set_facecolor('black')
        tick_values, tick_labels = list(
            zip(*((val, reversed_steer_tq_ovrlyactv_dict[val]) for val in set(numerical_steerovrlyactvcmfd))))
        ax_steerovrlyactvcmfd.set_yticks(tick_values, tick_labels)
        ax_steerovrlyactvcmfd.set_title('PscmdpPscm1CanFrame02_10.steerovrlyactvcmfd')

        ax_steerassitmodreq.plot(numerical_steerassitmodreq)
        ax_steerassitmodreq.grid(True, color='white', linestyle='--', linewidth=0.4)
        ax_steerassitmodreq.set_facecolor('black')
        tick_values, tick_labels = list(
            zip(*((val, reversed_steer_assit_mod_req_dict[val]) for val in set(numerical_steerassitmodreq))))
        ax_steerassitmodreq.set_yticks(tick_values, tick_labels)
        ax_steerassitmodreq.set_title('PscmdpPscm1CanFrame03_100.SteerAssistModReq')

        plt.xlabel('Frame')
        plt.suptitle('CAN signals', fontsize=16)
        plt.tight_layout()
        plt.savefig(png_path)
        plt.show()

    def plot_lka_analysis_necessary_signals(self, *args, **kwargs):
        print('no function connected')
        return None

    def plot_signals_from_hpa_hib(self, *args, **kwargs):
        hdf5_path = f"{self.get_latest_folder_in_directory(self.ZEN_DECODED_PATH)}\\zen_qm_feature_a.hdf5"
        try:
            with h5py.File(hdf5_path, 'r') as h:
                aes_signal = \
                h["zen_qm_feature_a"]["zen_qm_feature_a_aes_diagnostics"]["data"]["frozen_manoeuvre"]["exists"][
                    "unitless"]["value"]
                aes_trigger = 1 in list(aes_signal)
                if aes_trigger:
                    msg = "AES IS TRIGGERED!"
                else:
                    msg = "AES is NOT triggered."
                self.ui.status_lbl.setText(msg)
                # save and plot image in QGraphicsView
                png_path = "aes_trigger.png"
                plt.figure()
                plt.plot(aes_signal[:])
                plt.savefig(png_path)
                scene = QGraphicsScene()
                pixmap = QPixmap(png_path)
                scene.addPixmap(pixmap)
                self.ui.graphicsView.setScene(scene)
                self.ui.graphicsView.fitInView(scene.sceneRect(), QtCore.Qt.IgnoreAspectRatio)

                return aes_trigger
        except Exception as e:
            err = repr(e).split("(")[0]
            err_msg = re.findall("error message = '(.*?)',", repr(e))
            self.ui.status_lbl.setText(f"Failed to check AES.\n{err}: {err_msg[0]}")
            return False

    def plot_signals_from_hib_hpa(self, *args, **kwargs):
        vcc_decoded_file = glob(f"{self.VCC_DECODED_PATH}/*.hdf5")
        latest_vcc_decoded_file = max(vcc_decoded_file, key=os.path.getmtime)
        hdf5_file = latest_vcc_decoded_file

        with h5py.File(hdf5_file, 'r') as file:
            fig, ax = plt.subplots(4, 2, figsize=(18, 12), sharex=True)

            # Axis 0
            signal_00_data = file["hostlog"]["channel_83"]["topic_0"]["data"]["overlay_torque_confirmation"]
            signal_00 = list(signal_00_data[:])
            timestamp_data = file["hostlog"]["channel_83"]["topic_0"]["timestamp"]
            timestamp = timestamp_data[:]

            ax[0, 0].plot(signal_00, timestamp, label="[AAM-input] overlay_torque_confirmation")
            ax[0, 0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[0, 0].set_facecolor('black')
            ax[0, 0].set_ylabel('AAM topic 0 data')
            ax[0, 0].legend()

            # Axis 1
            signal_10_data = file["hostlog"]["channel_83"]["topic_0"]["data"]["zen_lateral_feature_type_input"][
                "lateral_feature_type_"]
            signal_10 = signal_10_data[:]

            ax[1, 0].plot(signal_10, label="[AAM-input] lateral_feature_type")
            ax[1, 0].set_ylabel('AAM topic 0 data')
            ax[1, 0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[1, 0].set_facecolor('black')
            ax[1, 0].legend()

            # Axis 2
            signal_20_data = file["hostlog"]["channel_83"]["topic_0"]["data"]["steering_haptic_mode"]
            signal_20 = signal_20_data[:]

            ax[2, 0].plot(signal_20, label="[AAM-input] steering_haptic_mode")
            ax[2, 0].set_ylabel('AAM topic 0 data')
            ax[2, 0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[2, 0].set_facecolor('black')
            ax[2, 0].legend()

            # Axis 3
            signal_30_data = file["hostlog"]["channel_84"]["topic_0"]["data"]["powersteering_mode"]
            signal_30 = signal_30_data[:]

            ax[3, 0].plot(signal_30, label="[AAM-output] powersteering_mode")
            ax[3, 0].set_ylabel('AAM topic 0 data')
            ax[3, 0].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[3, 0].set_facecolor('black')
            ax[3, 0].legend()

            # Axis 4
            signal_01_data = file["hostlog"]["channel_84"]["topic_0"]["data"]["vmc_mode"]
            signal_01 = signal_01_data[:]

            ax[0, 1].plot(signal_01, label="[AAM-input] vmc_mode")
            ax[0, 1].set_ylabel('AAM topic 0 data')
            ax[0, 1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[0, 1].set_facecolor('black')
            ax[0, 1].legend()

            # Axis 5
            signal_11_data = file["hostlog"]["channel_84"]["topic_0"]["data"]["vmc_path_selection"]
            signal_11 = signal_11_data[:]

            ax[1, 1].plot(signal_11, label="[AAM-input] vmc_path_selection")
            ax[1, 1].set_ylabel('AAM topic 0 data')
            ax[1, 1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[1, 1].set_facecolor('black')
            ax[1, 1].legend()

            # Axis 6
            signal_21_data = file["hostlog"]["channel_84"]["topic_0"]["data"]["zens_lat_mode_confirmed"]
            signal_21 = signal_21_data[:]

            ax[2, 1].plot(signal_21, label="[AAM-input] zens_lat_mode_confirmed")
            ax[2, 1].set_ylabel('AAM topic 0 data')
            ax[2, 1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[2, 1].set_facecolor('black')
            ax[2, 1].legend()

            # Axis 7
            signal_31_data = file["hostlog"]["channel_84"]["topic_0"]["data"]["zens_long_mode_confirmed"]
            signal_31 = signal_31_data[:]

            ax[3, 1].plot(signal_31, label="[AAM-input] zens_long_mode_confirmed")
            ax[3, 1].set_ylabel('AAM topic 0 data')
            ax[3, 1].grid(True, color='white', linestyle='--', linewidth=0.4)
            ax[3, 1].set_facecolor('black')
            ax[3, 1].legend()

            # Add labels, legend, and title
            plt.xlabel('Time')
            plt.suptitle('Multiple Signals from adas-manager-safe', fontsize=16)
            plt.tight_layout()
            plt.show()
            return fig

    def gen_lat_report(self, *args, **kwargs):
        with PdfPages('all_plots.pdf') as pdf:
            pdf.savefig(self.plot_signals_from_hpa_hib())
            pdf.savefig(self.plot_signals_from_hib_hpa())
        url = QtCore.QUrl.fromLocalFile(f"{os.getcwd()}\\all_plots.pdf").toString()
        self.ui.status_lbl.setText(f'<a href="{url}">Click to open all_plots.pdf</a>')

    def run_lat_pytest(self, *args, **kwargs):
        pytest.main([f"{os.getcwd()}\\pytest\\function_test\\test_lat_func.py", r"--html=pytest\reports\report_lateral_check.html", "-o", "log_cli=true", "-v"])
        report_destination = f"{os.getcwd()}\\pytest\\reports"
        self.ui.status_lbl.setText(f'<a href="{report_destination}">Report(s) can be found here: {report_destination}</a>')

    def fill_tdf_list(self, data, *args, **kwargs):
        self.ui.tdf_list.clear()
        for key in data['dcf_configuration'].keys():
            if "topic" in key:
                self.ui.tdf_list.addItem(QListWidgetItem(key))

    def update_tdf(self, *args, **kwargs):
        chosn_item = self.ui.tdf_list.currentItem()
        with open("gui_parameters.yaml", "r") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            self.TOPICS_TO_BE_LOGGED = data["dcf_configuration"][chosn_item.text()]
        if self.TOPICS_TO_BE_LOGGED:
            self.ui.status_lbl.setText(f"TDF is updated to {self.TOPICS_TO_BE_LOGGED}")
        else:
            self.ui.status_lbl.setText("TDF is updated to all topics.")
            QGuiApplication.processEvents()

    def sga2hpa(self, *args, **kwargs):
        if self.is_host_responsive():
            self.ui.status_lbl.setText("Running SGA -> HPA Command")
            self.ui.progressBar.setProperty("value", 50)
            QGuiApplication.processEvents()
            self.vehicle_test.update_IP(self.IP_address)
            self.vehicle_test.connect_sga2hpa()
            sgs2hpa_text = "The forwarding rules are applied to the port from SGA -> HPA"
            self.ui.status_lbl.setText(
                sgs2hpa_text if "SGA -> HPA" in self.ui.status_lbl.text() else self.ui.status_lbl.text() + "\n" + sgs2hpa_text)
            self.ui.progressBar.setProperty("value", 100)
        else:
            self.ui.status_lbl.setText("SGA2HPA - Host not responsive.")
        return

    def fetch_a2l_s19_button_action(self, *args, **kwargs):
        if self.is_host_responsive():
            xcp_file_path_in_hpa = r"/etc/apps/adas-domain-controller"
            xcp_file_dst_path = self.A2L_S19_BASE_FOLDER
            if not os.path.exists(xcp_file_dst_path):
                os.mkdir(xcp_file_dst_path)
            veridict = self.fetch_xcp_files(xcp_file_path_in_hpa, xcp_file_dst_path)
            if veridict:
                self.ui.status_lbl.setText("Successfully connected to VCU (SGA -> HPA)"
                                           "\nand copied XCP files from HPA....")
        else:
            self.ui.status_lbl.setText(f"Host {self.IP_address} not responsive.")

    def fetch_xcp_files(self, xcp_file_path_in_hpa, xcp_file_dst_path, xcp_file_name="adasdomaincontroller_server",
                        *args, **kwargs):
        """
        args
        xcp_file_path_in_hpa can be for example "/etc/apps/adas-domain-controller"
        xcp_file_dst_path can be for example ""
        xcp_file_name cam be for example "adasdomaincontroller_server"
        """
        if not isinstance(xcp_file_path_in_hpa, str) and \
                not isinstance(xcp_file_dst_path, str) and \
                not isinstance(xcp_file_name, str):
            raise Exception("You need to provide path as string!")

        xcp_file_path_vcu = xcp_file_path_in_hpa
        destination_folder = self.A2L_S19_BASE_FOLDER

        if not os.path.exists(destination_folder):
            os.mkdir(destination_folder)

        open_ssh_tunnel = f'open sftp://root:root@198.19.0.1/ -rawsettings FSProtocol=2 Tunnel=1 ' \
                          f'TunnelHostName="{self.IP_address}" TunnelUserName="swupdate" ' \
                          f'TunnelPasswordPlain="swupdate" -hostkey=*  '

        get_file_a2l = 'get ' + f"{xcp_file_path_vcu}/{xcp_file_name}.a2l " + str(destination_folder) + "\\"
        get_file_s19 = 'get ' + f"{xcp_file_path_vcu}/{xcp_file_name}.s19 " + str(destination_folder) + "\\"
        exit_ssh_tunnel = 'exit'

        copy_remote_to_local_winScp = [open_ssh_tunnel, get_file_a2l, get_file_s19, exit_ssh_tunnel]

        with open('Copy_Remote_To_Local_Folder.scpt', 'w') as file_handler:
            for item in copy_remote_to_local_winScp:
                file_handler.write("{}\n".format(item))

        log = subprocess.run([f"{self.WINSCP_PATH}\\WinSCP.com", "/log= WinScp.log",
                              "/script=" + 'Copy_Remote_To_Local_Folder.scpt'],
                             shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        if log.returncode == 0:
            print("Successfully connected to VCU (SGA -> HPA) and copied XCP files from HPA....")
            return True
        else:
            print("Failed to connect to VCU (SGA -> HPA) and copy XCP files from HPA....")
            self.ui.status_lbl.setText("Failed to connect to VCU (SGA -> HPA) and copy XCP files from HPA....")
            return False

    def start_xcp_calibration_threading(self, function_name, *args, **kwargs):
        self.ui.status_lbl.setText("XCP calibration started!!!")

        self.worker_xcp = Worker_for_xcp_domain_controller(
            lambda: self.enable_aeb_n_fcw_domain_controller(function_name))
        self.worker_progressbar_xcp = Worker_for_progressbar()
        self.worker_progressbar_xcp.change_value.connect(self.setProgressVal)
        self.worker_progressbar_xcp.duration = 60 / 100
        self.worker_xcp.finished.connect(self.xcp_worker_ended)
        self.worker_progressbar_xcp.finished.connect(self.task_xcp_calibration_finished)
        # Start Thread
        self.worker_xcp.start()
        self.worker_progressbar_xcp.start()
        self.ui.set_function_is_active_state()

    def xcp_worker_ended(self, *args, **kwargs):
        print("XCP worker done!")
        self.worker_progressbar_xcp.stop()

    def task_xcp_calibration_finished(self, *args, **kwargs):
        QApplication.processEvents()
        self.ui.set_waiting_for_request_state()

    def enable_aeb_n_fcw_domain_controller(self, function_name, *args, **kwargs):
        if self.is_host_responsive():
            xcp_ip = self.IP_address  # SGA
            xcp_port = 30207  # Domain Controller port = 30207
            a2l_file = f"{self.A2L_S19_BASE_FOLDER}\\adasdomaincontroller_server.a2l"

            tries = 10
            for i in range(tries):
                try:
                    xcp = Xcp.default_instance(xcp_ip, xcp_port, str(a2l_file))
                    print(f"Number of tries took to create XCP instance: '{i + 1}'")
                    break
                except IndexError as e:
                    if i < tries - 1:
                        sleep(1)
                        continue
                    else:
                        print(e)
                        self.ui.status_lbl.setText(f"Got an error : {e}")

            # calibrating value to the specefic signal and read calibration value
            signals = []
            if function_name == 'aeb_n_fcw':
                signals.append("calibration_data_override_enable_collision_mitigation_by_braking_with_braking_cal")
                signals.append("calibration_data_override_enable_forward_collision_warning_cal")
            elif function_name == 'rsi':
                signals.append("calibration_data_override_enable_road_sign_information_vision_cal")
                signals.append("calibration_data_override_enable_road_sign_information_electronic_horizon_cal")
                signals.append("calibration_data_override_enable_road_sign_information_cal")
            elif function_name == 'ddaw':
                signals.append("calibration_data_override_enable_driver_performance_support_cal")
                signals.append("calibration_data_override_enable_driver_monitoring_camera_enable_cal")
                signals.append("calibration_data_override_enable_driver_monitoring_lane_marking_enable_cal")
            elif function_name == 'lka':
                signals.append("calibration_data_override_enable_lane_keeping_aid_steering_cal")
                signals.append("calibration_data_override_enable_lane_keeping_aid_inattention_cal")
                signals.append("calibration_data_override_enable_lane_keeping_aid_braking_cal")
                signals.append("calibration_data_override_enable_lane_departure_warning_cal")
                signals.append("calibration_data_override_enable_emergency_lane_keeping_aid_warning_cal")
                signals.append("calibration_data_override_enable_emergency_lane_keeping_aid_steering_cal")
            elif function_name == 'pa':
                signals.append("calibration_data_override_enable_undertaking_prevention_cal")
                signals.append("calibration_data_override_enable_steering_assist_cal")
                signals.append("calibration_data_override_enable_lane_change_assist_cal")
                signals.append("calibration_data_override_enable_emergency_stop_assist_cal")
                signals.append("calibration_data_override_enable_distance_keeping_cal")
                signals.append("calibration_data_override_enable_curve_speed_assist_cal")
            elif function_name == 'pap':
                signals.append("calibration_data_override_enable_park_assist_sensor_cal")
                signals.append("calibration_data_override_enable_park_assist_camera_cal")
                signals.append("calibration_data_override_enable_parking_pilot_assist_cal")

            if self.ui.buttonGroup.checkedButton() == self.ui.dc_0_radio_btn:
                calibration_value = 0
            elif self.ui.buttonGroup.checkedButton() == self.ui.dc_1_radio_btn:
                calibration_value = 1
            elif self.ui.buttonGroup.checkedButton() == self.ui.dc_2_radio_btn:
                calibration_value = 2
            try:
                function_value = []
                for signal in signals:
                    xcp.calibrate(signal, calibration_value)
                    sleep(5)
                    function_value.append(xcp.read_calibration(signal))

                calibration_result = [val == calibration_value for val in function_value]

                if all(calibration_result):
                    self.ui.status_lbl.setText(
                        f"{function_name} set successfully! Calibration value = {calibration_value}")
                else:
                    self.ui.status_lbl.setText(f"{function_name} not correct! Calibration value = {calibration_value}")
            except:
                print("Didnt manage to set calibration!")
                self.ui.status_lbl.setText(f"Didnt manage to set calibration")
        else:
            self.ui.status_lbl.setText(f"Didnt manage to set calibration\nCheck connection - "
                                       f"VCU is not responsive.")

    def gen_report_long(self, *args, **kwargs):
        with PdfPages('all_plots.pdf') as pdf:
            pdf.savefig(self.signals_aeb_analysis_necessary())
            pdf.savefig(self.signals_from_manager_safe())
            pdf.savefig(self.signals_from_adas_actuation_arbitration_manager())
            pdf.savefig(self.signals_from_domain_controller())
        url = QtCore.QUrl.fromLocalFile(f"{os.getcwd()}\\all_plots.pdf").toString()
        self.ui.status_lbl.setText(f'<a href="{url}">Click to open all_plots.pdf</a>')

    def run_all_func_pytest(self, *args, **kwargs):
        pytest.main([f"{os.getcwd()}\\pytest\\function_test\\test_adas_all_func.py", r"--html=pytest\reports\test_report_all_adas_func.html", "-o", "log_cli=true", "-v"])
        report_destination = f"{os.getcwd()}\\pytest\\reports"
        self.ui.status_lbl.setText(f'<a href="{report_destination}">Report(s) can be found here: {report_destination}</a>')

    def run_aeb_pytest(self, *args, **kwargs):
        pytest.main([f"{os.getcwd()}\\pytest\\function_test\\test_aeb_func.py", r"--html=pytest\reports\report_aeb_check.html", "-o", "log_cli=true", "-v"])
        report_destination = f"{os.getcwd()}\\pytest\\reports"
        self.ui.status_lbl.setText(f'<a href="{report_destination}">Report(s) can be found here: {report_destination}</a>')

    def run_lka_pytest(self, *args, **kwargs):
        pytest.main([f"{os.getcwd()}\\pytest\\function_test\\test_lka_func.py", r"--html=pytest\reports\report_lka_check.html", "-o", "log_cli=true", "-v"])
        report_destination = f"{os.getcwd()}\\pytest\\reports"
        self.ui.status_lbl.setText(f'<a href="{report_destination}">Report(s) can be found here: {report_destination}</a>')

    def run_rsi_pytest(self, *args, **kwargs):
        pytest.main([f"{os.getcwd()}\\pytest\\function_test\\test_rsi_func.py", r"--html=pytest\reports\report_rsi_check.html", "-o", "log_cli=true", "-v"])
        report_destination = f"{os.getcwd()}\\pytest\\reports"
        self.ui.status_lbl.setText(f'<a href="{report_destination}">Report(s) can be found here: {report_destination}</a>')

    def run_ddaw_pytest(self, *args, **kwargs):
        pytest.main([f"{os.getcwd()}\\pytest\\function_test\\test_ddaw_func.py", r"--html=pytest\reports\report_ddaw_check.html", "-o", "log_cli=true", "-v"])
        report_destination = f"{os.getcwd()}\\pytest\\reports"
        self.ui.status_lbl.setText(f'<a href="{report_destination}">Report(s) can be found here: {report_destination}</a>')

    def run_pa_pytest(self, *args, **kwargs):
        pytest.main([f"{os.getcwd()}\\pytest\\function_test\\test_pa_func.py", r"--html=pytest\reports\report_pa_check.html", "-o", "log_cli=true", "-v"])
        report_destination = f"{os.getcwd()}\\pytest\\reports"
        self.ui.status_lbl.setText(f'<a href="{report_destination}">Report(s) can be found here: {report_destination}</a>')

    def run_pap_pytest(self, *args, **kwargs):
        pytest.main([f"{os.getcwd()}\\pytest\\function_test\\test_pap_func.py", r"--html=pytest\reports\report_pa_check.html", "-o", "log_cli=true", "-v"])
        report_destination = f"{os.getcwd()}\\pytest\\reports"
        self.ui.status_lbl.setText(f'<a href="{report_destination}">Report(s) can be found here: {report_destination}</a>')

    def sanity_check_fault_matrix(self, *args, **kwargs):
        if self.is_host_responsive():
            self.ui.progressBar.setProperty("value", 25)
            QGuiApplication.processEvents()
            # 1. set topics to channel 95 only
            self.TOPICS_TO_FM = self.data["dcf_configuration"]["topics_to_fault_matrix"]
            # 2. take only 5 second hostlog
            self.ui.status_lbl.setText("Quick check fault matrix started!!!")
            QGuiApplication.processEvents()
            self.hostlog_start_logging(self.DCF_TDF_PATH, self.DCF_PATH, self.DCF_LOG_DESTINATION_FOLDER, 10,
                                       self.TOPICS_TO_FM)
            self.ui.progressBar.setProperty("value", 75)
            # 3. decode
            decode_dcf_log_vcc(self)
            self.ui.progressBar.setProperty("value", 100)
            # 4. pop up fault matrix
            self.check_fault_matrix()
        else:
            self.ui.status_lbl.setText("SGA2HPA - Host not responsive.")

    def sanity_check_zen_fault_matrix(self, *args, **kwargs):
        if self.is_host_responsive():
            self.ui.progressBar.setProperty("value", 25)
            QGuiApplication.processEvents()

            # 1. set topics to channel 95 only
            self.topics_to_zen_fm_check = self.data["dcf_configuration"]["topics_to_adas"]

            # 2. take only 5 second hostlog
            self.ui.status_lbl.setText("Quick check fault matrix started!!!")
            QGuiApplication.processEvents()
            self.hostlog_start_logging(self.DCF_TDF_PATH, self.DCF_PATH, self.DCF_LOG_DESTINATION_FOLDER, 10,
                                       self.topics_to_zen_fm_check)
            self.ui.progressBar.setProperty("value", 75)

            # 3. decode
            decode_dcf_log_zenseact(self)
            self.ui.progressBar.setProperty("value", 100)

            # 4. pop up zen fault check table
            self.generate_health_monitor_table()
        else:
            self.ui.status_lbl.setText("SGA2HPA - Host not responsive.")

    def sanity_check(self, *args, **kwargs):
        pytest.main([f"{os.getcwd()}\\pytest\\sanity_check", r"--html=pytest\reports\report_sanity_check.html", "-o", "log_cli=true", "-v"])
        report_destination = f"{os.getcwd()}\\pytest\\reports"
        self.ui.status_lbl.setText(f'<a href="{report_destination}">Report(s) can be found here: {report_destination}</a>')

    def get_hostlog_client_version(self):
        try:
            with open(self.CHANGE_LOG) as md:
                content = md.read()
                match = re.search(r"## \[(\d+)\.(\d+)\.(\d+)\]", content)
                return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        except:
            return (0, 0, 0)

    def load_dbc_asc(self, *args, **kwargs):
        dbc_files = glob(os.path.join(self.CAN_LOGS_PATH, "*.dbc"))
        asc_files = glob(os.path.join(self.CAN_LOGS_PATH, "*.asc"))
        dbc_files.sort(key=os.path.getmtime, reverse=True)
        asc_files.sort(key=os.path.getmtime, reverse=True)
        if dbc_files and asc_files:
            dbc_file = dbc_files[0]
            asc_file = asc_files[0]
        else:
            self.ui.status_lbl.setText(f"Please make sure dbc and asc file under {self.CAN_LOGS_PATH}")
            return None
        db = cantools.database.load_file(dbc_file)
        return db, asc_file

    def can_signal_converter(self, can_signal, frame, db, asc_file, converter, signal_mapping_dict=None, debug=False,
                             *args, **kwargs):
        '''
        To check CAN signals and return numerical values in order to plot

        Parameters:
        can_signal (str): can signal name
        frame (str): can frame name
        db (cantools.database.can.database.Database): dbc file
        asc_file (str): asc file
        converter (type): convert signal original type to str or float
        signal_mapping_dict (dict): map signal values to plot according to signal definition
        '''
        message = db.get_message_by_name(frame)
        for signal in message.signals:
            if signal.name == can_signal:
                signal_wanted = signal
        can_signal_val = []
        with can.io.ASCReader(asc_file) as reader:
            for msg in reader:
                # Check if this message has the same ID as the one we're interested in
                if msg.arbitration_id == message.frame_id:
                    # Decode the message
                    decoded_message = db.decode_message(msg.arbitration_id, msg.data)
                    if converter == str:
                        can_signal_val.append(str(decoded_message[signal_wanted.name]))
                    if converter == float:
                        can_signal_val.append(float(decoded_message[signal_wanted.name]))
        if signal_mapping_dict:
            numerical_signal_val = [signal_mapping_dict[value] for value in can_signal_val]
        else:
            numerical_signal_val = can_signal_val
        if debug:
            print(signal_wanted)
        return numerical_signal_val

    def check_aca(self, directory, *args, **kwargs):
        search_pattern_pre = os.path.join(directory, '**', '*pre_aca*.hdf5')
        search_pattern_post = os.path.join(directory, '**', '*post_aca*.hdf5')
        pre_aca_file = glob(search_pattern_pre, recursive=True)
        post_aca_file = glob(search_pattern_post, recursive=True)
        self.aca_mode_latest_log = len(pre_aca_file) > 0 and len(post_aca_file) > 0
        if self.aca_mode_latest_log:
            self.ui.aam_signal_analysis_btn.setEnabled(False)
            self.ui.aca_long_btn.setEnabled(True)
        else:
            self.ui.aam_signal_analysis_btn.setEnabled(True)
            self.ui.aca_long_btn.setEnabled(False)

    def gui_clear_dtc(self, *args, **kwargs):
        clear_DTC(self.OSB_PATH)
        self.ui.status_lbl.setText("Clearing DTC is done.")

    def gui_disable_firewall(self, *args, **kwargs):
        default_hpaa_pin_F = 'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
        default_hpaa_pin_5 = '5555555555555555555555555555555555555555555555555555555555555555'
        pin, ok = QInputDialog.getText(self.ui.DisableFirewall_btn, 'Enter HPAA (1D12) PIN',
                                       f'F = {default_hpaa_pin_F}\n5 = {default_hpaa_pin_5}', QLineEdit.Normal, 'F')
        if ok:
            if pin == 'F':
                print("Entered HPAA (1D12) PIN:", default_hpaa_pin_F)
                entered_pin = default_hpaa_pin_F
            elif pin == '5':
                print("Entered HPAA (1D12) PIN:", default_hpaa_pin_5)
                entered_pin = default_hpaa_pin_5
            else:
                entered_pin = pin
            self.ui.status_lbl.setText(f"Entered HPAA (1D12) PIN: {entered_pin}")
            self.sga2hpa()
            diag_unlock_level_17(self.OSB_PATH, entered_pin)
            disable_firewall(self.OSB_PATH, entered_pin)
            self.ui.status_lbl.setText(f"{self.ui.status_lbl.text()}\nDisabling the firewall is done.")

    def generate_health_monitor_table(self, *args, **kwargs):
        zen_qm_feature_a = f"{self.get_latest_folder_in_directory(self.ZEN_DECODED_PATH)}\\zen_qm_feature_a.hdf5"
        bin_name = zen_qm_feature_a.split('\\')[-2]
        with h5py.File(zen_qm_feature_a, 'r') as qm_feature_a:
            corrective_steering_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'corrective_steering_faults'][:]
            curve_speed_assist_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'curve_speed_assist_faults'][:]
            driver_state_estimation_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'driver_state_estimation_faults'][:]
            emergency_braking_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'emergency_braking_faults'][:]
            emergency_collision_warning_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'emergency_collision_warning_faults'][:]
            evasive_steering_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'evasive_steering_faults'][:]
            lane_centering_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'lane_centering_faults'][:]
            lane_change_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'lane_change_faults'][:]
            nominal_distance_control_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'nominal_distance_control_faults'][:]
            nominal_set_speed_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'nominal_set_speed_faults'][:]
            object_tracking_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'object_tracking_faults'][:]
            road_model_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'road_model_faults'][:]
            road_properties_estimation_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'road_properties_estimation_faults'][:]
            road_sign_information_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'road_sign_information_faults'][:]
            scene_estimation_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'scene_estimation_faults'][:]
            stop_in_lane_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['system_faults'][
                'stop_in_lane_faults'][:]
            flcw_blocked_faults = \
            qm_feature_a['zen_qm_feature_a']['health_monitor_a_outputs']['data']['cameras_blockage_status']['flcw'][
                'blocked']['unitless']['value'][:]
            yaw_rate_quality = \
            qm_feature_a['zen_qm_feature_a']['zen_qm_feature_a_vehicle_motion_state_data']['data']['yaw_rate'][
                'quality'][:]
            ###
            acc_dist_keeping_enable = \
            qm_feature_a['zen_qm_feature_a']['enabled_features']['data']['acc_with_distance_keeping_enabled'][
                'unitless']['value'][:]
            acc_without_dist_keeping_enable = \
            qm_feature_a['zen_qm_feature_a']['enabled_features']['data']['acc_without_distance_keeping_enabled'][
                'unitless']['value'][:]
            acs_enable_steering = \
            qm_feature_a['zen_qm_feature_a']['enabled_features']['data']['acs_enabled']['steering']['unitless'][
                'value'][:]
            acs_enable_warning = \
            qm_feature_a['zen_qm_feature_a']['enabled_features']['data']['acs_enabled']['warning']['unitless'][
                'value'][:]
            aeb_enable = \
            qm_feature_a['zen_qm_feature_a']['enabled_features']['data']['aeb_enabled']['enable_aeb']['unitless'][
                'value'][:]
            aeb_enable_warning = \
            qm_feature_a['zen_qm_feature_a']['enabled_features']['data']['aeb_enabled']['enable_cw']['unitless'][
                'value'][:]
            rms_enable = qm_feature_a['zen_qm_feature_a']['enabled_features']['data']['rms_enabled']['unitless'][
                             'value'][:]
            rsi_enable = qm_feature_a['zen_qm_feature_a']['enabled_features']['data']['rsi_enabled']['unitless'][
                             'value'][:]
            lca_enable = qm_feature_a['zen_qm_feature_a']['enabled_features']['data']['lca_enabled']['unitless'][
                             'value'][:]
            ###
            feature_enable_aeb = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['calong_feature_enable']['enable_aeb'][
                'unitless']['value'][:]
            feature_enable_cw = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['calong_feature_enable']['enable_cw'][
                'unitless']['value'][:]
            # feature_enable_acc_aeb_disable = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc']['enable_details_acc']['aeb_disabled']['unitless']['value'][:]
            # feature_enable_acc_driver_door_not_closed = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc']['enable_details_acc']['camera_calibration_faulted']['unitless']['value'][:]
            # feature_enable_cc_enabled = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc']['enable_details_acc']['cc_enabled']['unitless']['value'][:]
            # feature_enable_cc_esc_disable = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc']['enable_details_acc']['cruise_stability_control_deactivation_requested']['unitless']['value'][:]
            feature_enable_acc_driver_door_not_closed = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc'][
                'enable_details_acc']['driver_door_not_closed']['unitless']['value'][:]
            feature_enable_acc_driver_not_buckled = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc'][
                'enable_details_acc']['driver_not_buckled']['unitless']['value'][:]  # expected to be 1
            feature_enable_acc_driver_not_present = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc'][
                'enable_details_acc']['driver_not_present']['unitless']['value'][:]  # expected to be 0 ?
            feature_enable_acc_unavailable = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc'][
                'enable_details_acc']['feature_unavailable']['unitless']['value'][:]  # expected to be 0 ?
            feature_enable_acc_gear_not_in_drive = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc'][
                'enable_details_acc']['gear_not_in_drive']['unitless']['value'][:]
            # feature_enable_acc_matured_system_faults = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc']['enable_details_acc']['matured_system_faults']['unitless']['value'][:]
            feature_enable_acc_sensor_blocked = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc'][
                'enable_details_acc']['sensor_blocked']['unitless']['value'][:]
            # feature_enable_acc_service_calibration_active = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc']['enable_details_acc']['service_calibration_active']['unitless']['value'][:]
            feature_enable_acc_trailer_present = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_acc'][
                'enable_details_acc']['trailer_present']['unitless']['value'][:]
            feature_enable_ta_acc_disabled = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_ta'][
                'enable_details_ta']['acc_disabled']['unitless']['value'][:]
            feature_enable_ta_acs_disabled = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_ta'][
                'enable_details_ta']['acs_disabled']['unitless']['value'][:]
            feature_enable_ta_dmc_blocked = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_ta'][
                'enable_details_ta']['dmc_blocked']['unitless']['value'][:]
            feature_enable_ta_dsw_disabled = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_ta'][
                'enable_details_ta']['dsw_disabled']['unitless']['value'][:]
            feature_enable_ta_externally_disabled = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_ta'][
                'enable_details_ta']['externally_disabled']['unitless']['value'][:]
            feature_enable_ta_system_incapable = \
            qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_ta'][
                'enable_details_ta']['system_incapable']['unitless']['value'][:]
            # feature_enable_ta = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_ta']['enable_state_ta']['unitless']['value'][:]
            # feature_enable_lca = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_lca']['enable_state_lca']['unitless']['value'][:]
            # feature_enable_rsi = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_rsi']['enable_state_rsi']['unitless']['value'][:]
            # feature_enable_rms_steering = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_rms']['steering']['enable_state']['unitless']['value'][:]
            # feature_enable_rms_braking = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_rms']['braking']['enable_state']['unitless']['value'][:]
            # feature_enable_aes = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_aes']['enabled']['unitless']['value']['unitless']['value'][:]
            # feature_enable_dsw_drowsiness = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_dsw']['enable_state_drowsiness']['unitless']['value'][:]
            # feature_enable_dsw_inattention = qm_feature_a['zen_qm_feature_a']['feature_enable_flags']['data']['feature_enable_dsw']['enable_state_inattention']['unitless']['value'][:]
            ###
            target_tracking_age_flr = qm_feature_a['zen_qm_feature_a']['comfort_features_manager_debug']['data'][
                                          'nominal_comfort_ability_debug']['target_tracking_sensor_aging_status'][
                                          'forward_looking_radar']['aging_check']['unitless']['value'][:]
            target_tracking_age_fsrl = qm_feature_a['zen_qm_feature_a']['comfort_features_manager_debug']['data'][
                                           'nominal_comfort_ability_debug']['target_tracking_sensor_aging_status'][
                                           'front_left_radar']['aging_check']['unitless']['value'][:]
            target_tracking_age_fsrr = qm_feature_a['zen_qm_feature_a']['comfort_features_manager_debug']['data'][
                                           'nominal_comfort_ability_debug']['target_tracking_sensor_aging_status'][
                                           'front_right_radar']['aging_check']['unitless']['value'][:]
            target_tracking_age_rsrl = qm_feature_a['zen_qm_feature_a']['comfort_features_manager_debug']['data'][
                                           'nominal_comfort_ability_debug']['target_tracking_sensor_aging_status'][
                                           'rear_left_radar']['aging_check']['unitless']['value'][:]
            target_tracking_age_rsrr = qm_feature_a['zen_qm_feature_a']['comfort_features_manager_debug']['data'][
                                           'nominal_comfort_ability_debug']['target_tracking_sensor_aging_status'][
                                           'rear_right_radar']['aging_check']['unitless']['value'][:]
        zen_asil_feature_a = f"{self.get_latest_folder_in_directory(self.ZEN_DECODED_PATH)}\\zen_asil_feature_a.hdf5"
        with h5py.File(zen_asil_feature_a, 'r') as asil_feature_a:
            # vms_yaw_rate_quality  = qm_feature_a['zen_qm_feature_a']['zen_qm_feature_a_vehicle_motion_state_data']['data']['yaw_rate']['quality']['unitless']['value'][:]
            ###
            asil_enable_manager = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'enable_manager_ok']['unitless']['value'][:]
            asil_lane_center_model = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'lane_center_model_ok']['unitless']['value'][:]
            asil_aes_lane_markers_ok = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'lane_markers_ok']['unitless']['value'][:]
            asil_aes_lat_req_confirmed = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'lateral_request_type_confirmed_ok']['unitless']['value'][:]
            asil_aes_parameters_ok = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'parameters_ok']['unitless']['value'][:]
            asil_aes_road_work_ok = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'road_work_ok']['unitless']['value'][:]
            asil_aes_TTok = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'target_tracking_output_ok']['unitless']['value'][:]
            asil_aes_validatedTT = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'validated_target_tracking_output_ok']['unitless']['value'][:]
            asil_aes_vehiclecontrol_ok = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'vehicle_control_state_ok']['unitless']['value'][:]
            asil_vehicle_motion_state_ok = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'vehicle_motion_state_ok']['unitless']['value'][:]
            asil_vision_free_space_ok = \
            asil_feature_a['zen_asil_feature_a']['zen_asil_feature_a_aes_diagnostics']['data']['health'][
                'vision_freespace_ok']['unitless']['value'][:]
        zen_qm_vision = f"{self.get_latest_folder_in_directory(self.ZEN_DECODED_PATH)}\\zen_qm_vision.hdf5"
        with h5py.File(zen_qm_vision, 'r') as qm_vision:
            dec_validity  = qm_vision['zen_qm_vision']['calibration_validity']['data']['is_valid']['unitless']['value'][:]
            calibration_fault  = qm_vision['zen_qm_vision']['calibration_fault']['data']['fault_state']['unitless']['value'][:]

            health_monitor_lst = {
                0: (corrective_steering_faults, 0),
                1: (curve_speed_assist_faults, 0),
                2: (driver_state_estimation_faults, 0),
                3: (emergency_braking_faults, 0),
                4: (emergency_collision_warning_faults, 0),
                5: (evasive_steering_faults, 0),
                6: (lane_centering_faults, 0),
                7: (lane_change_faults, 0),
                8: (nominal_distance_control_faults, 0),
                9: (nominal_set_speed_faults, 0),
                10: (object_tracking_faults, 0),
                11: (road_model_faults, 0),
                12: (road_properties_estimation_faults, 0),
                13: (road_sign_information_faults, 0),
                14: (scene_estimation_faults, 0),
                15: (stop_in_lane_faults, 0),
                16: (flcw_blocked_faults, 0),
                17: (acc_dist_keeping_enable, 1),
                18: (acc_without_dist_keeping_enable, 0),
                19: (acs_enable_steering, 1),
                20: (acs_enable_warning, 1),
                21: (aeb_enable, 1),
                22: (aeb_enable_warning, 1),
                23: (rms_enable, 1),
                24: (rsi_enable, 1),
                25: (lca_enable, 1),
                26: (feature_enable_aeb, 1),
                27: (feature_enable_cw, 1),
                28: (feature_enable_acc_driver_door_not_closed, 0),
                29: (feature_enable_acc_driver_not_buckled, 0),
                30: (feature_enable_acc_driver_not_present, 0),
                31: (feature_enable_acc_unavailable, 0),
                32: (feature_enable_acc_gear_not_in_drive, 0),
                33: (feature_enable_acc_sensor_blocked, 0),
                34: (feature_enable_acc_trailer_present, 0),
                35: (feature_enable_ta_acc_disabled, 0),
                36: (feature_enable_ta_acs_disabled, 0),
                37: (feature_enable_ta_dmc_blocked, 0),
                38: (feature_enable_ta_dsw_disabled, 0),
                39: (feature_enable_ta_externally_disabled, 0),
                40: (feature_enable_ta_system_incapable, 0),
                41: (target_tracking_age_flr, 1),
                42: (target_tracking_age_fsrl, 1),
                43: (target_tracking_age_fsrr, 1),
                44: (target_tracking_age_rsrl, 1),
                45: (target_tracking_age_rsrr, 1),
                46: (asil_enable_manager, 1),
                47: (asil_lane_center_model, 1),
                48: (asil_aes_lane_markers_ok, 1),
                49: (asil_aes_lat_req_confirmed, 1),
                50: (asil_aes_parameters_ok, 1),
                51: (asil_aes_road_work_ok, 1),
                52: (asil_aes_TTok, 1),
                53: (asil_aes_validatedTT, 1),
                54: (asil_aes_vehiclecontrol_ok, 1),
                55: (asil_vehicle_motion_state_ok, 1),
                56: (asil_vision_free_space_ok, 1),
                57: (dec_validity, 1),
                58: (calibration_fault, 0),
                59: (yaw_rate_quality, 2)
                }
            health_monitor_fault_dict = dict()
            health_monitor_fault_dict['Index'] = list(range(len(self.HEALTH_MONITOR)))
            health_monitor_fault_dict['Signals'] = [self.HEALTH_MONITOR[i] for i in health_monitor_fault_dict['Index']]
            # check signal data with expected values
            health_monitor_fault_check_result_lst = []
            for i in range(len(self.HEALTH_MONITOR)):
                signal_data, expected_value = health_monitor_lst[i]
                if i != 59:
                    health_monitor_fault_check_result_lst.append(self.signal_check_with_expected_values(signal_data, expected_value))
                # signal 59 is yaw_rate_quality, using a different check function
                elif i == 59:
                    health_monitor_fault_check_result_lst.append(self.signal_quality_check(signal_data))

            # print(f"{self.HEALTH_MONITOR=}")
            # print(f"{health_monitor_fault_check_result_lst=}")
            health_monitor_fault_dict['States'] = health_monitor_fault_check_result_lst
            # print(f"{health_monitor_fault_dict=}")
            self.health_monitor_table = TableDialog(health_monitor_fault_dict, ['Index', 'Signals', 'States'], f"Health Monitor Fault List - {bin_name}")
            self.health_monitor_table.exec_()

    def signal_check_with_expected_values(self, signal_data, expected_value, *args, **kwargs):
        unexpected_value = abs(expected_value - 1) # 0 -> 1 or 1 -> 0
        # Unexpected value exists
        if unexpected_value in signal_data:
            # Mixed with expected values and unexpected values
            if expected_value in signal_data:
                return "Intermittent fault / disabled"
            # All unexpected values
            else:
                return "Faulty / disabled all the time"
        # All expected values
        else:
            return "No fault / Always enabled"

    def signal_quality_check(self, data, *args, **kwargs):
        l, data_l = len(data), list(data)
        zero, one, two = data_l.count(0) / l * 100, data_l.count(1) / l * 100, data_l.count(2) / l * 100
        return f"Accurate {two}%\nOutsideSpecification {one}%\nUndefined{zero}%"

    def update_comment_panel(self, *args, **kwargs):
        plainTextEdit_text = self.ui.plainTextEdit.toPlainText()
        with open(self.CS_MANIFEST, 'r') as manifest:
            data = yaml.safe_load(manifest)
            adadas_ver = data['hp']['modules']['ad-adas-a']['version']
            self.ui.plainTextEdit.setPlainText(f"ad-adas version: {adadas_ver}\n{plainTextEdit_text}")

    def run_batch_decoder(self, *args, **kwargs):  # Correct method definition with 'self'
        try:
            subprocess.run(['python', 'batch_decoder.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    def run_car_ip(self, *args, **kwargs):
        try:
            result = subprocess.run(['python', 'car_ip.py'], capture_output=True, text=True, check=True)
            self.show_message(result.stdout)
        except subprocess.CalledProcessError as e:
            self.show_message(f"Error: {e}")

    def show_message(self, message):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Vehicle Information")

        plain_text_edit = QtWidgets.QPlainTextEdit()
        plain_text_edit.setPlainText(message)
        plain_text_edit.setReadOnly(True)
        plain_text_edit.setFixedSize(300, 100)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(plain_text_edit)

        layout_widget = QtWidgets.QWidget()
        layout_widget.setLayout(layout)

        msg_box.layout().addWidget(layout_widget, 0, msg_box.layout().rowCount(), 1, msg_box.layout().columnCount())
        msg_box.setFixedSize(200, 100)
        msg_box.exec_()

class TableDialog(QDialog):
    def __init__(self, data, headers, title):
        super(TableDialog, self).__init__()
        self.headers = headers
        self.resize(700, 1000)
        self.table = QTableWidget(len(data[headers[0]]), len(self.headers))
        self.setWindowTitle(title)
        # Hide the vertical headers (the row numbers)
        self.table.verticalHeader().setVisible(False)
        self.populate_table(data)
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+Shift+Q'), self)
        shortcut.activated.connect(self.close)
        # Auto-resize rows and columns to fit contents
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def populate_table(self, data):
        brush = QBrush(QColor(QtCore.Qt.red))
        yellow = QBrush(QColor(QtCore.Qt.yellow))
        for i in range(self.table.rowCount()):
            for j, header in enumerate(self.headers):
                item = QTableWidgetItem(str(data[header][i]))
                self.table.setItem(i, j, item)
            if data[self.headers[-1]][i] in [True, 'Terminated', 'Faulty / disabled all the time']:
                for c in range(len(self.headers)):
                    self.table.item(i, c).setBackground(brush)
            if data[self.headers[-1]][i] in ['Idle', 'Starting', 'Intermittent fault / disabled']:
                for c in range(len(self.headers)):
                    self.table.item(i, c).setBackground(yellow)
        self.table.setHorizontalHeaderLabels(self.headers)


class HeatmapDialog(QDialog):
    def __init__(self, data, title, fault_matrix_description, parent=None):
        super().__init__(parent)
        self.title = title
        self.fault_matrix_description = fault_matrix_description
        self.resize(1200, 800)
        self.initUI(data)
        self.setWindowIcon(QIcon('_resources/icons/fm.png'))
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+Shift+Q'), self)
        shortcut.activated.connect(self.close)

    def initUI(self, data):
        self.setWindowTitle(self.title)
        layout = QVBoxLayout(self)
        fig = plt.Figure()
        fig.tight_layout()
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=0.05, left=0.4, top=0.95)
        int_data = data.astype(int).T

        # Plot the heatmap
        ax.set_yticks(np.arange(-.5, 35, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='--', linewidth=0.5)
        im = ax.imshow(int_data, cmap='viridis', aspect='auto', vmin=0, vmax=1, interpolation='none')
        ax.set_yticks(range(0, data.shape[1], 1))
        ax.set_yticklabels(self.fault_matrix_description, rotation='horizontal')
        cbar = fig.colorbar(im, ax=ax, ticks=[0, 1])
        cbar.set_ticklabels(['No Fault', 'Fault'])

        # mark verdicts on each fault if it is always faulty or flickering
        for index, row in enumerate(int_data):
            if True in row and False in row:
                ax.get_yticklabels()[index].set_backgroundcolor('gray')
            elif row.all():  # Check if all elements in the row are True which means the fault is always there
                ax.get_yticklabels()[index].set_backgroundcolor('yellow')

        # Create a canvas for the figure and add to the layout
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas, 95)
        linkLabel = QLabel('<a href="open_excel">Check Fault matrix in details</a>', self)
        linkLabel.setOpenExternalLinks(False)
        linkLabel.linkActivated.connect(self.openExcelFile)
        layout.addWidget(linkLabel, 5)
        self.setLayout(layout)

    def openExcelFile(self):
        # Specify the path to your Excel file
        excelFilePath = r'_resources\files\FaultMatrix_CarweaverBased.xlsx'
        # Open the Excel file
        QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(excelFilePath))
