from dashboard.models import Product, Valuation, Undelivered, Badstock, Count
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

def product_manager_dashboard(request):
    try:
        products = Product.objects.all().order_by('description')
        product_skus = products.values_list('product_sku', flat=True)
        missing_valuations = Valuation.objects.exclude(product_sku__in=product_skus)
        missing_counts = Count.objects.exclude(product_sku__in=product_skus)
        missing_undelivered = Undelivered.objects.exclude(product_sku__in=product_skus)

        context = {'products_list': products,
                    'missing_valuations': missing_valuations,
                    'missing_counts': missing_counts,
                    'missing_undelivered': missing_undelivered,
        }
        return render(request, 'product_manager_dashboard.html', context)
    except Exception as e:
        return render(request, 'product_manager_dashboard.html', {'error_message': str(e)})

def update_file(request):
    try:
        if request.method == 'POST':
            if request.POST.get('xcode') == '641525':
                product_details_file = request.FILES.get('fileProductDetails')
                valuation_file = request.FILES.get('fileValuation')
                undelivered_file = request.FILES.get('fileUndelivered')
                count_file = request.FILES.get('fileCount')

                created_product_count = 0
                updated_product_count = 0
                deleted_count_entry = 0
                newly_added_count_entry = 0
                deleted_valuation_entry = 0
                newly_added_valuation_entry = 0
                deleted_undelivered_entry = 0
                newly_added_undelivered_entry = 0
                updated_product = []
                context = None
                result = None

                if product_details_file:
                    result = process_excel_file_for_product_details(product_details_file)
                    created_product_count = result['created_product_count']
                    updated_product_count = result['updated_product_count']
                    updated_product = result['updated_product']

                if valuation_file:
                    result = process_excel_file_for_valuation(valuation_file)
                    deleted_valuation_entry = result['deleted_valuation_entry']
                    newly_added_valuation_entry = result['newly_added_valuation_entry']

                if count_file:
                    result = process_excel_file_for_count(count_file)
                    deleted_count_entry = result['deleted_count_entry']
                    newly_added_count_entry = result['newly_added_count_entry']

                if undelivered_file:
                    result = process_excel_file_for_undelivered(undelivered_file)
                    deleted_undelivered_entry = result['deleted_undelivered_entry']
                    newly_added_undelivered_entry = result['newly_added_undelivered_entry']

            else:
                return HttpResponse("Access Denied")
        else:
            return HttpResponse("Submit data through POST only.")

        products = Product.objects.all().order_by('description')
        context = {
            'products_list': products,
            'created_product_count': created_product_count,
            'updated_product_count': updated_product_count,
            'deleted_count_entry': deleted_count_entry,
            'newly_added_count_entry': newly_added_count_entry,
            'deleted_valuation_entry': deleted_valuation_entry,
            'newly_added_valuation_entry': newly_added_valuation_entry,
            'deleted_undelivered_entry': deleted_undelivered_entry,
            'newly_added_undelivered_entry': newly_added_undelivered_entry,
            'updated_product': updated_product,
        }
        return render(request, 'product_manager_dashboard.html', context)
    except Exception as e:
        return render(request, 'product_manager_dashboard.html', {'error_message': str(e)})

def process_excel_file_for_product_details(uploaded_file):
    print('. . .Start of Updating Product. . .')
    created_product_count = 0
    updated_product = set()
    product_sku = ''

    df = pd.read_excel(uploaded_file, engine='xlrd')

    for index, row in df.iterrows():
        product_sku = str(row['Stock Code'])
        print(f'Excel Stockcode form: {product_sku}')
        existing_product = Product.objects.filter(product_sku=product_sku).first()

        if existing_product:
            description = str(row['Description'])
            qtyperpcs = int(row['ConversionFactor'])
            bccs = str(row['BCCS'])
            bcib = str(row['BCIB'])
            bcpcs = str(row['BCPCS'])

            if(
                existing_product.description != description or
                existing_product.qtyperpcs != qtyperpcs or
                existing_product.bccs != bccs or
                existing_product.bcib != bcib or
                existing_product.bcpcs != bcpcs
            ):
                if( existing_product.description != description ):
                    existing_product.description = description
                    updated_product.add(existing_product)
                if( existing_product.qtyperpcs != qtyperpcs ):
                    existing_product.qtyperpcs = qtyperpcs
                    updated_product.add(existing_product)
                if( (existing_product.bccs != bccs) and (bccs not in [None,'','nan']) ):
                    existing_product.bccs = bccs
                    updated_product.add(existing_product)
                if( existing_product.bcib != bcib and (bcib not in [None,'','nan']) ):
                    existing_product.bcib = bcib
                    updated_product.add(existing_product)
                if( existing_product.bcpcs != bcpcs and (bcpcs not in [None,'','nan']) ):
                    existing_product.bcpcs = bcpcs
                    updated_product.add(existing_product)

                existing_product.save()
        else:
            if (is_valid_stock_code(product_sku)):
                Product.objects.create(
                    product_sku=product_sku,
                    description=row['Description'],
                    qtyperpcs=row['ConversionFactor'],
                    bccs = row['BCCS'],
                    bcib = row['BCIB'],
                    bcpcs = row['BCPCS'])
                created_product_count += 1
    return {'created_product_count': created_product_count, 'updated_product_count': len(updated_product), 'updated_product': updated_product}


def process_excel_file_for_valuation(uploaded_file):
    deleted_valuation_entry = 0
    newly_added_valuation_entry = 0
    deleted_valuation_entry = Valuation.objects.all().delete()[0]

    df = pd.read_excel(uploaded_file)
    for index, row in df.iterrows():
        if (
            is_valid_stock_code(str(row['StockCode']))
        ):
            Valuation.objects.create(
                product_sku=row['StockCode'],
                cs=row['CS'],
                ib=row['IB'],
                pcs=row['PCS']
            )
            newly_added_valuation_entry += 1
    return {'deleted_valuation_entry': deleted_valuation_entry, 'newly_added_valuation_entry': newly_added_valuation_entry}


def process_excel_file_for_count(uploaded_file):
    deleted_count_entry = 0
    newly_added_count_entry = 0
    deleted_count_entry = Count.objects.all().delete()[0]


    dtype_spec = {'StockCode': str}
   #df = pd.read_excel(uploaded_file)
    df = pd.read_excel(uploaded_file, dtype=dtype_spec)
   #df.fillna('', inplace=True)

    for index, row in df.iterrows():
        if (
            is_valid_stock_code(str(row['StockCode']))
        ):
            Count.objects.create(
                product_sku=row['StockCode'],
                cs=row['CS'],
                ib=row['IB'],
                pcs=row['PCS']
            )
            newly_added_count_entry += 1
    return {'deleted_count_entry': deleted_count_entry, 'newly_added_count_entry': newly_added_count_entry}

def process_excel_file_for_undelivered(uploaded_file):
    deleted_undelivered_entry = 0
    newly_added_undelivered_entry = 0
    deleted_undelivered_entry = Undelivered.objects.all().delete()[0]

    df = pd.read_excel(uploaded_file)
    for index, row in df.iterrows():
        if (
            is_valid_stock_code(str(row['StockCode']))
        ):
            Undelivered.objects.create(
                product_sku=row['StockCode'],
                cs=row['CS'],
                ib=row['IB'],
                pcs=row['PCS']
            )
            newly_added_undelivered_entry += 1
    return {'deleted_undelivered_entry': deleted_undelivered_entry, 'newly_added_undelivered_entry': newly_added_undelivered_entry}

def is_valid_stock_code(stock_code):
    valu_of_validation = (((5 <= len(stock_code)) <= 9) and all(char in '0123456789F' for char in stock_code))
    print(f'Validating Stockcode: {stock_code} => {valu_of_validation}')
    return valu_of_validation

def export_poduct_details(request):
    queryset = Product.objects.all()
    data = pd.DataFrame(list(queryset.values()))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=product_data.xlsx'
    data.to_excel(response, index=False)
    return response

def export_recon(request):
    product_queryset = Product.objects.all()
    res = []

    for p in product_queryset:
        bscs = 0
        bsib = 0
        bspcs = 0
        udcs = 0
        udib = 0
        udpcs = 0
        valcs = 0
        valib = 0
        valpcs = 0
        cntcs = 0
        cntib = 0
        cntpcs = 0

        bs = Badstock.objects.filter(product_sku=p.product_sku).first()
        ud = Undelivered.objects.filter(product_sku=p.product_sku).first()
        val = Valuation.objects.filter(product_sku=p.product_sku).first()
        cnt = Count.objects.filter(product_sku=p.product_sku).first()

        if bs:
            bscs=bs.cs
            bsib=bs.ib
            bspcs=bs.pcs
        if ud:
            udcs=ud.cs
            udib=ud.ib
            udpcs=ud.pcs
        if val:
            valcs=val.cs
            valib=val.ib
            valpcs=val.pcs
        if cnt:
            cntcs=cnt.cs
            cntib=cnt.ib
            cntpcs=cnt.pcs

        include_bo = True
        if include_bo:
            result = {
                'product_sku': p.product_sku,
                'description': p.description,
                'rescs': (valcs + udcs - cntcs) * -1,
                'resib': (valib + udib - cntib) * -1,
                'respcs': (valpcs + udpcs - cntpcs) * -1,
            }
        else:
            result = {
                'product_sku': p.product_sku,
                'description': p.description,
                'rescs': (valcs + udcs - bscs - cntcs) * -1,
                'resib': (valib + udib - bsib - cntib) * -1,
                'respcs': (valpcs + udpcs - bspcs - cntpcs) * -1,
            }


        if (result['rescs'] + result['resib'] + result['respcs']) != 0:
            res.append(result)

    data = pd.DataFrame(res)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=product_data.xlsx'
    data.to_excel(response, index=False)
    return response




