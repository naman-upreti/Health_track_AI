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

# Import prediction function
try:
    from train_model import predict_fitness_goal
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
            "meal_plan": "/meal_plan"
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
