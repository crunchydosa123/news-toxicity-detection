import React from 'react'
import TopicsCard from './TopicsCard'

const Topics = () => {
  return (
    <div className='flex flex-col mt-10'>
        <div className='flex justify-between '>
            <div className='font-bold text-3xl'>Today's Headlines</div>
            <div className='text-[#E2711D]'>See all</div>
        </div>
        <div className='flex justify-between mt-2'>
            <TopicsCard />
            <TopicsCard />
            <TopicsCard />
            <TopicsCard />
            <TopicsCard />
        </div>
    </div>
  )
}

export default Topics