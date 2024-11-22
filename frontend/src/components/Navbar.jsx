import React from 'react'

const Navbar = () => {
  return (
    <div className='flex justify-between'>
        <div className='text-2xl font-bold text-[#E2711D]'>PRUTLInsight</div>
        <div className='flex justify-center'>
          <div className='mx-4 hover:font-bold'>Topics</div>
          <div className='mx-4 hover:font-bold'>Global Peace Score</div>
          <div className='mx-4 hover:font-bold'>Bias Ratings</div>
        </div>
    </div>
  )
}

export default Navbar