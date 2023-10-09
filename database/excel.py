import openpyxl
from openpyxl.styles import Font, Alignment

from loader import db

def create_excel(filename) -> str:
    # Список данных
    data_list = db.get_report_list_for_excel()

    # Создаем новую книгу Excel и выбираем активный лист
    wb = openpyxl.Workbook()
    ws = wb.active

    # Задаем шрифт и выравнивание для заголовков
    title_font = Font(bold=True)
    alignment = Alignment(horizontal='center')

    # Заголовки для столбцов
    headers = [
        "ДАТА", "ИМЯ", "ОБР ЗАПРОСЫ", "ВЫСТ СЧЕТА",
        "ОПЛ СЧЕТА", "МАРЖА", "ВЫРУЧКА", "КОНВ ЗАПР В СЧЁТ",
        "КОНВ СЧЕТ В ОПЛ", "ПРОЦЕНТ НАЦЕНКИ"
    ]

    # Устанавливаем заголовки и форматирование
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = title_font
        cell.alignment = alignment

    # Заполняем данные
    for row_num, row_data in enumerate(data_list, 2):
        for col_num, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_num, column=col_num, value=value)
            # Выравнивание по центру для всех ячеек
            cell.alignment = alignment

    file = f'folder_to_reports/{filename}'
    # Сохраняем Excel-файл
    wb.save(filename=file)
    return file
