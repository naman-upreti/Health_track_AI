from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
import sys

# Add the ml directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml'))

from recommender import FitnessRecommender
from genai import FitnessAIAdvisor
from database import db

# Import prediction function
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from ml.train_model import predict_fitness_goal
except ImportError:
    def predict_fitness_goal(*args, **kwargs):
        return {"predicted_goal": "Maintenance", "confidence": 0.5, "probabilities": {"Maintenance": 0.5}}

app = FastAPI(
    title="Health Track AI API",
    description="Advanced AI-powered fitness recommendation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
recommender = FitnessRecommender()
ai_advisor = FitnessAIAdvisor()

class UserProfile(BaseModel):
    age: int
    weight: float
    height: float
    gender: str
    activity_level: str
    experience_level: Optional[str] = "Beginner"
    fitness_goal: Optional[str] = None

class PredictionRequest(BaseModel):
    age: int
    weight: float
    height: float
    gender: str
    activity_level: str
    experience_level: Optional[str] = "Beginner"

class ProgressEntry(BaseModel):
    user_id: int
    log_type: str
    date: str
    value: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    data: Optional[Dict] = None

class UserRegistration(BaseModel):
    email: str
    password: str
    full_name: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[str] = None
    activity_level: Optional[str] = None
    experience_level: Optional[str] = None
    fitness_goal: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfileUpdate(BaseModel):
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[str] = None
    activity_level: Optional[str] = None
    experience_level: Optional[str] = None
    fitness_goal: Optional[str] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Health Track AI API",
        "status": "active",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "recommend": "/recommend", 
            "genai": "/genai",
            "full_plan": "/full_plan",
            "meal_plan": "/meal_plan",
            "progress": "/progress",
            "auth": {
                "register": "/auth/register",
                "login": "/auth/login",
                "profile": "/auth/profile"
            }
        }
    }

@app.post("/predict")
async def predict_goal(request: PredictionRequest):
    """Predict fitness goal based on user profile"""
    try:
        # Calculate BMI
        bmi = request.weight / ((request.height / 100) ** 2)
        
        # Make prediction
        prediction_result = predict_fitness_goal(
            age=request.age,
            weight=request.weight,
            height=request.height,
            gender=request.gender,
            activity_level=request.activity_level,
            experience_level=request.experience_level
        )
        
        return {
            "success": True,
            "user_profile": {
                "age": request.age,
                "weight": request.weight,
                "height": request.height,
                "gender": request.gender,
                "activity_level": request.activity_level,
                "experience_level": request.experience_level,
                "bmi": round(bmi, 2)
            },
            "prediction": prediction_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/recommend")
async def get_recommendations(profile: UserProfile):
    """Get workout and diet recommendations"""
    try:
        # Calculate BMI
        bmi = profile.weight / ((profile.height / 100) ** 2)
        
        user_data = {
            "age": profile.age,
            "weight": profile.weight,
            "height": profile.height,
            "gender": profile.gender,
            "activity_level": profile.activity_level,
            "experience_level": profile.experience_level,
            "fitness_goal": profile.fitness_goal or "Maintenance",
            "bmi": bmi
        }
        
        # Get rule-based recommendations
        rule_based = recommender.get_rule_based_recommendations(user_data)
        
        # Get content-based recommendations
        content_based = recommender.get_content_based_recommendations(user_data)
        
        return {
            "success": True,
            "user_profile": user_data,
            "rule_based_recommendations": rule_based,
            "content_based_recommendations": content_based
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")

@app.post("/genai")
async def get_ai_advice(profile: UserProfile):
    """Get AI-generated personalized advice"""
    try:
        # Calculate BMI
        bmi = profile.weight / ((profile.height / 100) ** 2)
        
        user_data = {
            "age": profile.age,
            "weight": profile.weight,
            "height": profile.height,
            "gender": profile.gender,
            "activity_level": profile.activity_level,
            "experience_level": profile.experience_level,
            "fitness_goal": profile.fitness_goal or "Maintenance",
            "bmi": bmi
        }
        
        # Generate AI advice
        ai_result = ai_advisor.generate_fitness_advice(user_data)
        
        return {
            "success": True,
            "user_profile": user_data,
            "ai_advice": ai_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI advice generation failed: {str(e)}")

@app.post("/meal_plan")
async def get_meal_plan(profile: UserProfile):
    """Get AI-generated meal plan"""
    try:
        # Calculate BMI
        bmi = profile.weight / ((profile.height / 100) ** 2)
        
        user_data = {
            "age": profile.age,
            "weight": profile.weight,
            "height": profile.height,
            "gender": profile.gender,
            "activity_level": profile.activity_level,
            "experience_level": profile.experience_level,
            "fitness_goal": profile.fitness_goal or "Maintenance",
            "bmi": bmi
        }
        
        # Generate meal plan
        meal_plan_result = ai_advisor.generate_meal_plan(user_data)
        
        return {
            "success": True,
            "user_profile": user_data,
            "meal_plan": meal_plan_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Meal plan generation failed: {str(e)}")

@app.post("/full_plan")
async def get_full_plan(request: PredictionRequest):
    """Get complete health and fitness plan including prediction, recommendations, and AI advice"""
    try:
        # Calculate BMI
        bmi = request.weight / ((request.height / 100) ** 2)
        
        # Step 1: Predict fitness goal
        prediction_result = predict_fitness_goal(
            age=request.age,
            weight=request.weight,
            height=request.height,
            gender=request.gender,
            activity_level=request.activity_level,
            experience_level=request.experience_level
        )
        
        predicted_goal = prediction_result.get('predicted_goal', 'Maintenance')
        
        # Create user profile with predicted goal
        user_data = {
            "age": request.age,
            "weight": request.weight,
            "height": request.height,
            "gender": request.gender,
            "activity_level": request.activity_level,
            "experience_level": request.experience_level,
            "fitness_goal": predicted_goal,
            "bmi": bmi
        }
        
        # Step 2: Get recommendations
        rule_based = recommender.get_rule_based_recommendations(user_data)
        content_based = recommender.get_content_based_recommendations(user_data)
        
        # Step 3: Get AI advice
        ai_result = ai_advisor.generate_fitness_advice(user_data)
        
        # Step 4: Get meal plan
        meal_plan_result = ai_advisor.generate_meal_plan(user_data)
        
        return {
            "success": True,
            "user_profile": user_data,
            "prediction": prediction_result,
            "recommendations": {
                "rule_based": rule_based,
                "content_based": content_based
            },
            "ai_advice": ai_result,
            "meal_plan": meal_plan_result,
            "summary": {
                "predicted_goal": predicted_goal,
                "confidence": prediction_result.get('confidence', 0.5),
                "bmi": round(bmi, 2),
                "bmi_category": get_bmi_category(bmi)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full plan generation failed: {str(e)}")

# Progress Tracking Endpoints
@app.post("/progress")
async def add_progress_entry(entry: ProgressEntry):
    """Add a progress entry for a user"""
    try:
        from datetime import datetime
        entry_date = datetime.strptime(entry.date, '%Y-%m-%d').date()
        
        entry_id = db.log_progress(
            user_id=entry.user_id,
            log_type=entry.log_type,
            date=entry_date,
            value=entry.value,
            unit=entry.unit,
            notes=entry.notes,
            data=entry.data
        )
        
        if entry_id:
            return {
                "success": True,
                "message": "Progress entry added successfully",
                "entry_id": entry_id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to add progress entry")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Progress entry failed: {str(e)}")

@app.get("/progress/{user_id}")
async def get_user_progress(user_id: int, log_type: Optional[str] = None, limit: int = 100):
    """Get user progress entries"""
    try:
        progress_data = db.get_user_progress(user_id, log_type, limit)
        summary = db.get_progress_summary(user_id)
        
        return {
            "success": True,
            "user_id": user_id,
            "progress": progress_data,
            "summary": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get progress data: {str(e)}")

# Authentication Endpoints
@app.post("/auth/register")
async def register_user(user_data: UserRegistration):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.execute_query(
            "SELECT id FROM users WHERE email = %s", 
            (user_data.email,), 
            fetch_one=True
        )
        
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists with this email")
        
        # Create user profile data
        profile_data = {
            'age': user_data.age,
            'weight': user_data.weight,
            'height': user_data.height,
            'gender': user_data.gender,
            'activity_level': user_data.activity_level,
            'experience_level': user_data.experience_level,
            'fitness_goal': user_data.fitness_goal
        }
        
        # Create user
        user_id = db.create_user(user_data.email, user_data.password, user_data.full_name, profile_data)
        
        if user_id:
            return {
                "success": True,
                "message": "User registered successfully",
                "user_id": user_id
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/auth/login")
async def login_user(login_data: UserLogin):
    """Authenticate user login"""
    try:
        user = db.authenticate_user(login_data.email, login_data.password)
        
        if user:
            return {
                "success": True,
                "message": "Login successful",
                "user": user
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@app.get("/auth/profile/{user_id}")
async def get_user_profile(user_id: int):
    """Get user profile"""
    try:
        profile = db.get_user_profile(user_id)
        
        if profile:
            return {
                "success": True,
                "profile": profile
            }
        else:
            raise HTTPException(status_code=404, detail="User not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(e)}")

@app.put("/auth/profile/{user_id}")
async def update_user_profile(user_id: int, profile_data: UserProfileUpdate):
    """Update user profile"""
    try:
        # Convert to dict and remove None values
        update_data = {k: v for k, v in profile_data.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid data to update")
        
        success = db.update_user_profile(user_id, update_data)
        
        if success:
            return {
                "success": True,
                "message": "Profile updated successfully"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to update profile")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile update failed: {str(e)}")

def get_bmi_category(bmi: float) -> str:
    """Categorize BMI value"""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
