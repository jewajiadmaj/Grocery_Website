from django.shortcuts import render
from .models import Category
# Create your views here.
def index(request):
    category = Category.objects.all()
    paras={'category':category}
    return render(request, 'index.html',paras)