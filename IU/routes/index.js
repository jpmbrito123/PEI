var express = require('express');
var router = express.Router();
var axios = require('axios');

// GET home page (form de validação)
router.get('/', async function(req, res, next) {
  try {
    // Make a POST request to the Flask API:
    const apiResponse = await axios.get(`http://api:5000/analyses`);

    const results1 = apiResponse.data;

    console.log(results1['analyses'])

    // Retrieve the prompt/response stored in the session (if it exists).
    const previousPrompt = req.session.previousPrompt || null;
    const previousResponse = req.session.previousResponse || null;

    const analyses = {
      input: Object.keys(results1['analyses'])
        .filter(key => results1['analyses'][key]["type"] === "input" || results1['analyses'][key]["type"] === "all")
        .map(key => results1['analyses'][key]),
      output: Object.keys(results1['analyses'])
        .filter(key => results1['analyses'][key]["type"] === "output" || results1['analyses'][key]["type"] === "all")
        .map(key => results1['analyses'][key])
    };
    
    const validationType = 'input';
    const results = {'analyses_results':{}}
    res.render('index', {results, analyses, validationType, previousPrompt, previousResponse});
  } catch (error) {
    console.error("Error calling the API:", error);

    res.status(500).send("Error calling the analyses API.");
  }

});

// POST to submit the validation (input or output)
router.post('/', async function(req, res, next) {
  let { prompt, response, validationType, selectedAnalyses } = req.body;

  req.session.previousPrompt = prompt;
  req.session.previousResponse = response;
  console.log('Prompt stored in the session:', req.session.previousPrompt);
  console.log('Prompt stored in the session:', req.session.previousResponse);

// Store the selected checkboxes in the session
// If selectedAnalyses doesn't exist, set it as an empty array
  if (!selectedAnalyses) {
    selectedAnalyses = [];
  }

  if (typeof selectedAnalyses === 'string') {
    selectedAnalyses = [selectedAnalyses];
  }
  
  let apiUrl = validationType === 'input' ? '/validate_input' : '/validate_output';

  
  const selectAnalyses = selectedAnalyses.map((analysis) => {
    const paramsKey = `param_${analysis}`;
    if (Array.isArray(req.body[paramsKey])) {
      req.body[paramsKey] = req.body[paramsKey].filter(item => item.trim() !== '');
    }
    return {
      name: analysis,
      params: [req.body[paramsKey]]
    };
  });

  let payload ={}
  if (validationType === 'input'){
    payload = {
      prompt: prompt,
      analyses: selectAnalyses
    };
  }else{
    payload = {
      response: response,
      analyses: selectAnalyses
    };
  }

  console.log(payload)
  try {
    // Make the POST request to the Flask API.
    const apiResponse = await axios.post(`http://api:5000${apiUrl}`, payload);
    const results = apiResponse.data;

    console.log(results)
    
    // Render the results page.
    const apiResponse1 = await axios.get(`http://api:5000/analyses`);

    const analysesData = apiResponse1.data;

    console.log(analysesData['analyses'])

    const analyses = {
      input: Object.keys(analysesData['analyses'])
        .filter(key => analysesData['analyses'][key]["type"] === "input" || analysesData['analyses'][key]["type"] === "all")
        .map(key => analysesData['analyses'][key]),
      output: Object.keys(analysesData['analyses'])
        .filter(key => analysesData['analyses'][key]["type"] === "output" || analysesData['analyses'][key]["type"] === "all")
        .map(key => analysesData['analyses'][key])
    };

    const previousPrompt = req.session.previousPrompt || null;
    const previousResponse = req.session.previousResponse || null;

    res.render('index', {results, analyses, validationType, previousPrompt, previousResponse});
  } catch (error) {
    console.error("Error calling the API:", error);

    // Send a proper response on error
    res.status(500).send("Error calling the analyses API.");
  }
});

module.exports = router;

