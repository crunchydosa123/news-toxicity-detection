const express = require('express');
const axios = require('axios');

// Initialize Express app
const app = express();
const port = 3000;

// Middleware to parse JSON request bodies
app.use(express.json());

// URL of the Modelbit API endpoint
const modelbitUrl = "https://vit.us-east-2.aws.modelbit.com/v1/final_output2/latest";

// Function to call the Modelbit API for each text
async function callModelbitAPI(text) {
  try {
    const response = await axios.post(modelbitUrl, {
      data: [text] // Passing a single text as an array
    });
    return response.data;  // Return the result from the API
  } catch (error) {
    console.error('Error calling Modelbit API:', error);
    return { error: 'Failed to process the text' };  // Return error in case of failure
  }
}

// API endpoint to accept a large array of texts
app.post('/process_multiple_texts', async (req, res) => {
  const texts = req.body.texts;

  // Ensure the texts array is provided
  if (!Array.isArray(texts)) {
    return res.status(400).json({ error: 'Invalid input: texts must be an array' });
  }

  const results = [];

  // Loop through each text, call the Modelbit API, and store the result
  for (let i = 0; i < texts.length; i++) {
    const result = await callModelbitAPI(texts[i]);
    results.push(result);
  }

  // Send the combined results back to the client
  res.json({ results });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
