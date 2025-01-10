from transformers import AutoModelForSequenceClassification, XLMRobertaTokenizer
import torch

def language_detector(text):
    # Load the tokenizer and model
    tokenizer = XLMRobertaTokenizer.from_pretrained("LocalDoc/language_detection")
    model = AutoModelForSequenceClassification.from_pretrained("LocalDoc/language_detection")

    # Prepare the text for the model
    encoded_input = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)

    # Make the prediction
    model.eval()
    with torch.no_grad():
        outputs = model(**encoded_input)

    # Process the results
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    predicted_class_index = probabilities.argmax().item()

    # Mapping of indices to language codes
    labels = ["az", "ar", "bg", "de", "el", "en", "es", "fr", "hi", "it", "ja", "nl", "pl", "pt", "ru", "sw", "th", "tr", "ur", "vi", "zh"]
    language_names = {
        "az": "Azerbaijani",
        "ar": "Arabic",
        "bg": "Bulgarian",
        "de": "German",
        "el": "Greek",
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "hi": "Hindi",
        "it": "Italian",
        "ja": "Japanese",
        "nl": "Dutch",
        "pl": "Polish",
        "pt": "Portuguese",
        "ru": "Russian",
        "sw": "Swahili",
        "th": "Thai",
        "tr": "Turkish",
        "ur": "Urdu",
        "vi": "Vietnamese",
        "zh": "Chinese"
    }
    predicted_language = labels[predicted_class_index]

    # Return the full name of the language
    return language_names.get(predicted_language, "Unknown Language"), "N/A"

