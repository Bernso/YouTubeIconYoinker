try:
    import bs4
    import boLogger
    import requests
    import os
    from tkinter import messagebox
    from selenium.webdriver.chrome.service import Service
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError as e:
    print("Please install the required modules (console ver)")
    print(e)
    exit(1)
finally:
    logger = boLogger.Logging()
    logger.success("Imported all modules (console ver)")


class PfpYoink:
    def __init__(self, channel=''):
        if channel == '':
            logger.warning("Channel not specified, deafulting to '@bernso2547'")
            channel = 'bernso2547'
            
        self.url = None
        self.soup = None
        self.driver = None
        self.username = channel
        self.pfp_path = 'yt-core-image yt-spec-avatar-shape__image yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image--content-mode-scale-to-fill yt-core-image--loaded'
        self.banner_path = 'yt-core-image yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded'
        self.links = []
        
        os.makedirs(os.path.join(os.getcwd(),'Files'), exist_ok=True)
        os.makedirs(os.path.join(os.getcwd(), 'Files', f'{self.username}'), exist_ok=True)
        
        self.__venv_init()
    
    def __str__(self):
        return f"""
                This is a banner, profile picture and page source yoinker.
                Arguments: Channel username: str (default: 'bernso2547', the current username is {self.username})
                Methods: save_files(pfp=True, banner=True, page=True)
                """

    
    def __create_url(self):
        if not self.username.startswith('http://'):
            channel = f"https://www.youtube.com/@{self.username}"
        self.url = channel
        logger.info(f"Link created: {channel}")
        os.makedirs(os.path.join(os.getcwd(), 'Files', f'{self.username}'), exist_ok=True)

    def __venv_init(self):
        if self.driver == None:
            logger.info("Initializing selenium")
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--mute-audio")
                service = Service()
                self.driver = webdriver.Chrome(service=service, options=options)
                logger.success("Selenium initialized")
            except Exception as e:
                logger.error(f"Error initializing selenium: {e}")
        else:
            logger.warning("venv already initialized")
            return
    
    def __fetch_channel_page(self):
        logger.info("Fetching channel page...")
        self.driver.get(self.url)

        if self.driver.title == "Before you continue to YouTube":
            try:
                # Updated locator using `By.CLASS_NAME`
                logger.info("Detected re-direct, handling...")
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Accept all')]"))
                )
                button.click()

                logger.success("Redirect handled")
            except Exception as e:
                logger.error(f"Error fetching channel page: {e}")
                self.driver.quit()
                self.driver = None

        try:
            # Wait for a specific element that indicates the page has fully loaded
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f"//img[@class='{self.pfp_path}']"))
            )
            logger.success("Page fully loaded")
        except Exception as e:
            logger.error(f"Error waiting for page load: {e}")
            self.driver.quit()
            self.driver = None
            return
        
        self.soup = bs4.BeautifulSoup(self.driver.page_source, 'html.parser')
        logger.success("Page fetched and parsed")


    def __save_channel_page(self):
        def temp():
            logger.info("Creating channel page file...")
                    
            with open(path, 'w', encoding='utf-8') as file:
                file.write(self.soup.prettify())
                logger.success("Channel page saved successfully")
                file.close()
                logger.info(f"Channel file closed and saved to: {path}")
        
        if self.soup != None:
            path = os.path.join(os.getcwd(), 'Files', f"{self.username}", f'channel_page.html')
            if not os.path.exists(path):
                temp()
            else:
                logger.info("Asking if overwrite channel page...")
                choice = messagebox.askquestion("File already exists", "Would you like to overwrite it?")
                logger.info(f"User choice: {choice}")
                if choice.lower() == 'yes':
                    temp()
                else:
                    return
                
        else:
            logger.error("Please run fetch_channel_page() before trying to save the page")
    
    
    def __find_pfp(self):
        if self.soup != None:
            try:
                potential = self.soup.find('img', class_=self.pfp_path)
                
                if potential != None:
                    pfp = potential['src']
                    logger.info(f"Found images: {potential['src']}")
                    self.links.append(pfp)
                else:
                    logger.error("No images found")
            except Exception as e:
                logger.error(f"Error finding images: {e}")
                
        else:
            logger.error("Please run fetch_channel_page() before trying to save the page")

    def __find_banner(self):
        if self.soup != None:
            try:
                potential = self.soup.find('img', class_=self.banner_path)
                
                if potential != None:
                    banner = potential['src']
                    logger.info(f"Found images: {potential['src']}")
                    self.links.append(banner)
                else:
                    logger.error("No images found")
            except Exception as e:
                logger.error(f"Error finding images: {e}")
                
        else:
            logger.error("Please run fetch_channel_page() before trying to save the page")


    def __save_images(self):
        if len(self.links) > 0:
            logger.info("Downloading images...")
            for link in self.links:
                try:
                    response = requests.get(link, stream=True)
                    response.raise_for_status()
                    if '-no-rj' in link:
                        filename = f"pfp.jpg"
                    else:
                        filename = f"banner.jpg"
                    path = os.path.join(os.getcwd(), 'Files', f'{self.username}', filename)
                    with open(path, 'wb') as file:
                        for block in response.iter_content(1024):
                            if block:
                                file.write(block)
                    logger.success(f"Image saved at: {path}")
                    
                except Exception as e:
                    logger.error(f"Error downloading images: {e}")
                    return
        else:
            logger.error("No images found to download")
        
    def save_files(self, pfp=True, banner=True, page=True):
        self.__create_url()
        self.__fetch_channel_page()
        
        if pfp:
            self.__find_pfp()
        if banner:
            self.__find_banner()
        if page:
            self.__save_channel_page()
        
        self.__save_images()
    
    


if __name__ == '__main__':
    yoinker = PfpYoink("MrBeast")
    print(yoinker)
    yoinker.save_files()