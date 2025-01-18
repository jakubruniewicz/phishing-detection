from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class PhishingModel:
    def __init__(self):
        # Wymuszenie działania na CPU
        self.device = torch.device("cpu")
        self.model_name = "cybersectony/phishing-email-detection-distilbert_v2.4.1"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name).to(self.device)

    def classify_email(self, email_text):
        # Przygotowanie danych wejściowych na CPU
        inputs = self.tokenizer(email_text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=1)
        # Mapowanie wyniku na odpowiednią etykietę
        label_map = {0: "Safe Email", 1: "Phishing Email"}
        return label_map[predictions.item()]
