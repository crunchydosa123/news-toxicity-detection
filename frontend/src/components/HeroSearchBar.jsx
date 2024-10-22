import React from 'react'

const HeroSearchBar = () => {
  return (
  <div className="mx-40 flex justify-center mb-5">
    <input type="text" placeholder='Enter keywords and check toxicity' className="p-2 h-10 w-full border border-gray-500"/>
    <button className="text-white bg-[#E2711D] p-2 h-10 hover:bg-black">Search</button>
  </div>
  
  )
}

export default HeroSearchBar