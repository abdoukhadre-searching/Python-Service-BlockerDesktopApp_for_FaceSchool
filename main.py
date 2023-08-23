import customtkinter
from PIL import Image, ImageTk
import speedtest
import psutil
from CTkMessagebox import CTkMessagebox
from winotify import Notification, audio
from tkinter import messagebox
from tkinter import Label

# librairies for websiteBlocker strategy
import sys
import ctypes
from python_hosts import Hosts, HostsEntry
import os
import platform
from pathlib import Path
from websiteEnum import Websites


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, text, image=None):
        label = customtkinter.CTkLabel(
            self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, text=text, width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list),
                   column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        screen_width = self.winfo_screenwidth()
        screen_heigh = self.winfo_screenheight()

        app_w = 860
        app_h = 600

        x = (screen_width / 2) - (app_w / 2)
        y = (screen_heigh / 2) - (app_h / 2)

        self.title("Face School Agent.py")
        self.geometry(f'{app_w}x{app_h}+{int(x)}+{int(y)}')
        self.resizable(False, False)

        # Process for admin privileges
        try:
            self.ret = self.run_as_admin()
        except:
            pass

        try:
            if self.ret is True:
                print('I have admin privilege.')
                # raw_input('Press ENTER to exit.')
            elif self.ret is None:
                print('I am elevating to admin privilege.')
                # raw_input('Press ENTER to exit.')
                if platform.system() == 'Windows':
                    self.myetcFilePath = Path(
                        os.environ['DRIVERDATA']).parent / 'etc/hosts'
                    print(self.myetcFilePath)
                elif platform.system() == 'Linux':
                    self.myetcFilePath = Path('/etc/hosts')
                self.hosts = Hosts(path=self.myetcFilePath)
                new_entry = HostsEntry(entry_type='ipv4', address='127.0.0.1', names=[
                                       Websites.FACE_SCHOOL_ALIAS.value, Websites.FACE_SCHOOL.value])
                # we initially add the link for our plateform into the host file for blocking them
                # when the app is initialize
                self.hosts.add([new_entry])
                self.hosts.write()
                print("Host file updated ! website entry add")
            else:
                print('Error (self.ret=%d): cannot elevate privilege.' %
                      (self.ret, ))
        except:
            pass

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "images")
        # print("image_path --- ", image_path)
        self.logo_image = customtkinter.CTkImage(
            Image.open("./images/logo3.png"), size=(160, 160))
       # self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(
            Image.open("verifier.png"), size=(40, 40))
        self.home_image = customtkinter.CTkImage(light_image=Image.open("verifier.png"),
                                                 dark_image=Image.open("verifier.png"), size=(40, 40))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open("check.png"),
                                                 dark_image=Image.open("check.png"), size=(40, 40))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open("chat_light.png"),
                                                     dark_image=Image.open("chat_light.png"), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, image=self.logo_image, text="",
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=0, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, font=customtkinter.CTkFont(size=15, weight="bold"), corner_radius=0, height=40, border_spacing=10, text="Que fait notre agent ? ",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, font=customtkinter.CTkFont(size=15, weight="bold"), corner_radius=0, height=40, border_spacing=10, text="Analyser",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("lightblue", "green"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        # self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
        #                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        #                                               image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        # self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["light", "dark", "system"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(
            row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(
            self, width=500, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(1, weight=1)
        self.home_frame.rowconfigure(1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(
            self.home_frame, text="")  # , image=self.large_test_image)
        self.home_frame_large_image_label.grid(
            row=0, column=0, padx=20, pady=10)
        # create textbox in my pretty home frame
        self.textbox = customtkinter.CTkTextbox(
            self.home_frame, width=580, height=540, font=customtkinter.CTkFont(size=19, weight="normal"),)
        self.textbox.place(x=20, y=20)  # sticky="nsew"
        self.textbox.insert("0.0", "Documentation sur l'Agent 🟢 🕶 \n\n" +
                            "Nous sommes fiers de vous présenter notre nouvel agent de surveillance avancé, conçu pour assurer la sécurité, l'intégrité et l'équité de notre plateforme d'examen en ligne. Cet agent fonctionne en arrière-plan sur votre ordinateur, surveillant en temps réel les applications en cours d'exécution. " +

                            "L'objectif principal de cet agent est de garantir un environnement d'examen sûr et conforme à nos normes strictes. En plus de surveiller les applications, cet agent fournit une surveillance étendue grâce à notre système de proctoring intégré." +

                            "Le proctoring est une technologie qui permet de surveiller les sessions d'examen en ligne de manière sécurisée et équitable. \n\nGrâce à notre agent de surveillance avancé, nous sommes en mesure de détecter et de prévenir toute activité suspecte ou non autorisée pendant les examens. Cela inclut la détection des comportements frauduleux tels que la tricherie, l'utilisation de ressources non autorisées ou la présence de tiers non autorisés pendant l'examen. " +

                            "Notre agent de surveillance fonctionne de manière discrète et efficace, en analysant les applications en cours d'exécution pour détecter les violations potentielles de nos politiques d'examen. En cas de détection d'une activité non conforme, des mesures appropriées sont prises pour préserver l'intégrité de l'examen et garantir des résultats justes et fiables. " +

                            "Nous comprenons l'importance de la confiance dans le processus d'examen et nous nous engageons à fournir un environnement sécurisé pour tous les candidats. Grâce à notre agent de surveillance et à notre système de proctoring avancé, nous veillons à ce que chaque examen soit surveillé de manière efficace, permettant ainsi de garantir la validité des résultats et de préserver la valeur de vos qualifications." +

                            "Nous sommes à votre disposition pour répondre à toutes vos questions concernant notre agent de surveillance, notre système de proctoring ou toute autre demande liée à notre plateforme d'examen en ligne. Votre satisfaction et votre réussite sont notre priorité absolue, et nous sommes déterminés à vous offrir une expérience d'examen sécurisée et équitable.")

        # create second frame
        self.second_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(1, weight=1)
        self.second_frame.rowconfigure(1)

        self.btn_lancer_analyse = customtkinter.CTkButton(self.second_frame, font=(
            "Ubuntu", 18), hover_color="green", text="Lancer l'analyse", command=self.show_info, height=30)
        self.btn_lancer_analyse.grid(row=2, column=1, padx=20, pady=10)

        # create second frame for displaying app icons
        self.app_frame = customtkinter.CTkFrame(
            self.second_frame, corner_radius=8, height=330, width=450)
        self.app_frame.place(x=20, y=255)

        self.label_title = customtkinter.CTkLabel(
            self.app_frame,
            text="En cours...",
            anchor="w",
            compound="left", font=customtkinter.CTkFont(size=19, weight="bold"),
            justify="left",
            text_color="white",
            bg_color="transparent"
        )
        self.label_title.pack()

        # img = Image.open("./images/success.png")
        # rez = img.resize((100, 100), Image.Resampling.LANCZOS)
        # img_success = ImageTk.PhotoImage(rez)
        # self.label_success = Label(
        #     self.second_frame, background="#2b2b2b", image=img_success)
        # # self.label_success.place(x=300, y=510)
        # self.label_success.pack(fill="x", expand=1, side="left", pady=20)
        # ----var---

        self.file = open("ids.txt")
        self.ids = []
        global list_app_suspect
        self.list_app_suspect = []
        self.rest_apps = []
        self.images_apps = []
        img_success = ""

        # select default frame
        self.select_frame_by_name("acceuil")  # acceuil

        # self.label_vitesse_connexion = customtkinter.CTkLabel(self.home_frame, text="Chargement en cours...", compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        # self.label_vitesse_connexion.grid(row=3, column=0, padx=20, pady=10)

        # create scrollable label and button frame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(
            master=self.second_frame, width=500, command=self.label_button_frame_event, corner_radius=0)
        self.scrollable_label_button_frame.grid(
            row=1, column=1, padx=0, pady=0, sticky="nsew")
        for p in psutil.process_iter():  # add items with images
            self.scrollable_label_button_frame.add_item(
                f"{p.name()}", text="en cours...📌", image=customtkinter.CTkImage(Image.open("software-development.png")))

        # declarer une liste d'aplication suspect par exemple
        # global list_app_suspect
        # self.list_app_suspect = ["vlc.exe", "notepad.exe", "idea64.exe"]

    def run_as_admin(self, argv=None, debug=False):

        unicode = str

        shell32 = ctypes.windll.shell32
        if argv is None and shell32.IsUserAnAdmin():
            return True

        if argv is None:
            argv = sys.argv
        if hasattr(sys, '_MEIPASS'):
            # Support pyinstaller wrapped program.
            arguments = map(unicode, argv[1:])
        else:
            arguments = map(unicode, argv)
        argument_line = u' '.join(arguments)
        executable = unicode(sys.executable)
        if debug:
            print('Command line: ', executable, argument_line)
        ret = shell32.ShellExecuteW(
            None, u"runas", executable, argument_line, None, 1)
        if int(ret) <= 32:
            return False
        return None

    def get_notifiation(self):
        notification = Notification(
            app_id="Agent Face School v1",
            title="Lien vers notre plateforme pour démarrer votre examen",
            msg="Bonjour chere candidat apres l'analyse des application cliquez ci-dessous pour poursuivre.\n\nBonne chance à vous",
            duration="long",
        )
        notification.set_audio(audio.SMS, loop=True)
        notification.add_actions(
            label="🚀 Cliquez ici 🟢👉🏽 ", launch="https://face-school-protoring-v1.vercel.app/")
        notification.show()
        self.label_title.configure(
            text_color='green', text="Vous pouvez poursuivre")

    def show_goToFaceSchool_byLink(self):
        msg = messagebox.showinfo(
            message="Excellent 😎 ! Vous etes maintenant pret pour votre examen \nDites Merci à notre Agent 2.0 😉 \n\n Accéder à votre plateforme")
        if msg:  # "Accéder à la plateforme":
            # get link to our plateforme
            print("get the link to faceSchool")
            self.get_notifiation()

    def show_warning_app(self, numberOfApp):
        # Show some retry/cancel warnings
        msg = messagebox.showwarning(title="Alerte de sécurité !", message=f"Notre agent a détecté  {numberOfApp}  applications lancée sur votre machine et qui sont potentiellement suspects pour le bon déroulement de votre exament sur la plateforme\n \n Apuyyer sur OUI pour que notre agents s'occupe de leur extinction   ",
                                     icon="warning")

        # msg = CTkMessagebox(title="Alerte de securité !", message=f"Notre agent a détecté  {numberOfApp}  applications lancée sur votre machine et qui sont potentiellement suspects pour le bon déroulement de votre exament sur la plateforme\n \n Veuiller la fermer pour poursuivre   ",
        #             icon="warning", option_1="Poursuivre", option_2="Réessayer",  option_3="On s'en charge")
        # if msg == 'ok' :
        if numberOfApp != 0:
            # on devrait s'asure de maintenir le site inacessible d'abord: --> on next sprint may be
            # -------- on tue ces process suspects
            for application in self.list_app_suspect:
                try:
                    # while application == 'chrome.exe':
                    #     self.kill_by_process_name(application)
                    self.kill_by_process_name(application)
                except:
                    pass
                #   on le retire de la liste des applis
                self.list_app_suspect.remove(application)
                print(self.list_app_suspect)
                cnt = 0
                for app in self.list_app_suspect:
                    if self.check_process_exist_by_name(app):
                        cnt += 1
                        if app in self.list_app_suspect:  # si cette app a une icone dons nos assets
                            pass
            self.show_warning_app(cnt)
        else:
            self.show_goToFaceSchool_byLink()
            # on retire l'acces a notre plateforme pour cette machine -> host file winSys32 path
            # we remove all matching endpoint 🚀
            self.hosts.remove_all_matching(name=Websites.FACE_SCHOOL.value)
            self.hosts.remove_all_matching(
                name=Websites.FACE_SCHOOL_ALIAS.value)
            self.hosts.write()
            print('..host files reset to normal : website available 🟢')

    def show_info(self):
        msg = messagebox.showinfo(
            title="Agent", message="Notre agent va lancer l'analyse en quelques secondes")
        if msg:
            cnt = 0
            for line in self.file:
                line = line.rstrip("\n")
                line = line.split('-')
                self.ids.append(line[0])
                self.list_app_suspect.append(line[1])
            print(self.ids, self.list_app_suspect)

            for app in self.list_app_suspect:
                if self.check_process_exist_by_name(app):
                    cnt += 1
                    print(app, "app is in")
                print("total applis suspecte :", cnt)

        self.label_title.configure(
            text_color='red', text="  🚨 Applications suspectées par vos instructeurs")
        self.btn_lancer_analyse.configure(state='disabled')

        for i in range(len(self.list_app_suspect)):
            self.ids.append(i+1)
            # Resize the Image using resize method
            img = Image.open(f"./images/icones/{self.ids[i]}.png")
            resized_image = img.resize((100, 100), Image.Resampling.LANCZOS)
            self.images_apps.append(ImageTk.PhotoImage(resized_image))

            lbl = Label(self.app_frame, background="#2b2b2b",
                        image=self.images_apps[-1], width=100, height=100)
            lbl.pack(fill="x", expand=1, side="left", pady=20)

        self.show_warning_app(cnt)

    def check_process_exist_by_name(self, name):
        for proc in psutil.process_iter():
            if proc.name() == name:
                return True
        return False

    def kill_by_process_name(self, nameAppInterdite):
        for proc in psutil.process_iter():
            if proc.name() == nameAppInterdite:
                # print("Killing process: " + name)
                if (self.check_process_exist_by_name(nameAppInterdite)):
                    os.system("taskkill /f /pid "+str(proc.pid))
                    print("Killing process: " + nameAppInterdite + " sucess 😉")

                    for i in range(27):
                        # while proc.name() == 'chrome.exe':
                        os.system("taskkill /f /im chrome.exe")

                else:
                    print("Killing process: " + nameAppInterdite + " failed")
                return
        print("Not found process: " + nameAppInterdite)

    def label_button_frame_event(self, item):
        print(f"label button frame clicked: {item}")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        # self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "acceuil":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            pass
            # self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        # if name == "frame_3":
        #     pass #self.third_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     pass #self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
