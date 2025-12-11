import React, { useState, useEffect, useRef } from 'react';
import ChatWindow from './ChatWindow';
import './styles.css';

interface ChatWidgetProps {
  backendUrl?: string;
}

const ChatWidget: React.FC<ChatWidgetProps> = ({ backendUrl = '/api' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const widgetRef = useRef<HTMLDivElement>(null);

  // Check if there's selected text on the page
  const getSelectedText = (): string => {
    const selection = window.getSelection();
    return selection?.toString().trim() || '';
  };

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = getSelectedText();
      if (selectedText && !isOpen) {
        // Optionally show a hint to the user that they can ask about the selected text
        console.log('Selected text:', selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, [isOpen]);

  // Close widget when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (widgetRef.current && !widgetRef.current.contains(event.target as Node)) {
        if (isOpen) {
          setIsOpen(false);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  return (
    <div className="chat-widget" ref={widgetRef}>
      {isOpen ? (
        <ChatWindow
          backendUrl={backendUrl}
          onClose={() => setIsOpen(false)}
          initialContext={getSelectedText()}
        />
      ) : (
        <button
          className="chat-toggle-button"
          onClick={() => setIsOpen(true)}
          aria-label="Open chat"
          title="Open Physical AI Assistant"
          style={{
            backgroundImage: `url('/img/RAG.jpg')`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat'
          }}
        >
          <span className="chat-badge" style={{
            position: 'absolute',
            top: '-5px',
            right: '-5px',
            zIndex: 1
          }}>AI</span>
        </button>
      )}
    </div>
  );
};

export default ChatWidget;