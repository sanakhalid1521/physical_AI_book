import express, { Request, Response } from 'express';
import jwt from 'jsonwebtoken';
import User from '../models/User';
import { hashPassword, comparePassword } from '../utils/password';

const router = express.Router();

// Sign up route
router.post('/signup', async (req: Request, res: Response) => {
  try {
    const { email, password, displayName } = req.body;

    // Validation
    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required' });
    }

    if (password.length < 8) {
      return res.status(400).json({ message: 'Password must be at least 8 characters long' });
    }

    // Check if user already exists
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(409).json({ message: 'User with this email already exists' });
    }

    // Hash password
    const hashedPassword = await hashPassword(password);

    // Create new user
    const user = new User({
      email,
      password: hashedPassword,
      displayName: displayName || email.split('@')[0], // Use part of email as default display name
    });

    await user.save();

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

    res.status(201).json({
      message: 'User created successfully',
      user: userData,
      token
    });
  } catch (error) {
    console.error('Sign up error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// Login route
router.post('/login', async (req: Request, res: Response) => {
  try {
    const { email, password } = req.body;

    // Validation
    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required' });
    }

    // Find user by email
    const user = await User.findOne({ email });
    if (!user) {
      return res.status(401).json({ message: 'Invalid email or password' });
    }

    // Compare password
    const isPasswordValid = await comparePassword(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ message: 'Invalid email or password' });
    }

    // Update last login
    user.lastLoginAt = new Date();
    await user.save();

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

    res.json({
      user: userData,
      token
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ message: 'Internal server error' });
  }
});

// Logout route (client-side token removal is sufficient, but we can add server-side invalidation if needed)
router.post('/logout', async (req: Request, res: Response) => {
  res.json({ message: 'Logged out successfully' });
});

export default router;