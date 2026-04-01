from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from .forms import KeywordUploadForm
from .utils.handler import run_scraper
import os
from django.conf import settings


def home(request):

    if request.method == "POST":
        form = KeywordUploadForm(request.POST, request.FILES)

        if form.is_valid():

            uploaded_file = request.FILES["keywords_file"]
            location = form.cleaned_data["location"]

            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

            with open(file_path, "wb+") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            run_scraper(file_path, location)

            return render(request, "core/home.html", {"success": True})

    else:
        form = KeywordUploadForm()

    return render(request, "core/home.html", {"form": form})


# Create your views here.
