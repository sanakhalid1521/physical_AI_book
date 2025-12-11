import React, { useState } from 'react';

const InteractiveDemo = ({ title, description, initialState, onExecute }) => {
  const [state, setState] = useState(initialState || {});
  const [result, setResult] = useState(null);

  const handleExecute = () => {
    const output = onExecute ? onExecute(state) : null;
    setResult(output);
  };

  return (
    <div className="interactive-demo-container">
      <h3>{title}</h3>
      <p>{description}</p>
      <div className="demo-controls">
        {/* Demo controls would go here based on specific demo needs */}
        <button onClick={handleExecute}>Run Demo</button>
      </div>
      {result && (
        <div className="demo-result">
          <h4>Result:</h4>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default InteractiveDemo;