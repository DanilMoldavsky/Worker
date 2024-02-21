from selenium.webdriver.common.by import By
from main_func import driver_selenium, load_cookie
from check_accs import (check_first_loading, group_by_label, open_group_filters, click_select_all,
                        take_label, sort_label, open_tasks, refresh_proxy, check_finish)
import pyperclip as clipboard
import time


def copy_clipboard(string):
    clipboard.copy(string)


def check_errors(driver):
    log = driver.find_element(By.ID, 'quill_log').find_element(
        By.TAG_NAME, 'div').find_elements(By.TAG_NAME, 'p')
    log_color = [x.find_element(By.TAG_NAME, 'strong').get_attribute(
        'style').replace('color: ', '').replace(';', '') for x in log]
    log_error_color = [x for x in log_color if x == 'red']

    return log_error_color


def create_pages(driver, start: str, end: str, fp: int):
    driver.get('https://nooklz.com/profiles')
    check_first_loading(driver)

    group_by_label(driver)

    open_group_filters(driver)
    click_select_all(driver)
    sort_label(driver)
    amount_groups = take_label(driver, start, end)
    

    errors = 0
    while fp > 0:
        for i in range(1, amount_groups+1):
            refresh_proxy()
            time.sleep(2)
            chekbox_task = driver.find_element(
                By.XPATH, f'//div[@class="ag-full-width-container"]/div[{i}]/span/span[3]/div/div/div[2]/input')
            chekbox_task.click()
            time.sleep(0.2)

            open_tasks(driver)

            driver.find_element(By.ID, 'create-page').click()
            time.sleep(2)

            driver.find_element(By.ID, 'random-page-names').click()
            time.sleep(0.3)
            startpagetask = driver.find_element(
                By.ID, 'startPageTask')
            startpagetask.click()

            check_finish(driver)
            errors += len(check_errors(driver))
            # прокрутка страницы максимально вверх
            driver.execute_script("window.scrollTo(0, 0);")
            chekbox_task2 = driver.find_element(
                By.XPATH, f'//div[@class="ag-full-width-container"]/div[{i}]/span/span[3]/div/div/div[2]/input')
            time.sleep(2)
            chekbox_task2.click()
        fp -= 1

    help_string = f'Количество ошибок при создании фп: {errors}'
    copy_clipboard(help_string)
    print('[INFO] Количество ошибок при создании фп: ', errors)



def main():
    try:
        start = input(
            'Введите название группы, с которой начнётся работа с аккаунтами: ')
        end = input(
            'Введите название группы, на которой закончится работа с аккаунтами: ')
        fp = int(input('Введите количество фп: '))
        driver = driver_selenium()
        driver.maximize_window()
        driver.get('https://nooklz.com/')
        time.sleep(1)
        load_cookie(driver, 'nooklz')
        create_pages(driver, start, end, fp)

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
