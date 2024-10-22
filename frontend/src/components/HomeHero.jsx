import React from 'react'
import HeroSearchBar from './HeroSearchBar'

const HomeHero = () => {
  return (
    <div className='flex flex-col bg-[#F4EBE8] my-5 text-center p-4 rounded-md'>
        <div className='font-semibold text-[#636363]'>MACHINE LEARNING COURSE PROJECT: TYAIML-11</div>
        <div className='text-3xl my-3 font-bold mb-5'>Understand Toxicity in News and the factors that affect it</div>
        <HeroSearchBar />
    </div>
  )
}

export default HomeHero