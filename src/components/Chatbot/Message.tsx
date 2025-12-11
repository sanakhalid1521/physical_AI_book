import React from 'react';

interface MessageProps {
  message: {
    id: string;
    content: string;
    role: 'user' | 'assistant';
    timestamp: Date;
    sources?: Array<{
      id: string;
      content: string;
      source: string;
      chapter?: string;
      lesson?: string;
    }>;
  };
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="avatar-container" style={{
        display: 'flex',
        alignItems: 'flex-start',
        marginBottom: '8px',
        gap: '8px'
      }}>
        {isUser ? (
          <img
            src="/img/profile pic.png"
            alt="User"
            style={{
              width: '24px',
              height: '24px',
              borderRadius: '50%',
              alignSelf: 'flex-start',
              flexShrink: 0
            }}
          />
        ) : (
          <img
            src="/img/logo.png"
            alt="AI Assistant"
            style={{
              width: '24px',
              height: '24px',
              borderRadius: '50%',
              alignSelf: 'flex-start',
              flexShrink: 0
            }}
          />
        )}
        <div className="message-content">
          <div className="message-text">
            {message.content.split('\n').map((line, i) => (
              <React.Fragment key={i}>
                {line}
                {i < message.content.split('\n').length - 1 && <br />}
              </React.Fragment>
            ))}
          </div>

          {message.sources && message.sources.length > 0 && (
            <div className="message-sources">
              <details>
                <summary>Sources from textbook</summary>
                <ul>
                  {message.sources.map((source, index) => (
                    <li key={index} className="source-item">
                      <div className="source-content">
                        {source.chapter && <span className="source-chapter">Chapter: {source.chapter}</span>}
                        {source.lesson && <span className="source-lesson">Lesson: {source.lesson}</span>}
                        <span className="source-text">{source.content.substring(0, 100)}...</span>
                      </div>
                    </li>
                  ))}
                </ul>
              </details>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Message;