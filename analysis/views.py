from django.shortcuts import render
from .forms import EmailAnalysisForm
from .models import PhishingSender
from .model import PhishingModel

phishing_model = PhishingModel()

def analyze_email(request):
    # Wyniki analizy e-maila
    result = None
    result_class = None
    # Wyniki wyszukiwania
    results = None
    query = ""

    # Obsługa POST (analiza e-maila)
    if request.method == "POST":
        form = EmailAnalysisForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data["sender_name"]
            email_content = form.cleaned_data["email_content"]
            classification = phishing_model.classify_email(email_content)
            if classification == "Phishing Email":
                PhishingSender.objects.get_or_create(name=sender_name)
            result = classification
            if result == "Safe Email":
                result_class = "safe-result"
            elif result == "Phishing Email":
                result_class = "phishing-result"
    else:
        form = EmailAnalysisForm()

    # Obsługa GET (wyszukiwanie nadawców)
    if "q" in request.GET:
        query = request.GET.get("q", "")
        results = PhishingSender.objects.filter(name__icontains=query)

    return render(request, "analysis/analyze_email.html", {
        "form": form,
        "result": result,
        "result_class": result_class,
        "query": query,
        "results": results
    })
