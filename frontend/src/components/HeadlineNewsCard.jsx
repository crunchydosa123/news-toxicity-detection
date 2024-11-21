import React from 'react'

const HeadlineNewsCard = () => {
  return (
    <div className='flex flex-col'>
        <img
        src="https://via.placeholder.com/10x20"
        alt="News Image"
        className="w-[288px] h-[173px] object-cover"
      />
      <div className='pr-5 pt-2 font-semibold'>Manipur government working  to restore peace: CM Biren Singh</div>
      <div className=''>UNITY</div>
      <div className=''>PRUTL Score: 1</div>
    </div>
  )
}

export default HeadlineNewsCard