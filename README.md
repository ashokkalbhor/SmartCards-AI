# SmartCards AI 💳

> Your intelligent credit card companion that maximizes rewards on every purchase

## 🚀 What it does

SmartCards AI tells you which credit card to use for maximum rewards based on the cards you already hold. Get instant answers to questions like:

- "Best card for Swiggy?"
- "Which card gives more at Croma offline?"
- "Best option for Amazon purchases?"

## ✨ Features

### Core Features
- **Smart Card Recommendations**: AI-powered suggestions for optimal card usage
- **User Management**: Secure authentication and profile management
- **Card Portfolio**: Remember and manage all your credit cards
- **Reward Tracking**: Monitor your rewards and cashback earnings
- **Real-time Updates**: Get instant recommendations based on current offers
- **Automated Card Updates**: GenAI-powered monthly updates to keep card data current (see [Admin Guide](ADMIN_CARD_UPDATES.md))

### Premium UI/UX
- **Smooth Animations**: Fluid transitions and micro-interactions
- **Dark/Light Mode**: Personalized theme preferences
- **Responsive Design**: Works seamlessly across all devices

### Multi-Platform Support
- **Web Application**: React-based web app
- **iOS App**: Native iOS experience
- **Android App**: Native Android experience
- **Cross-platform Sync**: Seamless data synchronization

## 🛠 Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **PostgreSQL** - Robust relational database
- **Redis** - Caching and session management
- **SQLAlchemy** - Database ORM
- **JWT** - Secure authentication
- **Pydantic** - Data validation

### Frontend
- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **React Query** - State management

### Mobile
- **React Native** - Cross-platform mobile development
- **Expo** - Development platform
- **React Native Paper** - Material Design components

### Infrastructure
- **Docker** - Containerization
- **Nginx** - Reverse proxy
- **AWS/GCP** - Cloud hosting
- **CI/CD** - Automated deployment

## 📁 Project Structure

```
smartcards-ai/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React web app
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── Dockerfile
├── mobile/                 # React Native app
│   ├── src/
│   │   ├── components/     # Mobile components
│   │   ├── screens/        # Screen components
│   │   └── navigation/     # Navigation setup
│   ├── package.json
│   └── app.json
├── docs/                   # Documentation
├── docker-compose.yml      # Development environment
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL
- Redis
- Docker (optional)

### Backend Setup
```bash
cd backend
python -m venv venv311
source venv311/bin/activate  # On Windows: venv311\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Mobile Setup
```bash
cd mobile
npm install
npx expo start
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for password security
- **Rate Limiting**: API protection against abuse
- **CORS**: Cross-origin resource sharing
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Parameterized queries

## 📱 Mobile App Features

- **Offline Support**: Cache card data locally
- **Push Notifications**: Real-time card recommendations
- **Biometric Authentication**: Fingerprint/Face ID support
- **Widget Support**: Quick access to recommendations
- **Deep Linking**: Seamless app navigation

## 🎨 Design System

Our design system is inspired by modern fintech apps like Cred, featuring:

- **Color Palette**: Premium gradients and modern colors
- **Typography**: Clean, readable fonts
- **Icons**: Consistent iconography
- **Spacing**: Systematic spacing scale
- **Components**: Reusable UI components

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💼 Admin Features

### Automated Card Data Updates
The platform includes a GenAI-powered system that automatically keeps credit card information up-to-date:

- **Monthly Automated Updates**: Runs on the 1st of every month
- **Manual Triggers**: Admin can update all cards or specific cards on-demand
- **Approval Workflow**: All automated changes require admin review
- **Community Transparency**: Approved changes are posted to community

**For Admins**: See [ADMIN_CARD_UPDATES.md](ADMIN_CARD_UPDATES.md) for complete documentation and [ADMIN_QUICK_REFERENCE.md](ADMIN_QUICK_REFERENCE.md) for quick commands.

## 🆘 Support

For support, email support@smartcardsai.com or join our Discord community.

---

Built with ❤️ for smart credit card users everywhere. 
