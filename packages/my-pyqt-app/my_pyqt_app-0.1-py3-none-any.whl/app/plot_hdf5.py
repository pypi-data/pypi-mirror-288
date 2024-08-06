import h5py
import matplotlib.pyplot as plt
import os

def plot_signals_from_zen_qm_feature_a(hdf5_file):
    with h5py.File(hdf5_file, 'r') as file:
        fig, ax = plt.subplots(3, 1, figsize=(16, 10), sharex=True)

        # Axis 0
        aeb_dataset = file["zen_qm_feature_a"]["emergency_brake_request"]["data"]["emergency_braking_request"]["unitless"]["value"]
        fcw_dataset = file["zen_qm_feature_a"]["warning_request_from_cw"]["data"]["request"]["unitless"]["value"]
        aeb_timestamp_dataset = file["zen_qm_feature_a"]["emergency_brake_request"]["zeader"]["timestamp_ns"]
        fcw_timestamp_dataset = file["zen_qm_feature_a"]["warning_request_from_cw"]["zeader"]["timestamp_ns"]

        aeb_signal = aeb_dataset[:]
        fcw_signal = fcw_dataset[:]
        aeb_timestamp = aeb_timestamp_dataset[:]
        fcw_timestamp = fcw_timestamp_dataset[:]

        ax[0].plot(aeb_timestamp, aeb_signal, label="zen_qm_feature_a.emergency_brake_request.data.emergency_braking_request.unitless.value")
        ax[0].plot(fcw_timestamp, fcw_signal, label="zen_qm_feature_a.warning_request_from_cw.data.request.unitless.value")
        ax[0].set_ylabel('AEB/FCW')
        ax[0].legend()

        # Axis 1
        speed_datset = file["zen_qm_feature_a"]["zen_qm_feature_a_vehicle_motion_state_data"]["data"]["longitudinal_velocity"]["velocity"]["meters_per_second"]["value"]
        speed_timestamp_dataset = file["zen_qm_feature_a"]["zen_qm_feature_a_vehicle_motion_state_data"]["zeader"]["timestamp_ns"]

        speed_signal = speed_datset[:]
        speed_timestamp = speed_timestamp_dataset[:]

        ax[1].plot(speed_timestamp, speed_signal, label="zen_qm_feature_a.zen_qm_feature_a_vehicle_motion_state_data.data.longitudinal_velocity.velocity.meters_per_second.value")
        ax[1].set_ylabel('Speed')
        ax[1].legend()

        # Axis 2
        acceleration_datset = file["zen_qm_feature_a"]["zen_qm_feature_a_vehicle_motion_state_data"]["data"]["longitudinal_acceleration_unfiltered"]["acceleration"]["meters_per_second2"]["value"]
        acceleration_timestamp_dataset = file["zen_qm_feature_a"]["zen_qm_feature_a_vehicle_motion_state_data"]["zeader"]["timestamp_ns"]

        acceleration_signal = acceleration_datset[:]
        acceleration_timestamp = acceleration_timestamp_dataset[:]

        ax[2].plot(acceleration_timestamp, acceleration_signal, label="zen_qm_feature_a.zen_qm_feature_a_vehicle_motion_state_data.data.longitudinal_acceleration_unfiltered.acceleration.meters_per_second2.value")
        ax[2].set_ylabel('Acceleration')
        ax[2].legend()

        # Add labels, legend, and title
        plt.xlabel('Time')
        plt.suptitle('Multiple Signals from zen_qm_feature_a', fontsize=16)
        plt.tight_layout()

def plot_signals_from_adas_actuation_arbitration_manager(hdf5_file):
    with h5py.File(hdf5_file, 'r') as file:
        fig, ax = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

        # Axis 0
        signal_1_data = file["hostlog"]["channel_83"]["topic_0"]["data"]["accel_pedal_percentage"]["position_"]
        signal_2_data = file["hostlog"]["channel_83"]["topic_0"]["data"]["accel_pedal_percentage"]["pressed_qm_"]
        signal_3_data = file["hostlog"]["channel_83"]["topic_0"]["data"]["braking_request"]["deceleration_request_"]

        signal_1 = signal_1_data[:]
        signal_2 = signal_2_data[:]
        signal_3 = signal_3_data[:]

        ax[0].plot(signal_1, label="hostlog.topic_0.data.accel_pedal_percentage.position_")
        ax[0].plot(signal_2, label="hostlog.topic_0.data.accel_pedal_percentage.pressed_qm_")
        ax[0].plot(signal_3, label="hostlog.topic_0.data.braking_request.deceleration_request_")
        ax[0].set_ylabel('AAAM input-channel:83')
        ax[0].legend()

        # Axis 1
        signal_1_data = file["hostlog"]["channel_84"]["topic_0"]["data"]["emergency_braking_state_is_enable"]
        signal_1 = signal_1_data[:]
        ax[1].plot(signal_1, label="hostlog.topic_0.data.emergency_braking_state_is_enable.")
        ax[1].set_ylabel('AAAM output-channel:84')
        ax[1].legend()

        # Add labels, legend, and title
        plt.xlabel('Time')
        plt.suptitle('Multiple Signals from adas-actuation-arbitration-manager', fontsize=16)
        plt.tight_layout()

def plot_signals_from_manager_safe(hdf5_file):
    with h5py.File(hdf5_file, 'r') as file:
        fig, ax = plt.subplots(4, 1, figsize=(16, 10), sharex=True)

        # Axis 0
        signal_1_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["brake_request_v1"]["deceleration_request_"]
        signal_1 = signal_1_data[:]

        ax[0].plot(signal_1, label="hostlog.topic_1.data.brake_request_v1.deceleration_request_")
        ax[0].set_ylabel('MS topic 1 data')
        ax[0].legend()

        # Axis 1
        signal_1_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["brake_request_v1"]["deceleration_enable_"]
        signal_2_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["collision_threat_v1"]

        signal_1 = signal_1_data[:]
        signal_2 = signal_2_data[:]

        ax[1].plot(signal_1, label="hostlog.topic_1.data.brake_request_v1.deceleration_enable_")
        ax[1].plot(signal_2, label="hostlog.topic_1.data.collision_threat_v1")

        ax[1].set_ylabel('MS topic 1 data')
        ax[1].legend()

        # Axis 2
        signal_1_data = file["hostlog"]["channel_26"]["topic_2"]["data"]["deceleration_request_enable"]
        signal_2_data = file["hostlog"]["channel_26"]["topic_2"]["data"]["deceleration_request_value"]

        signal_1 = signal_1_data[:]
        signal_2 = signal_2_data[:]

        ax[2].plot(signal_1, label="hostlog.topic_2.data.deceleration_request_enable")
        ax[2].plot(signal_2, label="hostlog.topic_2.data.deceleration_request_value")

        ax[2].set_ylabel('MS topic 2 data')
        ax[2].legend()

        # Axis 3
        signal_1_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["override_by_throttle"]
        signal_2_data = file["hostlog"]["channel_26"]["topic_1"]["data"]["override_by_throttle_e2e_ok"]

        signal_1 = signal_1_data[:]
        signal_2 = signal_2_data[:]

        ax[3].plot(signal_1, label="hostlog.topic_1.data.override_by_throttle")
        ax[3].plot(signal_2, label="hostlog.topic_1.data.override_by_throttle_e2e_ok")
        ax[3].set_ylabel('MS topic 1 data')
        ax[3].legend()

        # Add labels, legend, and title
        plt.xlabel('Time')
        plt.suptitle('Multiple Signals from adas-manager-safe', fontsize=16)
        plt.tight_layout()

def plot_signals_from_domain_controller(hdf5_file):

    with h5py.File(hdf5_file, 'r') as file:
        fig, ax = plt.subplots(2, 1, figsize=(18, 10), sharex=True)

        # Axis 0
        sensor_blockage_fc_dataset = file["hostlog"]["channel_97"]["topic_0"]["data"]["configuration_interface_"]["sensor_blockage_"]["front_camera_"]
        sensor_blockage_fc_timestamp_dataset = file["hostlog"]["channel_97"]["topic_0"]["timestamp"]
        sensor_blockage_flr_dataset = file["hostlog"]["channel_97"]["topic_0"]["data"]["configuration_interface_"]["sensor_blockage_"]["front_looking_radar_"]
        sensor_blockage_flr_timestamp_dataset = file["hostlog"]["channel_97"]["topic_0"]["timestamp"]

        sensor_blockage_fc = sensor_blockage_fc_dataset[:]
        sensor_blockage_fc_timestamp = sensor_blockage_fc_timestamp_dataset[:]
        sensor_blockage_flr = sensor_blockage_flr_dataset[:]
        sensor_blockage_flr_timestamp = sensor_blockage_flr_timestamp_dataset[:]

        ax[0].plot(sensor_blockage_fc_timestamp, sensor_blockage_fc, label="hostlog.channel_97.topic_0.data.configuration_interface_.sensor_blockage_.front_camera_")
        ax[0].plot(sensor_blockage_flr_timestamp, sensor_blockage_flr, label="hostlog.channel_97.topic_0.data.configuration_interface_.sensor_blockage_.front_looking_radar_")
        ax[0].set_ylabel('DC Sensor blockage')
        ax[0].legend()

        # Axis 1
        sensor_calibration_fc_dataset = file["hostlog"]["channel_97"]["topic_0"]["data"]["configuration_interface_"]["sensor_calibration_"]["front_camera_"]
        sensor_calibration_fc_timestamp_dataset = file["hostlog"]["channel_97"]["topic_0"]["timestamp"]
        sensor_calibration_flr_dataset = file["hostlog"]["channel_97"]["topic_0"]["data"]["configuration_interface_"]["sensor_calibration_"]["front_looking_radar_"]
        sensor_calibration_flr_timestamp_dataset = file["hostlog"]["channel_97"]["topic_0"]["timestamp"]

        sensor_calibration_fc = sensor_calibration_fc_dataset[:]
        sensor_calibration_fc_timestamp = sensor_calibration_fc_timestamp_dataset[:]
        sensor_calibration_flr = sensor_calibration_flr_dataset[:]
        sensor_calibration_flr_timestamp = sensor_calibration_flr_timestamp_dataset[:]

        ax[1].plot(sensor_calibration_fc_timestamp, sensor_calibration_fc, label="hostlog.channel_97.topic_0.data.configuration_interface_.sensor_calibration_.front_camera_")
        ax[1].plot(sensor_calibration_flr_timestamp, sensor_calibration_flr, label="hostlog.channel_97.topic_0.data.configuration_interface_.sensor_calibration_.front_looking_radar_")
        ax[1].set_ylabel('DC Sensor calibration')
        ax[1].legend()

        # Add labels, legend, and title
        plt.xlabel('Time')
        plt.suptitle('Multiple Signals from domain controller', fontsize=16)
        plt.tight_layout()

def plot_all_necessary_signals(hdf5_file1, hdf5_file2, hdf5_file3):
    fig, ax = plt.subplots(3, 1, figsize=(18, 10), sharex=True)

    with h5py.File(hdf5_file1, 'r') as file1, h5py.File(hdf5_file2, 'r') as file2, h5py.File(hdf5_file3, 'r') as file3:
        # Axis 0
        aeb_dataset = file1["zen_qm_feature_a"]["emergency_brake_request"]["data"]["emergency_braking_request"]["unitless"]["value"]
        fcw_dataset = file1["zen_qm_feature_a"]["warning_request_from_cw"]["data"]["request"]["unitless"]["value"]
        aeb_timestamp_dataset = file1["zen_qm_feature_a"]["emergency_brake_request"]["zeader"]["timestamp_ns"]
        fcw_timestamp_dataset = file1["zen_qm_feature_a"]["warning_request_from_cw"]["zeader"]["timestamp_ns"]

        asil_thread_validator_dataset = file2["zen_asil_feature_a"]["threat_validator_output"]["data"]["validated_acceleration_request"]["acceleration_request"]["emergency_acceleration_request"]["unitless"]["value"]
        asil_thread_validator_timestamp_dataset = file2["zen_asil_feature_a"]["threat_validator_output"]["zeader"]["timestamp_ns"]

        aeb_signal = aeb_dataset[:]
        fcw_signal = fcw_dataset[:]
        aeb_timestamp = aeb_timestamp_dataset[:]
        fcw_timestamp = fcw_timestamp_dataset[:]
        asil_thread_validator_signal = asil_thread_validator_dataset[:]
        asil_thread_validator_timestamp = asil_thread_validator_timestamp_dataset[:]

        ax[0].plot(aeb_timestamp, aeb_signal, label="zen_qm_feature_a.emergency_brake_request.data.emergency_braking_request.unitless.value")
        ax[0].plot(fcw_timestamp, fcw_signal, label="zen_qm_feature_a.warning_request_from_cw.data.request.unitless.value")
        ax[0].plot(asil_thread_validator_timestamp, asil_thread_validator_signal, label="zen_asil_feature_a.threat_validator_output.data.validated_acceleration_request.acceleration_request.emergency_acceleration_request.unitless.value")
        ax[0].legend()

        # Axis 1
        ms_brake_request_dataset = file3["hostlog"]["channel_26"]["topic_1"]["data"]["brake_request_v1"]["deceleration_request_"]
        ms_brake_request_timestamp_dataset = file3["hostlog"]["channel_26"]["topic_1"]["timestamp"]

        ms_brake_request_signal = ms_brake_request_dataset[:]
        ms_brake_request_timestamp = ms_brake_request_timestamp_dataset[:]

        aam_acceleration_level_dataset = file3["hostlog"]["channel_83"]["topic_0"]["data"]["braking_request"]["deceleration_request_"]
        aam_acceleration_level_timestamp_dataset = file3["hostlog"]["channel_83"]["topic_0"]["timestamp"]

        aam_acceleration_level_signal = aam_acceleration_level_dataset[:]
        aam_acceleration_level_timestamp = aam_acceleration_level_timestamp_dataset[:]

        asil_speed_reduction_monitor_dataset = file2["zen_asil_feature_a"]["speed_reduction_monitor_output"]["data"]["validated_acceleration_request"]["maximum_acceleration_limit"]["meters_per_second2"]["value"]
        asil_speed_reduction_monitor_timestamp_dataset = file2["zen_asil_feature_a"]["speed_reduction_monitor_output"]["zeader"]["timestamp_ns"]

        asil_speed_reduction_monitor_signal = asil_speed_reduction_monitor_dataset[:]
        asil_speed_reduction_monitor_timestamp = asil_speed_reduction_monitor_timestamp_dataset[:]

        ax[1].plot(ms_brake_request_timestamp, ms_brake_request_signal, label="hostlog.channel_26.topic_1.data.brake_request_v1.deceleration_request_")
        ax[1].plot(aam_acceleration_level_timestamp, aam_acceleration_level_signal, label="hostlog.channel_83.topic_0.data.braking_request.deceleration_request_")
        ax[1].plot(asil_speed_reduction_monitor_timestamp, asil_speed_reduction_monitor_signal, label="zen_asil_feature_a.speed_reduction_monitor_output.data.validated_acceleration_request.maximum_acceleration_limit.meters_per_second2.value")
        ax[1].legend()

        # Axis 2
        asil_threat_validated_debug_dataset = file2["zen_asil_feature_a"]["threat_validator_debug"]["data"]["confirmed_threat"]["unitless"]["value"]
        asil_threat_validated_debug_timestamp_dataset = file2["zen_asil_feature_a"]["threat_validator_debug"]["zeader"]["timestamp_ns"]

        asil_threat_validated_debug_signal = asil_threat_validated_debug_dataset[:]
        asil_threat_validated_debug_timestamp = asil_threat_validated_debug_timestamp_dataset[:]

        ax[2].plot(asil_threat_validated_debug_timestamp, asil_threat_validated_debug_signal, label="zen_asil_feature_a.threat_validator_debug.data.confirmed_threat.unitless.value")
        ax[2].legend()

    plt.suptitle('All necessary signals', fontsize=16)
    plt.tight_layout()

if __name__ == "__main__":
    print(os.getcwd())
    zen_qm_feature_a_hdf5_file = os.getcwd() + "\\decoded_Zenseact\\bin-20230620_094719036.1\\zen_qm_feature_a.hdf5"
    zen_qm_asil_hdf5_file = os.getcwd() + "\\decoded_Zenseact\\bin-20230620_094719036.1\\zen_asil_feature_a.hdf5"
    vcc_decoded_hdf5_file = os.getcwd() + "\\decoded_Zenseact\\bin-20230620_094719036.1\\20230728_115922108-hostlog-messages.hdf5"

    #plot_signals_from_zen_qm_feature_a(zen_qm_feature_a_hdf5_file)
    #plot_signals_from_adas_actuation_arbitration_manager(vcc_decoded_hdf5_file)
    #plot_signals_from_manager_safe(vcc_decoded_hdf5_file)
    #plot_all_necessary_signals(zen_qm_feature_a_hdf5_file, zen_qm_asil_hdf5_file, vcc_decoded_hdf5_file)
    plot_signals_from_domain_controller(vcc_decoded_hdf5_file)

    plt.show()
