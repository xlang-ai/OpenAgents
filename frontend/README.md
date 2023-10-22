# Frontend Environment Setup

Before you begin, make sure you've got the necessary tools:

- [node.js](https://nodejs.org/en/) - JavaScript runtime.
- [npm](https://www.npmjs.com/) - Node.js package manager.

Follow these steps to set up the frontend:

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the required packages:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

Once started, the frontend UI will be accessible at `http://localhost:3000`.

To set up the Chrome extension for Web Agent, follow these steps:

1. Unzip `webot_extension.zip` at the `frontend` directory
2. Navigate to `chrome://extensions/`
3. Toggle `Developer mode`
4. Click on `Load unpacked extension`
5. Select the unzipped `builder` folder

The extension named `XLang Web Agent` will be available on your Chrome now.

## One Click Deploy With Vercel

[![Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fxlang-ai%2FOpenAgents%2Ftree%2Fmain%2Ffrontend)
