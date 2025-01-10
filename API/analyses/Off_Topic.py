from transformers import pipeline

def off_topic_classifier(text, off_topics, threshold=0.5):
    # Hugging Face model
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    scores = {}

    for topic in off_topics:
        # Evaluate each topic independently
        result = classifier(text, candidate_labels=[topic])
        scores[topic] = result['scores'][0]  # First score corresponds to the provided topic

    # Check if any of the undesired topics exceed the threshold
    for topic, score in scores.items():
        if score > threshold:
            return "Detected off topics.", scores

    return "No off topics detected.", scores
