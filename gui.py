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
        self.newLine = True
        self.log = False
        self.filename = ""
        self.file = None

    def write(self, text):
        text = text.encode("utf-8", errors="replace").decode("utf-8")  # Décodage unicode
        if text != '\n':
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            if self.newLine:
                self.stream.write(f"{timestamp} {text}")
                if self.log:
                    self.file = open(self.filename, "a", encoding="utf-8")
                    if not self.file.closed:
                        self.file.write(f"{timestamp} {text}")
                        self.file.close()  # Close de sauvegarde si pb
            else:
                self.stream.write(text)
                if self.log:
                    self.file = open(self.filename, "a", encoding="utf-8")
                    if not self.file.closed:
                        self.file.write(text)
                        self.file.close()  # Close de sauvegarde si pb
            self.newLine = False
        else:
            self.stream.write(text)
            if self.log:
                self.file = open(self.filename, "a", encoding="utf-8")
                if not self.file.closed:
                    self.file.write(text)
                    self.file.close()  # Close de sauvegarde si pb
            self.newLine = True

    def startLog(self, filename):
        self.log = True
        self.filename = filename
        self.file = open(filename, "a", encoding="utf-8")
        self.file.write(f"AutoSuite {version}\n")
        self.file.close()

    def stopLog(self):
        self.log = False
        self.file.close()
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
    def btn_clbk_pathParameters(self):  # Callback Widget
        print("Image file selection window openned.")
        global path_image
        path_image = tk.filedialog.askopenfilename(title="Select a file...", filetypes=(("Parameter file", "*.xml"),), ).replace("/", "\\")  # tkinter fcts sends back "/" instead of "\"
        if path_image:
            print('Parameter file: "', path_image, '" selected.', sep="")
        else:
            print("No file selected.")
            pathParameters = ""
        self.ntry_pathParameters.configure(state="normal", placeholder_text=path_image)
        self.ntry_pathParameters.configure(state="disabled")

    def btn_clbk_launch(self):  # Callback Widget
        # Global variables + Init des variables
        # region
        global pathCpg, pathCpgDigital, pathCpgAnalog, pathReportModel, pathReportModelDigital, pathReportModelAnalog
        pathCpg = r""
        pathReportModel = r""
        # endregion

        # Protections pré-exécution
        # region
        if pathRunTests == "":
            msg_box("Error", 'No "run_tests.exe" parent folder selected! Please go to the Settings tab!', "cancel")
            return
        if pathMakeReport == "":
            msg_box("Error", 'No "make_report.exe" parent folder selected! Please go to the Settings tab!', "cancel")
            return
        if mode.lower() == "digital suite":  # Digital
            if pathCpgDigital == "":
                msg_box("Error", "No Digital Suite file selected! Please go to the Settings tab!", "cancel")
                return
            else:
                pathCpg = pathCpgDigital
            if pathReportModelDigital == "":
                msg_box("Error", "No Digital Report Model file selected! Please go to the Settings tab!", "cancel")
                return
            else:
                pathReportModel = pathReportModelDigital
        else:  # Analog
            if pathCpgAnalog == "":
                msg_box("Error", "No Analog Suite file selected! Please go to the Settings tab!", "cancel")
                return
            else:
                pathCpg = pathCpgAnalog
            if pathReportModelAnalog == "":
                msg_box("Error", "No Analog Report Model file selected! Please go to the Settings tab!", "cancel")
                return
            else:
                pathReportModel = pathReportModelAnalog
        if enableClimateChamber:  # Si on a activé l'étuve
            if ipClimateChamber == "":
                msg_box("Error", "No climate chamber IP address! Please go to the Settings tab!", "cancel")
                return
            elif not isIp(ipClimateChamber):
                msg_box("Error", "Invalid climate chamber IP address! Please go to the Settings tab!", "cancel")
                return
            elif stableTimeout == "":
                msg_box("Error", "No climate chamber stable timeout time! Please go to the Settings tab!", "cancel")
                return
            elif settlingTime == "":
                msg_box("Error", "No climate chamber settling time! Please go to the Settings tab!", "cancel")
                return
            elif maxTempDiff == None:
                msg_box("Error",
                       "No climate chamber maximum temperature difference value! Please go to the Settings tab!",
                       "cancel")
                return
        if pathParameters == "":
            msg_box("Error", "No Parameter file selected!", "cancel")
            return
        if os.path.abspath(os.path.join(pathParameters, os.pardir)) != os.path.abspath(
                os.path.join(pathCpg, os.pardir)):
            msg_box("Error", "Parameter file and Suite file aren't in the same folder!", "cancel")
            return
        if pathOutputFolder == "":
            msg_box("Error", "No Output folder selected!", "cancel")
            return
        if len(Temperatures) == 0:
            msg_box("Error", "No Temperatures!", "cancel")
            return
        else:
            for valeurs in Temperatures:
                if len(valeurs) == 0:
                    msg_box("Error", "No Temperatures!", "cancel")
                    return
        if mode.lower() != "analog suite":  # [Digital]
            if len(Fields) == 0:
                msg_box("Error", "No Fields!", "cancel")
                return
            else:
                for valeurs in Fields:
                    if len(valeurs) == 0:
                        msg_box("Error", "No Fields!", "cancel")
                        return
            if len(Speeds) == 0:
                msg_box("Error", "No Speeds!", "cancel")
                return
            else:
                for valeurs in Speeds:
                    if len(valeurs) == 0:
                        msg_box("Error", "No Speeds!", "cancel")
                        return
        # endregion

        # Lancement de l'exécution si tout OK
        # region
        self.btn_Launch.configure(state="disabled")
        self.iconify()
        self.execution()
        self.deiconify()
        self.btn_Launch.configure(state="normal")
        # endregion

        # Reset des variables
        # region
        pathCpg = r""
        pathReportModel = r""
        # endregion
    # endregion
    def __init__(self):  # Initialisation du GUI
        # Globals et variables
        # region
        super().__init__()
        global version
        global Temperatures
        global Cards
        global Fields
        global Speeds
        global CardExec
        CardExec = customtkinter.IntVar()
        # endregion

        # Configuration de la fenêtre
        # region
        self.geometry("900x515")
        self.resizable(True, False)
        self.minsize(650, 515)
        self.title("AutoSuite " + version)
        self.iconbitmap(default=os.path.join(application_path, "Thales.ico"))
        # endregion

        # Widgets
        # region
        self.frm_topRibbon = customtkinter.CTkFrame(master=self, fg_color="transparent")  # Cadre du ruban haut
        self.btn_settings = customtkinter.CTkButton(master=self.frm_topRibbon, text="Settings",
                                                    command=self.btn_clbk_settings)
        self.btn_regenCSV = customtkinter.CTkButton(master=self.frm_topRibbon, text="Regenerate csv",
                                                    command=self.btn_clbk_regenCSV)
        self.btn_rerunTests = customtkinter.CTkButton(master=self.frm_topRibbon, text="Rerun test(s)",
                                                      command=self.btn_clbk_rerunTests)
        self.om_mode = customtkinter.CTkOptionMenu(master=self.frm_topRibbon, values=["Digital suite", "Analog suite"],
                                                   command=self.om_clbk_mode)
        self.frm_pathParameters = customtkinter.CTkFrame(
            master=self)  # Cadre de la zone de param�trage des parametres XML
        self.lbl_pathParameters = customtkinter.CTkLabel(master=self.frm_pathParameters, text="Parameter file",
                                                         justify=customtkinter.LEFT)
        self.btn_pathParameters = customtkinter.CTkButton(master=self.frm_pathParameters, text="Browse...",
                                                          command=self.btn_clbk_pathParameters)
        self.ntry_pathParameters = customtkinter.CTkEntry(master=self.frm_pathParameters, placeholder_text="",
                                                          state="disabled")
        self.frm_pathOutputFolder = customtkinter.CTkFrame(
            master=self)  # Cadre de la zone de param�trage du dossier de sortie
        self.lbl_pathOutputFolder = customtkinter.CTkLabel(master=self.frm_pathOutputFolder, text="Output folder",
                                                           justify=customtkinter.LEFT)
        self.ntry_pathOutputFolder = customtkinter.CTkEntry(master=self.frm_pathOutputFolder, placeholder_text="",
                                                            state="disabled")
        self.btn_pathOutputFolder = customtkinter.CTkButton(master=self.frm_pathOutputFolder, text="Browse...",
                                                            command=self.btn_clbk_pathOutputFolder)
        self.frm_ExecSettings = customtkinter.CTkFrame(
            master=self)  # Cadre de la zone d'entr�e des param�tres d'�x�cution
        self.tv_ExecSettings = customtkinter.CTkTabview(master=self.frm_ExecSettings)
        self.tv_ExecSettings.add("Temperatures")
        self.tv_ExecSettings.add("Cards")
        self.tv_ExecSettings.add("Fields")
        self.tv_ExecSettings.add("Speeds")
        self.tv_ExecSettings_ntry_temperatures = customtkinter.CTkEntry(master=self.tv_ExecSettings.tab("Temperatures"),
                                                                        placeholder_text=Temperatures,
                                                                        font=customtkinter.CTkFont(size=20),
                                                                        state="disabled")
        self.tv_ExecSettings_btn_temperatures = customtkinter.CTkButton(master=self.tv_ExecSettings.tab("Temperatures"),
                                                                        text="Add/Modify",
                                                                        command=self.btn_clbk_Temperatures)
        self.frm_ExecSettings_cards_upper = customtkinter.CTkFrame(master=self.tv_ExecSettings.tab("Cards"),
                                                                   fg_color="transparent")  # Cadre des cartes haut
        self.tv_ExecSettings_rbtn_continuous_exec = customtkinter.CTkRadioButton(
            master=self.frm_ExecSettings_cards_upper, text="Continuous execution", variable=CardExec, value=0,
            command=self.rbtn_clbk_continuous_exec)
        self.tv_ExecSettings_rbtn_one_card_exec = customtkinter.CTkRadioButton(master=self.frm_ExecSettings_cards_upper,
                                                                               text="One card execution",
                                                                               variable=CardExec, value=1,
                                                                               command=self.rbtn_clbk_one_card_exec)
        self.frm_ExecSettings_cards_lower = customtkinter.CTkFrame(master=self.tv_ExecSettings.tab("Cards"),
                                                                   fg_color="transparent")  # Cadre des cartes bas
        self.tv_ExecSettings_btn_minus_cards = customtkinter.CTkButton(master=self.frm_ExecSettings_cards_lower,
                                                                       text="-", command=self.btn_clbk_minus_Cards,
                                                                       font=customtkinter.CTkFont(size=25))
        self.tv_ExecSettings_lbl_cards = customtkinter.CTkLabel(master=self.frm_ExecSettings_cards_lower,
                                                                text=str(Cards), justify="center",
                                                                font=customtkinter.CTkFont(size=25))
        self.tv_ExecSettings_btn_plus_cards = customtkinter.CTkButton(master=self.frm_ExecSettings_cards_lower,
                                                                      text="+", command=self.btn_clbk_plus_Cards,
                                                                      font=customtkinter.CTkFont(size=25))
        self.tv_ExecSettings_ntry_fields = customtkinter.CTkEntry(master=self.tv_ExecSettings.tab("Fields"),
                                                                  placeholder_text=Fields,
                                                                  font=customtkinter.CTkFont(size=20), state="disabled")
        self.tv_ExecSettings_btn_fields = customtkinter.CTkButton(master=self.tv_ExecSettings.tab("Fields"),
                                                                  text="Add/Modify", command=self.btn_clbk_Fields)
        self.frm_ExecSettings_speeds_l = customtkinter.CTkFrame(master=self.tv_ExecSettings.tab("Speeds"),
                                                                fg_color="transparent")  # Cadre des vitesses gauche
        self.frm_ExecSettings_speeds_r = customtkinter.CTkFrame(master=self.tv_ExecSettings.tab("Speeds"),
                                                                fg_color="transparent")  # Cadre des vitesses droite
        self.tv_ExecSettings_scrfrm_speeds = customtkinter.CTkScrollableFrame(master=self.frm_ExecSettings_speeds_l)
        self.tv_ExecSettings_cb_106 = customtkinter.CTkCheckBox(master=self.tv_ExecSettings_scrfrm_speeds,
                                                                text="106 kbit/s",
                                                                command=lambda: self.cb_clbk_Speeds("106 kbit/s"))
        self.tv_ExecSettings_cb_212 = customtkinter.CTkCheckBox(master=self.tv_ExecSettings_scrfrm_speeds,
                                                                text="212 kbit/s",
                                                                command=lambda: self.cb_clbk_Speeds("212 kbit/s"))
        self.tv_ExecSettings_cb_424 = customtkinter.CTkCheckBox(master=self.tv_ExecSettings_scrfrm_speeds,
                                                                text="424 kbit/s",
                                                                command=lambda: self.cb_clbk_Speeds("424 kbit/s"))
        self.tv_ExecSettings_cb_848 = customtkinter.CTkCheckBox(master=self.tv_ExecSettings_scrfrm_speeds,
                                                                text="848 kbit/s",
                                                                command=lambda: self.cb_clbk_Speeds("848 kbit/s"))
        self.tv_ExecSettings_cb_1700 = customtkinter.CTkCheckBox(master=self.tv_ExecSettings_scrfrm_speeds,
                                                                 text="1.7 Mbit/s",
                                                                 command=lambda: self.cb_clbk_Speeds("1.7 Mbit/s"))
        self.tv_ExecSettings_cb_3400 = customtkinter.CTkCheckBox(master=self.tv_ExecSettings_scrfrm_speeds,
                                                                 text="3.4 Mbit/s",
                                                                 command=lambda: self.cb_clbk_Speeds("3.4 Mbit/s"))
        self.tv_ExecSettings_cb_6800 = customtkinter.CTkCheckBox(master=self.tv_ExecSettings_scrfrm_speeds,
                                                                 text="6.8 Mbit/s",
                                                                 command=lambda: self.cb_clbk_Speeds("6.8 Mbit/s"))
        self.tv_ExecSettings_om_MbitsKbits = customtkinter.CTkOptionMenu(master=self.frm_ExecSettings_speeds_r,
                                                                         values=["Mbits (digital 08.02)",
                                                                                 "kbits only (digital 08.04+)"],
                                                                         command=self.om_clbk_MbitsKbits)
        self.frm_Launch = customtkinter.CTkFrame(master=self, fg_color="transparent")  # Cadre du bouton de démarrage
        self.btn_Launch = customtkinter.CTkButton(master=self.frm_Launch, text="Launch", command=self.btn_clbk_launch,
                                                  font=customtkinter.CTkFont(size=24, weight="bold"))
        # endregion

        # Packs
        # region
        self.frm_topRibbon.pack(pady=5, padx=10, fill="x", expand=True)
        self.btn_settings.pack(side="left", pady=0, padx=0)
        self.btn_regenCSV.pack(side="left", pady=0, padx=10)
        self.btn_rerunTests.pack(side="left", pady=0, padx=0)
        self.om_mode.pack(side="right", pady=0, padx=0)
        self.frm_pathParameters.pack(pady=5, padx=10, fill="x", expand=True)
        self.lbl_pathParameters.pack(side="left", pady=10, padx=10)
        self.btn_pathParameters.pack(side="right", pady=10, padx=10, ipadx=1)
        self.ntry_pathParameters.pack(side="left", pady=5, padx=5, fill="x", expand=True)
        self.frm_pathOutputFolder.pack(pady=5, padx=10, fill="x", expand=True)
        self.lbl_pathOutputFolder.pack(side="left", pady=10, padx=10)
        self.btn_pathOutputFolder.pack(side="right", pady=10, padx=10, ipadx=1)
        self.ntry_pathOutputFolder.pack(side="left", pady=5, padx=5, fill="x", expand=True)
        self.frm_ExecSettings.pack(pady=5, padx=10, fill="both", expand=True)
        self.tv_ExecSettings.pack(pady=10, padx=10, fill="x", expand=True)
        self.tv_ExecSettings_ntry_temperatures.pack(side="top", pady=10, padx=10, fill="both", expand=True)
        self.tv_ExecSettings_btn_temperatures.pack(side="bottom", pady=10, padx=10)
        self.frm_ExecSettings_cards_upper.pack(side="top", pady=0, padx=0, fill="both", expand=True)
        self.tv_ExecSettings_rbtn_continuous_exec.pack(side="left", pady=10, padx=10, expand=True)
        self.tv_ExecSettings_rbtn_one_card_exec.pack(side="right", pady=10, padx=10, expand=True)
        self.frm_ExecSettings_cards_lower.pack(side="bottom", pady=0, padx=0, fill="both", expand=True)
        self.tv_ExecSettings_btn_minus_cards.pack(side="left", pady=10, padx=10, expand=True)
        self.tv_ExecSettings_lbl_cards.pack(side="left", pady=10, padx=10, expand=True)
        self.tv_ExecSettings_btn_plus_cards.pack(side="left", pady=10, padx=10, expand=True)
        self.tv_ExecSettings_ntry_fields.pack(side="top", pady=10, padx=10, fill="both", expand=True)
        self.tv_ExecSettings_btn_fields.pack(side="bottom", pady=10, padx=10)
        self.frm_ExecSettings_speeds_l.pack(side="left", pady=0, padx=0, fill="both", expand=True)
        self.frm_ExecSettings_speeds_r.pack(side="right", pady=0, padx=0, fill="both", expand=True)
        self.tv_ExecSettings_scrfrm_speeds.pack(side="right", pady=5, padx=10)
        self.tv_ExecSettings_cb_106.pack(side="top", pady=10, padx=10, fill="x", expand=True)
        self.tv_ExecSettings_cb_212.pack(side="top", pady=10, padx=10, fill="x", expand=True)
        self.tv_ExecSettings_cb_424.pack(side="top", pady=10, padx=10, fill="x", expand=True)
        self.tv_ExecSettings_cb_848.pack(side="top", pady=10, padx=10, fill="x", expand=True)
        self.tv_ExecSettings_cb_1700.pack(side="top", pady=10, padx=10, fill="x", expand=True)
        self.tv_ExecSettings_cb_3400.pack(side="top", pady=10, padx=10, fill="x", expand=True)
        self.tv_ExecSettings_cb_6800.pack(side="top", pady=10, padx=10, fill="x", expand=True)
        self.tv_ExecSettings_om_MbitsKbits.pack(side="left", pady=5, padx=10)
        self.frm_Launch.pack(pady=5, padx=10, fill="x", expand=True)
        self.btn_Launch.pack(pady=0, padx=0, fill="both", expand=True)
        # endregion

        # Fin de l'initialisation
        # region
        print("######## ##     ##    ###    ##       ########  ###### ")
        print("   ##    ##     ##   ## ##   ##       ##       ##    ##")
        print("   ##    ##     ##  ##   ##  ##       ##       ##      ")
        print("   ##    ######### ##     ## ##       ######    ###### ")
        print("   ##    ##     ## ######### ##       ##             ##")
        print("   ##    ##     ## ##     ## ##       ##       ##    ##")
        print("   ##    ##     ## ##     ## ######## ########  ###### ")
        print(r" ______           __           ____                __             ")
        print(r"/\  _  \         /\ \__       /\  _`\           __/\ \__          ")
        print(r"\ \ \L\ \  __  __\ \ ,_\   ___\ \,\L\_\  __  __/\_\ \ ,_\    __   ")
        print(r" \ \  __ \/\ \/\ \\ \ \/  / __`\/_\__ \ /\ \/\ \/\ \ \ \/  /'__`\ ")
        print(r"  \ \ \/\ \ \ \_\ \\ \ \_/\ \L\ \/\ \L\ \ \ \_\ \ \ \ \ \_/\  __/ ")
        print(r"""   \ \_\ \_\ \____/ \ \__\ \____/\ `\____\ \____/\ \_\ \__\ \____\ """)
        print(r"    \/_/\/_/\/___/   \/__/\/___/  \/_____/\/___/  \/_/\/__/\/____/")
        print("Initialization completed.")
        # endregion

    def execution(self, rerun=None):  # Ex�cution du programme
        # Global variables
        # region
        global Temperatures
        global Cards
        global Fields
        global Speeds
        global SpeedsUnit
        global stabilized
        global settled
        quitAllLoops = False  # Init
        warningTempExec = []
        previousCard = None  # [Rerun]
        i = 0  # [Rerun] Défilement d'index de rerun
        # endregion

        # [Rerun] Sauvegarde des états des variables et mise en place des variables de rerun
        # region
        if rerun != None:
            # Save
            # region
            tempTemperatures = Temperatures
            tempCards = Cards
            tempFields = Fields
            tempSpeeds = Speeds
            # endregion

            # Réinit
            # region
            Temperatures = []  # Init
            Cards = []  # Init
            Fields = []  # Init
            Speeds = []  # Init
            # endregion

            # Valeurs de rerun
            # region
            for runs in rerun:
                if runs["Temperature"] not in Temperatures:
                    Temperatures.append(runs["Temperature"])
                if runs["Card"] not in Cards:
                    Cards.append(runs["Card"])
                if runs["Field"] not in Fields:
                    Fields.append(runs["Field"])
                if runs["Speed"] not in Speeds:
                    Speeds.append(runs["Speed"])
            previousCard = int(
                min(Cards))  # Min => Int pour avoir la première carte testée (et ne pas mettre le message de changement 2 fois)
            Cards = int(max(Cards))  # Max => Int pour avoir la range de cartes comprenant toutes les cartes
            # endregion

            # Sort
            # region
            Temperatures.sort()
            Fields.sort()
            Speeds.sort()
            # endregion
        # endregion

        # Setup du fichier log
        # region
        pathASFiles = pathOutputFolder + "\\AS Files"
        if not os.path.exists(pathASFiles):
            os.makedirs(pathASFiles)
        pathLogFile = pathASFiles + "\\Log.txt"
        sys.stdout.startLog(pathLogFile)
        # endregion

        # Message de start
        # region
        if rerun == None:
            print("===============")
            print("Execution launched with:")
            print('=> Parameter file: "', pathParameters, '".', sep="")
            print('=> Output folder: "', pathOutputFolder, '".', sep="")
            print('=> "run_tests.exe" parent folder: "', pathRunTests, '".', sep="")
            print('=> "make_report.exe" parent folder: "', pathMakeReport, '".', sep="")
            print('=> Suite file: "', pathCpg, '".', sep="")
            print('=> Report Model file: "', pathReportModel, '".', sep="")
            print('=> Climate chamber IP address: "', ipClimateChamber, '".', sep="")
            print('=> Climate chamber stable timeout: "', stableTimeout, '".', sep="")
            print('=> Climate chamber settling time: "', settlingTime, '".', sep="")
            print('=> Climate chamber maximum temperature difference: "', str(maxTempDiff), '°C".', sep="")
            print("=> Temperatures: ", Temperatures, ".", sep="")
            if CardExec == 1:
                print('=> Card selected: "', Cards, '".', sep="")
            else:
                print('=> Number of Cards: "', Cards, '".', sep="")
            if mode.lower() == "digital suite":
                print("=> Fields: ", Fields, ".", sep="")
                print("=> Speeds: ", Speeds, ".", sep="")
            print("===============")
        else:
            print("===============")
            print("Rerun launched with:")
            print('=> Parameter file: "', pathParameters, '".', sep="")
            print('=> Output folder: "', pathOutputFolder, '".', sep="")
            print('=> "run_tests.exe" parent folder: "', pathRunTests, '".', sep="")
            print('=> "make_report.exe" parent folder: "', pathMakeReport, '".', sep="")
            print('=> Suite file: "', pathCpg, '".', sep="")
            print('=> Report Model file: "', pathReportModel, '".', sep="")
            print('=> Climate chamber IP address: "', ipClimateChamber, '".', sep="")
            print('=> Climate chamber stable timeout: "', stableTimeout, '".', sep="")
            print('=> Climate chamber settling time: "', settlingTime, '".', sep="")
            print('=> Climate chamber maximum temperature difference: "', str(maxTempDiff), '°C".', sep="")
            print('=> Tests that will be rerun:')
            for runs in rerun:
                print("\t=> ", runs, ".", sep="")
            print("===============")
        # endregion

        # Setup de l'étuve si activée
        # region
        if enableClimateChamber:
            print("Testing connection to climate chamber...")
            if ping(ipClimateChamber):  # ping de l'étuve pour vérifier le fonctionnment
                try:
                    climateChamber = ClimateChamber(ip=ipClimateChamber, temperature_min=-42, temperature_max=180)
                except Exception as e:
                    msg_box("Error",
                           f"An error occurred while connecting to the climate chamber: {str(e)}! Stopping execution...",
                           "cancel")
                    return
                print("Connection to climate chamber OK: ", climateChamber.idn, ".", sep="")
            else:
                msg_box("Error", "No response from climate chamber! Stopping execution...", "cancel")
                return
        # endregion

        # Calcul des timings et des boucles si étuve activée
        # region
        if enableClimateChamber:  # SI TEMPÉRATURES AUTO
            # stableTimeout
            if " min" in stableTimeout:
                stableTimeoutSec = float(stableTimeout.replace(" min", "")) * 60
            elif " sec" in stableTimeout:
                stableTimeoutSec = float(stableTimeout.replace(" sec", ""))
            else:
                msg_box("Error", "Invalid climate chamber stable timeout time! Stopping...", "cancel")
                return
            # settlingTime
            if " min" in settlingTime:
                settlingTimeSec = float(settlingTime.replace(" min", "")) * 60
            elif " sec" in settlingTime:
                settlingTimeSec = float(settlingTime.replace(" sec", ""))
            else:
                msg_box("Error", "Invalid climate chamber settling time! Stopping...", "cancel")
                return
            # Boucles de 30s
            stableTimeoutBoucles = math.ceil(stableTimeoutSec / 30)
            settlingTimeBoucles = math.ceil(settlingTimeSec / 30)
        # endregion

        # Sélection de l'unité des vitesses (v.08.02/v.08.04)
        # region
        if SpeedsUnit == "kbits only (digital 08.04+)":
            for i, n in enumerate(Speeds):
                if n == "1.7 Mbit/s":
                    Speeds[i] = "1700 kbit/s"
                elif n == "3.4 Mbit/s":
                    Speeds[i] = "3400 kbit/s"
                elif n == "6.8 Mbit/s":
                    Speeds[i] = "6800 kbit/s"
        # endregion

        # Création des fichiers de Paramétrages XML - Champs
        # region
        pathBackupFolder = pathASFiles + "\\XML Backup"
        if mode.lower() != "analog suite":  # [Digital]
            if not os.path.exists(pathBackupFolder):
                os.makedirs(pathBackupFolder)
            for dirFields in Fields:
                for dirSpeeds in Speeds:  # Vitesses
                    xmlGenerator(pathParameters, dirFields, dirSpeeds,
                                 pathBackupFolder)  # Création du fichier de Paramétrage XML spécifique
        else:  # [Analog]
            try:
                pathBackupAnalog = pathBackupFolder + "\\" + os.path.basename(pathParameters)
                os.makedirs(os.path.dirname(pathBackupAnalog), exist_ok=True)
                shutil.copy(pathParameters, pathBackupAnalog)
            except Exception as e:
                msg_box("Error", f"An error occurred while copying the Parameter file: {str(e)}! Stopping execution...",
                       "cancel")
                return
        # endregion

        # Choix des ranges des cartes pour l'éxécution principale
        # region
        if (CardExec == 1) or ((rerun != None) and (Cards == 1)):  # SI ON NE VEUT QU'UNE CARTE - [Rerun]
            rangeCards = range(Cards - 1, Cards,
                               1)  # On n'atteint pas le "Cards" comme on a un pas de 1 ; ON VEUT "Cards-1" CAR LE RESTE DES TRAITEMENTS EST FAIT EN ACCORD AVEC LE "+1 à cause du range"
            msg_box("Card Change", f'Please check that current card is number: "{str(Cards)}".', "info", False)
        else:  # SI ON VEUT PLUSIEURS CARTES - [Rerun]
            rangeCards = range(0, Cards)
        # endregion

        # Mise en place de la fenêtre de monitoring
        # region
        if rerun == None:
            if mode.lower() != "analog suite":  # [Digital]
                execMonitoring = monitoring(len(Temperatures) * Cards * len(Fields) * len(Speeds))
            else:  # [Analog]
                execMonitoring = monitoring(len(Temperatures) * Cards)
        else:
            execMonitoring = monitoring(len(rerun))
        execMonitoring.grab_set()
        # endregion

        # Éxécution principale - Arborescence
        # region
        for dirTemperatures in Temperatures:  # Arborescence des fichiers de sortie et Exécution - Températures
            if quitAllLoops:  # [Rerun] Exit des loops
                break  # [Rerun]
            while (rerun == None) or (
                    (not quitAllLoops) and (rerun[i]["Temperature"] == dirTemperatures)):  # [Rerun] - Températures
                if not enableClimateChamber:  # SI TEMPÉRATURES MANUELLES
                    msg_box("Temperature Change",
                           f'Please check that the current temperature is set to: "{dirTemperatures}°C".', "info",
                            False)
                stabilized = False
                dirTemperaturesPath = pathOutputFolder + "\\" + dirTemperatures
                if not os.path.exists(dirTemperaturesPath):
                    os.makedirs(dirTemperaturesPath)
                for dirCards in rangeCards:  # Arborescence des fichiers de sortie et Exécution - Cartes
                    if quitAllLoops:  # [Rerun] Exit des loops
                        break  # [Rerun]
                    while (rerun == None) or ((not quitAllLoops) and (int(rerun[i]["Card"]) == (dirCards + 1)) and (
                            rerun[i]["Temperature"] == dirTemperatures)):  # [Rerun] - Cartes  (+1 à cause du range)
                        if ((rerun == None) and (CardExec != 1)) or ((rerun != None) and ((
                                                                                                  dirCards + 1) != previousCard)):  # SI ON VEUT PLUSIEURS CARTES ou [Rerun] et pas même carte que précédente (+1 à cause du range)
                            msg_box("Card Change", f'Please check that current card is number: "{str(dirCards + 1)}".',
                                   "info", False)
                        settled = False  # Reset de la stabilisation de la pièce
                        dirCardsPath = dirTemperaturesPath + r"\Card" + str((dirCards + 1))  # +1 à cause du range
                        if not os.path.exists(dirCardsPath):
                            os.makedirs(dirCardsPath)
                        if mode.lower() == "analog suite":  # [Analog]
                            if not enableClimateChamber:  # SI TEMPÉRATURES MANUELLES
                                self.executionCore(dirTemperatures=dirTemperatures, dirCards=dirCards,
                                                   dirCardsPath=dirCardsPath, execMonitoring=execMonitoring)
                            else:  # SI TEMPÉRATURES AUTO
                                self.executionCore(dirTemperatures=dirTemperatures, dirCards=dirCards,
                                                   dirCardsPath=dirCardsPath, execMonitoring=execMonitoring,
                                                   climateChamber=climateChamber,
                                                   stableTimeoutBoucles=stableTimeoutBoucles,
                                                   settlingTimeBoucles=settlingTimeBoucles,
                                                   warningTempExec=warningTempExec)
                        else:  # [Digital]
                            for dirFields in Fields:  # Arborescence des fichiers de sortie et Exécution - Champs
                                if quitAllLoops:  # [Rerun] Exit des loops
                                    break  # [Rerun]
                                while (rerun == None) or ((not quitAllLoops) and (rerun[i]["Field"] == dirFields) and (
                                        int(rerun[i]["Card"]) == (dirCards + 1)) and (rerun[i][
                                                                                          "Temperature"] == dirTemperatures)):  # [Rerun] - Champs
                                    dirFieldsPath = dirCardsPath + "\\" + dirFields + "Am"
                                    if not os.path.exists(dirFieldsPath):
                                        os.makedirs(dirFieldsPath)
                                    for dirSpeeds in Speeds:  # Arborescence des fichiers de sortie et Exécution - Vitesses
                                        if quitAllLoops:  # [Rerun] Exit des loops
                                            break  # [Rerun]
                                        while (rerun == None) or (
                                                (not quitAllLoops) and (rerun[i]["Speed"] == dirSpeeds) and (
                                                rerun[i]["Field"] == dirFields) and (
                                                        int(rerun[i]["Card"]) == (dirCards + 1)) and (rerun[i][
                                                                                                          "Temperature"] == dirTemperatures)):  # [Rerun] - Vitesses
                                            dirSpeedsPath = dirFieldsPath + "\\" + dirSpeeds.replace("/",
                                                                                                     "")  # Replace pour ne pas créer deux sous dossiers avec "/"
                                            if not os.path.exists(dirSpeedsPath):
                                                os.makedirs(dirSpeedsPath)
                                            if not enableClimateChamber:  # SI TEMPÉRATURES MANUELLESSI TEMPÉRATURES MANUELLES
                                                self.executionCore(dirTemperatures=dirTemperatures, dirCards=dirCards,
                                                                   dirCardsPath=dirCardsPath,
                                                                   execMonitoring=execMonitoring, dirFields=dirFields,
                                                                   dirSpeeds=dirSpeeds, dirSpeedsPath=dirSpeedsPath)
                                            else:  # SI TEMPÉRATURES AUTO
                                                self.executionCore(dirTemperatures=dirTemperatures, dirCards=dirCards,
                                                                   dirCardsPath=dirCardsPath,
                                                                   execMonitoring=execMonitoring, dirFields=dirFields,
                                                                   dirSpeeds=dirSpeeds, dirSpeedsPath=dirSpeedsPath,
                                                                   climateChamber=climateChamber,
                                                                   stableTimeoutBoucles=stableTimeoutBoucles,
                                                                   settlingTimeBoucles=settlingTimeBoucles,
                                                                   warningTempExec=warningTempExec)
                                            if rerun != None:  # [Rerun]
                                                if ((i + 1) < len(
                                                        rerun)):  # [Rerun] Passage au rerun suivant s'il en reste
                                                    i = i + 1  # [Rerun]
                                                else:  # [Rerun]
                                                    quitAllLoops = True  # [Rerun]
                                                    break  # [Rerun]
                                            if rerun == None:  # [Std]
                                                break  # [Std]
                                    if rerun == None:  # [Std]
                                        break  # [Std]
                        previousCard = (
                                    dirCards + 1)  # [Rerun] Mise en mémoire de la dernière carte  (+1 à cause du range)
                        if rerun == None:  # [Std]
                            break  # [Std]
                if rerun == None:  # [Std]
                    break  # [Std]
        # endregion

        # Arrêt de l'étuve si sélectionnée
        # region
        if enableClimateChamber:  # SI TEMPÉRATURES AUTO
            print("Stopping climate chamber...")
            climateChamber.stop()  # Arrêt de l'étuve
        # endregion

        # Génération du rapport csv
        # region
        if mode.lower() != "analog suite":  # [Digital]
            self.generateCSV(pathOutputFolder, warningTempExec)
        else:  # [Analog]
            msg_box("Warning", ".csv generation isn't currently available in Analog mode.", "warning", False)
        # endregion

        # Fermeture de la fenêtre de monitoring
        # region
        execMonitoring.destroy()
        # endregion

        # Message de fin
        # region
        if len(warningTempExec) == 0:  # Si pas d'écart de températures durant exécution/températures manuelles
            print("===============")
            print("Execution ended.")
            print("===============")
            msg_box("Execution ended", "Execution ended.", "info", False)
        else:  # Si écart de températures durant l'exécution
            print("===============")
            print("Execution ended with temperature disparities:")
            for disparity in warningTempExec:
                if mode.lower() != "analog suite":  # [Digital]
                    print(
                        f'Temperature: "{disparity["temperature"]}°C", card: "{str(disparity["card"])}", speed: "{disparity["speed"]}" and field: "{disparity["field"]}A/m": "{disparity["disparity"]}°C".')
                else:  # [Analog]
                    print(
                        f'Temperature: "{disparity["temperature"]}°C" and card: "{str(disparity["card"])}": "{disparity["disparity"]}°C".')
            print("===============")
            msg_box("Warning",
                   "Execution ended with temperature disparities. Please see console or log for further details.",
                   "warning", False)
        # endregion

        # Fermeture du fichier log
        # region
        sys.stdout.stopLog()
        # endregion

        # [Rerun] Remise en place des variables initiales
        # region
        if rerun != None:
            Températures = tempTemperatures
            Cards = tempCards
            Fields = tempFields
            Speeds = tempSpeeds
        # endregion

    def executionCore(self, dirTemperatures, dirCards, dirCardsPath, execMonitoring, dirFields=None, dirSpeeds=None,
                      dirSpeedsPath=None, climateChamber=None, stableTimeoutBoucles=None, settlingTimeBoucles=None,
                      warningTempExec=None):
        global stabilized
        global settled
        pathOutput = dirCardsPath if (dirFields == None and dirSpeeds == None) else dirSpeedsPath
        if (mode.lower() == "digital suite" and creationBat(pathRunTests, pathMakeReport, pathCpg, (
                os.path.dirname(pathParameters) + r"\AS_Parameters_" + dirFields + "Am_" + dirSpeeds.replace("/",
                                                                                                             "").replace(
                " ", "") + ".xml"), pathReportModel, pathOutput)) or (
                mode.lower() == "analog suite" and creationBat(pathRunTests, pathMakeReport, pathCpg, pathParameters,
                                                               pathReportModel,
                                                               pathOutput)):  # Si la création du fichier d'éxécution est OK, on l'exécute
            if enableClimateChamber:  # SI TEMPÉRATURES AUTO - VERIF ÉTUVE OK
                climateChamber.temperature_set_point = float(dirTemperatures)
                if not climateChamber.is_running:  # Si étuve à l'arrêt, lancement de celle-ci
                    print("Starting climate chamber...")
                    climateChamber.start()
                Temp = 0
                if abs(climateChamber.temperature_set_point - climateChamber.temperature_measured) >= maxTempDiff:  # On vérifie que l'étuve est toujours stabilisée, sinon, on la restabilise
                    stabilized = False
                    settled = False
                while not stabilized:  # Tant que la température n'est pas stabilisée, on attend
                    print(
                        f'Waiting for chamber temperature to stabilize, current temperature: "{climateChamber.temperature_measured:.2f}°C", target temperature: "{climateChamber.temperature_set_point}°C".')
                    if abs(climateChamber.temperature_set_point - climateChamber.temperature_measured) <= maxTempDiff:  # Si valeur mesurée proche de la valeur de consigne à maxTempDiff°C près
                        if Temp >= stableTimeoutBoucles:  # Si la température mesurée est proche de la valeur de consigne à maxTempDiff°C près
                            print("Climate chamber temperature is stabilized.")
                            stabilized = True  # On sort de l'attente de la stabilisation
                        else:
                            print(f"Waiting stable timeout end... ({(stableTimeoutBoucles - Temp) * 30} sec left).")
                            time.sleep(30)  # Attente de 30s
                        Temp += 1  # Incrémentation du compteur
                    else:  # Si valeur mesurée n'est pas proche de la valeur de consigne à maxTempDiff°C près
                        Temp = 0  # Reset du compteur
                        time.sleep(30)  # Attente de 30s
                if not settled:  # Si le composant n'est pas encore "chaud"
                    Temp = 0
                    while Temp < settlingTimeBoucles:
                        print(f"Waiting for the card to settle... ({(settlingTimeBoucles - Temp) * 30} sec left).")
                        time.sleep(30)  # Attente de 30s
                        Temp += 1
                    settled = True
            if mode.lower() != "analog suite":  # [Digital]
                print('===== Started run for temperature: "' + dirTemperatures + '°C", card: "' + str(
                    (dirCards + 1)) + '", speed: "' + dirSpeeds + '" and field: "' + dirFields + 'A/m". =====')
                execMonitoring.updateCurrent((dirTemperatures + "°C"), str((dirCards + 1)), (dirFields + "A/m"),
                                             dirSpeeds)  # Update de la fenêtre de monitoring - +1 à cause du range
            else:  # [Analog]
                print('===== Started run for temperature: "' + dirTemperatures + '°C", card: "' + str(
                    (dirCards + 1)) + '". =====')
                execMonitoring.updateCurrent((dirTemperatures + "°C"), str((dirCards + 1)), "N/A",
                                             "N/A")  # Update de la fenêtre de monitoring - +1 à cause du range
            execMonitoring.update()  # Update de l'affichage de la fenêtre de monitoring
            if enableClimateChamber:  # SI TEMPÉRATURES AUTO - VERIF ÉTUVE OK DURANT PROCESS
                deltaTempExec = []  # On vide l'historique des températures
                process = subprocess.Popen(pathOutput + r"\Exec+Rap.bat", shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)  # Lancement du fichier d'exécution
                threadConsoleLog = threading.Thread(target=consoleLog, args=(process,))
                threadTempMonitor = threading.Thread(target=tempMonitor, args=(climateChamber, process, deltaTempExec,))
                threadConsoleLog.start()  # On démarre le thread de log
                threadTempMonitor.start()  # On démarre le thread de surveillance de la température
                process.wait()  # Attente de la fin de l'exécution
                threadTempMonitor.join()  # Arrêt du thread de surveillance de la température
                threadConsoleLog.join()  # Arrêt du thread de log
                if max(deltaTempExec) > maxTempDiff:  # Vérification de l'historique de surveillance de la température
                    if mode.lower() != "analog suite":  # [Digital]
                        warningTempExec.append(
                            {"temperature": dirTemperatures, "card": (dirCards + 1), "speed": dirSpeeds,
                             "field": dirFields, "disparity": str(
                                "{:.2f}".format(max(deltaTempExec)))})  # On reporte l'écart de température
                    else:  # [Analog]
                        warningTempExec.append({"temperature": dirTemperatures, "card": (dirCards + 1),
                                                "disparity": str("{:.2f}".format(
                                                    max(deltaTempExec)))})  # On reporte l'écart de température
            else:  # SI TEMPÉRATURES MANUELLES
                process = subprocess.Popen(pathOutput + r"\Exec+Rap.bat", shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)  # Lancement du fichier d'exécution
                threadConsoleLog = threading.Thread(target=consoleLog, args=(process,))
                threadConsoleLog.start()  # On démarre le thread de log
                process.wait()  # Attente de la fin de l'exécution
                threadConsoleLog.join()  # Arrêt du thread de log
            if getHTML(pathOutput) != []:
                if mode.lower() != "analog suite":  # [Digital]
                    execMonitoring.updateLast((dirTemperatures + "°C"), str((dirCards + 1)), (dirFields + "A/m"),
                                              dirSpeeds, analyzeHTML(
                            getLatest(getHTML(pathOutput))))  # Update de la fenêtre de monitoring - +1 à cause du range
                else:  # [Analog]
                    execMonitoring.updateLast((dirTemperatures + "°C"), str((dirCards + 1)), "N/A", "N/A", analyzeHTML(
                        getLatest(getHTML(pathOutput))))  # Update de la fenêtre de monitoring - +1 à cause du range
            else:
                if mode.lower() != "analog suite":  # [Digital]
                    execMonitoring.updateLast((dirTemperatures + "°C"), str((dirCards + 1)), (dirFields + "A/m"),
                                              dirSpeeds, {"Number of executed scripts": "/", "Tests passed": "/",
                                                          "Tests failed": "/", "Tests inconclusive": "/",
                                                          "Tests with warning": "/", "Tests not applicable": "/",
                                                          "Tests with environment errors": "/",
                                                          "Tests not executed": "/"})  # Update de la fenêtre de monitoring - +1 à cause du range
                else:  # [Analog]
                    execMonitoring.updateLast((dirTemperatures + "°C"), str((dirCards + 1)), "N/A", "N/A",
                                              {"Number of executed scripts": "/", "Tests passed": "/",
                                               "Tests failed": "/", "Tests inconclusive": "/",
                                               "Tests with warning": "/", "Tests not applicable": "/",
                                               "Tests with environment errors": "/", "Tests not executed": "/"})
            execMonitoring.update()  # Update de l'affichage de la fenêtre de monitoring
            print()  # Correction bug pas d'horodatage
            if mode.lower() != "analog suite":  # [Digital]
                print('===== Ended run for temperature: "' + dirTemperatures + '°C", card: "' + str((
                                                                                                                dirCards + 1)) + '", speed: "' + dirSpeeds + '" and field: "' + dirFields + 'A/m". =====')  # +1 à cause du range
            else:  # [Analog]
                print('===== Ended run for temperature: "' + dirTemperatures + '°C", card: "' + str(
                    (dirCards + 1)) + '". =====')
        else:
            if mode.lower() != "analog suite":  # [Digital]
                print("===== Couldn't start" + ' run for temperature: "' + dirTemperatures + '°C", card: "' + str((
                                                                                                                              dirCards + 1)) + '", speed: "' + dirSpeeds + '" and field: "' + dirFields + 'A/m". =====')  # +1 à cause du range
            else:  # [Analog]
                print("===== Couldn't start" + ' run for temperature: "' + dirTemperatures + '°C", card: "' + str(
                    (dirCards + 1)) + '". =====')

    def generateCSV(self, folder,
                    disparities=[]):  # Fonction de génération de rapport csv /!\ ATTENTION /!\ LE REGENERATE PERD LES INFORMATIONS DE TEMP DISPARITIES
        # Message de start + Récupération des fichiers HTML dans le dossier principal
        # region
        print("Starting report generation.")
        files = getHTML(folder)
        if len(files) == 0:
            print("Warning: No HTML file found!")
            return False
        # endregion

        # Récupération des paramètres des dimensions pour créer la structure de récupération des résultats de test
        # region
        cards = []
        temperatures = []
        fields = []
        speeds = []
        for file in files:
            cardFound = False
            temperatureFound = False
            fieldFound = False
            speedFound = False
            pathParts = file.split(os.path.sep)
            pathParts.reverse()
            for part in pathParts:
                if not cardFound:
                    matchCard = re.search(r'Card(\d+)', part)
                    if matchCard:
                        if int(matchCard.group(1)) not in cards:
                            cards.append(int(matchCard.group(1)))
                        cardFound = True
                if not temperatureFound:
                    try:
                        number = int(part)  # Test du numéro (exception)
                        if part not in temperatures:  # Report du numéro (str)
                            temperatures.append(part)  # Report du numéro (str)
                        temperatureFound = True
                    except ValueError:
                        pass
                if not fieldFound:
                    matchField = re.search(r'(\d+\.\d)Am', part)
                    if matchField:
                        if part not in fields:
                            fields.append(part)
                        fieldFound = True
                if not speedFound:
                    matchSpeed = re.search(r'(\d+)\s*(?:[a-zA-Z]+\s*)?bits?',
                                           part)  # Prend en compte la lettre précédant les bits
                    if matchSpeed:
                        if part.replace("bits", "bit/s") not in speeds:
                            speeds.append(part.replace("bits", "bit/s"))
                        speedFound = True
        if len(cards) == 0:  # Si une seule carte
            print("Warning: No Card folder found!")
            return False
        # endregion

        # Mise en place de la structure de récupération des résultats de test
        # region
        cards.sort()
        temperatures.sort()
        fields.sort()
        speeds.sort()
        results = []
        for temp in temperatures:
            temperatureData = {"temperature": temp, "card": []}
            for card in cards:
                cardData = {"cardNumber": card, "field": []}
                for field in fields:
                    fieldData = {"fieldValue": field.replace("Am", ""), "speed": []}
                    for speed in speeds:
                        speedData = {"speedValue": speed, "date": "", "result": {}}
                        fieldData["speed"].append(speedData)
                    cardData["field"].append(fieldData)
                temperatureData["card"].append(cardData)
            results.append(temperatureData)
        # endregion

        # Récupération des informations dans les fichiers HTML
        # region
        for file in files:
            # Récupération des informations dans le chemin
            # region
            card = None
            temperature = None
            field = None
            speed = None
            date = None
            pathParts = file.split(os.path.sep)
            pathParts.reverse()
            for part in pathParts:
                if not card:
                    matchCard = re.match(r'Card(\d+)', part)
                    if matchCard:
                        card = int(matchCard.group(1))
                if not temperature:
                    try:
                        temperature = int(part)  # Test du nombre (exception)
                        temperature = part  # Report du nombre (str)
                    except ValueError:
                        pass
                if not field:
                    matchField = re.search(r'(\d+\.\d)Am', part)
                    if matchField:
                        field = part.replace("Am", "")
                if not speed:
                    matchSpeed = re.search(r'(\d+)\s*(?:[a-zA-Z]+\s*)?bits?', part)
                    if matchSpeed:
                        speed = part
                if not date:
                    matchDate = re.match(r'\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}', part)
                    if matchDate:
                        date = part
            # endregion

            # Analyse du fichier HTML & ajout du résultat au rapport
            # region
            for i, t in enumerate(results):
                if t["temperature"] == temperature:
                    for j, c in enumerate(t["card"]):
                        if c["cardNumber"] == card:
                            for k, f in enumerate(c["field"]):
                                if f["fieldValue"] == field:
                                    for m, s in enumerate(f["speed"]):
                                        if s["speedValue"] == speed.replace("bits", "bit/s"):
                                            results[i]["card"][j]["field"][k]["speed"][m]["date"] = date
                                            results[i]["card"][j]["field"][k]["speed"][m]["result"] = analyzeHTML(file)
                                            break
            # endregion
        # endregion

        # Report des résultats de test
        # region
        pathASF = folder + "\\AS Files\\"
        if not os.path.exists(pathASF):
            os.makedirs(pathASF)
        pathCSV = pathASF + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S") + f" - {version} - Results.csv"
        with open(pathCSV, "a+") as file:
            file.write(
                "Date;Temperature;Card;Field;Speed;Number of executed scripts;Tests passed;Tests failed;Tests inconclusive;Tests with warning;Tests not applicable;Tests with environment errors;Tests not executed;Tests failed details;Tests with warning details;Temperature disparities;\n")
            for i, t in enumerate(results):
                for j, c in enumerate(t["card"]):
                    for k, f in enumerate(c["field"]):
                        for m, s in enumerate(f["speed"]):
                            try:
                                if len(disparities) > 0:  # S'il y a des disparités
                                    for d in disparities:
                                        if ((t["temperature"] == d["temperature"]) and (
                                                c["cardNumber"] == d["card"]) and (f["fieldValue"] == d["field"]) and (
                                                s["speedValue"] == d["speed"])):
                                            disp = d["disparity"]
                                            break
                                        else:
                                            disp = ""
                                else:
                                    disp = ""
                                if len(results[i]["card"][j]["field"][k]["speed"][m]["result"].values()) != 0:
                                    file.write(
                                        f'{results[i]["card"][j]["field"][k]["speed"][m]["date"]};{t["temperature"]};{c["cardNumber"]};{f["fieldValue"]};{s["speedValue"]};{";".join(results[i]["card"][j]["field"][k]["speed"][m]["result"].values())};{disp};\n')
                                else:
                                    file.write(
                                        f'{results[i]["card"][j]["field"][k]["speed"][m]["date"]};{t["temperature"]};{c["cardNumber"]};{f["fieldValue"]};{s["speedValue"]};;;;;;;;;;;{disp};\n')
                            except:
                                file.write(
                                    f';{t["temperature"]};{c["cardNumber"]};{f["fieldValue"]};{s["speedValue"]}\n')
        if os.path.exists(pathCSV):
            print("Report successfully generated.")
            return True
        else:
            print("Error: Failed to generate report!")
            return False
        # endregion

    def rerunTests(self, folder):  # Fonction permettant de réeffectuer les tests fail ou non conformes
        # Ouverture du rapport csv et récupération des tests à refaire
        # region
        csv = getLatest(getCSV(folder))
        if csv == None:
            print("Warning: No CSV file found!")
            return False
        else:
            reruns = []
            print(f'Rerun will be done using "{os.path.basename(csv)}" as a reference.')
            with open(csv, 'r') as csvFile:
                for lines in csvFile:
                    line = lines.split(";")
                    if ((len(line) <= 6) or (line[5] == "") or any("Too many" in item for item in line) or any(
                            "rerun" in item.lower() for item in line)):
                        reruns.append({"Temperature": line[1], "Card": line[2],
                                       "Field": line[3].replace("Am", "").replace("A/m", ""),
                                       "Speed": line[4].replace("bits", "bit/s").replace("1700 kbit/s",
                                                                                         "1.7 Mbit/s").replace(
                                           "3400 kbit/s", "3.4 Mbit/s").replace("6800 kbit/s",
                                                                                "6.8 Mbit/s")})  # [Legacy] bits => bit/s pour les logs pré v1.4.X (pas de replace dans le generateCSV et le analyzeHTML) & "Am"/"A/m" pour les logs pré v1.4.X & 8.02-8.04 speed formatting
        # endregion

        # Lancement des reruns
        # region
        if reruns != []:
            self.btn_rerunTests.configure(state="disabled")
            self.btn_Launch.configure(state="disabled")
            self.iconify()
            self.execution(reruns)
            self.deiconify()
            self.btn_Launch.configure(state="normal")
            self.btn_rerunTests.configure(state="normal")
            return True
        else:
            print("Warning: No test to rerun!")
            msg_box("Warning", "No test to rerun!", "warning", False)
            return False
        # endregion
