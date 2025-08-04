# Data Breach Analysis Tool

A comprehensive full-stack application for analyzing historical data breach records using machine learning and predictive analytics.

## 🚀 Features

- **Dashboard Analytics**: Real-time statistics and visualizations
- **Data Breach Management**: CRUD operations for breach records
- **Predictive Analytics**: ML-powered risk assessment
- **Trend Analysis**: Yearly and categorical trend analysis
- **User Authentication**: Secure login/registration system
- **Responsive UI**: Modern Material-UI interface

## 🛠️ Tech Stack

### Backend

- **Node.js** with Express.js
- **MongoDB** for data storage
- **JWT** for authentication
- **RESTful APIs**

### Frontend

- **React.js** with hooks
- **Material-UI** for components
- **Recharts** for data visualization
- **React Router** for navigation
- **Axios** for API calls

### Machine Learning

- **Python** with Flask
- **Scikit-learn** for ML models
- **Pandas & NumPy** for data processing
- **TensorFlow/Keras** for deep learning
- **Matplotlib & Seaborn** for visualization

## 📁 Project Structure

```
data-breach-analysis-tool/
├── backend/                 # Node.js Express server
│   ├── controllers/         # Business logic
│   ├── middleware/          # Auth middleware
│   ├── models/             # MongoDB schemas
│   ├── routes/             # API routes
│   └── server.js           # Main server file
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   └── App.js         # Main app component
│   └── package.json
├── python-ml/              # Python ML service
│   ├── app.py             # Flask ML API
│   ├── data_processor.py  # Data preprocessing
│   └── requirements.txt   # Python dependencies
├── data/                   # Sample data files
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- MongoDB (local or cloud)
- npm or yarn

### 1. Clone the Repository

```bash
git clone <repository-url>
cd data-breach-analysis-tool
```

### 2. Backend Setup

```bash
cd backend
npm install
```

Create a `.env` file in the backend directory:

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/data-breach-analysis
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
NODE_ENV=development
```

Start the backend server:

```bash
npm run dev
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

Start the React development server:

```bash
npm start
```

### 4. Python ML Service Setup

```bash
cd python-ml
pip install -r requirements.txt
```

Create a `.env` file in the python-ml directory:

```env
MONGO_URI=mongodb://localhost:27017/data-breach-analysis
ML_PORT=5001
```

Start the ML service:

```bash
python app.py
```

## 📊 API Endpoints

### Authentication

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Data Breaches

- `GET /api/breaches` - Get all breaches (with pagination)
- `GET /api/breaches/stats` - Get breach statistics
- `POST /api/breaches` - Create new breach
- `PUT /api/breaches/:id` - Update breach
- `DELETE /api/breaches/:id` - Delete breach

### Analysis

- `GET /api/analysis` - Get analysis history
- `GET /api/analysis/trends/yearly` - Yearly trends
- `GET /api/analysis/trends/by-type` - Breach type analysis
- `POST /api/analysis/predictive` - Predictive analysis

### ML Service

- `GET /health` - Health check
- `POST /predict` - Risk prediction
- `POST /train` - Retrain model

## 🎯 Usage

1. **Register/Login**: Create an account or sign in
2. **Dashboard**: View overview statistics and charts
3. **Data Breaches**: Manage breach records with filtering
4. **Analysis**: Run predictive analytics on organizations

## 🔧 Development

### Adding New Features

1. Backend: Add routes in `backend/routes/`
2. Frontend: Create components in `frontend/src/components/`
3. ML: Extend models in `python-ml/app.py`

### Database Schema

```javascript
// User Schema
{
  name: String,
  email: String,
  password: String (hashed),
  createdAt: Date
}

// DataBreach Schema
{
  organization: String,
  breachType: String,
  date: Date,
  recordsCompromised: Number,
  description: String,
  year: Number
}

// Analysis Schema
{
  user: ObjectId,
  analysisType: String,
  parameters: Object,
  results: Object,
  status: String,
  createdAt: Date
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Material-UI for the beautiful components
- Recharts for data visualization
- Scikit-learn for machine learning capabilities
- MongoDB for flexible data storage
