from transformers import pipeline

def detect_prompt_injection(text, threshold=0.5):
    # Load the Hugging Face model for prompt injection detection
    classifier = pipeline("text-classification", model="protectai/deberta-v3-base-prompt-injection-v2")

    # Make a prediction using the model
    result = classifier(text)

    # Initialize the scores dictionary
    scores = {r['label']: r['score'] for r in result}

    # Check if 'INJECTION' label is present and get its score
    injection_score = 0.0
    if 'INJECTION' in scores and scores['INJECTION'] > threshold:
        injection_score = scores['INJECTION']
        # Remove 'INJECTION' label from the dictionary after calculating the score
        del scores['INJECTION']

    # Add the 'SAFE' label if not already present
    if 'SAFE' not in scores:
        scores['SAFE'] = 1 - injection_score  # Calculate 'SAFE' as 1 - INJECTION score

    # Return the response with the adjusted scores
    if injection_score > 0:
        return ("Possible prompt injection attempt detected.", scores)
    else:
        return ("It seems safe.", scores)