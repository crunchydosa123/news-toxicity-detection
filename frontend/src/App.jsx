import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Homepage from './pages/Homepage';
import SingleNewsArticle from './pages/SingleNewsArticle';
import SingleTopic from './pages/SingleTopic';
import TestNews from './pages/TestNews';
import Keyword_Prutl from './pages/Keyword_Prutl';
import TestNews2 from './pages/TestNews2';


function App() {

  return (
    <Router>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/singlenews/:id" element={<SingleNewsArticle />} />
          <Route path="/topic/:id" element={<SingleTopic />} />
          <Route path="/test/" element={<TestNews2 />} />
          <Route path="/batch_text" element={<Keyword_Prutl />} />
        </Routes>
    </Router>
  )
}

export default App
