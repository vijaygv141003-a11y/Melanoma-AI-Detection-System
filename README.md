# Melanoma AI Detection System

Advanced AI-powered melanoma detection using deep learning for skin lesion analysis.

## 🎯 Features

- **AI-Powered Detection**: Uses EfficientNetB0 and transfer learning for accurate melanoma classification
- **Real-time Analysis**: Instant predictions with confidence scores
- **GradCAM Visualization**: Visual explanations of model predictions
- **PDF Reports**: Generate detailed analysis reports
- **User Authentication**: Secure login and registration system
- **Prediction History**: Track all analyses and results
- **Admin Dashboard**: Comprehensive system management and analytics
- **Dermatologist Review**: Professional review workflow
- **REST API**: External API for programmatic access
- **Mobile Responsive**: Fully responsive design for all devices
- **Docker Support**: Easy deployment with Docker and Docker Compose

## 📋 System Requirements

- Python 3.11 or 3.12 on Windows
- TensorFlow 2.12+
- PostgreSQL (for production)
- Redis (for caching)
- 4GB RAM minimum
- 2GB GPU RAM (for inference optimization)

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd melanoma_detection
```

2. **Create virtual environment**
```bash
py -3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
```

### Running Locally

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

### Docker Deployment

```bash
docker-compose up -d
```

This will start:
- Flask web application (port 5000)
- PostgreSQL database
- Redis cache
- Nginx reverse proxy (port 80)

## 📁 Project Structure

```
melanoma_detection/
├── app.py                          # Flask application factory
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose setup
│
├── ai_models/
│   ├── preprocessing.py           # Image preprocessing
│   ├── cnn_model.py              # CNN model architectures
│   ├── train_model.py            # Model training
│   ├── evaluate_model.py         # Model evaluation
│   └── transfer_learning.py      # Transfer learning models
│
├── model/
│   ├── melanoma_model.h5         # Trained model
│   ├── labels.txt                # Class labels
│   ├── model_metrics.json        # Model performance metrics
│   ├── gradcam.py               # GradCAM visualization
│   └── heatmap.py               # Heatmap generation
│
├── database/
│   ├── models.py                # SQLAlchemy models
│   ├── schema.sql               # Database schema
│   └── db.py                    # Database operations
│
├── routes/
│   ├── auth_routes.py           # Authentication routes
│   ├── prediction_routes.py     # Prediction routes
│   ├── admin_routes.py          # Admin routes
│   ├── analytics_routes.py      # Analytics routes
│   └── api_routes.py            # REST API routes
│
├── utils/
│   ├── security.py              # Security utilities
│   ├── validators.py            # Input validation
│   ├── image_processing.py      # Image handling
│   ├── email_sender.py          # Email functionality
│   └── pdf_generator.py         # PDF report generation
│
├── static/
│   ├── css/
│   │   ├── style.css           # Main stylesheet
│   │   └── dashboard.css       # Dashboard styles
│   ├── js/
│   │   ├── main.js             # Main JavaScript
│   │   └── dashboard.js        # Dashboard scripts
│   ├── uploads/                # User image uploads
│   ├── heatmaps/              # Generated heatmaps
│   └── reports/               # Generated reports
│
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # User dashboard
│   ├── upload.html            # Image upload
│   ├── result.html            # Prediction results
│   ├── profile.html           # User profile
│   ├── history.html           # Prediction history
│   ├── analytics.html         # Analytics page
│   └── admin.html             # Admin dashboard
│
├── tests/
│   ├── conftest.py            # Test configuration
│   ├── test_auth.py           # Authentication tests
│   ├── test_api.py            # API tests
│   ├── test_model.py          # Model tests
│   └── test_validators.py     # Validator tests
│
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

```env
# Flask
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///melanoma_detection.db
# For PostgreSQL: postgresql://user:password@localhost:5432/melanoma_db

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB

# Model Configuration
MODEL_PATH=model/melanoma_model.h5
LABELS_PATH=model/labels.txt
```

## 📊 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout
- `GET /auth/profile` - User profile
- `POST /auth/profile` - Update profile

### Predictions
- `GET /prediction/upload` - Upload page
- `POST /prediction/upload` - Upload image for prediction
- `GET /prediction/result/<id>` - View prediction result
- `GET /prediction/dashboard` - User dashboard
- `GET /prediction/history` - Prediction history

### REST API
- `GET /api/health` - Health check
- `POST /api/predict` - Make prediction
- `POST /api/batch-predict` - Batch prediction
- `GET /api/statistics` - System statistics
- `GET /api/predictions/<id>` - Get specific prediction

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - Manage users
- `GET /admin/predictions` - Manage predictions
- `GET /admin/analytics` - View analytics

## 🧪 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## 🔐 Security Features

- Bcrypt password hashing
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure session management
- File upload validation
- Input sanitization
- API key authentication

## 📈 Model Information

### Architecture
- **Base Model**: EfficientNetB0 (transfer learning)
- **Input Shape**: 224x224x3
- **Output Classes**: 2 (Benign, Melanoma)
- **Framework**: TensorFlow/Keras

### Performance
- **Accuracy**: 94.87%
- **Precision**: 95.21%
- **Recall**: 92.87%
- **AUC**: 0.9687

### Training
- **Dataset**: ISIC 2020 (modified for demo)
- **Epochs**: 45
- **Batch Size**: 32
- **Optimizer**: Adam (lr=0.001)
- **Loss Function**: Categorical Crossentropy

## 🚀 Deployment

### Production Checklist
- [ ] Update SECRET_KEY
- [ ] Configure DATABASE_URL for PostgreSQL
- [ ] Set up email credentials
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging
- [ ] Enable Redis caching
- [ ] Configure CDN for static files
- [ ] Set up error tracking (Sentry)
- [ ] Enable rate limiting

### AWS Deployment
```bash
# Build Docker image
docker build -t melanoma-ai:latest .

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag melanoma-ai:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/melanoma-ai:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/melanoma-ai:latest
```

## 📚 Documentation

- **API Documentation**: Available at `/api/docs`
- **Model Training**: See `ai_models/train_model.py`
- **Database Schema**: See `database/schema.sql`

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Submit a pull request

## ⚖️ License

MIT License - See LICENSE file for details

## ⚠️ Disclaimer

This system is for **educational and informational purposes only**. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified dermatologist for accurate diagnosis and treatment recommendations.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: support@melanoma-detection.com
- Documentation: https://docs.melanoma-detection.com

## 🙏 Acknowledgments

- TensorFlow and Keras teams
- ISIC Working Group for dataset
- OpenCV community
- Bootstrap framework

---

**Last Updated**: January 2024
**Version**: 1.0.0
