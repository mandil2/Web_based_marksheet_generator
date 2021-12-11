from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import csv
# Create your views here.
from .marksheet_generator import *
from .concise_marksheet import *
from .email import *


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'index.html', {
            'file_url': uploaded_file_url
        })
    return render(request, 'index.html')


def marks(request):
    # print(request.GET)
    with open('Vikas/marks.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow([request.GET['correct'], request.GET['wrong']])
    return HttpResponse("MARKING SCHEME COLLECTED")


def marksheet(request):
    marksheet_generator()
    print("ALL MARKSHEETS GENERATED")
    return HttpResponse("ALL MARKSHEETS GENERATED")


def concise(request):
    concise_marksheet_generator()
    print("CONCISE MARKSHEET GENERATED")
    return HttpResponse("CONCISE MARKSHEET GENERATED")


def email(request):
    email_generator()
    print("EMAIL SENT SUCCESFULLY")
    return HttpResponse("EMAIL SENT SUCCESFULLY")
