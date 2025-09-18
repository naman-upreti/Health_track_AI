import pandas as pd
import numpy as np
from typing import Dict, List, Any
import os

class FitnessRecommender:
    def __init__(self):
        """Initialize the recommender with workout and diet databases"""
        self.workout_database = self._create_workout_database()
        self.diet_database = self._create_diet_database()
    
    def _create_workout_database(self):
        """Create a comprehensive workout database"""
        return {
            'Weight Loss': {
                'cardio': [
                    {
                        'name': 'High-Intensity Interval Training (HIIT)',
                        'duration': '20-30 minutes',
                        'frequency': '3-4 times per week',
                        'description': 'Alternating high-intensity bursts with recovery periods',
                        'calories_burned': '300-450 per session'
                    },
                    {
                        'name': 'Running/Jogging',
                        'duration': '30-45 minutes',
                        'frequency': '4-5 times per week',
                        'description': 'Steady-state cardio for fat burning',
                        'calories_burned': '300-500 per session'
                    },
                    {
                        'name': 'Cycling',
                        'duration': '45-60 minutes',
                        'frequency': '3-4 times per week',
                        'description': 'Low-impact cardio suitable for all fitness levels',
                        'calories_burned': '400-600 per session'
                    }
                ],
                'strength': [
                    {
                        'name': 'Circuit Training',
                        'duration': '30-40 minutes',
                        'frequency': '2-3 times per week',
                        'description': 'Full-body workout with minimal rest between exercises',
                        'exercises': ['Burpees', 'Mountain climbers', 'Jump squats', 'Push-ups']
                    },
                    {
                        'name': 'Compound Movements',
                        'duration': '45 minutes',
                        'frequency': '2-3 times per week',
                        'description': 'Multi-joint exercises for maximum calorie burn',
                        'exercises': ['Deadlifts', 'Squats', 'Pull-ups', 'Overhead press']
                    }
                ]
            },
            'Muscle Gain': {
                'strength': [
                    {
                        'name': 'Progressive Overload Training',
                        'duration': '60-75 minutes',
                        'frequency': '4-5 times per week',
                        'description': 'Gradually increasing weight, reps, or sets over time',
                        'exercises': ['Bench press', 'Squats', 'Deadlifts', 'Rows']
                    },
                    {
                        'name': 'Split Training',
                        'duration': '45-60 minutes',
                        'frequency': '5-6 times per week',
                        'description': 'Targeting specific muscle groups each session',
                        'splits': ['Push (Chest, Shoulders, Triceps)', 'Pull (Back, Biceps)', 'Legs (Quads, Hamstrings, Glutes)']
                    }
                ],
                'cardio': [
                    {
                        'name': 'Low-Intensity Steady State (LISS)',
                        'duration': '20-30 minutes',
                        'frequency': '2-3 times per week',
                        'description': 'Light cardio to maintain cardiovascular health without interfering with muscle growth',
                        'activities': ['Walking', 'Light cycling', 'Swimming']
                    }
                ]
            },
            'Endurance': {
                'cardio': [
                    {
                        'name': 'Long Distance Running',
                        'duration': '60-120 minutes',
                        'frequency': '3-4 times per week',
                        'description': 'Building aerobic capacity and endurance',
                        'progression': 'Gradually increase distance by 10% each week'
                    },
                    {
                        'name': 'Tempo Training',
                        'duration': '30-45 minutes',
                        'frequency': '2 times per week',
                        'description': 'Sustained effort at comfortably hard pace',
                        'target_hr': '85-90% of max heart rate'
                    },
                    {
                        'name': 'Cross Training',
                        'duration': '45-60 minutes',
                        'frequency': '2-3 times per week',
                        'description': 'Alternative activities to prevent overuse injuries',
                        'activities': ['Swimming', 'Cycling', 'Rowing', 'Elliptical']
                    }
                ],
                'strength': [
                    {
                        'name': 'Muscular Endurance Training',
                        'duration': '30-45 minutes',
                        'frequency': '2-3 times per week',
                        'description': 'High repetition, low weight exercises',
                        'rep_range': '15-25 reps per set'
                    }
                ]
            },
            'Maintenance': {
                'mixed': [
                    {
                        'name': 'Balanced Fitness Routine',
                        'duration': '45-60 minutes',
                        'frequency': '3-4 times per week',
                        'description': 'Combination of cardio and strength training',
                        'weekly_split': '2 cardio sessions, 2 strength sessions'
                    },
                    {
                        'name': 'Functional Training',
                        'duration': '30-45 minutes',
                        'frequency': '2-3 times per week',
                        'description': 'Exercises that mimic daily activities',
                        'exercises': ['Farmer walks', 'Turkish get-ups', 'Kettlebell swings']
                    }
                ]
            }
        }
    
    def _create_diet_database(self):
        """Create a comprehensive diet database"""
        return {
            'Weight Loss': {
                'principles': [
                    'Create a moderate caloric deficit (300-500 calories below maintenance)',
                    'Prioritize protein to preserve muscle mass',
                    'Include plenty of fiber-rich foods for satiety',
                    'Control portion sizes and meal timing'
                ],
                'macros': {
                    'protein': '25-30% of total calories',
                    'carbohydrates': '35-45% of total calories',
                    'fats': '20-30% of total calories'
                },
                'foods_to_emphasize': [
                    'Lean proteins: chicken breast, fish, tofu, legumes',
                    'Complex carbohydrates: quinoa, brown rice, sweet potatoes',
                    'Healthy fats: avocado, nuts, olive oil',
                    'Vegetables: leafy greens, broccoli, bell peppers',
                    'Fruits: berries, apples, citrus fruits'
                ],
                'meal_timing': 'Eat 4-5 smaller meals throughout the day to maintain stable blood sugar'
            },
            'Muscle Gain': {
                'principles': [
                    'Maintain a slight caloric surplus (200-500 calories above maintenance)',
                    'Consume adequate protein for muscle protein synthesis',
                    'Time protein intake around workouts',
                    'Stay hydrated and get adequate sleep'
                ],
                'macros': {
                    'protein': '1.6-2.2g per kg of body weight',
                    'carbohydrates': '45-55% of total calories',
                    'fats': '20-30% of total calories'
                },
                'foods_to_emphasize': [
                    'High-quality proteins: eggs, Greek yogurt, lean meats, protein powder',
                    'Complex carbohydrates: oats, pasta, rice, potatoes',
                    'Calorie-dense healthy foods: nuts, nut butters, dried fruits',
                    'Post-workout nutrition: protein + carbohydrates within 30-60 minutes'
                ],
                'supplements': 'Consider creatine, whey protein, and vitamin D (consult healthcare provider)'
            },
            'Endurance': {
                'principles': [
                    'Focus on carbohydrate availability for sustained energy',
                    'Maintain adequate protein for recovery',
                    'Optimize hydration and electrolyte balance',
                    'Practice race-day nutrition strategies'
                ],
                'macros': {
                    'carbohydrates': '55-65% of total calories',
                    'protein': '15-20% of total calories',
                    'fats': '20-25% of total calories'
                },
                'foods_to_emphasize': [
                    'Complex carbohydrates: pasta, rice, quinoa, oatmeal',
                    'Simple carbohydrates during exercise: sports drinks, bananas',
                    'Anti-inflammatory foods: fatty fish, tart cherries, turmeric',
                    'Hydrating foods: watermelon, cucumber, soups'
                ],
                'timing': 'Eat carb-rich meal 3-4 hours before long training sessions'
            },
            'Maintenance': {
                'principles': [
                    'Maintain current caloric intake',
                    'Focus on nutrient density and food quality',
                    'Practice portion control and mindful eating',
                    'Allow flexibility for social eating'
                ],
                'macros': {
                    'protein': '15-25% of total calories',
                    'carbohydrates': '45-50% of total calories',
                    'fats': '25-35% of total calories'
                },
                'foods_to_emphasize': [
                    'Variety of whole foods from all food groups',
                    'Seasonal fruits and vegetables',
                    'Whole grains and lean proteins',
                    'Moderate amounts of treats and indulgences'
                ],
                'lifestyle': 'Follow the 80/20 rule: 80% nutritious foods, 20% flexibility'
            }
        }
    
    def get_rule_based_recommendations(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate rule-based recommendations based on fitness goal"""
        fitness_goal = user_profile.get('fitness_goal', 'Maintenance')
        age = user_profile.get('age', 30)
        activity_level = user_profile.get('activity_level', 'Moderate')
        experience_level = user_profile.get('experience_level', 'Beginner')
        
        # Get base recommendations
        workout_recommendations = self.workout_database.get(fitness_goal, self.workout_database['Maintenance'])
        diet_recommendations = self.diet_database.get(fitness_goal, self.diet_database['Maintenance'])
        
        # Adjust based on experience level
        adjustments = self._get_experience_adjustments(experience_level)
        
        # Adjust based on age
        age_adjustments = self._get_age_adjustments(age)
        
        return {
            'fitness_goal': fitness_goal,
            'workout_plan': workout_recommendations,
            'diet_plan': diet_recommendations,
            'adjustments': {
                'experience': adjustments,
                'age': age_adjustments
            },
            'general_recommendations': self._get_general_recommendations(user_profile)
        }
    
    def get_content_based_recommendations(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content-based recommendations using similarity matching"""
        
        # Load user data if available
        try:
            df = pd.read_csv('data/fitness_data.csv')
        except FileNotFoundError:
            return {"error": "User data not available for content-based recommendations"}
        
        # Calculate user similarity scores
        user_bmi = user_profile.get('bmi', 22)
        user_age = user_profile.get('age', 30)
        user_weight = user_profile.get('weight', 70)
        
        # Find similar users
        df['similarity_score'] = df.apply(
            lambda row: self._calculate_user_similarity(
                user_bmi, user_age, user_weight,
                row['bmi'], row['age'], row['weight']
            ), axis=1
        )
        
        # Get top 5 similar users
        similar_users = df.nlargest(5, 'similarity_score')
        
        # Aggregate recommendations from similar users
        similar_goals = similar_users['fitness_goal'].value_counts()
        recommended_goal = similar_goals.index[0] if len(similar_goals) > 0 else 'Maintenance'
        
        return {
            'recommended_goal': recommended_goal,
            'similarity_confidence': similar_users['similarity_score'].mean(),
            'similar_users_count': len(similar_users),
            'goal_distribution': similar_goals.to_dict(),
            'recommendations': self.get_rule_based_recommendations({
                **user_profile,
                'fitness_goal': recommended_goal
            })
        }
    
    def _calculate_user_similarity(self, user_bmi, user_age, user_weight, other_bmi, other_age, other_weight):
        """Calculate similarity score between users"""
        bmi_diff = abs(user_bmi - other_bmi) / 10.0  # Normalize BMI difference
        age_diff = abs(user_age - other_age) / 50.0  # Normalize age difference
        weight_diff = abs(user_weight - other_weight) / 50.0  # Normalize weight difference
        
        # Calculate similarity (closer to 1 is more similar)
        similarity = 1 / (1 + bmi_diff + age_diff + weight_diff)
        return similarity
    
    def _get_experience_adjustments(self, experience_level: str) -> Dict[str, str]:
        """Get adjustments based on experience level"""
        adjustments = {
            'Beginner': {
                'workout_intensity': 'Start with lower intensity and focus on form',
                'progression': 'Increase intensity gradually over 4-6 weeks',
                'frequency': 'Begin with 2-3 sessions per week',
                'rest': 'Allow 48-72 hours rest between similar muscle groups'
            },
            'Intermediate': {
                'workout_intensity': 'Moderate to high intensity with proper form',
                'progression': 'Progressive overload every 1-2 weeks',
                'frequency': '3-5 sessions per week depending on goals',
                'variation': 'Incorporate exercise variations to prevent plateaus'
            },
            'Advanced': {
                'workout_intensity': 'High intensity with advanced techniques',
                'progression': 'Periodized training with deload weeks',
                'frequency': '4-6 sessions per week with proper recovery',
                'specialization': 'Focus on specific weaknesses or goals'
            }
        }
        return adjustments.get(experience_level, adjustments['Beginner'])
    
    def _get_age_adjustments(self, age: int) -> Dict[str, str]:
        """Get adjustments based on age"""
        if age < 25:
            return {
                'recovery': 'Generally faster recovery, can handle higher volume',
                'focus': 'Build good movement patterns and habits',
                'considerations': 'Focus on long-term development'
            }
        elif age < 40:
            return {
                'recovery': 'Good recovery capacity with proper sleep and nutrition',
                'focus': 'Peak performance and goal achievement',
                'considerations': 'Maintain work-life balance with training'
            }
        elif age < 55:
            return {
                'recovery': 'May need longer recovery periods',
                'focus': 'Maintain strength and prevent age-related muscle loss',
                'considerations': 'Include mobility and flexibility work'
            }
        else:
            return {
                'recovery': 'Prioritize recovery and listen to your body',
                'focus': 'Functional fitness and quality of life',
                'considerations': 'Low-impact exercises and joint health'
            }
    
    def _get_general_recommendations(self, user_profile: Dict[str, Any]) -> List[str]:
        """Get general health and fitness recommendations"""
        recommendations = [
            "Stay hydrated by drinking at least 8-10 glasses of water daily",
            "Aim for 7-9 hours of quality sleep each night",
            "Include a 5-10 minute warm-up before exercise",
            "Cool down with light stretching after workouts",
            "Listen to your body and rest when needed",
            "Track your progress with photos, measurements, or performance metrics",
            "Consider working with a qualified trainer when starting a new program"
        ]
        
        # Add goal-specific recommendations
        goal = user_profile.get('fitness_goal', 'Maintenance')
        if goal == 'Weight Loss':
            recommendations.append("Focus on creating a sustainable caloric deficit")
            recommendations.append("Weigh yourself consistently at the same time of day")
        elif goal == 'Muscle Gain':
            recommendations.append("Prioritize protein intake and post-workout nutrition")
            recommendations.append("Track strength gains and progressive overload")
        elif goal == 'Endurance':
            recommendations.append("Gradually increase training volume to prevent injury")
            recommendations.append("Include rest days and active recovery in your schedule")
        
        return recommendations
