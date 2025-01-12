try:
    import consoleVer
    import boLogger
    import customtkinter as ctk
except ImportError as e:
    print("Please install the required modules (GUI ver)")
    print(e)
    exit(1)
finally:
    logger = boLogger.Logging()
    logger.success("Imported all modules (GUI ver)")


class ConsoleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YT pfp and banner yoinker by Bernso")
        self.geometry("500x210")
        self.resizable(False, False)
        self.option_add("*Font", "Arial 12")
        options = {'padx': 10, "pady": 10}

        
        # Elements
        self.label = ctk.CTkLabel(self, text="Welcome to the YT Yoinker!", font=("Arial", 36))
        self.label.grid(column = 0, row = 0, columnspan=3, **options)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter the username...", width=250)
        self.entry.grid(column = 0, row = 1, columnspan=2, **options)

        self.pfp_check = ctk.CTkCheckBox(self, text="Profile Picture")
        self.pfp_check.grid(column = 0, row = 2, **options)
        
        self.banner_check = ctk.CTkCheckBox(self, text="Banner")
        self.banner_check.grid(column = 1, row = 2, **options)
        
        self.page_check = ctk.CTkCheckBox(self, text="Page Source")
        self.page_check.grid(column = 2, row = 2, **options)
        
        self.button = ctk.CTkButton(self, text="Start", command=self.on_submit)
        self.button.grid(column = 0, row = 3, **options)

    def on_submit(self):
        username = self.entry.get()
        pfp = bool(self.pfp_check.get())
        banner = bool(self.banner_check.get())
        page = bool(self.page_check.get())
        
        logger.info(f"Username: {username}")
        logger.info(f"Profile Picture: {pfp}")
        logger.info(f"Banner: {banner}")
        logger.info(f"Page Source: {page}")

        yoinker = consoleVer.PfpYoink(username)
        yoinker.save_files(pfp=pfp, banner=banner, page=page)


if __name__ == "__main__":
    app = ConsoleApp()
    app.mainloop()
