import os
import json
from groq import Groq

class FitnessAIAdvisor:
    def __init__(self):
        """Initialize the Groq client"""
        # Using Groq for free API access with fast inference
        api_key = os.getenv("GROQ_API_KEY", "gsk-default-key")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-70b-versatile"
    
    def generate_fitness_advice(self, user_profile):
        """Generate personalized fitness and nutrition advice"""
        try:
            # Create a comprehensive prompt
            prompt = f"""
            You are a certified fitness trainer and nutritionist. Generate personalized advice for the following user:
            
            User Profile:
            - Age: {user_profile.get('age', 'Unknown')}
            - Weight: {user_profile.get('weight', 'Unknown')} kg
            - Height: {user_profile.get('height', 'Unknown')} cm
            - Gender: {user_profile.get('gender', 'Unknown')}
            - Activity Level: {user_profile.get('activity_level', 'Unknown')}
            - Fitness Goal: {user_profile.get('fitness_goal', 'Unknown')}
            - Experience Level: {user_profile.get('experience_level', 'Beginner')}
            - BMI: {user_profile.get('bmi', 'Unknown')}
            
            Provide personalized advice in JSON format with the following structure:
            {{
                "workout_advice": [
                    "Specific workout tip 1",
                    "Specific workout tip 2", 
                    "Specific workout tip 3"
                ],
                "nutrition_advice": [
                    "Specific nutrition tip 1",
                    "Specific nutrition tip 2",
                    "Specific nutrition tip 3"
                ],
                "lifestyle_tips": [
                    "Lifestyle recommendation 1",
                    "Lifestyle recommendation 2"
                ],
                "weekly_schedule": {{
                    "monday": "Recommended activity",
                    "tuesday": "Recommended activity",
                    "wednesday": "Recommended activity",
                    "thursday": "Recommended activity",
                    "friday": "Recommended activity",
                    "saturday": "Recommended activity",
                    "sunday": "Recommended activity"
                }},
                "motivation_message": "Personalized motivational message"
            }}
            
            Make sure all advice is specific to the user's profile, safe, and evidence-based.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert fitness trainer and nutritionist. Provide safe, personalized, and evidence-based fitness advice. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            if content:
                advice = json.loads(content)
                return {
                    "success": True,
                    "advice": advice
                }
            else:
                return {
                    "success": False,
                    "error": "Empty response from AI",
                    "advice": self._get_fallback_advice(user_profile)
                }
            
        except Exception as e:
            print(f"Error generating AI advice: {e}")
            return {
                "success": False,
                "error": str(e),
                "advice": self._get_fallback_advice(user_profile)
            }
    
    def _get_fallback_advice(self, user_profile):
        """Provide fallback advice when AI is unavailable"""
        goal = user_profile.get('fitness_goal', 'Maintenance')
        
        fallback_advice = {
            "workout_advice": [
                f"Focus on exercises that support your {goal.lower()} goal",
                "Start with 3-4 workout sessions per week",
                "Include both cardio and strength training"
            ],
            "nutrition_advice": [
                "Eat a balanced diet with adequate protein",
                "Stay hydrated with 8-10 glasses of water daily",
                "Include plenty of fruits and vegetables"
            ],
            "lifestyle_tips": [
                "Get 7-9 hours of quality sleep",
                "Manage stress through relaxation techniques"
            ],
            "weekly_schedule": {
                "monday": "Full body strength training",
                "tuesday": "Cardio workout",
                "wednesday": "Rest or light activity",
                "thursday": "Upper body strength training",
                "friday": "Cardio workout",
                "saturday": "Lower body strength training",
                "sunday": "Rest and recovery"
            },
            "motivation_message": "Consistency is key to achieving your fitness goals. Start small and build momentum!"
        }
        
        return fallback_advice

    def generate_meal_plan(self, user_profile):
        """Generate a personalized meal plan"""
        try:
            prompt = f"""
            Create a 3-day meal plan for the following user profile:
            
            - Age: {user_profile.get('age')}
            - Weight: {user_profile.get('weight')} kg
            - Height: {user_profile.get('height')} cm
            - Gender: {user_profile.get('gender')}
            - Activity Level: {user_profile.get('activity_level')}
            - Fitness Goal: {user_profile.get('fitness_goal')}
            - BMI: {user_profile.get('bmi')}
            
            Provide a meal plan in JSON format:
            {{
                "daily_calories": "estimated daily calorie needs",
                "meal_plan": {{
                    "day_1": {{
                        "breakfast": "meal description with approximate calories",
                        "lunch": "meal description with approximate calories",
                        "dinner": "meal description with approximate calories",
                        "snacks": ["snack 1", "snack 2"]
                    }},
                    "day_2": {{
                        "breakfast": "meal description with approximate calories",
                        "lunch": "meal description with approximate calories", 
                        "dinner": "meal description with approximate calories",
                        "snacks": ["snack 1", "snack 2"]
                    }},
                    "day_3": {{
                        "breakfast": "meal description with approximate calories",
                        "lunch": "meal description with approximate calories",
                        "dinner": "meal description with approximate calories",
                        "snacks": ["snack 1", "snack 2"]
                    }}
                }},
                "nutritional_guidelines": [
                    "guideline 1",
                    "guideline 2",
                    "guideline 3"
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a certified nutritionist. Create safe, balanced meal plans. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            if content:
                meal_plan = json.loads(content)
                return {
                    "success": True,
                    "meal_plan": meal_plan
                }
            else:
                return {
                    "success": False,
                    "error": "Empty response from AI",
                    "meal_plan": self._get_fallback_meal_plan()
                }
            
        except Exception as e:
            print(f"Error generating meal plan: {e}")
            return {
                "success": False,
                "error": str(e),
                "meal_plan": self._get_fallback_meal_plan()
            }
    
    def _get_fallback_meal_plan(self):
        """Provide fallback meal plan"""
        return {
            "daily_calories": "2000-2500 (adjust based on individual needs)",
            "meal_plan": {
                "day_1": {
                    "breakfast": "Oatmeal with berries and nuts (350 calories)",
                    "lunch": "Grilled chicken salad with mixed vegetables (450 calories)",
                    "dinner": "Salmon with quinoa and steamed broccoli (500 calories)",
                    "snacks": ["Greek yogurt with fruit", "Handful of almonds"]
                },
                "day_2": {
                    "breakfast": "Scrambled eggs with whole grain toast (400 calories)",
                    "lunch": "Turkey and avocado wrap (500 calories)",
                    "dinner": "Lean beef stir-fry with brown rice (550 calories)",
                    "snacks": ["Apple with peanut butter", "Protein smoothie"]
                },
                "day_3": {
                    "breakfast": "Greek yogurt parfait with granola (380 calories)",
                    "lunch": "Quinoa bowl with vegetables and chickpeas (480 calories)",
                    "dinner": "Baked chicken breast with sweet potato (520 calories)",
                    "snacks": ["Hummus with vegetables", "Mixed berries"]
                }
            },
            "nutritional_guidelines": [
                "Focus on whole, unprocessed foods",
                "Include lean protein with each meal",
                "Stay hydrated throughout the day"
            ]
        }
