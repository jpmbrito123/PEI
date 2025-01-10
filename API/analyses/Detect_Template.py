import Levenshtein
from fuzzywuzzy import fuzz
from nltk.util import ngrams

def detect_template_in_output(output, template, similarity_threshold=80, n=6, overall_threshold=70):
    # Split the template and output into words
    template_words = template.split()
    output_words = output.split()
    
    # Generate n-grams for template and output
    template_ngrams = list(ngrams(template_words, n))
    output_ngrams = list(ngrams(output_words, n))

    detected_ngrams = []
    total_similarity = 0
    total_count = 0

    # Compare each n-gram from the template with the n-grams in the output
    for t_ngram in template_ngrams:
        t_phrase = ' '.join(t_ngram)
        
        max_similarity = 0
        for o_ngram in output_ngrams:
            o_phrase = ' '.join(o_ngram)
            
            # Similarity using Levenshtein and FuzzyWuzzy
            levenshtein_similarity = Levenshtein.ratio(t_phrase, o_phrase) * 100
            fuzzy_similarity = fuzz.partial_ratio(t_phrase, o_phrase)
            average_similarity = (levenshtein_similarity + fuzzy_similarity) / 2
            max_similarity = max(max_similarity, average_similarity)

        # Check for significant matches
        if max_similarity >= similarity_threshold:
            detected_ngrams.append({
                'phrase': t_phrase,
                'max_similarity': f"{max_similarity:.2f}%"
            })

        # Add similarity to the total for calculating the overall average
        total_similarity += max_similarity
        total_count += 1

    # Calculate the overall average similarity
    overall_similarity = (total_similarity / total_count) if total_count > 0 else 0

    # Report results based on overall similarity and detected n-grams
    if detected_ngrams:
        if overall_similarity >= overall_threshold:
            return f"Detected significant parts of the template in output: {detected_ngrams}", f"{overall_similarity:.2f}%"
        else:
            return "Detected parts of the template, but not significant enough.", f"{overall_similarity:.2f}% (Not significant)"
    else:
        return "No significant parts of the template detected in output.", "N/A"
