import React from 'react'
import HeadlineNewsCard from './HeadlineNewsCard'

const Headlines = () => {
  return (
    
    <div className='flex flex-col mt-2'>
        <div className='flex justify-between '>
            <div className='font-bold text-3xl'>Today's Headlines</div>
            <div className='text-[#E2711D]'>See all</div>
        </div>
        <div className='flex justify-between mt-2'>
            <HeadlineNewsCard />
            <HeadlineNewsCard />
            <HeadlineNewsCard />
            <HeadlineNewsCard />
        </div>
    </div>
  )
}

export default Headlines