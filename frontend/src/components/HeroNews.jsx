import React from 'react';

const HeroNews = () => {
  return (
    <div className="w-full flex justify-start items-center pl-0 px-4 py-4">
      <img
        src="https://via.placeholder.com/10x20"
        alt="News Image"
        className="w-[543px] h-[305px] object-cover rounded-lg"
      />
      <div className="text-left pl-10">
        <div className='flex flex-col justify-between'>
            <div className='pb-2'>Monday, 19 Aug 2024</div>
            <div className='text-5xl pb-10 font-bold'>Israel kills 12 in strike on Gaza City school</div>
            <div className='flex justify-between'>
                <div>
                    <div>Affects: Peace</div>
                    <div>Total Bias: 7%</div>
                    <div>PRUTL Score: 1</div>
                </div>
                <div className='flex flex-col justify-end'>
                    <button className='border border-[#E2711D] p-3 rounded-md text-[#E2711D] hover:bg-[#E2711D] hover:text-white'>Read Complete Report</button>
                </div>
                
            </div>
            
        </div>
      </div>
    </div>
  );
};

export default HeroNews;
