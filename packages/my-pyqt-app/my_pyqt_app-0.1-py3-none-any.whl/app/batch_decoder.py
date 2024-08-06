import subprocess
import tkinter as tk
from tkinter import filedialog
import os
from tkinter import font
from typing import Text


#-----------Adjust this folder to where the hostlog-client is located on your machine--------------------#
hostlog_client_folder=r"C:\hostlog\hostlog-client"
#--------------------------------------------------------------------------------------------------------#

bin_files = []
tdf_folder = ""
bin_folder = []
decoder_path = ""

def list_files(folder_path, file_format):
    file_list = []
    for file in os.listdir(folder_path):
        if file.endswith(file_format):
            file_list.append(os.path.join(folder_path, file))
    return file_list

def run_decoder():
    if checkbtn_decode_vcc_var.get():
        if not bin_files or not tdf_folder:
            update_status("Please select .bin folder and TDF folder")
            return
    if checkbtn_decode_zen_var.get():
        if not bin_files or not decoder_path:
            update_status("Please select .bin folder and dcf_decoder")
            return
        else:
            zen_out_path = bin_folder + "/zen_decoded"
            if not os.path.exists(zen_out_path):
                os.mkdir(zen_out_path)

    for index in range(listbox.size()):
        listbox.itemconfig(index, fg = 'black')

    decode_button.config(state=tk.DISABLED)

    for i, file_path in enumerate(bin_files, start=1):
        filename = os.path.basename(file_path)
        filename, _ = os.path.splitext(filename)
        vcc_out_path = bin_folder + "/vcc_decoded/" + filename
        try:
            if checkbtn_decode_zen_var.get():
                update_status(f"Decoding file {i} of {len(bin_files)} (Zenseact)")
                run_zen_decoder(zen_out_path,file_path)
            if checkbtn_decode_vcc_var.get():
                update_status(f"Decoding file {i} of {len(bin_files)} (VCC)")
                run_vcc_decoder(vcc_out_path,file_path)
            listbox.itemconfigure(i-1,fg = "Green")
        except:
            listbox.itemconfigure(i-1,fg = "Red")
    update_status("Decoding completed. Logs stored in .bin folder")
    decode_button.config(state=tk.NORMAL)

def run_zen_decoder(zen_out_path,file_path):
    bin_wsl_path = os.popen(f'wsl wslpath -u "{file_path}"').read().strip()
    bin_wsl_out_path = os.popen(f'wsl wslpath -u "{zen_out_path}"').read().strip()
    decoder_wsl_path = os.popen(f'wsl wslpath -u "{decoder_path}"').read().strip()
    command = f"wsl '{decoder_wsl_path}' --log='{bin_wsl_path}' --out='{bin_wsl_out_path}'"
    os.system(command)

def run_vcc_decoder(vcc_out_path,file_path):
    command = f"hostlog offline binary-playback --binary-files \"{file_path}\" --output \"{vcc_out_path}\" --definitions \"{tdf_folder}\" --to-hdf5 --appconfig output.files.hdf5_decode_enum_as_int=False"
    os.system(str(f"{hostlog_client_folder}\\set_path.bat") + " && " + command)
    os.remove(f"{vcc_out_path}/hostlog-client.log")

def update_status(status_text):
    status_label.config(text=status_text)
    root.update()

def update_listbox(file_list):
    listbox.delete(0, tk.END)
    for file_path in file_list:
        filename = os.path.basename(file_path)
        listbox.insert(tk.END, filename)

def update_bin_folder_label():
    bin_folder_label.config(text=bin_folder)

def update_tdf_folder_label():
    tdf_folder_label.config(text=tdf_folder)

def update_decoder_label(zen_version):
    decoder_label.config(text=zen_version)

def select_tdf_folder():
    global tdf_folder
    tdf_folder = filedialog.askdirectory(title="Select TDF Folder")
    if tdf_folder:
        update_tdf_folder_label()

def select_bin_folder():
    global bin_files, bin_folder
    bin_folder = filedialog.askdirectory(title="Select .bin Folder")
    if bin_folder:
        listbox.configure(fg="Black")
        bin_files = list_files(bin_folder, '.bin')
        if bin_files:
            bin_num = len(bin_files)
            update_listbox(bin_files)
            update_bin_folder_label()
            update_status(f"{bin_num} bin-files found")
        else:
            update_status("No .bin files found in the selected folder.")
    else:
        update_status(".bin folder not selected.")

def select_decoder():
    global decoder_path
    decoder_path = filedialog.askopenfilename(title="Select dcf_decoder")
    if decoder_path:
        decoder_wsl_path = os.popen(f'wsl wslpath -u "{decoder_path}"').read().strip()
        command = f"wsl '{decoder_wsl_path}'"
        zen_version=subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        zen_version = zen_version.stdout
        zen_version = zen_version.split(',')
        zen_version = zen_version[0]
        update_decoder_label(zen_version)
    else:
        update_status("dcf_decoder not selected.")

def enable_disable_buttons():
    if checkbtn_decode_vcc_var.get():
        select_tdf_button.config(state=tk.NORMAL)
    else:
        select_tdf_button.config(state=tk.DISABLED)

    if checkbtn_decode_zen_var.get():
        select_decoder_button.config(state=tk.NORMAL)
    else:
        select_decoder_button.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Batch decoder")
root.geometry("400x700")

select_bin_button = tk.Button(root, text="Select .bin Folder", command=select_bin_folder)
select_bin_button.pack(pady=10)
bin_folder_label = tk.Label(root, text=" ")
bin_folder_label.pack()

checkbtn_decode_vcc_var=tk.BooleanVar(value = True)
checkbtn_decode_vcc = tk.Checkbutton(root, text = "Decode VCC", variable=checkbtn_decode_vcc_var, command=enable_disable_buttons)
checkbtn_decode_vcc.pack()

select_tdf_button = tk.Button(root, text="Select TDF Folder", command=select_tdf_folder)
select_tdf_button.pack()
tdf_folder_label = tk.Label(root, text=" ")
tdf_folder_label.pack()

checkbtn_decode_zen_var=tk.BooleanVar(value = True)
checkbtn_decode_zen = tk.Checkbutton(root, text = "Decode Zenseact", variable=checkbtn_decode_zen_var, command=enable_disable_buttons)
checkbtn_decode_zen.pack()

select_decoder_button = tk.Button(root, text="Select dcf_decoder", command=select_decoder)
select_decoder_button.pack()
decoder_label = tk.Label(root, text=" ")
decoder_label.pack()

listbox = tk.Listbox(root, width=65, height=25)
listbox.pack()

decode_button = tk.Button(root, text="Decode", command=run_decoder)
decode_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
