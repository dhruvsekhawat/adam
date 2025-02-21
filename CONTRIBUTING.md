# Contributing to Adam AI

We love your input! We want to make contributing to Adam AI as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html)
Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Process

1. Clone the repository:
```bash
git clone https://github.com/yourusername/adam-ai.git
cd adam-ai
```

2. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

3. Set up development environment:
```bash
# Copy environment files
cp backend/config/.env.example backend/config/.env.development
cp frontend/.env.example frontend/.env.development

# Start development environment
docker-compose up --build
```

4. Make your changes and test them:
```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test
```

## Code Style

### Backend (Python)
- Use Black for formatting
- Use isort for import sorting
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions and classes

### Frontend (TypeScript/React)
- Use ESLint and Prettier
- Follow React best practices
- Use functional components
- Write clean, reusable components
- Add proper TypeScript types

## Commit Messages
- Use clear and meaningful commit messages
- Start with a verb in present tense
- Keep the first line under 72 characters
- Reference issues and pull requests

Example:
```
Add user authentication system

- Implement JWT token authentication
- Add login and registration endpoints
- Create user model
- Add tests for authentication flow

Fixes #123
```

## Any contributions you make will be under the MIT Software License
In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issue tracker](https://github.com/yourusername/adam-ai/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/adam-ai/issues/new).

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License
By contributing, you agree that your contributions will be licensed under its MIT License. 