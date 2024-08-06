import os
import shutil
import zipfile
import re
from pathlib import Path

'''
How-to:
1.Place the script (decode_it_all.py) inside C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app
2.Create a folder called "zip_files" in C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app
3.Place all zip-files in the  zip_files  folder
4.Decoder needs to be downloaded & correct tdf needs to be present. (edited) 
'''


def unpack_and_filter_zip(input_zip, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Extract the contents of the zip file
    #with zipfile.ZipFile(input_zip, 'r') as zip_ref:
        #zip_ref.extractall(output_folder)

def list_zip_files(folder_path):
    zip_files = [f for f in os.listdir(folder_path) if f.endswith(".bin")]
    return zip_files

def get_latest_folder_in_directory(directory):
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    if not folders:
        return None
    return max(folders, key=lambda f: os.path.getmtime(os.path.join(directory, f)))

def get_latest_file_w_pattern_in_directory(folder_path, file_extension=".bin"):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                return os.path.join(root, file)

def extract_main_folder(wsl_path):
    match = re.match(r'^/mnt/([a-zA-Z])/', wsl_path)
    if match:
        drive_letter = match.group(1).lower()
        return f'{drive_letter}:\\' + wsl_path[7:]
    else:
        return None

def convert_to_wsl_path(windows_path):
    wsl_path = windows_path.replace("\\", "/")
    if wsl_path[1] == ":":
        wsl_path = "/mnt/" + wsl_path[0].lower() + wsl_path[2:]
    return wsl_path

def decode_zen(input_folder):
    output_folder_name = r"C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app\decoded_Zenseact"
    print('started dcf decoding')
    bin_file_path = get_latest_file_w_pattern_in_directory(input_folder)
    output_folder_name_wsl_path = convert_to_wsl_path(output_folder_name)

    bin_files = get_bin_files_in_main_folder(Path(bin_file_path).parent)

    for bin_file in bin_files:
        bin_wsl_path = convert_to_wsl_path(bin_file)

        command = f"wsl ./dcf_decoder/dcf_decoder --log={bin_wsl_path} --out={output_folder_name_wsl_path}"
        os.system(command)

def get_bin_files_in_main_folder(main_folder):
    bin_files = []
    for file_name in os.listdir(main_folder):
        if file_name.endswith(".bin") and os.path.isfile(os.path.join(main_folder, file_name)):
            bin_files.append(os.path.abspath(os.path.join(main_folder, file_name)))
    return bin_files

def copy_bin_files(bin_files, destination_folder):
    for file_path in bin_files:
        shutil.copy(file_path, destination_folder)

def decode_dcf_log_vcc():
    tdf_path = r"C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app\tdf"
    bat_path = r"C:\hostlog\hostlog-client"
    log_dst_path = r"C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app"
    DCF_BINARY_PATH = r"C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app\bin"

    tdf_folder =  f"{tdf_path}/{get_latest_folder_in_directory(tdf_path)}"
    # to fix the bug that vcc decoder decodes all binary files under the same folder
    # create a tmp folder under the current folder and do the decoding there and remove it afterwards

    tmp = f"{DCF_BINARY_PATH}\\tmp"
    if os.path.exists(tmp):
        shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)

    latest_bin = get_latest_file_w_pattern_in_directory(DCF_BINARY_PATH)
    bin_files = get_bin_files_in_main_folder(Path(latest_bin).parent)
    copy_bin_files(bin_files, tmp)
    bin_files = get_bin_files_in_main_folder(tmp)

    for bin_log_file in bin_files:
        # decoding VCC
        arguments = f"hostlog offline binary-playback --binary-files {bin_log_file} --output {log_dst_path} " \
                    f"--definitions {tdf_folder} --to-hdf5"
        os.system(f"{bat_path}/set_path.bat && {arguments}")

        # post process
        src = f"{log_dst_path}/logs"
        dst = f"{log_dst_path}/decoded_VCC"
        latest_bin = Path(latest_bin)
        dst_bin = f"{dst}/{latest_bin.name[:-5]}"  # removes "1.bin"
        create_folder_and_move_file(src, dst_bin)

    if os.path.exists(tmp):
        shutil.rmtree(tmp, ignore_errors=True)

def rename_file_in_folder(folder_path, old_name, new_name):
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, new_name)
    os.rename(old_path, new_path)

def remove_files_and_subfolders(folder_path):
    # Iterate over the contents of the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Check if the item is a file
        if os.path.isfile(item_path):
            os.remove(item_path)

        # Check if the item is a directory (subfolder)
        elif os.path.isdir(item_path):
            # Use shutil.rmtree to remove the directory and its contents
            shutil.rmtree(item_path)

def create_folder_and_move_file(source_folder, destination_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Move files from source folder to destination folder
    for file_name in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        shutil.move(source_file, destination_file)

def remove_extension(file_name):
    return os.path.splitext(file_name)[0]

def run_pytest_on_decoded_bin():
    os.system(r"python C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app\_sanity_check\src\run_sanity_check.py")

def decode_zen_and_vcc():
    zip_files_folder = Path(r"C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app\zip_files")
    zip_list = list_zip_files(zip_files_folder)
    bin_path = r"C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app\bin"
    zen_source_folder = r"C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app\decoded_Zenseact"
    vcc_source_folder = r"C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app\decoded_VCC"
    dst_folder = Path(r"C:\gerrit\collision-avoidance\Vehicle_logger_GUI\app\zip_files")

    run_sanity_check = False

    for zip_file in zip_list:
        unpack_and_filter_zip(f"{zip_files_folder}/{zip_file}",
                              'bin')
        # decode_zen(bin_path)
        decode_dcf_log_vcc()

        if run_sanity_check:
            # run basic sanity check
            run_pytest_on_decoded_bin()

        create_folder_and_move_file(zen_source_folder, f"{dst_folder}/{remove_extension(zip_file)}")
        create_folder_and_move_file(vcc_source_folder, f"{dst_folder}/{remove_extension(zip_file)}")
        create_folder_and_move_file(bin_path, f"{dst_folder}/{remove_extension(zip_file)}")
        remove_files_and_subfolders(bin_path)
        remove_files_and_subfolders(vcc_source_folder)

decode_zen_and_vcc()
