import React, { useState } from 'react';
import { useAuth } from './AuthContext';
import Login from './Login';
import SignUp from './SignUp';

const AuthWrapper: React.FC = () => {
  const [isLoginView, setIsLoginView] = useState(true);
  const { isAuthenticated, user } = useAuth();

  if (isAuthenticated && user) {
    return (
      <div className="auth-status">
        <p>Welcome, {user.displayName || user.email}!</p>
        <button
          onClick={() => {
            // In a real implementation, you would call logout from context
            console.log("Logout functionality would go here");
          }}
        >
          Logout
        </button>
      </div>
    );
  }

  return (
    <div className="auth-wrapper">
      {isLoginView ? (
        <Login onSwitchToSignup={() => setIsLoginView(false)} />
      ) : (
        <SignUp onSwitchToLogin={() => setIsLoginView(true)} />
      )}
    </div>
  );
};

export default AuthWrapper;