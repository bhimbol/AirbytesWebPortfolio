from django.shortcuts import render
import pandas as pd
from django.contrib import messages
from django import forms
from .models import Invoice
from datetime import datetime
from django.db import transaction

EXPECTED_COLUMNS = {
    "Salesman": str,
    "Customer": str,
    "Customer Name": str,
    "Invoice Amount": float,
    "Invoice Date": "datetime",
    "Dispatch Date": "datetime_or_none",
    "Delivery Date": "datetime_or_none",
    "Remarks / Justification": str,
}

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select a file')



def validate_excel(file_path):
    try:
        df = pd.read_excel(file_path, skiprows=4)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    for column, expected_type in EXPECTED_COLUMNS.items():
        if column not in df.columns:
            continue

        if expected_type == "datetime":
            try:
                df[column] = pd.to_datetime(df[column], errors="coerce")
                if df[column].isnull().any():
                    raise ValueError(
                        f"Invalid or missing date format in column '{column}'. Problematic rows: {df[df[column].isnull()].index.tolist()}"
                    )
            except Exception as e:
                raise ValueError(f"Error converting column '{column}' to datetime: {e}")

        elif expected_type == "datetime_or_none":
            try:
                df[column] = pd.to_datetime(df[column], errors="coerce")
                # Allow None (NaT) values but raise errors for invalid non-blank entries
                invalid_rows = df[pd.to_datetime(df[column], errors="coerce").isnull() & df[column].notnull()]
                if not invalid_rows.empty:
                    raise ValueError(
                        f"Invalid date format in column '{column}'. Problematic rows: {invalid_rows.index.tolist()}"
                    )
            except Exception as e:
                raise ValueError(f"Error converting column '{column}' to datetime: {e}")

        else:
            if column == "Remarks / Justification":
                df[column].fillna("N/A", inplace=True)
            elif df[column].isnull().any():
                raise ValueError(f"Column '{column}' contains missing values.")

            if not df[column].apply(lambda x: isinstance(x, expected_type) or pd.isnull(x)).all():
                raise ValueError(f"Invalid data type in column: {column}")

    print("Excel file validation passed!")
    return df


def PushNewInvoices(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                validated_df = validate_excel(file)
                with transaction.atomic():
                    for _, row in validated_df.iterrows():
                        Invoice.objects.update_or_create(
                            number=row['Invoice #'],
                            defaults={
                                'si': row.get('SI', ''),  # Handle missing 'SI'
                                'date': row['Invoice Date'] if pd.notnull(row['Invoice Date']) else None,
                                'amount': float(row['Invoice Amount']) if pd.notnull(row['Invoice Amount']) else 0.0,
                                'customer_number': str(row['Customer']),
                                'customer_name': str(row['Customer Name']),
                                'dispatch_date': row['Dispatch Date'] if pd.notnull(row['Dispatch Date']) else None,
                                'delivery_date': row['Delivery Date'] if pd.notnull(row['Delivery Date']) else None,
                                'remarks': str(row['Remarks / Justification']) if pd.notnull(row['Remarks / Justification']) else '',
                                'accountable': row.get('Accountable', ''),
                                's_code': row.get('S Code', ''),
                            }
                        )
                messages.success(request, "Invoices processed successfully!")
            except ValueError as e:
                messages.error(request, f"Validation Error: {e}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = UploadFileForm()

    invoices = Invoice.objects.all()
    context = {
        'form': form,
        'invoices': invoices,
        'invoice_count': invoices.count(),
    }
    return render(request, 'delivery_monitoring_dashboard.html', context)


def DeliveryPlanning(request):
    pending_invoices = Invoice.objects.filter(
        dispatch_date__isnull=True
    ).exclude(
        customer_name='WALK-IN ACCOUNT (BOOKING)'
    ).filter(
        s_code__in=["N08", "N05"]
    )
    context = {
        'pending_invoices': pending_invoices,
    }
    return render(request, 'delivery_planning.html', context)

def create_plan(request):
    invoices_to_process = None
    pending_invoices = Invoice.objects.filter(
        dispatch_date__isnull=True
    ).exclude(
        customer_name='WALK-IN ACCOUNT (BOOKING)'
    ).filter(
        s_code__in=["N08", "N05"]
    )

    if request.method == 'POST':
        selected_invoices = request.POST.getlist('invoices')
        invoices_to_process = Invoice.objects.filter(number__in=selected_invoices)

    context = {
        'pending_invoices': pending_invoices,
        'invoices_to_process': invoices_to_process
    }
    return render(request, 'delivery_planning.html', context)


def delivery_monitoring_dashboard(request):
    PushNewInvoices(request)
    form = UploadFileForm()
    invoices = Invoice.objects.all()
    context = {
        'form': form,
        'invoices': invoices,
        'invoice_count': invoices.count(),
    }
    return render(request, 'delivery_monitoring_dashboard.html', context)
