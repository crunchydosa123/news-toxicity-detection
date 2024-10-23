import React from 'react'
import Navbar from '../components/Navbar'
import HomeHero from '../components/HomeHero'
import ArticleComponent from '../components/ArticleComponent'
import ArticleTable from '../components/ArticleTable'
import { KeywordsProvider } from '../contexts/KeywordsContext'

const Homepage = () => {
  return (
    <div className='px-20 py-5'>
      <KeywordsProvider>
        <Navbar />
        <HomeHero />
        <ArticleTable />
      </KeywordsProvider>
    </div>
  )
}

export default Homepage