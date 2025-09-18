import os
import psycopg2
import psycopg2.extras
from typing import Optional, Dict, List, Any
import bcrypt
import json
from datetime import datetime, date

class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('PGHOST', 'localhost'),
            'port': os.getenv('PGPORT', '5432'),
            'database': os.getenv('PGDATABASE'),
            'user': os.getenv('PGUSER'),
            'password': os.getenv('PGPASSWORD')
        }
    
    def get_connection(self):
        """Get a database connection"""
        return psycopg2.connect(**self.connection_params)
    
    def execute_query(self, query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = False):
        """Execute a database query"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute(query, params)
            
            result = None
            if fetch_one:
                result = dict(cursor.fetchone()) if cursor.fetchone() else None
                cursor.execute(query, params)  # Re-execute for fetchone
                result = dict(cursor.fetchone()) if cursor.fetchone() else None
            elif fetch_all:
                result = [dict(row) for row in cursor.fetchall()]
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return result
            
        except Exception as e:
            print(f"Database error: {str(e)}")
            return None
    
    # User Management
    def create_user(self, email: str, password: str, full_name: str, profile_data: Dict = None) -> Optional[int]:
        """Create a new user"""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        query = """
        INSERT INTO users (email, password_hash, full_name, age, weight, height, gender, activity_level, experience_level, fitness_goal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        params = (
            email, password_hash, full_name,
            profile_data.get('age') if profile_data else None,
            profile_data.get('weight') if profile_data else None,
            profile_data.get('height') if profile_data else None,
            profile_data.get('gender') if profile_data else None,
            profile_data.get('activity_level') if profile_data else None,
            profile_data.get('experience_level') if profile_data else None,
            profile_data.get('fitness_goal') if profile_data else None
        )
        
        result = self.execute_query(query, params, fetch_one=True)
        return result['id'] if result else None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate a user"""
        query = "SELECT id, password_hash, full_name FROM users WHERE email = %s"
        result = self.execute_query(query, (email,), fetch_one=True)
        
        if result and bcrypt.checkpw(password.encode('utf-8'), result['password_hash'].encode('utf-8')):
            return {'id': result['id'], 'full_name': result['full_name'], 'email': email}
        return None
    
    def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """Get user profile"""
        query = """
        SELECT id, email, full_name, age, weight, height, gender, activity_level, experience_level, fitness_goal, created_at
        FROM users WHERE id = %s
        """
        return self.execute_query(query, (user_id,), fetch_one=True)
    
    def update_user_profile(self, user_id: int, profile_data: Dict) -> bool:
        """Update user profile"""
        fields = []
        values = []
        
        for field in ['age', 'weight', 'height', 'gender', 'activity_level', 'experience_level', 'fitness_goal']:
            if field in profile_data:
                fields.append(f"{field} = %s")
                values.append(profile_data[field])
        
        if not fields:
            return False
        
        fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(user_id)
        
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
        result = self.execute_query(query, tuple(values))
        return result is not None
    
    # Progress Tracking
    def log_progress(self, user_id: int, log_type: str, date: date, value: float = None, 
                    unit: str = None, notes: str = None, data: Dict = None) -> Optional[int]:
        """Log user progress"""
        query = """
        INSERT INTO progress_logs (user_id, log_type, date, value, unit, notes, data)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        params = (user_id, log_type, date, value, unit, notes, json.dumps(data) if data else None)
        result = self.execute_query(query, params, fetch_one=True)
        return result['id'] if result else None
    
    def get_user_progress(self, user_id: int, log_type: str = None, limit: int = 100) -> List[Dict]:
        """Get user progress logs"""
        if log_type:
            query = """
            SELECT * FROM progress_logs 
            WHERE user_id = %s AND log_type = %s 
            ORDER BY date DESC, created_at DESC 
            LIMIT %s
            """
            params = (user_id, log_type, limit)
        else:
            query = """
            SELECT * FROM progress_logs 
            WHERE user_id = %s 
            ORDER BY date DESC, created_at DESC 
            LIMIT %s
            """
            params = (user_id, limit)
        
        return self.execute_query(query, params, fetch_all=True) or []
    
    def get_progress_summary(self, user_id: int) -> Dict:
        """Get progress summary statistics"""
        query = """
        SELECT 
            log_type,
            COUNT(*) as count,
            MIN(date) as first_log,
            MAX(date) as latest_log,
            AVG(value) as avg_value,
            MIN(value) as min_value,
            MAX(value) as max_value
        FROM progress_logs 
        WHERE user_id = %s AND value IS NOT NULL
        GROUP BY log_type
        """
        
        results = self.execute_query(query, (user_id,), fetch_all=True)
        return {row['log_type']: dict(row) for row in results} if results else {}
    
    # Workout Plans
    def save_workout_plan(self, user_id: int, plan_name: str, fitness_goal: str,
                         exercises: Dict, difficulty_level: str = None, 
                         duration_weeks: int = None, ai_generated: bool = False) -> Optional[int]:
        """Save a workout plan"""
        query = """
        INSERT INTO workout_plans (user_id, plan_name, fitness_goal, difficulty_level, 
                                  duration_weeks, exercises, ai_generated)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        params = (user_id, plan_name, fitness_goal, difficulty_level, 
                 duration_weeks, json.dumps(exercises), ai_generated)
        result = self.execute_query(query, params, fetch_one=True)
        return result['id'] if result else None
    
    def get_user_workout_plans(self, user_id: int) -> List[Dict]:
        """Get user's workout plans"""
        query = """
        SELECT * FROM workout_plans 
        WHERE user_id = %s 
        ORDER BY created_at DESC
        """
        return self.execute_query(query, (user_id,), fetch_all=True) or []
    
    # Nutrition Plans
    def save_nutrition_plan(self, user_id: int, plan_name: str, fitness_goal: str,
                           meals: Dict, daily_calories: int = None, ai_generated: bool = False) -> Optional[int]:
        """Save a nutrition plan"""
        query = """
        INSERT INTO nutrition_plans (user_id, plan_name, fitness_goal, daily_calories, meals, ai_generated)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        params = (user_id, plan_name, fitness_goal, daily_calories, json.dumps(meals), ai_generated)
        result = self.execute_query(query, params, fetch_one=True)
        return result['id'] if result else None
    
    def get_user_nutrition_plans(self, user_id: int) -> List[Dict]:
        """Get user's nutrition plans"""
        query = """
        SELECT * FROM nutrition_plans 
        WHERE user_id = %s 
        ORDER BY created_at DESC
        """
        return self.execute_query(query, (user_id,), fetch_all=True) or []
    
    # Session Tracking
    def log_user_session(self, user_id: int, session_type: str, input_data: Dict, output_data: Dict) -> Optional[int]:
        """Log user AI session"""
        query = """
        INSERT INTO user_sessions (user_id, session_type, input_data, output_data)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        
        params = (user_id, session_type, json.dumps(input_data), json.dumps(output_data))
        result = self.execute_query(query, params, fetch_one=True)
        return result['id'] if result else None

# Global database instance
db = DatabaseManager()