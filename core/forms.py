from django import forms

class KeywordUploadForm(forms.Form):
    keywords_file = forms.FileField()
    location = forms.ChoiceField(choices=[
        ("us", "USA"),
        ("ca", "Canada"),
        ("uk", "UK"),
        ("in", "India"),
        ("au", "Australia"),
        ("cn", "China"),
        ("jp", "Japan"),
    ])