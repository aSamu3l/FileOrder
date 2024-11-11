import json
import os.path
import signal
import webbrowser
import functions as f
from lockf import LockFolder
from PIL import Image
import customtkinter as CTk
from CTkMessagebox import CTkMessagebox as CTkM

baseColor = ("#ebebeb", "#242424")
cardContent = ("#dbdbdb", "#2b2b2b")
boxContent = ("#f9f9fa", "#1d1e1e")

folder = LockFolder()

with open('./settings/img.json') as iJ:
    imgJson = json.load(iJ)

with open('./settings/lang.json', encoding='utf-8') as lJ:
    langJson = json.load(lJ)

with open('./settings/setting.json') as sJ:
    settingsJson = json.load(sJ)

lang = settingsJson["lang"]

if lang not in langJson.keys():
    lang = "EN"

    with open('./settings/setting.json', 'w') as sJ:
        settingsJson["lang"] = "EN"
        json.dump(settingsJson, sJ, indent=4)

def on_closing():
    folder.unlock()
    root.destroy()

def handle_exit(signum, frame):
    folder.unlock()
    exit(0)

def open_repo(event):
    webbrowser.open_new("https://github.com/aSamu3l/FileOrder")

def open_profile(event):
    webbrowser.open_new("https://github.com/aSamu3l/")

def changeLang(event):
    global lang
    newLang = langSelector.get()

    if newLang == lang:
        return

    with open('./settings/setting.json', 'w') as sJ:
        settingsJson["lang"] = newLang
        json.dump(settingsJson, sJ, indent=4)

    lang = newLang
    update_texts()

def update_texts():
    selectOriginLabel.configure(text=langJson[lang]["selectOriginLabelText"])
    originFolderButton.configure(text=langJson[lang]["Browse"])
    selectDestinationLabel.configure(text=langJson[lang]["selectDestinationLabelText"])
    destinationFolderButton.configure(text=langJson[lang]["Browse"])
    selectNameLabel.configure(text=langJson[lang]["selectNameLabelText"])
    nameEntry.configure(placeholder_text=langJson[lang]["nameEntryText"])
    selectExtensionLabel.configure(text=langJson[lang]["selectExtensionLabelText"])
    extensionEntry.configure(placeholder_text=langJson[lang]["extensionEntryText"])
    startWithCheck.configure(text=langJson[lang]["startWithCheckText"])
    caseSensitiveCheck.configure(text=langJson[lang]["caseSensitiveCheckText"])
    searchButton.configure(text=langJson[lang]["Search"])
    moveButton.configure(text=langJson[lang]["Move"])
    creditLabel.configure(text=langJson[lang]["creditLabelText"])

def origin_folder():
    global originFolderPath
    originFolderPath.set(f.select_origin_folder())

def destination_folder():
    global destinationFolderPath, folder
    dest = f.select_destination_folder()
    destinationFolderPath.set(dest)
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    folder.change_path(dest)
    folder.lock()


def search():
    global fileList
    name = nameEntry.get()
    extension = extensionEntry.get()
    start_with = startWithCheck.get()
    case_sensitive = caseSensitiveCheck.get()

    if possible_path_error():
        return

    files = f.list_files_to_move(originFolderPath.get(), name, extension, start_with, case_sensitive)

    if len(files) == 0:
        CTkM(title=langJson[lang]["Error"], message=langJson[lang]["noFilesFound"], icon="cancel")
    elif len(files) == 1:
        CTkM(title=langJson[lang]["Success"], message=langJson[lang]["fileFound"], icon="info")
    else:
        CTkM(title=langJson[lang]["Success"], message=langJson[lang]["filesFound"].replace("#", str(len(files))), icon="info")

    fileList.destroy()
    fileList = CTk.CTkScrollableFrame(optionFileFrame, fg_color=boxContent, width=238, height=360)
    fileList.pack()
    fileList.place(x=10, y=10)

    for file, move in files:
        var = CTk.BooleanVar(value=move)
        checkbox = CTk.CTkCheckBox(fileList, text=file, variable=var)
        checkbox.pack(anchor='w', pady=5)

def move():
    lista = []
    for widget in fileList.winfo_children():
        lista.append((widget.cget("text"), bool(widget.get())))

    if possible_path_error():
        return

    if f.move_files_list(originFolderPath.get(), destinationFolderPath.get(), lista) == 0:
        CTkM(title=langJson[lang]["Success"], message=langJson[lang]["allFilesMoved"], icon="info")
    else:
        CTkM(title=langJson[lang]["Error"], message=langJson[lang]["someFilesMoved"], icon="cancel")

def copy():
    lista = []
    for widget in fileList.winfo_children():
        lista.append((widget.cget("text"), bool(widget.get())))

    if possible_path_error():
        return

    if f.copy_files_list(originFolderPath.get(), destinationFolderPath.get(), lista) == 0:
        CTkM(title=langJson[lang]["Success"], message=langJson[lang]["allFilesCopied"], icon="info")
    else:
        CTkM(title=langJson[lang]["Error"], message=langJson[lang]["someFilesCopied"], icon="cancel")

def possible_path_error():
    if not os.path.exists(originFolderPath.get()):
        CTkM(title=langJson[lang]["Error"], message=langJson[lang]["pathOriginDoesNotExist"], icon="cancel")
        return True

    if not os.path.exists(destinationFolderPath.get()):
        CTkM(title=langJson[lang]["Error"], message=langJson[lang]["pathDestinationDoesNotExist"], icon="cancel")
        return True

    if originFolderPath.get() == destinationFolderPath.get():
        CTkM(title=langJson[lang]["Error"], message=langJson[lang]["pathOriginAndDestinationAreTheSame"], icon="cancel")
        return True

    return False

# CTk.set_appearance_mode("dark") // only for testing purposes
root = CTk.CTk()
root.geometry("800x500")
root.title("File Order")
root.iconbitmap("./img/icon.ico")
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Option Folder Frame
optionFolderFrame = CTk.CTkFrame(root, fg_color=cardContent, width=490, height=200)
optionFolderFrame.pack()
optionFolderFrame.place(x=10, y=10)

# Option Folder Frame Content
# Origin Folder Path
selectOriginLabel = CTk.CTkLabel(optionFolderFrame, text = langJson[lang]["selectOriginLabelText"], font=("Arial", 20))
selectOriginLabel.pack()
selectOriginLabel.place(x = 10, y = 10)

originFolderPath = CTk.StringVar()
originFolderPath.set(langJson[lang]["originFolderPathText"])
originFolderPathEntry = CTk.CTkEntry(optionFolderFrame, textvariable = originFolderPath, width = 405, height = 29, state="disabled")
originFolderPathEntry.pack()
originFolderPathEntry.place(x = 10, y = 40)

originFolderButton = CTk.CTkButton(optionFolderFrame, text=langJson[lang]["Browse"], command=origin_folder, width=61)
originFolderButton.pack()
originFolderButton.place(x=420, y=40)

# Img scheme
imgScheme = CTk.CTkImage(Image.open(imgJson["file"][CTk.get_appearance_mode()]), size=(240, 40))

imageFileLabel = CTk.CTkLabel(optionFolderFrame, image=imgScheme, text="", fg_color=None, width=470)
imageFileLabel.pack()
imageFileLabel.place(x=10, y=77)

# Destination Folder Path
selectDestinationLabel = CTk.CTkLabel(optionFolderFrame, text = langJson[lang]["selectDestinationLabelText"], font=("Arial", 20))
selectDestinationLabel.pack()
selectDestinationLabel.place(x = 10, y = 120)

destinationFolderPath = CTk.StringVar()
destinationFolderPath.set(langJson[lang]["destinationFolderPathText"])
destinationFolderPathEntry = CTk.CTkEntry(optionFolderFrame, textvariable = destinationFolderPath, width = 405, height = 29, state="disabled")
destinationFolderPathEntry.pack()
destinationFolderPathEntry.place(x = 10, y = 150)

destinationFolderButton = CTk.CTkButton(optionFolderFrame, text=langJson[lang]["Browse"], command=destination_folder, width=61)
destinationFolderButton.pack()
destinationFolderButton.place(x=420, y=150)

# Option File Frame
optionFileFrame = CTk.CTkFrame(root, fg_color=cardContent, width=490, height=220)
optionFileFrame.pack()
optionFileFrame.place(x=10, y=220)

# Option File Frame Content
# File Name
selectNameLabel = CTk.CTkLabel(optionFileFrame, text = langJson[lang]["selectNameLabelText"], font=("Arial", 20))
selectNameLabel.pack()
selectNameLabel.place(x = 10, y = 10)

nameEntry = CTk.CTkEntry(optionFileFrame, width = 370, height = 29, placeholder_text=langJson[lang]["nameEntryText"])
nameEntry.pack()
nameEntry.place(x = 10, y = 40)

# File img
imgFile = CTk.CTkImage(Image.open(imgJson["filename"][CTk.get_appearance_mode()]), size=(100, 100))

imageExtLabel = CTk.CTkLabel(optionFileFrame, image=imgFile, text="", fg_color=None)
imageExtLabel.pack()
imageExtLabel.place(x=385, y=30)

# File Extension
selectExtensionLabel = CTk.CTkLabel(optionFileFrame, text = langJson[lang]["selectExtensionLabelText"], font=("Arial", 20))
selectExtensionLabel.pack()
selectExtensionLabel.place(x = 10, y = 80)

extensionEntry = CTk.CTkEntry(optionFileFrame, width = 370, height = 29, placeholder_text=langJson[lang]["extensionEntryText"])
extensionEntry.pack()
extensionEntry.place(x = 10, y = 110)

# Start With Checkbox
startWithCheck = CTk.CTkCheckBox(optionFileFrame, text=langJson[lang]["startWithCheckText"])
startWithCheck.pack()
startWithCheck.place(x=10, y=148)

# Case Sensitive Checkbox
caseSensitiveCheck = CTk.CTkCheckBox(optionFileFrame, text=langJson[lang]["caseSensitiveCheckText"])
caseSensitiveCheck.pack()
caseSensitiveCheck.place(x=250, y=148)

# Search Button
searchButton = CTk.CTkButton(optionFileFrame, text=langJson[lang]["Search"], width=80, command=search)
searchButton.pack()
searchButton.place(x=155, y=180)

# Option File Frame
optionFileFrame = CTk.CTkFrame(root, fg_color=cardContent, width=280, height=430)
optionFileFrame.pack()
optionFileFrame.place(x=510, y=10)

# Option File Frame Content
# File List
fileList = CTk.CTkScrollableFrame(optionFileFrame, fg_color=boxContent, width=238, height=360)
fileList.pack()
fileList.place(x=10, y=10)

# Move Button
moveButton = CTk.CTkButton(optionFileFrame, text=langJson[lang]["Move"], width=80, command=move)
moveButton.pack()
moveButton.place(x=145, y=390)

# Copy Button
copyButton = CTk.CTkButton(optionFileFrame, text=langJson[lang]["Copy"], width=80, command=copy)
copyButton.pack()
copyButton.place(x=55, y=390)

# Credit Frame
creditFrame = CTk.CTkFrame(root, fg_color=cardContent, width=780, height=40)
creditFrame.pack()
creditFrame.place(x=10, y=450)

# Lang Selector
langSelector = CTk.CTkComboBox(creditFrame, width=70, values=list(langJson.keys()), command=changeLang)
langSelector.set(lang)
langSelector.pack()
langSelector.place(x=6, y=6)

# Credit Frame Content
creditLabel = CTk.CTkLabel(creditFrame, text = langJson[lang]["creditLabelText"], font=("Arial", 20), height=20, width=300)
creditLabel.pack()
creditLabel.place(x = 230, y = 10)
creditLabel.bind("<Button-1>", open_profile)

imgGit = CTk.CTkImage(Image.open(imgJson["git"][CTk.get_appearance_mode()]), size=(30, 30))

imageExtLabel = CTk.CTkLabel(creditFrame, image=imgGit, text="", fg_color=None)
imageExtLabel.pack()
imageExtLabel.place(x=745, y=5)
imageExtLabel.bind("<Button-1>", open_repo)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()