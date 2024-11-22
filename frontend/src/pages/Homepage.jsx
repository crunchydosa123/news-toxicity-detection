import React from 'react'
import Navbar from '../components/Navbar'
import HomeHero from '../components/HomeHero'
import ArticleComponent from '../components/ArticleComponent'
import ArticleTable from '../components/ArticleTable'
import { KeywordsProvider } from '../contexts/KeywordsContext'
import HeroNews from '../components/HeroNews'
import Headlines from '../components/Headlines'
import Footer from '../components/Footer'
import Topics from '../components/Topics'

const Homepage = () => {
  return (
    <div>
      <div className='px-20 py-5'>

      
      <KeywordsProvider>
        <Navbar />
        <HomeHero />
        <HeroNews />
        <Headlines />
        
      </KeywordsProvider>
      <Topics />
      </div>
      <Footer />
    </div>
  )
}

export default Homepage