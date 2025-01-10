from transformers import pipeline

def on_topic_classifier(text, on_topics, threshold=0.5):
    # Hugging Face model
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    scores = {}

    for topic in on_topics:
        # Evaluate each topic independently
        result = classifier(text, candidate_labels=[topic])
        scores[topic] = result['scores'][0]  # First score corresponds to the provided topic

    # Check if any of the desired topics exceed the threshold
    for topic, score in scores.items():
        if score > threshold:
            return "Detected on topics.", scores

    return "No on topics detected.", scores
