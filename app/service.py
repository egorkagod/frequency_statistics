import aiofiles
import re
import uuid
import pymorphy3
from openpyxl import Workbook


async def count_frequency_stat(filepath: str):
    pattern = r"[aA-яЯ|aA-zZ]+"
    result = dict() # {"житель": [3, 2, 1, 1, 1], ...}
    async with aiofiles.open(filepath, "r") as f:
        morph = pymorphy3.MorphAnalyzer()
        cnt = 0
        while (row := await f.readline()) != "":
            cnt += 1
            words = re.findall(pattern, row)
            for word in words:
                word = morph.parse(word.lower())[0].normal_form
                word_data = result.setdefault(word, [0] * (cnt + 1))
                word_data[0] += 1
                if len(word_data) < cnt + 1:
                    word_data = _add_zeros(word_data, cnt + 1 - len(word_data))
                word_data[cnt] += 1
                result[word] = word_data

        for word in result.keys():
            result[word] = _add_zeros(result[word], cnt + 1 - len(result[word]))

    return _make_report(result)

def _add_zeros(data: list[int], length: int) -> list[int]:
    data.extend([0] * length)
    return data 

def _make_report(result: dict) -> str:
    wb = Workbook(write_only=True)
    ws = wb.create_sheet("Частотная характеристика")
    
    for word in result.keys():
        ws.append([word, result[word][0], ', '.join(list(map(str, result[word][1:])))])

    report_path = f"files/reports/Отчет-{uuid.uuid4()}.xlsx"
    wb.save(report_path)
    return report_path