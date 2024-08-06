import os
import io
import sys
import shutil
import tarfile
import zipfile
import requests
from glob import glob
from _resources.decoder import decoder
import _resources.local_keywords as local_keywords
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QCheckBox, QFileDialog, QShortcut
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QKeySequence


def get_file_paths(directory):
    file_paths = []  # List to store full paths of files.
    for foldername, _, filenames in os.walk(directory):
        for filename in filenames:
            file_paths.append(os.path.join(foldername, filename))  # Add the full file path to the list.
    return file_paths

class FileDropArea(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.parent().handle_dropped_file(f)
        self.setReadOnly(True)

    def focusInEvent(self, event):
        self.setReadOnly(False)
        super().focusInEvent(event)


class DecoderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.output_path = "./"
        self.file_paths = {'tdf_folder' : '', 'bin' : '', 'yml' : ''}
        self.dcf_path = "C:\\hostlog\\hostlog-client"
        self.fast_decoder_folder = f"{os.getcwd()}\\fast_decoded"
        self.fast_decoder_zips = f"{os.getcwd()}\\fast_decoded_zips"
        self.decoded_vcc_path = f"{self.fast_decoder_folder}\\decoded_VCC"
        self.img_output_path = f"{os.getcwd()}\\output"
        self.ara_user = "svahil"
        self.ara_password = "AKCp8mZcaVkSzAqFUtJCWJcStKPzRopxcy4aCv8Lrfsz6NPL6ofBnTQgRAeoSE5pkuAqF5mnt"

        self.local = local_keywords.local_commands()
        self.create_folders()
        self.init_ui()

    def create_folders(self):
        if not os.path.exists(self.fast_decoder_folder):
            os.mkdir(self.fast_decoder_folder)
        if not os.path.exists(self.fast_decoder_zips):
            os.mkdir(self.fast_decoder_zips)

    def init_ui(self):
        self.setWindowTitle('Fast Decoder')
        self.setFixedWidth(600)
        self.setFixedHeight(700)

        self.drop_area = FileDropArea(self)
        self.drop_area.setPlaceholderText("Drag & drop files here...\nFiles needed:\n    tdf folder\n    bin file\n    cs-manifest.yml\nNote:\n1. Unexpected behaviour may happen if you feed this tool with unexpected files/folder.\n2. Make sure hostlog_client is under C:\\hostlog\\hostlog-client")
        self.drop_area.setFixedHeight(200)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(200)

        self.bin_checkbox = QCheckBox("bin file")
        self.bin_checkbox.setEnabled(False)
        self.cs_yml_checkbox = QCheckBox("cs-manifest.yml")
        self.cs_yml_checkbox.setEnabled(False)
        self.tdf_checkbox = QCheckBox("tdf folder")
        self.tdf_checkbox.setEnabled(False)

        self.decode_button = QPushButton("Decode")
        self.decode_button.setEnabled(True)
        self.decode_button.clicked.connect(self.decode_files)

        self.zip_button = QPushButton("Zip")
        self.zip_button.setEnabled(True)
        self.zip_button.clicked.connect(self.zip_files)

        self.zen_dcf_button = QPushButton("Download Zen decoder")
        self.zen_dcf_button.setEnabled(True)
        self.zen_dcf_button.clicked.connect(self.download_zen_decoder)

        self.output_link = QLabel()
        self.output_link.setOpenExternalLinks(True)

        layout = QVBoxLayout()
        layout.addWidget(self.drop_area)
        layout.addWidget(self.log_area)
        layout.addWidget(self.bin_checkbox)
        layout.addWidget(self.cs_yml_checkbox)
        layout.addWidget(self.tdf_checkbox)
        layout.addWidget(self.zen_dcf_button)
        layout.addWidget(self.decode_button)
        layout.addWidget(self.zip_button)
        layout.addWidget(self.output_link)

        self.setLayout(layout)

        self.quit_shortcut = QShortcut(QKeySequence('Ctrl+Q'), self)
        self.quit_shortcut.activated.connect(app.quit)

    def handle_dropped_file(self, file_path):
        file_ext = ''
        if os.path.isfile(file_path):
            file_ext = file_path.split('.')[-1].lower()
        elif os.path.isdir(file_path):
            file_ext = file_path.split('/')[-1].lower().split('-')[0] + '_folder'
        self.file_paths[file_ext] = file_path

        if file_ext == "bin":
            self.bin_checkbox.setChecked(True)
        elif file_ext == "yml":
            self.cs_yml_checkbox.setChecked(True)
            self.zen_software_name = self.local.get_zenseact_version_from_manifest(self.file_paths['yml'])
        elif file_ext == "tdf_folder":
            self.tdf_checkbox.setChecked(True)

        self.log_area.append(f"File received: {file_path}")

        if self.bin_checkbox.isChecked() and self.cs_yml_checkbox.isChecked() and self.tdf_checkbox.isChecked():
            self.decode_button.setEnabled(True)

    def decode_files(self):
        self.log_area.clear()
        if self.file_paths['tdf_folder'] and self.file_paths['bin'] and self.file_paths['yml']:
            self.log_area.append(f"Copying files to: {self.fast_decoder_folder}")
            # copy tdf_folder, bin and yml into fast_decoded folder
            self.fast_decoder_tdf_new, self.fast_decoder_bin_new = self.copy_three_files()
            self.log_area.append("Decoding files...")
            try:
                self.decode_vcc()
                self.log_area.append("Decoding VCC complete.")
            except Exception as e:
                self.log_area.append("Decoding VCC failed with exception: " + e)
            try:
                self.decode_zen()
                self.log_area.append("Decoding Zenseact complete.")
            except Exception as e:
                self.log_area.append("Decoding Zenseact failed with exception: " + e)
            try:
                self.decode_images()
                self.log_area.append("Decoding images complete.")
            except Exception as e:
                self.log_area.append("Decoding images failed with exception: " + e)


            url = QUrl.fromLocalFile(self.fast_decoder_folder).toString()
            self.output_link.setText(f'<a href="{url}">Open fast_decoded folder</a>')
            self.log_area.append("Decoding complete. Click the link below to open the output folder.")
        else:
            self.output_link.setText("Necessary files are missing, check the list.")

    def copy_three_files(self):
        fast_decoder_path_new = self.fast_decoder_folder + '\\'+ self.file_paths['tdf_folder'].split('/')[-1]
        fast_decoder_bin_new = self.fast_decoder_folder + '\\'+ self.file_paths['bin'].split('/')[-1]
        try:
            shutil.copytree(self.file_paths['tdf_folder'], fast_decoder_path_new)
            shutil.copy(self.file_paths['bin'], self.fast_decoder_folder)
            shutil.copy(self.file_paths['yml'], self.fast_decoder_folder)
        except FileExistsError:
            print("File exits already.")
        return fast_decoder_path_new, fast_decoder_bin_new

    def decode_vcc(self):
        arguments = f"hostlog offline binary-playback --binary-files {self.fast_decoder_bin_new} --output {self.fast_decoder_folder} " \
                    f"--definitions {self.fast_decoder_tdf_new} --to-hdf5"
        print(f"Command : {arguments}")
        print(f"{self.dcf_path}/set_path.bat && {arguments}")
        os.system(f"{self.dcf_path}/set_path.bat && {arguments}")

        if os.path.exists(self.decoded_vcc_path):
            shutil.rmtree(self.decoded_vcc_path)
        os.rename(f"{self.fast_decoder_folder}\\logs", self.decoded_vcc_path)

    def decode_zen(self):
        # Decode the Hpa logs
        print("******* Decoding Zenseact logs *******")
        wsl_bin_path = "/mnt/" + self.fast_decoder_bin_new.replace(':', '').replace('\\', '/').lower()

        decoder(self.zen_software_name, wsl_bin_path,
                'fast_decoded/decoded_Zen', use_existing_decoder=True, ara_user_name=self.ara_user, ara_api_key=self.ara_password, fast=1)
        print(f"******* Successfully decoded Zenseact containers ******")

    def zip_files(self):
        bin_file = self.file_paths['bin'].split('/')[-1].split('.')[0]
        shutil.make_archive(f"{self.fast_decoder_zips}\\{bin_file}", 'zip', self.fast_decoder_folder)
        self.output_link.setText("All files in fast_decoded folder are zipped.")
        url = QUrl.fromLocalFile(self.fast_decoder_zips).toString()
        self.output_link.setText(f'<a href="{url}">Open fast_decoded_zips folder</a>')

    def decode_images(self):
        command = f"python _resources/dcf_image_decoder.py --path {self.file_paths['bin']}"
        os.system(command)
        # move output to fast_decoded
        if os.path.exists(self.img_output_path):
            img_decoded_folder = self.fast_decoder_folder + "\\decoded_img"
            if os.path.exists(img_decoded_folder):
                shutil.rmtree(img_decoded_folder, ignore_errors=True)
            shutil.copytree(self.img_output_path, img_decoded_folder)
            shutil.rmtree(self.img_output_path, ignore_errors=True)

    def download_zen_decoder(self):
        self.output_link.setText(f"Downloading Zenseact dcf decoder {self.zen_software_name} from Aratifactory.")
        try:
            print('Deleting dcf_decoder/out folder')
            # Delete the previous folder and its contents
            os.system("wsl rm -rf dcf_decoder")
        except:
            print("Nothing to delete!")
        # Get the name of the folder to be created and the path of the log file
        # Send a GET request to the URL and store the response
        r = requests.get("https://ara-artifactory.volvocars.biz/artifactory/AD-Zenuity-External-LTS/zen-ad-adas-vcu-hp-deliveries/" +
                         self.zen_software_name + "/zen_upload.zip", auth=(self.ara_user, self.ara_password), stream=True)
        # Add check on "config1" and "config2"
        if "200" not in str(r):
            self.zen_software_name = self.zen_software_name.replace("config1", "config2")
            r = requests.get("https://ara-artifactory.volvocars.biz/artifactory/AD-Zenuity-External-LTS/zen-ad-adas-vcu-hp-deliveries/" +
                         self.zen_software_name + "/zen_upload.zip", auth=(self.ara_user, self.ara_password), stream=True)

        if "200" in str(r):
            print("Download -> Possitive response")
            self.zen_decoder_folder = f"{os.getcwd()}\\zen_dcf_decoder_{self.zen_software_name}"
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(self.zen_decoder_folder)
            # some version has csp version as a suffix
            tar_gz = glob(f"{self.zen_decoder_folder}\\{self.zen_software_name}*.tar.gz")[0]
            with tarfile.open(tar_gz, 'r') as tar_ref:
                tar_ref.extract('dcf_decoder_pkg.tar.gz',self.zen_decoder_folder)
            with tarfile.open(self.zen_decoder_folder+"\\dcf_decoder_pkg.tar.gz", 'r') as tar_ref:
                tar_ref.extract('dcf_decoder/dcf_decoder', os.getcwd())
            self.output_link.setText("Software download for dcf decoder is completed!")
            print(f"Result -> {os.getcwd()}\zen_dcf_decoder")
        else:
            print("Download -> Negative response")
            return 0
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = DecoderGUI()
    gui.show()
    sys.exit(app.exec_())
