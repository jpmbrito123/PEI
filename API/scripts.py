
from analyses import detect_toxicity,on_topic_classifier,off_topic_classifier,detect_prompt_injection,language_detector, detect_template_in_output, translate_pt_to_en
import json, os

# Mapping of analyses to their specific functions
available_analyses = {
    "DetectToxicity": detect_toxicity,
    "OnTopic": on_topic_classifier,
    "OffTopic": off_topic_classifier,
    "DetectPromptInjection" : detect_prompt_injection,
    "LanguageDetector" : language_detector,
    "PromptTemplate" : detect_template_in_output
}

# Function to execute the specific analyses and store the result
def run_analyses(analysis, text, results):
    try:
        # Execute the analysis function directly
        if analysis['params'][0] == None:
            result = available_analyses[analysis['name']](text)
        else:
            result = available_analyses[analysis['name']](text,*analysis['params'])
        results[analysis['name']] = { 
            "message" : result[0],
            "score" : str(result[1])
        }
    except Exception as e:
        results[analysis['name']] = {
            "message": f"Error executing analysis {analysis['name']}: {str(e)}",
            "score": None
        }

# Helper function to save logs in a JSON file
def save_log_to_json(data,path):
    # If the file doesn't exist, create it with an empty list
    if not os.path.exists(path):
        with open(path, 'w') as file:
            json.dump([], file)
    
    # Load existing file
    with open(path, 'r') as file:
        logs = json.load(file)
    
    # Append the new log
    logs.append(data)
    
    # Write the updated logs back to the file
    with open(path, 'w') as file:
        json.dump(logs, file, indent=4)

# Support portuguese
def support_portuguese(prompt):
    response,score =language_detector(prompt)
    if response == "Portuguese":
        prompt = translate_pt_to_en(prompt)
    
    return prompt ,(response,score)