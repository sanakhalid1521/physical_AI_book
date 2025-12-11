import React from 'react';
import Layout from '@theme/Layout';
import SignUp from '../components/Auth/SignUp';
import { useAuth } from '../components/Auth/AuthContext';

function SignupPage(): JSX.Element {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return (
      <Layout title="Sign Up" description="Create a new account">
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
    <Layout title="Sign Up" description="Create a new account">
      <main>
        <div className="container margin-vert--lg">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <div className="padding-vert--md">
                <h1 className="text--center">Sign Up</h1>
                <SignUp onSwitchToLogin={() => window.location.href = '/login'} />
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}

export default SignupPage;