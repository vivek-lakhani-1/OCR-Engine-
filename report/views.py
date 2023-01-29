from django.shortcuts import render

def reportpage(request):
    return render(request,'report.html')