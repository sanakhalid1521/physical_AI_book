import express, { Request, Response } from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import dotenv from 'dotenv';
import passport from 'passport';
import session from 'express-session';
import { createProxyMiddleware } from 'http-proxy-middleware';
import authRoutes from './api/routes/auth';
import googleAuthRoutes from './api/routes/googleAuth';
import passportSetup from './api/utils/passport';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000', // Allow your frontend origin
  credentials: true // Allow cookies/credentials to be sent
}));
app.use(express.json());

// Session configuration
app.use(session({
  secret: process.env.SESSION_SECRET || 'fallback_session_secret',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production' ? true : false, // Secure in production
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  }
}));

// Passport middleware
app.use(passport.initialize());
app.use(passport.session());

// Proxy middleware for RAG API
const ragProxy = createProxyMiddleware({
  target: 'http://localhost:8000', // Python FastAPI backend
  changeOrigin: true,
  pathRewrite: {
    '^/api/query': '/api/v1/query', // Rewrite /api/query to /api/v1/query
    '^/api/chat': '/api/v1/chat',   // Rewrite /api/chat to /api/v1/chat
    '^/api/documents': '/api/v1/documents', // Rewrite /api/documents to /api/v1/documents
    '^/api/rag': '/api/v1', // Rewrite /api/rag to /api/v1
  },
  onProxyReq: (proxyReq, req, res) => {
    console.log(`Proxying ${req.method} ${req.url} to http://localhost:8000`);
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`Response from Python backend: ${proxyRes.statusCode} ${req.url}`);
  }
});

// Proxy RAG-related routes to Python backend
app.use('/api/query', ragProxy);
app.use('/api/chat', ragProxy);
app.use('/api/documents', ragProxy);
app.use('/api/rag', ragProxy);

// Other routes
app.use('/api/auth', authRoutes);
app.use('/api/auth', googleAuthRoutes);

// Health check endpoint
app.get('/api/health', (req: Request, res: Response) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Connect to MongoDB
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/learningbook';

mongoose.connect(MONGODB_URI)
  .then(() => {
    console.log('Connected to MongoDB');

    // Start server only after DB connection
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
      console.log(`Authentication API available at http://localhost:${PORT}/api/auth`);
    });
  })
  .catch((error) => {
    console.error('Error connecting to MongoDB:', error);
    process.exit(1);
  });

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\nShutting down gracefully...');
  await mongoose.connection.close();
  process.exit(0);
});