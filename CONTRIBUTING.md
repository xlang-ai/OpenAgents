# Contributing to OpenAgents

Welcome and thank you for considering a contribution to OpenAgents! As an evolving open-source project, 
we truly value all forms of contribution – whether it's adding new features, 
refining our infrastructure, enhancing documentation, or resolving bugs.

## 🗺️ Guidelines

### 👩‍💻 Code Contributions

1. **Fork & PR Workflow**: We use a ["fork and pull request"](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) model. Please avoid pushing directly to the main repo unless you're a maintainer.
3. **PR Template**: When initiating a pull request, adhere to the provided template. Ensure to link related issues and mention relevant maintainers.

### 🚩 Managing GitHub Issues

1. **Existing Issues**: Explore our up-to-date [issues page](https://github.com/langchain-ai/langchain/issues) for bugs, suggestions, and feature needs.
2. **Fixing Issues**: If an issue sparks your interest, comment on it to get it assigned to you by a maintainer.
3. **Creating New Issues**: When adding a new issue, please try to keep it focused on a single, modular bug/improvement/feature. If two issues are related, or blocking, please link them rather than combining them.
4. **Stay Updated**: The rapid pace of developments might occasionally lead to outdated issues. Your prompt notifications on such instances would be appreciated.

### 🙋 Need Assistance?

**Developer Experience Matters**: Our vision is to offer a seamless developer setup. If you hit a snag at any point, don't hesitate to reach out to a maintainer. Not only are we here to help, but your feedback also aids in refining the experience for subsequent contributors.

## 🚀 Quick Setup

- **Frontend**: Get started with the frontend by following the guidelines [here](https://github.com/xlang-ai/OpenAgents/blob/main/frontend/README.md).
- **Backend**: Set up the backend using instructions available [here](https://github.com/xlang-ai/OpenAgents/blob/main/backend/README.md).

## 🗺️ Contributing Steps

- **Fork the Repository:**
  Start by forking the OpenAgents repository on GitHub. This creates a copy of the project under your 
  GitHub account, which you can freely modify.

- **Clone the Repository:**
  Use the `git clone` command to create a local copy of your forked repository. Replace `<your-forked-repo-url>` with the URL of your forked repository:
  ```bash
    git clone <your-forked-repo-url>
  ```

- **Create a New Branch:**
  Before making changes, create a new branch where you'll work on your specific contribution. Give the branch a descriptive name:
  ```bash
     git branch <branch-name>
  ```

- **Switch to the New Branch:**
  Use the `git checkout` command to switch to the new branch:
  ```bash
    git checkout <branch-name>
  ```

- **Make Changes:**
  Make your desired changes to the code, documentation, or other project files.

- **Stage Changes:**
  Use `git add` to stage the changes you've made for commit. You can specify individual files or use a wildcard to stage all changes:

  ```bash
    git add <file1> <file2>   # Stage specific files
    git add .                # Stage all changes
  ```

- **Commit Changes:**
  Commit your staged changes with a descriptive message using `git commit`:
  ```bash
     git commit -m "Your commit message here"
  ```

- **Push Changes to Your Fork:**
   Push your branch with the changes to your forked repository on GitHub:
  ```bash
    git push origin <branch-name>
  ```

- **Create a Pull Request:**
  Visit your forked repository on GitHub and create a Pull Request(PR).

  > Once your pull request is approved, it can be merged into the main project repository.










  
