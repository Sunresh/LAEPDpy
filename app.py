import customtkinter as ctk

class Application(ctk.CTk):
    def __init__(self, appname="Deposition Controller", *args, **kwargs):
        super().__init__()
        self.btn_list = ['Start Deposition', 'Stop Deposition']
        self.btn_command = [self.start_deposition, self.stop_deposition]
        self.appname = appname
        self.title(self.appname)
        self.geometry("500x700")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)

        self.create_label()
        self.create_buttons()
        self.create_log_textbox()

    def create_label(self):
        """Creates a label to display the application name."""
        label = ctk.CTkLabel(self.main_frame, text=self.appname, font=("Arial", 16, "bold"))
        label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

    def create_buttons(self):
        """Creates buttons for deposition control."""
        for i in range(len(self.btn_list)):
            self.create_button(self.btn_list[i], self.btn_command[i], i + 1)

    def create_button(self, text, command, row):
        """Creates a button and adds it to the main frame."""
        button = ctk.CTkButton(self.main_frame, text=text, command=command)
        button.grid(row=row, column=0, padx=20, pady=(0, 10), sticky="ew")

    def create_log_textbox(self):
        """Creates a text box for logging messages."""
        self.log_text = ctk.CTkTextbox(self.main_frame, height=100)
        self.log_text.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.log_message("Application started")

    def log_message(self, message):
        """Logs a message to the text box."""
        self.log_text.insert(ctk.END, message + "\n")
        self.log_text.see(ctk.END)  # Auto-scroll to the bottom

    def start_deposition(self):
        """Logic for starting deposition."""
        self.log_message("Starting deposition...")

    def stop_deposition(self):
        """Logic for stopping deposition."""
        self.log_message("Stopping deposition...")

if __name__ == "__main__":
    app = Application(appname="Deposition Controller")
    app.mainloop()
