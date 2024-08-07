from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

# Create your views here.
def app_view(request):
    return render(request,'frontend/app/index.html', context=None)

@xframe_options_exempt
def shopify_view(request):
    return render(request,'frontend/shopify/index.html', context=None)