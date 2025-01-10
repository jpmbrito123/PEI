from transformers import pipeline

def detect_toxicity(text, threshold=0.5):
    # Load the pre-trained Hugging Face model
    classifier = pipeline("text-classification", model="unitary/toxic-bert")
    
    # Make a prediction using the Hugging Face model
    hf_result = classifier(text)

    # Prepare the scores for each label
    scores = {r['label']: r['score'] for r in hf_result}

    # Check if there's toxic content with Hugging Face based on the threshold
    for r in hf_result:
        if r['label'] == 'toxic' and r['score'] > threshold:
            return ("It contains toxicity.", scores)

    return ("No toxicity detected.", scores)
