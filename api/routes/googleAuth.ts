import express, { Request, Response } from 'express';
import passport from 'passport';
import jwt from 'jsonwebtoken';
import User from '../models/User';

const router = express.Router();

// Google OAuth login route
router.get('/google',
  passport.authenticate('google', { scope: ['profile', 'email'] })
);

// Google OAuth callback route
router.get('/google/callback',
  passport.authenticate('google', { session: false }),
  async (req: Request, res: Response) => {
    try {
      // Check if the user object exists (from passport strategy)
      if (!req.user) {
        return res.status(401).json({ message: 'Authentication failed' });
      }

      const user = req.user as any;

      // Generate JWT token
      const JWT_SECRET = process.env.JWT_SECRET || 'fallback_secret_for_development';
      const token = jwt.sign(
        { userId: user._id, email: user.email },
        JWT_SECRET,
        { expiresIn: '30d' } // Token valid for 30 days
      );

      // Return user data and token (without password)
      const userData = {
        id: user._id,
        email: user.email,
        displayName: user.displayName,
      };

      // In a production app, you'd want to redirect to your frontend with the token
      // For now, we'll send a simple HTML page that stores the token and redirects
      const frontendUrl = process.env.FRONTEND_URL || 'http://localhost:3000';
      const html = `
        <!DOCTYPE html>
        <html>
        <head>
          <title>Authenticating...</title>
        </head>
        <body>
          <script>
            // Store the token and user in localStorage
            localStorage.setItem('authToken', '${token}');
            localStorage.setItem('user', JSON.stringify(${JSON.stringify(userData)}));

            // Redirect back to the frontend
            window.location.href = '${frontendUrl}';
          </script>
        </body>
        </html>
      `;
      res.send(html);
    } catch (error) {
      console.error('Google OAuth error:', error);
      res.status(500).json({ message: 'Internal server error' });
    }
  }
);

export default router;