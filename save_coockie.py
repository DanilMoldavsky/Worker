from main import driver_selenium, save_cookie
import time

def main():
    driver = driver_selenium()
    driver.get('https://nooklz.com/')
    time.sleep(40)
    save_cookie(driver, 'nooklz')
    
if __name__ == '__main__':
    main()