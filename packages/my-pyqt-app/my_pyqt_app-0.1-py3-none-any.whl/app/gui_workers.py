from PyQt5.QtCore import QObject, QThread, pyqtSignal
from _resources.get_vehicle_logs import *
from time import sleep


class Worker_for_get_vehicle_logs(QThread):
    # Create a counter thread
    def __init__(self, vehicle_test) -> None:
        super().__init__()
        self.vehicle_test = vehicle_test

    finished = pyqtSignal(str)
    def run(self):
        get_vehicle_logs(self.vehicle_test)
        self.finished.emit('Worker_for_get_vehicle_logs -> finished...')

class Worker_for_run_bundle_script(QThread):
    # Create a counter thread
    def __init__(self, vehicle_test) -> None:
        super().__init__()
        self.vehicle_test = vehicle_test

    finished = pyqtSignal(str)
    def run(self):
        run_bundle_script(self.vehicle_test)
        self.finished.emit('Bundle script is done, check log_files folder -> finished...')

class Worker_for_run_tracelogger_script(QThread):
    # Create a counter thread
    def __init__(self, vehicle_test) -> None:
        super().__init__()
        self.vehicle_test = vehicle_test

    finished = pyqtSignal(str)
    def run(self):
        run_tracelogger(self.vehicle_test)
        self.finished.emit('Tracelogger script is done, check log_files folder -> finished...')


class Worker_for_fetch_topics(QThread):
    def __init__(self, func, DCF_BASE_PATH, DCF_PATH, *args):
        super().__init__()
        self.parm_1 = DCF_BASE_PATH
        self.parm_2 = DCF_PATH
        self.fetch_topics_func = func
    finished = pyqtSignal(str)

    def run(self):
        self.fetch_topics_func(self.parm_1, self.parm_2)
        self.finished.emit('Fetch Topids Done finished...')


class Worker_for_hostlog_start_logging(QThread):
    def __init__(self, func, DCF_TDF_PATH, DCF_PATH, DCF_LOG_DESTINATION_FOLDER, DCF_LOG_DURATION, TOPICS_TO_BE_LOGGED, *args):
        super().__init__()
        self.parm_1 = DCF_TDF_PATH
        self.parm_2 = DCF_PATH
        self.parm_3 = DCF_LOG_DESTINATION_FOLDER
        self.parm_4 = DCF_LOG_DURATION
        self.parm_5 = TOPICS_TO_BE_LOGGED
        self.start_logging_func = func
    finished = pyqtSignal(str)

    def run(self):
        self.start_logging_func(self.parm_1,
                                self.parm_2,
                                self.parm_3,
                                self.parm_4,
                                self.parm_5)
        self.finished.emit('Hostlog finished...')


class Worker_for_progressbar(QThread):
    # Create a counter thread
    def __init__(self):
        super().__init__()
        self.duration = 0.3
        self._isRunning = True
    change_value = pyqtSignal(int)
    finished = pyqtSignal(str)

    def run(self):
        cnt = 0
        while cnt < 100 and self._isRunning:
            cnt+=1
            sleep(self.duration)
            self.change_value.emit(cnt)
        self.finished.emit('Progress bar finished...')

    def stop(self):
        cnt = 100
        self.change_value.emit(cnt)
        sleep(1)
        self._isRunning = False


class Worker_for_xcp_domain_controller(QThread):
    def __init__(self, func, *args):
        super().__init__()
        self.run_xcp_calibration = func
    finished = pyqtSignal(str)

    def run(self):
        self.run_xcp_calibration()
        self.finished.emit('XCP finished...')
