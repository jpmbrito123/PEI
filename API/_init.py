from flask import Flask, jsonify, request
from configs.app_config import *
from scripts import *
import json , threading, time

app = Flask(__name__)

@app.route('/analyses', methods=["GET"])
def analyses_list():
    # Create a dictionary to log the incoming request data
    log_data = {
        'method': request.method,
        'url': request.url,
        'sender': request.remote_addr,
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    # Save the log data to a JSON file
    save_log_to_json(log_data,'logs/requests.json') 

    with open("configs/analyses_info.json", 'r') as file:
        analyses_info = json.load(file)
    
    response = { "analyses":[ {"name":key} | analyses_info[key] for key in analyses_info.keys()] }
    
    return jsonify(response), 200

@app.route('/analysis/<analysis_name>', methods=["GET"])
def analysis(analysis_name):
    # Log the incoming request details
    log_data = {
        'method': request.method,
        'url': request.url,
        'sender': request.remote_addr,
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    # Save the log data to a JSON file
    save_log_to_json(log_data,'logs/requests.json')

    with open("configs/analyses_info.json", 'r') as file:
        analysis_info = json.load(file)
    
    # Check if the requested analysis exists in the loaded data
    if analysis_name in analysis_info.keys():
        response = { analysis_name: analysis_info[analysis_name] }
        return jsonify(response), 200
    else:
        return f"Analysis {analysis_name} does not exist.",404

# Route to validate the input
@app.route("/validate_input", methods=["POST"])
def validate_input():
    log_data = {
        'method': request.method,
        'url': request.url,
        'sender': request.remote_addr,
        'body': request.json,
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    save_log_to_json(log_data,'logs/requests.json')

    data = request.json
    analyses = data.get("analyses", [])
    
    status= "success"

    # Dictionary to store the results of the analyses
    analyses_results = {}

    #Preprocessing
    prompt,detect_language = support_portuguese(data.get("prompt"))
    for analysis in analyses:
        if analysis['name'] == "LanguageDetector":
            analyses_results["LanguageDetector"]={"message":detect_language[0],"score":detect_language[1]}
            break

    analyses = [
        analysis for analysis in analyses
        if not (analysis["name"] == "LanguageDetector")
    ]

    # List of threads for parallel execution of analyses
    threads = []

    # Create a thread for each requested analysis in the JSON
    for analysis in analyses:
        if analysis['name'] in available_analyses:
            thread = threading.Thread(target=run_analyses, args=(analysis, prompt, analyses_results))
            threads.append(thread)
            thread.start()
        else:
            # If the analysis is not available
            analyses_results[analysis['name']] = {
                "message": f"Analysis {analysis['name']} not available.",
                "score": None
            }
            status = "fail"

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Return the results of the analyses
    return jsonify({"status": status, "prompt": data.get("prompt"), "analyses_results": analyses_results}), 200

# Route to validate the output
@app.route("/validate_output", methods=["POST"])
def validate_output():
    log_data = {
        'method': request.method,
        'url': request.url,
        'sender': request.remote_addr,
        'body': request.json,
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    }
    save_log_to_json(log_data,'logs/requests.json')

    data = request.json
    analyses = data.get("analyses", [])

    status= "success"
    # Dictionary to store the results of the analyses
    analyses_results = {}
    
    #Preprocessing
    response,detect_language = support_portuguese(data.get("response"))
    for analysis in analyses:
        if analysis['name'] == "LanguageDetector":
            analyses_results["LanguageDetector"]={"message":detect_language[0],"score":detect_language[1]}
            break

    analyses = [
        analysis for analysis in analyses
        if not (analysis["name"] == "LanguageDetector")
    ]

    # List of threads for parallel execution of analyses
    threads = []
    
    # Create a thread for each requested analyses in the JSON
    for analysis in analyses:
        if analysis['name'] in available_analyses:
            thread = threading.Thread(target=run_analyses, args=(analysis, response, analyses_results))
            threads.append(thread)
            thread.start()
        else:
            # If the analysis is not available
            analyses_results[analysis['name']] = {
                "message": f"Analysis {analysis['name']} not available.",
                "score": None
            }
            status = "fail"

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    save_log_to_json({'sender': request.remote_addr,
                      'time': time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                       'analyses_results' : analyses_results},
                    'logs/results.json')

    # Return the results of the analyses
    return jsonify({"status": status, "response": response, "analyses_results": analyses_results}), 200


app.run(debug=True,port=API_PORT,host=HOST)