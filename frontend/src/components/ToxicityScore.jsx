import React from 'react'

const ToxicityScore = ({score}) => {
    const styles = score === 'Toxic' ? 'bg-red-600 p-2 text-white font-bold' : 'bg-green-400 p-2 text-white font-bold';

  return (
    <div className={styles}>{score}</div>
  )
}

export default ToxicityScore