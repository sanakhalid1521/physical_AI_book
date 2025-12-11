import passport from 'passport';
import { Strategy as GoogleStrategy } from 'passport-google-oauth20';
import User from '../models/User';
import { hashPassword } from './password';

// Configure Google OAuth strategy
passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
      callbackURL: '/api/auth/google/callback',
    },
    async (accessToken, refreshToken, profile, done) => {
      try {
        // Check if user already exists
        let user = await User.findOne({ email: profile.emails?.[0].value });

        if (user) {
          // User exists, return the user
          return done(null, user);
        }

        // User doesn't exist, create a new user
        // Generate a temporary password since Google auth doesn't require one
        const tempPassword = `google_${profile.id}_${Date.now()}`;
        const hashedPassword = await hashPassword(tempPassword);

        user = new User({
          email: profile.emails?.[0].value,
          password: hashedPassword, // This is a generated password for OAuth users
          displayName: profile.displayName || profile.emails?.[0].value.split('@')[0],
        });

        await user.save();
        return done(null, user);
      } catch (error) {
        return done(error as any, undefined);
      }
    }
  )
);

// Serialize user for session
passport.serializeUser((user: any, done) => {
  done(null, user._id);
});

// Deserialize user from session
passport.deserializeUser(async (id: string, done) => {
  try {
    const user = await User.findById(id);
    done(null, user);
  } catch (error) {
    done(error, null);
  }
});

export default passport;