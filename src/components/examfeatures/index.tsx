import React, { useState, useEffect } from 'react';
import Link from '@docusaurus/Link';

export default function ExamsIndex() {
  const [lastQuestion, setLastQuestion] = useState<number | null>(null);

  const getRandomQuestion = () => {
    let randomNum;
    do {
      randomNum = Math.floor(Math.random() * 500) + 1;
    } while (randomNum === lastQuestion);
    
    setLastQuestion(randomNum);
    return randomNum;
  };

  const handleRandomClick = () => {
    const questionNum = getRandomQuestion();
    window.location.href = `/docs/exams/SAP-C02/${questionNum}`;
  };

  return (
    <div>
      <h1>Exams</h1>
      <p>
        <Link to="SAP-C02/1">SAP-C02 Question 1</Link>
      </p>
      <p>
        <button 
          className="button button--primary"
          onClick={handleRandomClick}>
          Random SAP-C02 Question
        </button>
      </p>
    </div>
  );
}