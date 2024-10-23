import React, { useContext, useState } from 'react';
import KeywordsContext from '../contexts/KeywordsContext';

const HeroSearchBar = () => {
  const { keywords, setKeywords } = useContext(KeywordsContext);
  const [localKeyword, setLocalKeyword] = useState('');

  const handleInputChange = (e) => {
    setLocalKeyword(e.target.value); // Update local keyword state
  };

  const handleSearchClick = () => {
    // Split input by spaces and commas, remove empty values, and set the keywords
    const keywordsArray = localKeyword
      .split(/[\s,]+/) // Split by space or comma
      .filter(keyword => keyword.trim() !== ''); // Filter out empty values

    setKeywords(keywordsArray); // Update context with the keywords array
  };

  return (
    <div className="mx-40 flex justify-center mb-5">
      <input
        type="text"
        placeholder='Enter keywords and check toxicity'
        className="p-2 h-10 w-full border border-gray-500"
        value={localKeyword}
        onChange={handleInputChange} // Pass the input change handler
      />
      <button
        className="text-white bg-[#E2711D] p-2 h-10 hover:bg-black"
        onClick={handleSearchClick} // Pass the search click handler
      >
        Search
      </button>
    </div>
  );
}

export default HeroSearchBar;
