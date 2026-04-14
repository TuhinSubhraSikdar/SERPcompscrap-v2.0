from django.shortcuts import render
from core.forms import KeywordUploadForm
from core.utils.handler import run_scraper
import tempfile
import os


def home(request):
    print("🔥 VIEW HIT")

    if request.method == "POST":
        print("🔥 FORM SUBMITTED")

        form = KeywordUploadForm(request.POST, request.FILES)

        if form.is_valid():
            print("✅ FORM VALID")

            uploaded_file = form.cleaned_data["keywords_file"]
            location = form.cleaned_data["location"]
            api_key = form.cleaned_data["api_key"]

            print("FILE:", uploaded_file)
            print("LOCATION:", location)
            print("API KEY:", api_key)

            # ✅ SAFE TEMP FILE CREATION
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")

            try:
                # write uploaded file to temp storage
                for chunk in uploaded_file.chunks():
                    temp_file.write(chunk)

                temp_file.flush()
                temp_file.close()

                file_path = temp_file.name
                print("Saved file path:", file_path)

                # 🚀 RUN SCRAPER
                result = run_scraper(file_path, location, api_key)

                print("📊 RESULT:", result)

                return render(request, "core/home.html", {
                    "form": form,
                    "result": result
                })

            finally:
                # 🧹 cleanup temp input file
                if os.path.exists(temp_file.name):
                    os.remove(temp_file.name)

        else:
            print("❌ FORM ERRORS:", form.errors)

    else:
        form = KeywordUploadForm()

    return render(request, "core/home.html", {"form": form})