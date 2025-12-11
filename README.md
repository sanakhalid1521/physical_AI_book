# Physical AI & Humanoid Robotics Textbook

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## RAG Chatbot Integration

This textbook features an integrated RAG (Retrieval-Augmented Generation) chatbot that can answer questions about the textbook content using AI. The system consists of:

- **Frontend**: Docusaurus-based textbook interface with integrated chat widget
- **Backend**: Python FastAPI server with Qwen AI integration
- **Vector Database**: Qdrant for semantic search
- **NLP Services**: Cohere for enhanced processing

## Installation

```bash
npm install
```

## Local Development

### Method 1: Development Mode (Recommended)

1. **Start the Python backend:**
   ```bash
   # On Windows
   start-backend.bat

   # On Linux/Mac
   ./start-backend.sh
   ```

2. **In a separate terminal, start the Docusaurus frontend:**
   ```bash
   npm run start
   ```

### Method 2: Using Yarn (Alternative)

```bash
yarn
yarn start
```

**Note**: When using Method 2, you'll still need to separately start the Python backend using the start-backend script.

## Build

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true npm run deploy
```

Not using SSH:

```bash
GIT_USER=<Your GitHub username> npm run deploy
```

If you are using GitHub pages for hosting, this command is a convenient way to build the website and push to the `gh-pages` branch.

## Troubleshooting

**Issue**: Chatbot input not responding or "chatbot ka input hi nhi le raha he"
**Solution**: Make sure the Python backend is running on port 8000. Run `start-backend.bat` (Windows) or `./start-backend.sh` (Linux/Mac) in a separate terminal.

**Issue**: API connection errors
**Solution**: Verify your API keys in `backend/.env` are correct and have sufficient permissions.
