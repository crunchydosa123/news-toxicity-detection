import React, { useContext, useEffect, useState } from 'react';
import ArticleComponent from './ArticleComponent';
import KeywordsContext from '../contexts/KeywordsContext';

const ArticleTable = () => {
    const { keywords } = useContext(KeywordsContext);
    const [articles, setArticles] = useState([]);

    useEffect(() => {
        const fetchArticles = async () => {
            try {
                // Fetch articles from the GET route
                const response = await fetch(`http://localhost:5000/scrape?keywords[]=${keywords.join('&keywords[]=')}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch articles');
                }
                const data = await response.json();

                // Send the fetched data to the POST route for sentiment analysis
                const sentimentResponse = await fetch('http://localhost:5000/analyze_sentiment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data), // Send the data for sentiment analysis
                });

                if (!sentimentResponse.ok) {
                    throw new Error('Failed to analyze sentiment');
                }

                const sentimentResults = await sentimentResponse.json();
                setArticles(sentimentResults); // Set the analyzed results as articles

            } catch (error) {
                console.error(error);
            }
        };

        
        fetchArticles();
    }, [keywords]); // Fetch articles when keywords change

    return (
        <div className='flex flex-col'>
            {articles.map((item, index) => (
                <ArticleComponent 
                    key={index}
                    link={item.link} 
                    title={item.title} 
                    score={item.score} 
                    sentiment={item.sentiment} 
                /> 
            ))}
        </div>
    );    
}

export default ArticleTable;
