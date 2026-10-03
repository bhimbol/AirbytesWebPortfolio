from django.shortcuts import render
#from django.http import HttpResponse

def image_processor_dashboard(request):
    return render(request, 'image_processor_dashboard.html', )