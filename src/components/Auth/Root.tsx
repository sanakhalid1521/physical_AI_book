import React from 'react';
import { AuthProvider } from './AuthContext';

// This Root component will wrap the entire Docusaurus app
const Root: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return <AuthProvider>{children}</AuthProvider>;
};

export default Root;