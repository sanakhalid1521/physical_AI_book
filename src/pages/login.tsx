import React from 'react';
import Layout from '@theme/Layout';
import Login from '../components/Auth/Login';
import { useAuth } from '../components/Auth/AuthContext';

function LoginPage(): JSX.Element {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return (
      <Layout title="Login" description="Login to your account">
        <main>
          <div className="container margin-vert--lg">
            <div className="row">
              <div className="col col--6 col--offset-3">
                <div className="text--center padding-vert--md">
                  <h1>You are already logged in</h1>
                  <p>
                    <a href="/">Go to homepage</a>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </Layout>
    );
  }

  return (
    <Layout title="Login" description="Login to your account">
      <main>
        <div className="container margin-vert--lg">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <div className="padding-vert--md">
                <h1 className="text--center">Log In</h1>
                <Login onSwitchToSignup={() => window.location.href = '/signup'} />
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default LoginPage;