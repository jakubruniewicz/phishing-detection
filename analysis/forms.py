from django import forms

class EmailAnalysisForm(forms.Form):
    sender_name = forms.CharField(label="Sender Name", max_length=255)
    email_content = forms.CharField(label="Email Content", widget=forms.Textarea)
