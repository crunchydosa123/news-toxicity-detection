import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Homepage from './pages/Homepage';
import SingleNewsArticle from './pages/SingleNewsArticle';
import SingleTopic from './pages/SingleTopic';


function App() {

  return (
    <Router>
        <Routes>
          <Route path="/" element={<Homepage />} />
          <Route path="/singlenews/:id" element={<SingleNewsArticle />} />
          <Route path="/topic/:id" element={<SingleTopic />} />
        </Routes>
    </Router>
  )
}

export default App
