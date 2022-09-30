import undetected_chromedriver as uc
from fake_useragent import UserAgent


def create_Driver():
    options = uc.ChromeOptions()
    options.headless = True
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('disable-extensions')
    options.add_argument("disable-default-apps")
    options.add_argument('disable-component-extensions-with-background-pages')
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--window-size=1920,1080")
    driver = uc.Chrome(executable_path="D:\Python-Development\Projects\Free-Up-Scrapper\chromedriver.exe",
                       options=options)
    return driver
