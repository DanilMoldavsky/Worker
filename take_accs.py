from selenium.webdriver.common.by import By
from datetime import date
from main import driver_selenium, load_cookie
import pandas as pd
import glob
import time

PROXY_ID = "71790"

#todo сделать динамическое имя пользователя
def combine_csv():
    list_csv = []
    list_csv.extend(glob.glob('C:\\Users\\Arbitrazh\\Downloads\\***.csv'))
    df = pd.concat([pd.read_csv(f) for f in list_csv], ignore_index=True)
    sorted_df = df.sort_values('group', key=lambda x: x.str.split('.').str[-1].astype(int))
    sorted_df.to_csv("C:\\Users\\Arbitrazh\\Downloads\\result.csv", index=False)


def read_accs_ids():
    lines = []
    with open('E:\\OSPanel\\domains\\my_life\\ad_fb\\accs_ids_crm.txt', 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


def write_list_to_file(lines: list = []):
    with open('E:\\OSPanel\\domains\\my_life\\ad_fb\\accs_ids_crm.txt', 'w') as file:
        for line in lines:
            file.write(line + '\n')


def upload_octa(driver):

    driver.find_element(By.CLASS_NAME, 'ts-control').click()
    time.sleep(1)

    upload_button = driver.find_element(
        By.CLASS_NAME, 'ts-dropdown-content').find_elements(By.TAG_NAME, 'div')[1]
    upload_button.click()
    time.sleep(1)

    driver.find_element(
        By.CSS_SELECTOR, '#post-form > fieldset > div > div.form-group.mb-0 > button').click()
    time.sleep(1)
    driver.find_element(
        By.CSS_SELECTOR, '#confirm-dialog > div > div > div.modal-footer > div > button').click()
    time.sleep(20)


def download_xls(driver, group_num: str = "1", accs_quantity: int = 1):
    today = date.today().strftime("%d.%m")
    if accs_quantity == 100:
        group_name = today + " 100." + group_num
    else:
        group_name = today + "." + group_num

    export_button = driver.find_element(
        By.CLASS_NAME, 'form-group').find_element(By.TAG_NAME, 'button')
    driver.execute_script("arguments[0].scrollIntoView(true);", export_button)
    time.sleep(3)
    export_button.click()
    time.sleep(1)
    group_input = driver.find_element(By.NAME, 'group')
    group_input.clear()
    group_input.send_keys(group_name)
    time.sleep(1)

    proxy_input = driver.find_element(By.NAME, 'proxy')
    proxy_input.clear()
    proxy_input.send_keys(PROXY_ID)
    time.sleep(1)
    # убираем чек бокс check_updates
    driver.find_element(
        By.CLASS_NAME, 'form-check').find_element(By.NAME, 'check_updates').click()
    time.sleep(1)
    # кликаем выгрузить
    driver.find_element(By.ID, 'submit-modal-exportNooklz').click()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'btn-close').click()
    time.sleep(1)

    upload_octa(driver)


def take_accounts(driver, url_page: str = "1", packs_quantity: int = 1, accs_quantity: int = 1, group_num: int = 1):

    try:
        url = 'https://crm.clickengine.net/admin/buyer/accs-fb?page=' + url_page

        driver.get(url)
        time.sleep(2)

        ids_list = read_accs_ids()
        acc_count = 0
        ostatok = accs_quantity
        while packs_quantity > 0:

            for i in range(100, 0, -1):

                is_octa_fill = driver.find_element(
                    By.XPATH, f'//tbody/tr[{i}]/td[7]/div[1]//*[name()="svg"]').get_attribute("fill")
                acc_id = driver.find_element(
                    By.XPATH, f'/html/body/div[1]/div[1]/div[2]/div/div/div/form/div[2]/div/table/tbody/tr[{i}]/td[1]/div').text.strip()

                if is_octa_fill == "red" and acc_id not in ids_list:
                    checkbox = driver.find_element(
                        By.XPATH, f'/html/body/div[1]/div[1]/div[2]/div/div/div/form/div[2]/div/table/tbody/tr[{i}]/td[10]/div/div/div/div/input')
                    try:
                        checkbox.click()
                        time.sleep(0.35)
                        acc_count += 1
                        ids_list.append(acc_id)
                    except:
                        driver.execute_script(
                            "arguments[0].click();", checkbox)
                        time.sleep(0.35)
                        acc_count += 1
                        ids_list.append(acc_id)

                if acc_count == ostatok:

                    packs_quantity -= 1
                    acc_count = 0
                    ostatok = accs_quantity
                    download_xls(driver, str(group_num), accs_quantity=accs_quantity)
                    group_num += 1
                    break
            if acc_count < accs_quantity and i == 1:
                if acc_count > 0:
                    download_xls(driver, str(group_num), accs_quantity=accs_quantity)
                    ostatok = accs_quantity - acc_count

                acc_count = 0
                url_page = str(int(url_page) - 1)
                url = 'https://crm.clickengine.net/admin/buyer/accs-fb?page=' + url_page
                driver.get(url)
                time.sleep(2)

    except Exception as ex:
        print('[INFO] Ошибка при сборке аккаунтов')
        with open('E:\\OSPanel\\domains\\my_life\\ad_fb\\log_take_accounts.txt', 'w') as f:
            f.write(str(ex))
    else:
        print('[INFO] Ошибок нет')
    finally:
        write_list_to_file(ids_list)
        print("Сборка аккаунтов закончена")


def main():
    try:
        url_page = input(
            'Введите номер страницы, с которой начинается сборка аккаунтов: ')
        accs_quantity = int(input('Введите количество аккаунтов в пачке: '))
        packs_quantity = int(input('Введите количество пачек аккаунтов: '))
        group_num = int(
            input("Введите номер группы, c которого пойдет отсчет: "))

        driver = driver_selenium()
        driver.maximize_window()
        driver.get('https://crm.clickengine.net/admin/main')
        time.sleep(1)
        load_cookie(driver, 'CRM')
        take_accounts(driver, url_page=url_page,
                      packs_quantity=packs_quantity, accs_quantity=accs_quantity, group_num=group_num)

        combine_csv()

    except Exception as ex:
        with open('E:\\OSPanel\\domains\\my_life\\ad_fb\\log_crm_error.txt', 'w') as f:
            f.write(str(ex))
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    main()
