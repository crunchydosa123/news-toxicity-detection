import React from 'react'
import Navbar from '../components/Navbar'

const SingleTopic = () => {
  return (
    <div className='px-20 py-5'>
        <Navbar />
        <img
        src="https://via.placeholder.com/10x20"
        alt="News Image"
        className="mt-5 w-full h-[367px] object-cover rounded-lg"
      />

        <div className='mt-10 mx-5 rounded-md bg-red-600 p-10 w-1/2 text-left flex flex-col text-white'>
            <div>PRUTL Score for all articles in this topic</div>
            <div className='text-7xl font-bold'>23</div>
        </div>


        <div className='text-2xl mt-10 font-bold'>Articles</div>
        <div className='flex flex-col mt-4'>
            <div className='my-2 flex justify-between border-b border-black'>
                <div className='flex flex-col'>
                    <div>Israel kills 12 in strike on Gaza City school</div>
                    <div>PRUTL SCORE: 23</div>
                </div>
                <div>Read Complete Report</div>
            </div>
            <div className='my-2 flex justify-between border-b border-black'>
                <div className='flex flex-col'>
                    <div>Israel kills 12 in strike on Gaza City school</div>
                    <div>PRUTL SCORE: 23</div>
                </div>
                <div>Read Complete Report</div>
            </div>
            <div className='my-2 flex justify-between border-b border-black'>
                <div className='flex flex-col'>
                    <div>Israel kills 12 in strike on Gaza City school</div>
                    <div>PRUTL SCORE: 23</div>
                </div>
                <div>Read Complete Report</div>
            </div>
            <div className='my-2 flex justify-between border-b border-black'>
                <div className='flex flex-col'>
                    <div>Israel kills 12 in strike on Gaza City school</div>
                    <div>PRUTL SCORE: 23</div>
                </div>
                <div>Read Complete Report</div>
            </div>
        </div>
    </div>
  )
}

export default SingleTopic