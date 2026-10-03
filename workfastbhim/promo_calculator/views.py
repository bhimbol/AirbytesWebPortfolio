from django.shortcuts import render
from dashboard.models import Promo, Product, PromoProduct
from django.http import HttpResponse

def promo_calculator_dashboard(request):
    promos = Promo.objects.all()
    return render(request, 'promo_calculator_dashboard.html', {'promos': promos})

def calculate(request):
    if request.method == 'POST':
        try:
            promo_code = request.POST.get('promo', 0)
            num_of_deals = int(request.POST.get('num_of_deals', 0))
            result_list = []
            qty_pcs = 0
            qty_cs = 0

            promo_products = PromoProduct.objects.filter(promo__promo_sku=promo_code)

            for pp in promo_products:
                conv_factor = pp.product.qtyperpcs
                qty_pcs = (pp.promo.mech_per_pcs * num_of_deals) % conv_factor
                qty_cs = (((pp.promo.mech_per_pcs * num_of_deals) - qty_pcs) / conv_factor)
                qty_pcs = "" if qty_pcs == 0 else qty_pcs
                qty_cs = "" if qty_cs == 0 else qty_cs
                result_list.append({
                    'product': pp.product,
                    'qty_cs': qty_cs,
                    'qty_pcs': qty_pcs,
                })

            context = {
                'num_of_deals': num_of_deals,
                'result_list': result_list,
                'promos': Promo.objects.all(),
            }
            return render(request, 'promo_calculator_dashboard.html', context)
        except Product.DoesNotExist:
            return HttpResponse("Promo Product not found.")
        except Exception as e:
            return HttpResponse(e)














'''

def calculate(request):
    result_list = []
    promo_parent_description = None
    num_of_deals = 0

    #try:
    if request.method == 'POST':
        promo_code = request.POST.get('promo', 0)
        promo_parent_product = Product.objects.get(sku=promo_code)
        promo_parent_description = promo_parent_product.description if promo_parent_product else None
        prods = promo_parent_product
        promo_child_products = Promo.objects.filter(sku=promo_code)
        num_of_deals = int(request.POST.get('num_of_deals', 0))

        for promo_child in promo_child_products:
            promo_child_sku = promo_child.child_sku
            promo_child_product = get_object_or_404(Product, sku=promo_child_sku)
            promo_child_product_description = promo_child_product.description if promo_child_product else None
            conv_factor = promo_child_product.qtyperpcs if promo_child_product else 1

            qty_pcs = (promo_child.mech_per_pcs * num_of_deals) % conv_factor
            qty_cs = (((promo_child.mech_per_pcs * num_of_deals) - qty_pcs) / conv_factor)

            qty_pcs = "" if qty_pcs == 0 else qty_pcs
            qty_cs = "" if qty_cs == 0 else qty_cs

            result_list.append({
                'child_sku': promo_child_sku,
                'mech_per_pcs': promo_child.mech_per_pcs,
                'description': promo_child_product_description,
                'conv_factor': conv_factor,
                'qty_cs': qty_cs,
                'qty_pcs': qty_pcs
            })

    context = {
        'promo_parent_description': promo_parent_description,
        'num_of_deals': num_of_deals,
        'result_list': result_list,
    }
    promos = Promo.objects.all()
    return render(request, 'promo_calculator_dashboard.html', {'promos': promos, 'prods':prods}, context)
    #except KeyError as e:
    #    return HttpResponse(f"KeyError: {e}")
    #except Exception as e:
    #    return HttpResponse(f"An Exception occurred: {e}")
'''