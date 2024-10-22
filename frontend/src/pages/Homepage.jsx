import React from 'react'
import Navbar from '../components/Navbar'
import HomeHero from '../components/HomeHero'

const Homepage = () => {
  return (
    <div className='px-20 py-5'>
        <Navbar />
        <HomeHero />
    </div>
  )
}

export default Homepage