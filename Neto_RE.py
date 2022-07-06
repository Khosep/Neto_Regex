import re
import csv
from pprint import pprint


def get_list_from_csv(file):
    with open(file, encoding='utf-8') as f:
        datareader = csv.reader(f, delimiter=",")
        contacts = []
        for row in datareader:
            if datareader.line_num == 1:
                columns_number = len(row)
            contacts.append(row[:columns_number])
        return contacts


def fix_name_fields(contacts):
    for i in range(1, len(contacts)):
        place = sum(bool(item) for item in contacts[i][:3])  # какое поле для ФИО последнее непустое
        if place != 3:
            res = re.split(r'\s+', contacts[i][place - 1])  # разбиваем по пробелам
            start = place - 1
            end = start + len(res)
            contacts[i][place - 1:end] = res  # разносим по столбцам Ф+И+О
    return contacts


def fix_phone_numbers(contacts):
    pattern = r'^(8|\+7)?' \
              r'\s?\(?' \
              r'(\d{3})' \
              r'\)?[\s|-]?' \
              r'(\d{3})\)?' \
              r'-?(\d{2})' \
              r'-?(\d{2})' \
              r'\s?\(?' \
              r'(доб.)?' \
              r'\s?(\d{4})?' \
              r'\)?$'
    repl = r'+7(\2)\3-\4-\5 \6\7'
    for i in range(1, len(contacts)):
        if contacts[i][5]:
            contacts[i][5] = re.sub(pattern, repl, contacts[i][5]).strip()
    return contacts


def delete_duplicate(contacts):
    position = {}
    len_r = len(contacts)
    i = 1
    while i < len_r:
        name = ' '.join(contacts[i][:2])
        if name in position:
            pos = position[name]
            for j in range(2, len((contacts[i]))):
                contacts[pos][j] = contacts[pos][j] or contacts[i][j]
            contacts.pop(i)
            len_r -= 1
        else:
            position[name] = i
            i += 1
    return contacts


def write_list_to_csv(file, contacts):
    with open(file, "w", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts)


if __name__ == '__main__':
    contacts = get_list_from_csv('phonebook_raw.csv')
    contacts = fix_name_fields(contacts)
    contacts = fix_phone_numbers(contacts)
    contacts = delete_duplicate(contacts)
    pprint(contacts)
    write_list_to_csv('phonebook.csv', contacts)
