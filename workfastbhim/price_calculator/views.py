import os
from django.conf import settings
from django.shortcuts import render
from openpyxl import load_workbook


def price_calculator_dashboard(request):
    existing_file_name = 'formulas.xlsx'
    existing_file_path = os.path.join(settings.BASE_DIR, 'common_files', existing_file_name)

    try:
        workbook = load_workbook(existing_file_path)
        sheet = workbook['data']
        headers = [cell.value for cell in sheet[1]]
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = {headers[i]: value for i, value in enumerate(row)}
            data.append(row_data)

        return render(request, 'price_calculator_dashboard.html', {
            'headers': headers,
            'items': data,
        })

    except FileNotFoundError:
        return render(request, 'price_calculator_dashboard.html', {
            'error': f"The file '{existing_file_name}' does not exist in the specified location.",
        })
    except KeyError:
        return render(request, 'price_calculator_dashboard.html', {
            'error': "The sheet 'Sheet2' does not exist in the Excel file.",
        })
    except Exception as e:
        return render(request, 'price_calculator_dashboard.html', {
            'error': f"An unexpected error occurred: {str(e)}",
        })
