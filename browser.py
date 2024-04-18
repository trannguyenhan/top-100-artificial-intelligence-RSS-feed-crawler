import undetected_chromedriver as uc

# init browser
# add proxy 
# add config
def get_browser(version_main = 119, user_agent = None, window_size = None):
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    
    if user_agent is not None:
        options.add_argument(f'--user-agent={user_agent}')

    if window_size is not None:
        options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(version_main=version_main, options=options)
    return driver