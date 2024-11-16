import React from 'react'
import Navbar from '../components/Navbar'

const SingleNewsArticle = () => {
  return (
    <div className='px-20 py-5'>
        <Navbar />
        <img
        src="https://via.placeholder.com/10x20"
        alt="News Image"
        className="mt-5 w-full h-[367px] object-cover rounded-lg"
      />
      <div className='flex flex-col mt-5 p-2'>
        <div className='text-gray-600'>Monday, 19 Aug 2024</div>
        <div className='text-6xl font-bold'>Israel kills 12 in strike on Gaza City school</div>
        <div className='mt-2 font-bold text-[#E2711D]'>INTERNATIONAL RELATIONS</div>
        <div className='mt-10 flex justify-between'>
            <div className='w-1/2 flex flex-col text-xl'>
                <div className='px-3 my-2 flex justify-between border-b border-black'>
                    <div>Peace</div>
                    <div>12</div>
                </div> 
                <div className='px-3 my-2 flex justify-between border-b border-black'>
                    <div>Peace</div>
                    <div>12</div>
                </div> 
                <div className='px-3 my-2 flex justify-between border-b border-black'>
                    <div>Peace</div>
                    <div>12</div>
                </div> 
                <div className='px-3 my-2 flex justify-between border-b border-black'>
                    <div>Peace</div>
                    <div>12</div>
                </div> 
                <div className='px-3 my-2 flex justify-between border-b border-black'>
                    <div>Peace</div>
                    <div>12</div>
                </div> 
            </div>
            <div className='mx-20 rounded-md bg-red-600 p-10 w-1/2 text-left flex flex-col text-white'>
                <div>PRUTL Score</div>
                <div className='text-7xl font-bold'>23</div>
                <div className='text-xl font-bold mt-5'>Threat to peace worldwide</div>
            </div>
        </div>

        <div className='mt-10 text-2xl font-bold'>Overall Effect</div>
        <div className='mt-2 text-xl '>Affects peace globally negatively. Language used across articles is negative. </div>

        <div className='mt-10 text-2xl font-bold'>Covered by:</div>
        <div className='flex justify-around'>
            <div className='flex flex-col'>
            <img
            src="https://via.placeholder.com/10x20"
            alt="News Image"
            className="mt-5 w-[84px] h-[84px] object-cover rounded-lg"
            />
            <div>ABP Majha</div>
            </div>
            <div className='flex flex-col'>
            <img
            src="https://via.placeholder.com/10x20"
            alt="News Image"
            className="mt-5 w-[84px] h-[84px] object-cover rounded-lg"
            />
            <div>ABP Majha</div>
            </div>
            <div className='flex flex-col'>
            <img
            src="https://via.placeholder.com/10x20"
            alt="News Image"
            className="mt-5 w-[84px] h-[84px] object-cover rounded-lg"
            />
            <div>ABP Majha</div>
            </div>
            <div className='flex flex-col'>
            <img
            src="https://via.placeholder.com/10x20"
            alt="News Image"
            className="mt-5 w-[84px] h-[84px] object-cover rounded-lg"
            />
            <div>ABP Majha</div>
            </div>
            <div className='flex flex-col'>
            <img
            src="https://via.placeholder.com/10x20"
            alt="News Image"
            className="mt-5 w-[84px] h-[84px] object-cover rounded-lg"
            />
            <div>ABP Majha</div>
            </div>
        </div>
      </div>
    </div>
  )
}

export default SingleNewsArticle