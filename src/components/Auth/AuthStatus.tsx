import React from 'react';
import { useAuth } from './AuthContext';

const AuthStatus: React.FC = () => {
  const { user, isAuthenticated, logout, loading } = useAuth();

  if (loading) {
    return <div className="auth-status">Loading...</div>;
  }

  if (isAuthenticated && user) {
    return (
      <div className="auth-status">
        {user.profilePicture ? (
          <img
            src={user.profilePicture}
            alt="Profile"
            className="profile-picture"
            style={{ width: '32px', height: '32px', borderRadius: '50%', marginRight: '8px' }}
          />
        ) : (
          <img
            src="/img/profile pic.png"
            alt="Profile"
            className="profile-picture"
            style={{ width: '32px', height: '32px', borderRadius: '50%', marginRight: '8px' }}
          />
        )}
        <span className="user-display">Welcome, {user.displayName || user.email}</span>
        <button
          className="logout-button"
          onClick={logout}
          aria-label="Logout"
        >
          Logout
        </button>
      </div>
    );
  }

  return (
    <div className="auth-status">
      <a href="/login" className="login-link">Log In</a>
      <span> or </span>
      <a href="/signup" className="signup-link">Sign Up</a>
    </div>
  );
};

export default AuthStatus;