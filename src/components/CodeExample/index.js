import React from 'react';

const CodeExample = ({ language, code, description }) => {
  return (
    <div className="code-example-container">
      {description && <p>{description}</p>}
      <pre>
        <code className={`language-${language}`}>
          {code}
        </code>
      </pre>
    </div>
  );
};

export default CodeExample;