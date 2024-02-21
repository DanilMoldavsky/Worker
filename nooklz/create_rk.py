from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from main_func import driver_selenium, load_cookie
from check_accs import check_first_loading, group_by_label, open_tasks, refresh_proxy, check_finish, create_list_text_group
import pyperclip as clipboard
import time


def click_select_all_bms(driver):
    checkbox = driver.find_element(
            By.XPATH, f'//div[@class="ag-virtual-list-container ag-filter-virtual-list-container"]/div[1]/div/div/div[2]/input')
    checkbox.click()
    time.sleep(0.2)


def sort_label_bms(driver):
    driver.find_element(
        By.XPATH, '//div[@class="ag-column-drop-wrapper"]/div[1]/div[2]/span').click()
    time.sleep(0.2)


def open_group_filters_bms(driver):
    filters = driver.find_element(By.CLASS_NAME, 'ag-side-button').click()
    time.sleep(1)
    labels = driver.find_elements(
        By.CLASS_NAME, 'ag-filter-toolpanel-group-wrapper')[4].click()
    time.sleep(1)


def take_label_bms(driver, start: str, end: str):
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


def create_rk(driver, start: str, end: str):
    TIME_ZONE = 'EUROPE_MINSK'
    CURRENCY = 'EUR'
    
    driver.get('https://nooklz.com/bms')
    check_first_loading(driver)

    group_by_label(driver)

    open_group_filters_bms(driver)
    click_select_all_bms(driver)
    amount_groups = take_label_bms(driver, start, end)
    # sort_label_bms(driver)
    
    
    
    # for i in range(1, amount_groups+1):
    for i in range(1, amount_groups):
        refresh_proxy()
        chekbox_task = driver.find_element(
            By.XPATH, f'//div[@class="ag-full-width-container"]/div[{i}]/span/span[3]/div/div/div[2]/input')
        chekbox_task.click()
        time.sleep(0.2)

        open_tasks(driver)

        driver.find_element(By.ID, 'create-bm-ad-account').click()
        time.sleep(2)

        driver.find_element(By.ID, 'randomName').click()
        time.sleep(0.3)
        
        if i == 1:
            driver.find_element(By.ID, 'select2-timezone_select-container').click()
            time.sleep(0.3)
            driver.find_element(By.CLASS_NAME, 'select2-search__field').send_keys(f'{TIME_ZONE}')
            time.sleep(0.3)
            driver.find_element(By.XPATH, f'//li[text()="{TIME_ZONE}"]').click()
            time.sleep(0.3)
            
            driver.find_element(By.ID, 'select2-currency_select-container').click()
            time.sleep(0.3)
            driver.find_element(By.CLASS_NAME, 'select2-search__field').send_keys(f'{CURRENCY}')
            time.sleep(0.3)
            driver.find_element(By.XPATH, f'//li[text()="{CURRENCY}"]').click()
            time.sleep(0.3)
        else:
            driver.find_element(By.ID, 'select2-timezone_select-container').click()
            time.sleep(0.3)
            driver.find_element(By.CLASS_NAME, 'select2-search__field').send_keys('EUROPE_MONACO')
            time.sleep(0.3)
            driver.find_element(By.XPATH, '//li[text()="EUROPE_MONACO"]').click()
            time.sleep(0.3)
            driver.find_element(By.ID, 'select2-timezone_select-container').click()
            time.sleep(0.3)
            driver.find_element(By.CLASS_NAME, 'select2-search__field').send_keys(f'{TIME_ZONE}')
            time.sleep(0.3)
            driver.find_element(By.XPATH, f'//li[text()="{TIME_ZONE}"]').click()
            time.sleep(0.3)
            
            driver.find_element(By.ID, 'select2-currency_select-container').click()
            time.sleep(0.3)
            driver.find_element(By.CLASS_NAME, 'select2-search__field').send_keys('FJD')
            time.sleep(0.3)
            driver.find_element(By.XPATH, '//li[text()="FJD"]').click()
            time.sleep(0.3)
            driver.find_element(By.ID, 'select2-currency_select-container').click()
            time.sleep(0.3)
            driver.find_element(By.CLASS_NAME, 'select2-search__field').send_keys(f'{CURRENCY}')
            time.sleep(0.3)
            driver.find_element(By.XPATH, f'//li[text()="{CURRENCY}"]').click()
            time.sleep(0.3)

        # print('клик на дискард')
        # driver.find_element(By.XPATH, '//*[@id="createActModal"]/div/div/div[3]/button[1]').click()
        # time.sleep(2)
        
        startpagetask = driver.find_element(
            By.ID, 'startCreateActTask')
        startpagetask.click()

        check_finish(driver)

        # прокрутка страницы максимально вверх
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1.5)
        chekbox_task2 = driver.find_element(
            By.XPATH, f'//div[@class="ag-full-width-container"]/div[{i}]/span/span[3]/div/div/div[2]/input')
        time.sleep(0.5)
        chekbox_task2.click()


def main():
    try:
        start = input(
            'Введите название группы, с которой начнётся работа с аккаунтами: ')
        end = input(
            'Введите название группы, на которой закончится работа с аккаунтами: ')
        # start = '08.11.1'
        # end = '08.11.5'


        driver = driver_selenium()
        driver.maximize_window()
        driver.get('https://nooklz.com/')
        time.sleep(1)
        load_cookie(driver, 'nooklz')
        create_rk(driver, start, end)

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
