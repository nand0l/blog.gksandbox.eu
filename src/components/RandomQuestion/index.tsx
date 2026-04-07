import React, { useState } from 'react';

export default function RandomQuestion() {
  const [lastQuestion, setLastQuestion] = useState<number | null>(null);
  const [questionNumber, setQuestionNumber] = useState('');

  const handleRandomClick = () => {
    let randomNum;
    do {
      randomNum = Math.floor(Math.random() * 500) + 1;
    } while (randomNum === lastQuestion);
    
    setLastQuestion(randomNum);
    window.location.href = `/docs/exams/SAP-C02/${randomNum}`;
  };

  const handleGoToQuestion = () => {
    const num = parseInt(questionNumber);
    if (num >= 1 && num <= 500) {
      window.location.href = `/docs/exams/SAP-C02/${num}`;
    }
  };

  return (
    <div className="margin-vert--md" style={{maxWidth: '300px'}}>
      <div className="margin-bottom--md">
        <button 
          className="button button--primary"
          style={{width: '100%'}}
          onClick={handleRandomClick}>
          Random SAP-C02 Question
        </button>
      </div>
      
      <div className="margin-bottom--md">
        <input
          type="number"
          min="1"
          max="500"
          placeholder="Question number (1-500)"
          value={questionNumber}
          onChange={(e) => setQuestionNumber(e.target.value)}
          style={{width: '100%', padding: '8px'}}
        />
      </div>
      
      <div>
        <button 
          className="button button--secondary"
          style={{width: '100%'}}
          onClick={handleGoToQuestion}
          disabled={!questionNumber || parseInt(questionNumber) < 1 || parseInt(questionNumber) > 500}>
          Go to Question
        </button>
      </div>
    </div>
  );
}