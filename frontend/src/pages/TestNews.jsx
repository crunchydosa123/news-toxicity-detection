import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import axios from 'axios';

const TestNews = () => {
  const [url, setUrl] = useState('');
  const [text, setText] = useState('');
  const [textFetched, setTextFetched] = useState(false);
  const [mlScoring, setMLScoring] = useState(null);
  const [report, setReport] = useState(null);

  const fetchText = (link) => {
    setTextFetched(false);
    setMLScoring(null);
    axios
      .post('http://127.0.0.1:5000/extract_text', { url: link })
      .then((response) => {
        const fetchedText = response.data.text;
        setText(fetchedText);
        setTextFetched(true);
        getMLScore(fetchedText);
      })
      .catch((error) => {
        console.error(error);
        setText('Error fetching text. Please try again.');
        setTextFetched(false);
      });
  };

  const getMLScore = (text) => {
    setMLScoring(null);
    axios
      .post('https://vit.us-east-2.aws.modelbit.com/v1/classify_text_as_json/latest', { data: text })
      .then((response) => {
        const parsedData = JSON.parse(response.data.data);
        console.log(parsedData); // Log the parsed data to verify its structure
        setReport(parsedData); 
        console.log('ML Scoring Success:', parsedData);
        //setReport(response.data.data); // Store the response data
        setMLScoring(true);
      })  
      .catch((error) => {
        console.error('ML Scoring Failed:', error);
        setMLScoring(false);
      });
  };

  return (
    <div className="p-4">
      <Navbar />
      <div className="m-10 text-4xl font-bold">Check any news article and its PRUTL score!</div>
      <div className="bg-[#F4EBE8] p-5 rounded-md flex justify-center mx-10">
        <input
          className="p-3 text-black w-full"
          placeholder="Enter URL of the news article here"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button
          className="p-3 w-1/6 bg-white text-[#E2711D] border border-[#E2711D] hover:bg-[#E2711D] hover:text-white hover:font-bold"
          onClick={() => fetchText(url)}
        >
          Search
        </button>
      </div>

      <div className="mx-10 mt-5 p-5 bg-white border rounded-md">
        {text
          ? text.split(' ').slice(0, 30).join(' ') + (text.split(' ').length > 30 ? '...' : '')
          : 'No text yet'}
      </div>

      <div className="m-10">
        {textFetched ? (
          <div className="bg-green-400 p-5 text-white">Text Fetched Successfully</div>
        ) : (
          <div className="bg-red-400 p-5 text-white">Text Not Fetched</div>
        )}
      </div>

      <div className="m-10">
        {mlScoring === null ? null : mlScoring ? (
          <div className="bg-green-400 p-5 text-white">ML Scoring Successful</div>
        ) : (
          <div className="bg-red-400 p-5 text-white">ML Scoring Failed</div>
        )}
      </div>

      {report ? (<div className='m-10 text-xl font-bold'>Affects: {report.Final_Attribute}</div>) : (<></>)}

    </div>
  );
};

export default TestNews;
