# Imports
# region
import datetime
import sys
import os
import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
# endregion

# Horodatage/log des print
# region
class TimestampedStream:
    def __init__(self, stream):
        self.stream = stream
        self.new_line = True
        self.log = False
        self.filename = ""
        self.file = None

    def write(self, text):
        text = text.encode("utf-8", errors="replace").decode("utf-8")  # Décodage unicode
        if text != '\n':
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            if self.new_line:
                self.stream.write(f"{timestamp} {text}")
                if self.log:
                    self.file = open(self.filename, "a", encoding="utf-8")
                    if not self.file.closed:
                        self.file.write(f"{timestamp} {text}")
                        self.file.close()
            else:
                self.stream.write(text)
                if self.log:
                    self.file = open(self.filename, "a", encoding="utf-8")
                    if not self.file.closed:
                        self.file.write(text)
                        self.file.close()
            self.new_line = False
        else:
            self.stream.write(text)
            if self.log:
                self.file = open(self.filename, "a", encoding="utf-8")
                if not self.file.closed:
                    self.file.write(text)
                    self.file.close()
            self.new_line = True

    def flush(self):
        self.stream.flush()
        if self.log:
            self.file.flush()

sys.stdout = TimestampedStream(sys.stdout)
# endregion

# Package Exe Ico
# region
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)
# endregion

# Initialisation des constantes/variables
# region
PROGRAM_NAME = "Act-O-Matic"
VERSION = "v1.0.0"
path_image = r""
# endregion

# Fonctions
# region
def msg_box(category, message, icon, log=True):
    if log:
        print(f"{category}: {message}")
    msgbox = CTkMessagebox(title=PROGRAM_NAME + " " + VERSION, message=message, icon=icon)
    msgbox.get()  # Tant que l'utilisateur ne valide/ferme pas la messagebox
# endregion

# R�glages g�n�raux du programme
# region
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# endregion

class gui(ctk.CTk):  # GUI
    # Callbacks
    # region
    def btn_clbk_path_image(self):  # Callback Widget
        print("Image file selection window openned.")
        global path_image
        # png and jpeg
        path_image = tk.filedialog.askopenfilename(title="Select a file...", filetypes=(("Image file", "*.png *.jpeg *.jpg"),))
        if path_image:
            print('Image file: "', path_image, '" selected.', sep="")
        else:
            print("No file selected.")
            pathParameters = ""
        self.ntry_path_image.configure(state="normal", placeholder_text=path_image)
        self.ntry_path_image.configure(state="disabled")

    def btn_clbk_launch(self):  # Callback Widget
        # Global variables + Init des variables
        # region
        # endregion

        # Protections pré-exécution
        # region
        if path_image == "":
            msg_box("Error", 'No image file selected! Please select an image file.', "cancel")
            return
        # endregion

        # Lancement de l'exécution si tout OK
        # region
        self.btn_launch.configure(state="disabled")
        self.execution()
        self.btn_launch.configure(state="normal")
        # endregion
    # endregion

    def __init__(self):
        # Globals et variables
        # region
        super().__init__()
        # endregion

        # Configuration de la fenêtre
        # region
        self.geometry("1200x650")
        self.resizable(True, True)
        self.minsize(700, 500)
        self.title(PROGRAM_NAME + " " + VERSION)
        self.iconbitmap("polytech.ico")
        #self.iconbitmap(default=os.path.join(application_path, "polytech.ico"))
        # endregion

        # Widgets
        # region
        self.frm_sidebar = ctk.CTkFrame(self)
        self.lbl_title = ctk.CTkLabel(self.frm_sidebar, text=PROGRAM_NAME + " " + VERSION, font=("Helvetica", 20))
        self.frm_path_image = ctk.CTkFrame(self.frm_sidebar)
        self.lbl_path_image = ctk.CTkLabel(self.frm_path_image, text="Image file:")
        self.ntry_path_image = ctk.CTkEntry(self.frm_path_image, placeholder_text="Image file path", state="disabled")
        self.btn_path_image = ctk.CTkButton(self.frm_path_image, text="Select image file", command=self.btn_clbk_path_image)
        self.frm_main = ctk.CTkFrame(self)
        # endregion

        # Packs
        # region
        self.frm_sidebar.pack(side="left", fill="both", expand=True)
        self.lbl_title.pack(side="top", fill="x", expand=True)
        self.frm_path_image.pack(side="top", padx=10, pady=10, fill="x", expand=True)
        self.lbl_path_image.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.ntry_path_image.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.btn_path_image.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        self.frm_main.pack(side="right", fill="both", expand=True)
        # endregion

        # Fin de l'initialisation
        # region
        print("""        ***** **               ***                                                     *      """)
        print("""     ******  ****               ***                       *                          **       """)
        print("""    **   *  *  ***               **                      **                          **       """)
        print("""   *    *  *    ***              **                      **                          **       """)
        print("""       *  *      **    ****      **    **   ****       ********                      **       """)
        print("""      ** **      **   * ***  *   **     **    ***  *  ********     ***       ****    **  ***  """)
        print("""      ** **      **  *   ****    **     **     ****      **       * ***     * ***  * ** * *** """)
        print("""    **** **      *  **    **     **     **      **       **      *   ***   *   ****  ***   ***""")
        print("""   * *** **     *   **    **     **     **      **       **     **    *** **         **     **""")
        print("""      ** *******    **    **     **     **      **       **     ********  **         **     **""")
        print("""      ** ******     **    **     **     **      **       **     *******   **         **     **""")
        print("""      ** **         **    **     **     **      **       **     **        **         **     **""")
        print("""      ** **          ******      **      *********       **     ****    * ***     *  **     **""")
        print("""      ** **           ****       *** *     **** ***       **     *******   *******   **     **""")
        print(""" **   ** **                       ***            ***              *****     *****     **    **""")
        print("""***   *  *                                *****   ***                                       * """)
        print(""" ***    *                               ********  **                                       *  """)
        print("""  ******                               *      ****                                        *   """)
        print("""    ***                                                                                  *    """)
        print('''MMP"""""""MM            dP            MMP"""""YMM          M"""""`'"""`YM            dP   oo          ''')
        print('''M' .mmmm  MM            88            M' .mmm. `M          M  mm.  mm.  M            88               ''')
        print('''M         `M .d8888b. d8888P          M  MMMMM  M          M  MMM  MMM  M .d8888b. d8888P dP .d8888b. ''')
        print('''M  MMMMM  MM 88'  `""   88   88888888 M  MMMMM  M 88888888 M  MMM  MMM  M 88'  `88   88   88 88'  `"" ''')
        print('''M  MMMMM  MM 88.  ...   88            M. `MMM' .M          M  MMM  MMM  M 88.  .88   88   88 88.  ... ''')
        print('''M  MMMMM  MM `88888P'   dP            MMb     dMM          M  MMM  MMM  M `88888P8   dP   dP `88888P' ''')
        print('''MMMMMMMMMMMM                          MMMMMMMMMMM          MMMMMMMMMMMMMM                             ''')
        print("Initialization completed.")
        # endregion

def execution():
    print("Execution started.")
    print("Execution completed.")

if __name__ == "__main__":
    app = gui()
    app.mainloop()
    sys.exit()
