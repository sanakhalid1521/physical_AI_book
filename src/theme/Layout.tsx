import React from 'react';
import { AuthProvider } from '../components/Auth/AuthContext';
import ChatWidget from '../components/Chatbot/ChatWidget';
import OriginalLayout from '@theme-original/Layout';

type LayoutProps = {
  children: React.ReactNode;
};

export default function Layout(props: LayoutProps): JSX.Element {
  return (
    <AuthProvider>
      <OriginalLayout {...props} />
      <ChatWidget backendUrl="/api" />
    </AuthProvider>
  );
}