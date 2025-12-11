import React from 'react';

const MathNotation = ({ expression, description }) => {
  return (
    <div className="math-notation-container">
      {description && <p>{description}</p>}
      <div className="math-expression">
        {expression}
      </div>
    </div>
  );
};

export default MathNotation;