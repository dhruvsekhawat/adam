# Adam AI - Executive Assistant

An AI-driven executive assistant web application designed for busy business owners. This application automates routine tasks like sending emails, scheduling meetings, triggering DocuSign workflows, and handling Slack messages using natural language commands.

## 🚀 Tech Stack

### Frontend
- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- React Query
- Radix UI Components
- Theme support (dark/light mode)

### Backend
- FastAPI (Python)
- PostgreSQL
- LangChain
- SQLAlchemy

### Infrastructure
- Docker & Docker Compose
- Environment-based configuration
- Health monitoring

## 🛠 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Git

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/adam-ai.git
cd adam-ai
```

2. Set up environment files:

Create backend environment file (backend/config/.env.development):
```bash
cp backend/config/.env.example backend/config/.env.development
```

Create frontend environment file:
```bash
cp frontend/.env.example frontend/.env.development
```

3. Start the application:

Development mode:
```bash
docker-compose up --build
```

Production mode:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 📁 Project Structure

```
adam-ai/
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI entry point
│   │   ├── routers/            # API endpoints
│   │   ├── models/             # Database models
│   │   ├── services/           # Business logic
│   │   └── utils/             # Helper functions
│   ├── config/
│   │   ├── .env.example       # Example environment variables
│   │   └── config.py          # Configuration management
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Backend Docker configuration
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js pages
│   │   ├── components/       # React components
│   │   └── lib/             # Utilities and hooks
│   ├── .env.example         # Example environment variables
│   └── Dockerfile          # Frontend Docker configuration
└── docker-compose.yml      # Docker composition
```

## 🔧 Development

### Running Tests
```bash
# Backend tests
docker-compose exec backend pytest

# Frontend tests
docker-compose exec frontend npm test
```

### Code Style
- Backend: Black formatter, isort for imports
- Frontend: ESLint, Prettier

### Environment Variables

#### Backend (.env.development)
- `ENV`: development/production
- `DEBUG`: true/false
- `POSTGRES_*`: Database configuration
- `SECRET_KEY`: Application secret key

#### Frontend (.env.development)
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_WS_URL`: WebSocket URL
- `NEXT_PUBLIC_ENV`: Environment name

## 🔐 Security

- Non-root Docker containers
- Environment-based configurations
- CORS protection
- Rate limiting (TODO)
- API authentication (TODO)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- None currently

## 🗺 Roadmap

- [ ] User authentication
- [ ] Email integration
- [ ] Calendar management
- [ ] Document processing
- [ ] Slack integration
- [ ] Mobile responsiveness improvements