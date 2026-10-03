from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
from dashboard.models import Product
from django.http import HttpResponse
import pandas as pd

def comments(request):
    comments_list = Comment.objects.all()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comments')
    return render(request, 'comment.html', {'comments_list': comments_list, 'form': form})

def export_product_to_excel():
    queryset = Product.objects.all()
    data = pd.DataFrame(list(queryset.values()))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=product_data.xlsx'
    data.to_excel(response, index=False)
    return response

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def update_product(request):
    try:
        sku = request.GET.get('sku')
        product = get_object_or_404(Product, sku=sku)

        new_description = request.GET.get('description')
        new_qtyperpcs = int(request.GET.get('qtyperpcs'))
        new_bccs = request.GET.get('bccs')
        new_bcib = request.GET.get('bcib')
        new_bcpcs = request.GET.get('bcpcs')

        # Update product attributes
        product.description = new_description
        product.qtyperpcs = new_qtyperpcs
        product.bccs = new_bccs
        product.bcib = new_bcib
        product.bcpcs = new_bcpcs

        # Save changes
        product.save()

        return JsonResponse({'message': 'Product updated successfully'})

    except ValueError as e:
        return JsonResponse({'error': f'Invalid value: {e}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Something went wrong: {e}'}, status=500)

def execute_command(request):
    response = update_product(request)
    return response

