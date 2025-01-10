from googletrans import Translator

def translate_pt_to_en(pt_text):
    # Initialize the Google Translate API
    translator = Translator()
    
    # Translate from Portuguese to English
    translation = translator.translate(pt_text, src='pt', dest='en')
    
    # Return the translated text
    return translation.text