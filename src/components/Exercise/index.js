import React from 'react';

const Exercise = ({ title, description, tasks, requirements }) => {
  return (
    <div className="exercise-container">
      <h3>{title}</h3>
      <p>{description}</p>
      <div className="exercise-tasks">
        <h4>Tasks:</h4>
        <ol>
          {tasks.map((task, index) => (
            <li key={index}>{task}</li>
          ))}
        </ol>
      </div>
      {requirements && (
        <div className="exercise-requirements">
          <h4>Requirements:</h4>
          <ul>
            {requirements.map((req, index) => (
              <li key={index}>{req}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Exercise;