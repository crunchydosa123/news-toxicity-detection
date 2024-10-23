import React from 'react';
import ToxicityScore from './ToxicityScore';

const ArticleComponent = ({ link, score, sentiment, title }) => {
    // Function to truncate the title to 12 words
    const truncateTitle = (title, limit) => {
        const words = title.split(' ');
        return words.length > limit ? `${words.slice(0, limit).join(' ')}...` : title;
    };

    return (
        <div className='flex flex-col'>
            <div className='flex justify-between p-0'>
                <div className='text-xl max-w-[550px] overflow-hidden whitespace-nowrap text-ellipsis'>
                    {title}
                </div>
                <div className=''><a href={link} target="_blank" rel="noopener noreferrer">Read Complete Article</a></div>
                <div className=''>{score}</div>
                <ToxicityScore score={sentiment} />
            </div>
            <hr className='my-4 border border-black' />
        </div>
    );
};

export default ArticleComponent;
