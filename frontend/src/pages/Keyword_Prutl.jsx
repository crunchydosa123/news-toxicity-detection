import React, { useState } from 'react';
import Navbar from '../components/Navbar';

const Keyword_Prutl = () => {
  const [keyword, setKeyword] = useState('');
  const [response, setResponse] = useState(null); // State to store the final processed response
  const [loading, setLoading] = useState(false); // State to manage loading state
  const [error, setError] = useState(null); // State to manage errors

  const handleSearch = async () => {
    if (keyword.trim()) {
      setLoading(true);
      setError(null);

      try {
        // Step 1: Fetch articles from the Flask API
        const flaskRes = await fetch(`http://localhost:5000/scrape?keywords[]=${encodeURIComponent(keyword)}`);
        if (!flaskRes.ok) {
          throw new Error(`Flask server responded with status ${flaskRes.status}`);
        }

        const flaskData = await flaskRes.json();

        // Step 2: Extract texts from the Flask API response
        const texts = flaskData.map((item) => item.text);

        // Step 3: Send texts to the Node.js API
        const nodeRes = await fetch('http://localhost:3000/process_multiple_texts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ texts }),
        });

        if (!nodeRes.ok) {
          throw new Error(`Node.js server responded with status ${nodeRes.status}`);
        }

        const nodeData = await nodeRes.json();

        // Step 4: Store the processed results
        setResponse(nodeData.results);
      } catch (err) {
        console.error('Error processing keywords:', err);
        setError('Failed to process keywords. Please try again.');
      } finally {
        setLoading(false);
      }
    } else {
      alert('Please enter a valid keyword.');
    }
  };

  return (
    <div className="m-10">
      <Navbar />
      <div className="m-10 text-4xl font-bold">
        Check any news keyword and its PRUTL score!
      </div>
      <div className="bg-[#F4EBE8] p-5 rounded-md flex justify-center mx-10">
        <input
          className="p-3 text-black w-full"
          placeholder="Enter a keyword to search"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
        <button
          className="p-3 w-1/6 bg-white text-[#E2711D] border border-[#E2711D] hover:bg-[#E2711D] hover:text-white hover:font-bold"
          onClick={handleSearch}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Search'}
        </button>
      </div>

      {/* Display Results */}
      <div className="m-10">
        {error && <p className="text-red-500">{error}</p>}
        {response ? (
          <div className="space-y-6">
            {response.map((result, index) => (
  <div key={index} className="p-5 border rounded-lg shadow-md bg-white">
    {result.error ? (
      <p className="text-red-500">{result.error}</p>
    ) : (
      <>
        {/* Display Cleaned Text */}
        <p className="text-gray-800 font-semibold mb-4">
          <strong>Cleaned Text:</strong>{' '}
          {result.Cleaned_Text
            ? result.Cleaned_Text.split(' ').slice(0, 30).join(' ') + '...'
            : 'No cleaned text available'}
        </p>

        {/* Display Scores */}
        <table className="table-auto border-collapse border border-gray-300 w-full text-left mb-4">
          <thead>
            <tr>
              <th className="border border-gray-300 p-2">Raw Scores</th>
              <th className="border border-gray-300 p-2">Aggregated Scores</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border border-gray-300 p-2">
                {result.Raw_Scores
                  ? Object.entries(result.Raw_Scores).map(([key, value]) => (
                      <div key={key}>
                        {key}: {value.toFixed(2)}
                      </div>
                    ))
                  : 'No raw scores available'}
              </td>
              <td className="border border-gray-300 p-2">
                {result.Aggregated_Scores
                  ? Object.entries(result.Aggregated_Scores).map(
                      ([key, value]) => (
                        <div key={key}>
                          {key}: {value.toFixed(2)}
                        </div>
                      )
                    )
                  : 'No aggregated scores available'}
              </td>
            </tr>
          </tbody>
        </table>

        {/* Display Final Attribute */}
        <div className="p-4 bg-gray-100 border border-gray-300 text-xl font-bold text-center rounded-lg text-gray-900">
          Final Attribute:{' '}
          {result.Final_Attribute || 'No final attribute available'}
        </div>
      </>
    )}
  </div>
))}

          </div>
        ) : (
          !loading && (
            <p className="text-gray-500">No results to display yet.</p>
          )
        )}
      </div>
    </div>
  );
};

export default Keyword_Prutl;
