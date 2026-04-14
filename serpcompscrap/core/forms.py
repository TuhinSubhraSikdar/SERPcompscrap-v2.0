from django import forms


class KeywordUploadForm(forms.Form):
    # 📄 CSV Upload
    keywords_file = forms.FileField(
        label="Upload Keywords CSV",
        widget=forms.ClearableFileInput(attrs={
            "class": "input-field"
        })
    )

    # 🌍 Location चयन
    LOCATION_CHOICES = [
        ("us", "USA"),
        ("ca", "Canada"),
        ("uk", "UK"),
        ("in", "India"),
        ("au", "Australia"),
        ("cn", "China"),
        ("jp", "Japan"),
    ]

    location = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        widget=forms.RadioSelect
    )

    # 🔑 USER API KEY (NEW 🔥)
    api_key = forms.CharField(
        max_length=255,
        required=True,
        label="Serper API Key",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your Serper API Key",
            "class": "input-field",
            "autocomplete": "off"
        })
    )

    # ✅ OPTIONAL VALIDATION (PRO TOUCH)
    def clean_keywords_file(self):
        file = self.cleaned_data.get("keywords_file")

        if not file.name.endswith(".csv"):
            raise forms.ValidationError("Only CSV files are allowed ❌")

        if file.size == 0:
            raise forms.ValidationError("Uploaded file is empty ❌")

        return file

    def clean_api_key(self):
        key = self.cleaned_data.get("api_key")

        if not key or len(key.strip()) < 10:
            raise forms.ValidationError("Invalid API Key ❌")

        return key.strip()