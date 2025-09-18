# Health Track AI - ML-Powered Fitness & Nutrition Coach

## Overview

Health Track AI is a comprehensive fitness recommendation system that combines machine learning predictions, rule-based recommendations, and AI-powered coaching to provide personalized fitness and nutrition guidance. The system predicts optimal fitness goals using a RandomForest classifier, delivers hybrid recommendations through content-based filtering, and generates personalized advice using AI language models.

The application features a dual-interface design with a main Streamlit app for user interactions and an administrative dashboard for monitoring. A FastAPI backend provides RESTful endpoints for ML predictions, recommendations, and AI-generated content.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Primary Interface**: Streamlit-based web application (`app.py`) for user input and results display
- **Administrative Dashboard**: Separate Streamlit dashboard (`dashboard/app.py`) for monitoring and analytics
- **Visualization**: Integrated matplotlib and seaborn for data visualization and progress tracking
- **API Integration**: Frontend makes HTTP requests to FastAPI backend for all ML and AI operations

### Backend Architecture
- **API Framework**: FastAPI with uvicorn server providing RESTful endpoints
- **CORS Configuration**: Cross-origin resource sharing enabled for frontend-backend communication
- **Request/Response Models**: Pydantic models for data validation and serialization
- **Microservices Pattern**: Modular components (ML predictions, recommendations, AI advice) exposed as separate endpoints

### Machine Learning Architecture
- **Goal Prediction**: RandomForest classifier trained on user demographics and fitness metrics
- **Feature Engineering**: BMI calculation, categorical encoding for gender/activity levels
- **Model Persistence**: Joblib-based model serialization for production deployment
- **Training Pipeline**: Synthetic dataset generation with realistic fitness goal distributions
- **Hybrid Recommendations**: Combination of rule-based logic and content-based filtering

### AI Integration Architecture
- **Language Model**: Groq API integration using Llama-3.1-70b-versatile model
- **Prompt Engineering**: Structured prompts for generating workout advice, nutrition tips, and weekly schedules
- **Response Formatting**: JSON-structured AI responses for consistent frontend consumption
- **Fallback Handling**: Error handling for API timeouts and rate limiting

### Data Architecture
- **In-Memory Processing**: Pandas and NumPy for data manipulation and feature engineering
- **Synthetic Data Generation**: Programmatic dataset creation with realistic fitness correlations
- **Feature Scaling**: BMI calculations and categorical encoding for ML model input
- **Database Design**: Rule-based workout and diet databases stored as Python dictionaries

## External Dependencies

### AI/ML Services
- **Groq API**: Primary language model service for generating personalized fitness and nutrition advice
- **Alternative Models**: OpenAI GPT integration capability built into the codebase structure

### Python Libraries
- **Web Framework**: FastAPI for backend API development, Streamlit for frontend interfaces
- **Machine Learning**: Scikit-learn for RandomForest classification and preprocessing
- **Data Processing**: Pandas for data manipulation, NumPy for numerical computations
- **Visualization**: Matplotlib and Seaborn for charts and progress tracking
- **Model Persistence**: Joblib for saving and loading trained ML models
- **HTTP Client**: Requests library for API communication between frontend and backend

### Development Dependencies
- **Server**: Uvicorn ASGI server for FastAPI deployment
- **Data Validation**: Pydantic for request/response model validation
- **Environment Management**: OS environment variables for API key configuration
- **Cross-Origin Support**: FastAPI CORS middleware for frontend-backend communication

### Deployment Considerations
- **Frontend Deployment**: Streamlit Cloud compatible configuration
- **Backend Deployment**: Render/Heroku compatible FastAPI setup with uvicorn
- **Environment Variables**: GROQ_API_KEY for AI model access
- **Port Configuration**: Default backend on port 8000, frontend auto-configured by Streamlit