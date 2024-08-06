#!/usr/bin/env python3.8
"""
This is the entry to the main GUI of Vehicle logger.
The link between functions and the widgets are connected in Main_GUI.

"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtWidgets import QMessageBox, QShortcut
from vehicle_logger_func import vehicle_logger_func


class Main_GUI(QtWidgets.QWidget, vehicle_logger_func):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Link functions to widgets

        # Button Actions Tab "Config and logging"
        self.ui.load_file_btn.clicked.connect(self.load_yaml_file)
        self.ui.fetch_tdf_btn.clicked.connect(self.hostlog_fetch_topics_threading)
        self.ui.start_logging_btn.clicked.connect(self.hostlog_start_logging_threading)
        self.ui.get_sw_info_btn.clicked.connect(self.get_sw_info)
        self.ui.decode_btn.clicked.connect(self.decode_dcf)
        self.ui.batch_decode_btn.clicked.connect(self.run_batch_decoder)
        self.ui.download_hostlog_btn.clicked.connect(self.download_hostlog_client)
        self.ui.update_tdf_btn.clicked.connect(self.update_tdf)
        self.ui.get_app_state_btn.clicked.connect(self.get_em_control_app_state)
        self.ui.get_ip_vin_btn.clicked.connect(self.run_car_ip)
        self.ui.SGA_IP_address.clicked.connect(self.get_ip_address)
        self.ui.HPA_IP_address.clicked.connect(self.get_ip_address)
        self.ui.custom_IP_address_radio_button.clicked.connect(self.get_ip_address)
        self.ui.custom_IP_address_line_edit.textChanged.connect(self.get_ip_address)
        self.ui.Comment_btn.clicked.connect(self.save_comment)
        self.ui.FM_quick_check_btn.clicked.connect(self.sanity_check_fault_matrix)
        self.ui.zen_fault_check_btn.clicked.connect(self.sanity_check_zen_fault_matrix)
        self.ui.sanity_check_btn.clicked.connect(self.sanity_check)
        self.ui.DisableFirewall_btn.clicked.connect(self.gui_disable_firewall)
        self.ui.ClearDTC_btn.clicked.connect(self.gui_clear_dtc)

        # AEB Check tab
        self.ui.can_check_btn.clicked.connect(self.can_check)
        self.ui.aeb_analysis_btn.clicked.connect(self.plot_aeb_analysis_necessary_signals)
        self.ui.ms_signal_analysis_btn.clicked.connect(self.plot_signals_from_manager_safe)
        self.ui.aam_signal_analysis_btn.clicked.connect(self.plot_signals_from_adas_actuation_arbitration_manager)
        self.ui.aca_long_btn.clicked.connect(self.plot_signals_from_aca_long)
        self.ui.domain_controller_signal_analysis_btn.clicked.connect(self.plot_signals_from_domain_controller)
        self.ui.fault_matrix_btn.clicked.connect(self.check_fault_matrix)
        self.ui.generate_report_btn.clicked.connect(self.gen_report_long)
        self.ui.health_monitor_fault_btn.clicked.connect(self.generate_health_monitor_table)
        self.ui.all_pytest_btn.clicked.connect(self.run_all_func_pytest)
        self.ui.aeb_pytest_btn.clicked.connect(self.run_aeb_pytest)
        self.ui.lat_pytest_btn.clicked.connect(self.run_lka_pytest)
        self.ui.rsi_pytest_btn.clicked.connect(self.run_rsi_pytest)
        self.ui.ddaw_pytest_btn.clicked.connect(self.run_ddaw_pytest)
        self.ui.pa_pytest_btn.clicked.connect(self.run_pa_pytest)
        self.ui.pap_pytest_btn.clicked.connect(self.run_pap_pytest)
        self.ui.Comment_btn.clicked.connect(self.save_comment)
        # Lateral Check tab
        self.ui.pscm_can_check_btn.clicked.connect(self.pscm_can_check)
        self.ui.lat_analysis_plots_btn.clicked.connect(self.plot_lka_analysis_necessary_signals)
        self.ui.hpa_hib_btn.clicked.connect(self.plot_signals_from_hpa_hib)
        self.ui.hib_hpa_btn.clicked.connect(self.plot_signals_from_hib_hpa)
        self.ui.aca_lat_btn.clicked.connect(self.plot_signals_from_aca_lat)
        self.ui.lat_dc_fault_mat_btn.clicked.connect(self.check_fault_matrix)
        self.ui.lat_analysis_plots_btn.clicked.connect(self.gen_lat_report)
        self.ui.lat_pytest_btn.clicked.connect(self.run_lat_pytest)

        # XCP tab
        self.ui.dl_adas_a2l_s19__btn.clicked.connect(self.fetch_a2l_s19_button_action)
        self.ui.ena_aeb_fcw_dc_btn.clicked.connect(lambda: self.start_xcp_calibration_threading('aeb_n_fcw'))
        self.ui.ena_rsi_btn.clicked.connect(lambda: self.start_xcp_calibration_threading('rsi'))
        self.ui.ena_ddaw_btn.clicked.connect(lambda: self.start_xcp_calibration_threading('ddaw'))
        self.ui.ena_lka_btn.clicked.connect(lambda: self.start_xcp_calibration_threading('lka'))
        self.ui.ena_pa_btn.clicked.connect(lambda: self.start_xcp_calibration_threading('pa'))
        self.ui.ena_pap_btn.clicked.connect(lambda: self.start_xcp_calibration_threading('pap'))
        self.ui.sanity_check_btn.clicked.connect(self.sanity_check)
        self.ui.refresh_hlc_btn.clicked.connect(self.get_latest_hostlog_version)


        # Button Actions Tab Post process
        self.ui.get_vehicle_logs_btn.clicked.connect(self.get_vcu_logs_thread)
        self.ui.make_bundle_btn.clicked.connect(self.run_cpu_load_bundle_script)
        self.ui.make_tracebuffer_btn.clicked.connect(self.run_cpu_load_tracelogger_script)
        self.ui.deploy_btn.clicked.connect(self.deploy_logs)
        self.ui.pack_logs_btn.clicked.connect(self.zip_dlt_can_dct_log)
        self.ui.sga2hpa_btn.clicked.connect(self.sga2hpa)


        # set up shortcuts to most frequent used functions
        QShortcut(QKeySequence('Ctrl+Shift+Q'), self, self.proper_shutdown)
        QShortcut(QKeySequence('Ctrl+Shift+L'), self, self.load_yaml_file)
        QShortcut(QKeySequence('Ctrl+Shift+F'), self, self.hostlog_fetch_topics_threading)
        QShortcut(QKeySequence('Ctrl+Shift+S'), self, self.sga2hpa)
        QShortcut(QKeySequence('Ctrl+Shift+H'), self, self.hostlog_start_logging_threading)
        QShortcut(QKeySequence('Ctrl+Shift+D'), self, self.decode_dcf)
        QShortcut(QKeySequence('Ctrl+Shift+Z'), self, self.zip_dlt_can_dct_log)
        QShortcut(QKeySequence('Ctrl+Shift+A'), self, self.deploy_logs)
        QShortcut(QKeySequence('Ctrl+Shift+M'), self, self.check_fault_matrix)

        self.setWindowIcon(QIcon('_resources/icons/sva.ico'))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close',
                                     'Are you sure you want to close \nCArbonaras super APP?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print('Window closed')
            self.proper_shutdown()
            event.accept()
        else:
            event.ignore()

    def proper_shutdown(self):
        app.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myWidget = Main_GUI()
    myWidget.show()
    sys.exit(app.exec_())
