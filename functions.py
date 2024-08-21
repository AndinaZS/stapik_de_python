import matplotlib.pyplot as plt
import csv
import os

'''
Блок для получения списка продаж из заданного файла с 
простой проверкой наличия файла в рабочей директории и проверкой формата строк.
'''


def read_sales_data(file_path):
    if chek_path(file_path):
        match file_path[-4:]:
            case '.csv':
                return read_csv_data(file_path)
            case '.txt':
                return read_txt_data(file_path)
    print("Файл не найден")
    return []


def chek_path(file_path):
    return os.path.isfile(f"./{file_path}")


def read_csv_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        res = get_data(csv.reader(file))
    return res


def read_txt_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        res = get_data(file)
    return res


def get_data(file):
    res_lst = []
    counter = 1
    for line in file:
        check_line = check_file_string(line)
        match check_line:
            case None:
                print(f'Строка {counter} задана некорректно. Пропускаем.')
            case _:
                res_lst.append(check_line)
        counter += 1
    return res_lst


def check_file_string(line):
    keys = ('product_name', 'quantity', 'price', 'date')
    line_new = [_.strip() for _ in line] if isinstance(line, list) else [_.strip() for _ in line.split(',')]
    chech = sum([(len(line_new) == 4), line_new[1].isnumeric(), line_new[2].isnumeric()])
    if chech == 3:
        line_new[1] = int(line_new[1])
        line_new[2] = int(line_new[2])
        return dict(zip(keys, line_new))
    else:
        return None


'''Блок для получения общей суммы продаж в запрошенных разрезах (дата, продукт) '''


def get_sales(sales_data, key_):
    res = {}
    for dct in sales_data:
        res[dct[key_]] = res.get(dct[key_], 0) + dct['quantity'] * dct['price']
    return res


def total_sales_per_product(sales_data):
    return get_sales(sales_data, 'product_name')


def sales_over_time(sales_data):
    return get_sales(sales_data, 'date')


'''Блок для расчета и вывода информации по максимальным показателям и отображения графиков'''


def get_max_values(values_dict):
    return max(values_dict, key=values_dict.get)


def plot_result(values_per_data, values_per_product):
    sorted_list_data = sorted(values_per_data.items())
    x1, y1 = zip(*sorted_list_data)

    sorted_list_products = sorted(values_per_product.items())
    x2, y2 = zip(*sorted_list_products)

    plt.subplot(2, 2, 1)
    plt.plot(x2, y2)
    plt.title("График продаж по продуктам")
    plt.text(0.5, 1.2, f"Наибольшую выручку нам принесли {get_max_values(values_per_product)}.", fontsize=12)

    # Две строки, два столбца. Текущая ячейка - 3
    plt.subplot(2, 2, 2)
    plt.plot(x1, y1)
    plt.title("График продаж по дням")
    plt.text(0.5, 1.2, f"Самый результативный день по выручке {get_max_values(values_per_data)}.", fontsize=12)

    plt.show()
    return None


def get_result(file_path):
    sales_data = read_sales_data(file_path)
    if sales_data:
        values_per_product = total_sales_per_product(sales_data)
        values_per_data = sales_over_time(sales_data)
        plot_result(values_per_data, values_per_product)
    return None
