from selenium.webdriver.common.by import By
from main_func import driver_selenium, load_cookie
from bs4 import BeautifulSoup as bs
import requests
import time


def group_by_label(driver):
    driver.find_element(
        By.ID, 'dropdownMenuClickableInside').click()
    time.sleep(1)
    driver.find_element(By.ID, 'labelCheck').click()
    time.sleep(1)


def open_group_filters(driver):
    filters = driver.find_element(By.CLASS_NAME, 'ag-side-button').click()
    time.sleep(1)
    labels = driver.find_elements(
        By.CLASS_NAME, 'ag-filter-toolpanel-group-wrapper')[5].click()
    time.sleep(1)


def create_list_text_group(driver):
    # ? Очень полезный способ искать элементы на странице
    group_divtext_list = driver.find_elements(
        By.XPATH, '//div[@class="ag-set-filter-item-checkbox ag-labeled ag-label-align-right ag-checkbox ag-input-field"]/div[1]')

    group_text_list = [x.text for x in group_divtext_list]

    return group_text_list


def click_select_all(driver):
    checkbox = driver.find_element(
            By.XPATH, f'/html[1]/body[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/div[2]/div[2]/div[6]/div[1]/div[3]/div[1]/div[2]/div[1]/form[1]/div[1]/div[1]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/input[1]')
    checkbox.click()
    time.sleep(0.2)
    
def sort_label(driver):
    driver.find_element(
        By.XPATH, '//div[@class="ag-column-drop-wrapper"]/div[1]/div[2]/span').click()
    time.sleep(0.2)


def open_tasks(driver):
    driver.find_element(By.ID, 'dropdownMenuReference').click()
    time.sleep(1)
    
    
def refresh_proxy():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }

    response = requests.get('http://176.106.53.179:8051/restart/42090/Fvsd45', headers=headers, verify=False)
    
    if response.status_code == 400:
        time.sleep(55)
        return refresh_proxy()

def take_label(driver, start: str, end: str):
    group_text_list = create_list_text_group(driver)

    start_index, end_index = group_text_list.index(
        start), group_text_list.index(end)
    task_list = group_text_list[start_index:end_index+1]

    for task in task_list:
        index_xpath = group_text_list.index(task)
        checkbox = driver.find_element(
            By.XPATH, f'//div[@class="ag-virtual-list-container ag-filter-virtual-list-container"]/div[{index_xpath+1}]/div[1]/div[1]/div[2]/input[1]')
        # полезный скрипт, для прокрутки до элемента
        driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", checkbox)
        time.sleep(0.3)
        try:
            checkbox.click()
            time.sleep(0.2)
        except:
            driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", checkbox)
            time.sleep(1)
            checkbox.click()
            time.sleep(0.2)
        
        
        tree = driver.find_element(
            By.XPATH, f'//div[@class="ag-full-width-container"]/div/span/span[1]/span')
        driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", tree)
        time.sleep(0.5)
        try:
            tree.click()
            time.sleep(0.2)
        except:
            driver.execute_script("arguments[0].scrollIntoViewIfNeeded(true);", tree)
            time.sleep(1)
            tree.click()
            time.sleep(0.2)

    return len(task_list)


def check_finish(driver):
    try:
        log = driver.find_element(By.ID, 'quill_log').find_element(
            By.TAG_NAME, 'div').find_elements(By.TAG_NAME, 'p')
        log_text = [x.text for x in log]
        if '[-] Task finished' not in log_text:
            time.sleep(10)
            check_finish(driver)
    except:
        time.sleep(10)
        check_finish(driver)


def check_first_loading(driver):
    loading = driver.find_element(
        By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]/div[7]')
    class_loading = loading.get_attribute('class')
    if class_loading == 'ag-overlay':
        time.sleep(10)
        check_first_loading(driver)


def check_accounts(driver, start: str = '', end: str = ''):
    driver.get('https://nooklz.com/profiles')
    check_first_loading(driver)

    group_by_label(driver)

    open_group_filters(driver)
    click_select_all(driver)
    sort_label(driver)
    amount_groups = take_label(driver, start, end)
    

    for i in range(1, amount_groups+1):
        refresh_proxy()
        chekbox_task = driver.find_element(
            By.XPATH, f'//div[@class="ag-full-width-container"]/div[{i}]/span/span[3]/div/div/div[2]/input')
        chekbox_task.click()
        time.sleep(0.2)

        open_tasks(driver)
        driver.find_element(By.ID, 'check-m-cookies').click()
        time.sleep(20)
        
        check_finish(driver)
        # прокрутка страницы максимально вверх
        driver.execute_script("window.scrollTo(0, 0);")
        chekbox_task2 = driver.find_element(
            By.XPATH, f'//div[@class="ag-full-width-container"]/div[{i}]/span/span[3]/div/div/div[2]/input')
        time.sleep(2)
        chekbox_task2.click()


def main():
    try:
        start = input(
            'Введите название группы, с которой начнётся работа с аккаунтами: ')
        end = input(
            'Введите название группы, на которой закончится работа с аккаунтами: ')
        driver = driver_selenium()
        driver.maximize_window()
        driver.get('https://nooklz.com/')
        time.sleep(1)
        load_cookie(driver, 'nooklz')

        check_accounts(driver, start, end)

    except Exception as ex:
        with open(r'E:\OSPanel\domains\my_life\ad_fb\nooklz\log_nooklz_error.txt', 'w') as f:
            f.write(str(ex))
    else:
        print('[INFO] Ошибок нет')
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
