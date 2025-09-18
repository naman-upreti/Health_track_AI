import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Health Track AI",
    page_icon="🏋️‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://0.0.0.0:8000"

def check_api_connection():
    """Check if the API is accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def make_api_request(endpoint, data=None):
    """Make API request with error handling"""
    try:
        if data:
            response = requests.post(f"{API_BASE_URL}/{endpoint}", json=data, timeout=30)
        else:
            response = requests.get(f"{API_BASE_URL}/{endpoint}", timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        return None

def main():
    # Main header
    st.title("🏋️‍♀️ Health Track AI")
    st.markdown("**Your Personal AI-Powered Fitness & Nutrition Coach**")
    
    # Check API connection
    if not check_api_connection():
        st.error("⚠️ Unable to connect to the API server. Please ensure the backend is running on port 8000.")
        st.info("To start the backend, run: `python api/main.py`")
        return
    
    # Sidebar for navigation
    st.sidebar.title("🎯 Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        ["🏠 Home", "🔮 Fitness Goal Prediction", "💪 Workout & Diet Plans", "🤖 AI Personal Coach", "📊 Progress Tracking"]
    )
    
    if page == "🏠 Home":
        show_home_page()
    elif page == "🔮 Fitness Goal Prediction":
        show_prediction_page()
    elif page == "💪 Workout & Diet Plans":
        show_recommendations_page()
    elif page == "🤖 AI Personal Coach":
        show_ai_coach_page()
    elif page == "📊 Progress Tracking":
        show_progress_page()
    elif page == "👤 User Profile":
        show_profile_page()

def show_home_page():
    """Display the home page"""
    st.header("Welcome to Health Track AI!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What We Offer
        
        **Health Track AI** is your comprehensive fitness companion that uses advanced machine learning and AI to provide:
        
        - 🔮 **Smart Goal Prediction**: ML-powered analysis of your fitness goals
        - 💪 **Personalized Workouts**: Custom exercise plans based on your profile
        - 🥗 **Nutrition Guidance**: Tailored diet recommendations
        - 🤖 **AI Coaching**: Groq-powered personalized advice
        - 📊 **Progress Tracking**: Monitor your fitness journey
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 How It Works
        
        1. **Enter Your Profile**: Age, weight, height, activity level
        2. **Get Predictions**: Our ML model predicts your ideal fitness goal
        3. **Receive Plans**: Get workout and nutrition recommendations
        4. **AI Coaching**: Receive personalized advice from our AI coach
        5. **Track Progress**: Monitor your journey and achievements
        """)
    
    # Quick Start section
    st.header("🚀 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔮 Predict My Goal", type="primary"):
            st.session_state.page = "🔮 Fitness Goal Prediction"
            st.rerun()
    
    with col2:
        if st.button("💪 Get Workout Plan", type="primary"):
            st.session_state.page = "💪 Workout & Diet Plans"
            st.rerun()
    
    with col3:
        if st.button("🤖 Talk to AI Coach", type="primary"):
            st.session_state.page = "🤖 AI Personal Coach"
            st.rerun()
    
    # Statistics section
    st.header("📈 Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ML Model Accuracy", "94.5%", "2.1%")
    
    with col2:
        st.metric("Fitness Goals Supported", "4", "Weight Loss, Muscle Gain, Endurance, Maintenance")
    
    with col3:
        st.metric("Workout Types", "50+", "Cardio, Strength, HIIT, Functional")
    
    with col4:
        st.metric("AI-Powered Features", "3", "Goal Prediction, Coaching, Meal Planning")

def show_prediction_page():
    """Display the fitness goal prediction page"""
    st.header("🔮 Fitness Goal Prediction")
    st.markdown("Let our ML model analyze your profile and predict your ideal fitness goal!")
    
    # Input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=16, max_value=80, value=25)
            weight = st.number_input("Weight (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.5)
            height = st.number_input("Height (cm)", min_value=140, max_value=220, value=175)
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female"])
            activity_level = st.selectbox("Activity Level", ["Low", "Moderate", "High", "Very High"])
            experience_level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
        
        submit_button = st.form_submit_button("🔮 Predict My Fitness Goal", type="primary")
    
    if submit_button:
        with st.spinner("Analyzing your profile..."):
            # Prepare data for API
            user_data = {
                "age": age,
                "weight": weight,
                "height": height,
                "gender": gender,
                "activity_level": activity_level,
                "experience_level": experience_level
            }
            
            # Make API request
            result = make_api_request("predict", user_data)
            
            if result and result.get("success"):
                prediction = result["prediction"]
                user_profile = result["user_profile"]
                
                # Display results
                st.header("🎯 Prediction Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Predicted Goal", prediction["predicted_goal"])
                
                with col2:
                    st.metric("Confidence", f"{prediction['confidence']:.1%}")
                
                with col3:
                    st.metric("BMI", f"{user_profile['bmi']:.1f}")
                
                # Probability distribution
                st.header("📊 Goal Probabilities")
                
                prob_df = pd.DataFrame(
                    list(prediction["probabilities"].items()),
                    columns=["Goal", "Probability"]
                )
                prob_df["Probability"] = prob_df["Probability"] * 100
                
                fig, ax = plt.subplots(figsize=(10, 6))
                bars = ax.bar(prob_df["Goal"], prob_df["Probability"], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
                ax.set_ylabel("Probability (%)")
                ax.set_title("Fitness Goal Prediction Probabilities")
                ax.set_ylim(0, 100)
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{height:.1f}%', ha='center', va='bottom')
                
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                
                # Store prediction in session state for other pages
                st.session_state.predicted_goal = prediction["predicted_goal"]
                st.session_state.user_profile = user_profile
                
                st.success(f"🎉 Based on your profile, we predict your primary fitness goal is: **{prediction['predicted_goal']}**")
                
                if st.button("💪 Get Workout & Diet Plan", type="primary"):
                    st.session_state.page = "💪 Workout & Diet Plans"
                    st.rerun()

def show_recommendations_page():
    """Display workout and diet recommendations"""
    st.header("💪 Workout & Diet Recommendations")
    
    # Input form
    with st.form("recommendations_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=16, max_value=80, value=25)
            weight = st.number_input("Weight (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.5)
            height = st.number_input("Height (cm)", min_value=140, max_value=220, value=175)
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female"])
            activity_level = st.selectbox("Activity Level", ["Low", "Moderate", "High", "Very High"])
            experience_level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
        
        fitness_goal = st.selectbox(
            "Fitness Goal",
            ["Weight Loss", "Muscle Gain", "Endurance", "Maintenance"],
            index=0 if "predicted_goal" not in st.session_state else 
            ["Weight Loss", "Muscle Gain", "Endurance", "Maintenance"].index(st.session_state.get("predicted_goal", "Weight Loss"))
        )
        
        submit_button = st.form_submit_button("💪 Get My Recommendations", type="primary")
    
    if submit_button:
        with st.spinner("Generating your personalized recommendations..."):
            # Prepare data for API
            user_data = {
                "age": age,
                "weight": weight,
                "height": height,
                "gender": gender,
                "activity_level": activity_level,
                "experience_level": experience_level,
                "fitness_goal": fitness_goal
            }
            
            # Make API request
            result = make_api_request("recommend", user_data)
            
            if result and result.get("success"):
                rule_based = result["rule_based_recommendations"]
                content_based = result["content_based_recommendations"]
                
                # Display rule-based recommendations
                st.header("🎯 Your Personalized Plan")
                
                # Workout recommendations
                st.subheader("🏋️‍♀️ Workout Plan")
                workout_plan = rule_based.get("workout_plan", {})
                
                for category, exercises in workout_plan.items():
                    if exercises:
                        st.markdown(f"**{category.title()} Training:**")
                        for exercise in exercises:
                            with st.expander(f"📋 {exercise['name']}"):
                                st.write(f"**Duration:** {exercise['duration']}")
                                st.write(f"**Frequency:** {exercise['frequency']}")
                                st.write(f"**Description:** {exercise['description']}")
                                if 'exercises' in exercise:
                                    st.write(f"**Key Exercises:** {', '.join(exercise['exercises'])}")
                                if 'calories_burned' in exercise:
                                    st.write(f"**Calories Burned:** {exercise['calories_burned']}")
                
                # Diet recommendations
                st.subheader("🥗 Nutrition Plan")
                diet_plan = rule_based.get("diet_plan", {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Key Principles:**")
                    for principle in diet_plan.get("principles", []):
                        st.write(f"• {principle}")
                    
                    st.markdown("**Macronutrient Targets:**")
                    macros = diet_plan.get("macros", {})
                    for macro, target in macros.items():
                        st.write(f"• **{macro.title()}:** {target}")
                
                with col2:
                    st.markdown("**Recommended Foods:**")
                    for food in diet_plan.get("foods_to_emphasize", []):
                        st.write(f"• {food}")
                
                # Adjustments based on experience and age
                st.subheader("⚙️ Personalized Adjustments")
                adjustments = rule_based.get("adjustments", {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Experience Level Adjustments:**")
                    exp_adj = adjustments.get("experience", {})
                    for key, value in exp_adj.items():
                        st.write(f"• **{key.replace('_', ' ').title()}:** {value}")
                
                with col2:
                    st.markdown("**Age-Based Considerations:**")
                    age_adj = adjustments.get("age", {})
                    for key, value in age_adj.items():
                        st.write(f"• **{key.replace('_', ' ').title()}:** {value}")
                
                # General recommendations
                st.subheader("📋 General Recommendations")
                general_recs = rule_based.get("general_recommendations", [])
                for i, rec in enumerate(general_recs, 1):
                    st.write(f"{i}. {rec}")
                
                # Content-based insights
                if not content_based.get("error"):
                    st.header("🤝 Similar Users Insights")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Recommended Goal", content_based.get("recommended_goal", "N/A"))
                    
                    with col2:
                        similarity = content_based.get("similarity_confidence", 0)
                        st.metric("Similarity Score", f"{similarity:.1%}")
                    
                    with col3:
                        st.metric("Similar Users", content_based.get("similar_users_count", 0))

def show_ai_coach_page():
    """Display AI coaching page"""
    st.header("🤖 AI Personal Coach")
    st.markdown("Get personalized advice from our AI coach powered by Groq's fast AI models!")
    
    # Check for Groq API key
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "gsk-default-key":
        st.warning("⚠️ Groq API key not configured. AI features may not work properly.")
        st.info("Please set the GROQ_API_KEY environment variable to use AI coaching features.")
    
    # Input form
    with st.form("ai_coach_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=16, max_value=80, value=25)
            weight = st.number_input("Weight (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.5)
            height = st.number_input("Height (cm)", min_value=140, max_value=220, value=175)
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female"])
            activity_level = st.selectbox("Activity Level", ["Low", "Moderate", "High", "Very High"])
            experience_level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
        
        fitness_goal = st.selectbox(
            "Fitness Goal",
            ["Weight Loss", "Muscle Gain", "Endurance", "Maintenance"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            get_advice = st.form_submit_button("🤖 Get AI Coaching", type="primary")
        
        with col2:
            get_meal_plan = st.form_submit_button("🥗 Get Meal Plan", type="secondary")
    
    if get_advice:
        with st.spinner("Your AI coach is analyzing your profile..."):
            user_data = {
                "age": age,
                "weight": weight,
                "height": height,
                "gender": gender,
                "activity_level": activity_level,
                "experience_level": experience_level,
                "fitness_goal": fitness_goal
            }
            
            result = make_api_request("genai", user_data)
            
            if result and result.get("success"):
                ai_advice = result["ai_advice"]
                
                if ai_advice.get("success"):
                    advice = ai_advice["advice"]
                    
                    st.header("🎯 Your Personal AI Coach Says:")
                    
                    # Motivation message
                    st.subheader(f"💪 {advice.get('motivation_message', 'Stay motivated!')}")
                    
                    # Workout advice
                    st.subheader("🏋️‍♀️ Workout Advice")
                    workout_advice = advice.get("workout_advice", [])
                    for i, tip in enumerate(workout_advice, 1):
                        st.write(f"{i}. {tip}")
                    
                    # Nutrition advice
                    st.subheader("🥗 Nutrition Advice")
                    nutrition_advice = advice.get("nutrition_advice", [])
                    for i, tip in enumerate(nutrition_advice, 1):
                        st.write(f"{i}. {tip}")
                    
                    # Lifestyle tips
                    st.subheader("🌟 Lifestyle Tips")
                    lifestyle_tips = advice.get("lifestyle_tips", [])
                    for i, tip in enumerate(lifestyle_tips, 1):
                        st.write(f"{i}. {tip}")
                    
                    # Weekly schedule
                    st.subheader("📅 Weekly Schedule")
                    weekly_schedule = advice.get("weekly_schedule", {})
                    
                    schedule_df = pd.DataFrame(
                        [(day.title(), activity) for day, activity in weekly_schedule.items()],
                        columns=["Day", "Recommended Activity"]
                    )
                    st.table(schedule_df)
                    
                else:
                    st.error(f"AI Error: {ai_advice.get('error', 'Unknown error')}")
                    if ai_advice.get("advice"):
                        st.subheader("📋 Fallback Recommendations")
                        st.json(ai_advice["advice"])
    
    if get_meal_plan:
        with st.spinner("Creating your personalized meal plan..."):
            user_data = {
                "age": age,
                "weight": weight,
                "height": height,
                "gender": gender,
                "activity_level": activity_level,
                "experience_level": experience_level,
                "fitness_goal": fitness_goal
            }
            
            result = make_api_request("meal_plan", user_data)
            
            if result and result.get("success"):
                meal_plan_data = result["meal_plan"]
                
                if meal_plan_data.get("success"):
                    meal_plan = meal_plan_data["meal_plan"]
                    
                    st.header("🍽️ Your 3-Day Meal Plan")
                    
                    # Daily calories
                    st.markdown(f"**Estimated Daily Calories:** {meal_plan.get('daily_calories', 'Not specified')}")
                    
                    # Meal plans for each day
                    meal_plan_days = meal_plan.get("meal_plan", {})
                    
                    for day_key, day_meals in meal_plan_days.items():
                        day_name = day_key.replace("_", " ").title()
                        st.subheader(f"📅 {day_name}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**🌅 Breakfast:**")
                            st.write(day_meals.get("breakfast", "Not specified"))
                            
                            st.markdown("**🍴 Lunch:**")
                            st.write(day_meals.get("lunch", "Not specified"))
                        
                        with col2:
                            st.markdown("**🌙 Dinner:**")
                            st.write(day_meals.get("dinner", "Not specified"))
                            
                            st.markdown("**🍎 Snacks:**")
                            snacks = day_meals.get("snacks", [])
                            for snack in snacks:
                                st.write(f"• {snack}")
                    
                    # Nutritional guidelines
                    st.subheader("📋 Nutritional Guidelines")
                    guidelines = meal_plan.get("nutritional_guidelines", [])
                    for i, guideline in enumerate(guidelines, 1):
                        st.write(f"{i}. {guideline}")
                
                else:
                    st.error(f"Meal Plan Error: {meal_plan_data.get('error', 'Unknown error')}")

def show_progress_page():
    """Display progress tracking page"""
    st.header("📊 Progress Tracking")
    st.markdown("Track your fitness journey and visualize your progress!")
    
    # Initialize session state for progress data
    if 'progress_data' not in st.session_state:
        st.session_state.progress_data = []
    
    # Add new progress entry
    st.subheader("📝 Log Your Progress")
    
    with st.form("progress_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date = st.date_input("Date", value=datetime.now().date())
            weight = st.number_input("Weight (kg)", min_value=40.0, max_value=200.0, value=70.0, step=0.1)
        
        with col2:
            workout_completed = st.checkbox("Workout Completed")
            workout_duration = st.number_input("Workout Duration (minutes)", min_value=0, max_value=300, value=0)
        
        with col3:
            energy_level = st.slider("Energy Level (1-10)", min_value=1, max_value=10, value=5)
            mood = st.selectbox("Mood", ["😞 Poor", "😐 Okay", "😊 Good", "😁 Great", "🤩 Excellent"])
        
        notes = st.text_area("Notes (optional)", placeholder="How did you feel? Any challenges or achievements?")
        
        if st.form_submit_button("📊 Log Progress", type="primary"):
            progress_entry = {
                "date": date,
                "weight": weight,
                "workout_completed": workout_completed,
                "workout_duration": workout_duration,
                "energy_level": energy_level,
                "mood": mood,
                "notes": notes
            }
            
            st.session_state.progress_data.append(progress_entry)
            st.success("✅ Progress logged successfully!")
    
    # Display progress if data exists
    if st.session_state.progress_data:
        st.subheader("📈 Your Progress Charts")
        
        # Convert to DataFrame
        df = pd.DataFrame(st.session_state.progress_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Weight progress chart
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Weight Progress**")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(df['date'], df['weight'], marker='o', linewidth=2, markersize=6)
            ax.set_xlabel("Date")
            ax.set_ylabel("Weight (kg)")
            ax.set_title("Weight Progress Over Time")
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.markdown("**Energy Levels**")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(df['date'], df['energy_level'], marker='o', color='orange', linewidth=2, markersize=6)
            ax.set_xlabel("Date")
            ax.set_ylabel("Energy Level (1-10)")
            ax.set_title("Energy Levels Over Time")
            ax.set_ylim(0, 10)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Workout statistics
        st.subheader("🏋️‍♀️ Workout Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_workouts = df['workout_completed'].sum()
            st.metric("Total Workouts", total_workouts)
        
        with col2:
            total_duration = df['workout_duration'].sum()
            st.metric("Total Duration", f"{total_duration} min")
        
        with col3:
            avg_energy = df['energy_level'].mean()
            st.metric("Avg Energy Level", f"{avg_energy:.1f}/10")
        
        with col4:
            consistency = (total_workouts / len(df)) * 100 if len(df) > 0 else 0
            st.metric("Workout Consistency", f"{consistency:.1f}%")
        
        # Recent entries
        st.subheader("📝 Recent Entries")
        recent_df = df.tail(5)[['date', 'weight', 'workout_completed', 'energy_level', 'mood']].copy()
        recent_df['date'] = recent_df['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(recent_df, use_container_width=True)
        
        # Clear data option
        if st.button("🗑️ Clear Progress Data", type="secondary"):
            st.session_state.progress_data = []
            st.success("Progress data cleared!")
            st.rerun()
    
    else:
        st.info("📝 No progress data yet. Start logging your fitness journey above!")
        
        # Sample data for demonstration
        if st.button("📊 Load Sample Data", type="secondary"):
            sample_data = []
            for i in range(7):
                sample_data.append({
                    "date": datetime.now().date() - timedelta(days=i),
                    "weight": 70 + (i * 0.2),
                    "workout_completed": i % 2 == 0,
                    "workout_duration": 30 + (i * 5),
                    "energy_level": 5 + (i % 4),
                    "mood": ["😊 Good", "😁 Great", "🤩 Excellent"][i % 3],
                    "notes": f"Day {i+1} notes"
                })
            
            st.session_state.progress_data = sample_data
            st.success("✅ Sample data loaded!")
            st.rerun()

def show_profile_page():
    """Display user profile and authentication page"""
    st.header("👤 User Profile & Authentication")
    
    # Initialize session state for user authentication
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False
        st.session_state.user_data = None
    
    if not st.session_state.user_authenticated:
        # Show login/registration form
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab1:
            st.subheader("Login to Your Account")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("🔑 Login", type="primary"):
                    if email and password:
                        login_data = {"email": email, "password": password}
                        response = make_api_request("auth/login", login_data)
                        
                        if response and response.get('success'):
                            st.session_state.user_authenticated = True
                            st.session_state.user_data = response.get('user')
                            st.session_state.user_id = response.get('user', {}).get('id')
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
                    else:
                        st.warning("Please fill in all fields")
        
        with tab2:
            st.subheader("Create New Account")
            with st.form("register_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    reg_email = st.text_input("Email*")
                    reg_name = st.text_input("Full Name*")
                    reg_password = st.text_input("Password*", type="password")
                    age = st.number_input("Age", min_value=16, max_value=100, value=25)
                
                with col2:
                    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
                    height = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=170.0, step=1.0)
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                    activity_level = st.selectbox("Activity Level", ["Low", "Moderate", "High", "Very High"])
                
                experience_level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
                fitness_goal = st.selectbox("Primary Fitness Goal", ["Weight Loss", "Muscle Gain", "Endurance", "Maintenance"])
                
                if st.form_submit_button("📝 Create Account", type="primary"):
                    if reg_email and reg_name and reg_password:
                        registration_data = {
                            "email": reg_email,
                            "password": reg_password,
                            "full_name": reg_name,
                            "age": age,
                            "weight": weight,
                            "height": height,
                            "gender": gender,
                            "activity_level": activity_level,
                            "experience_level": experience_level,
                            "fitness_goal": fitness_goal
                        }
                        
                        response = make_api_request("auth/register", registration_data)
                        
                        if response and response.get('success'):
                            st.success("✅ Account created successfully! You can now login.")
                        else:
                            error_msg = response.get('detail', 'Registration failed') if response else 'Connection error'
                            st.error(f"❌ {error_msg}")
                    else:
                        st.warning("Please fill in all required fields (*)")
    
    else:
        # Show user profile and settings
        st.success(f"👋 Welcome, {st.session_state.user_data.get('full_name', 'User')}!")
        
        # Logout button in sidebar
        if st.sidebar.button("🚪 Logout"):
            st.session_state.user_authenticated = False
            st.session_state.user_data = None
            st.session_state.user_id = None
            st.success("✅ Logged out successfully!")
            st.rerun()
        
        # Get user profile
        user_id = st.session_state.user_id
        profile_response = make_api_request(f"auth/profile/{user_id}")
        
        if profile_response and profile_response.get('success'):
            profile = profile_response.get('profile', {})
            
            # Display current profile
            st.subheader("📊 Your Profile")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Age", f"{profile.get('age', 'N/A')} years")
                st.metric("Weight", f"{profile.get('weight', 'N/A')} kg")
            
            with col2:
                st.metric("Height", f"{profile.get('height', 'N/A')} cm")
                bmi = None
                if profile.get('weight') and profile.get('height'):
                    bmi = profile['weight'] / ((profile['height'] / 100) ** 2)
                    st.metric("BMI", f"{bmi:.1f}")
                else:
                    st.metric("BMI", "N/A")
            
            with col3:
                st.metric("Activity Level", profile.get('activity_level', 'N/A'))
                st.metric("Experience", profile.get('experience_level', 'N/A'))
            
            # Profile update form
            st.subheader("✏️ Update Profile")
            
            with st.form("profile_update_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_age = st.number_input("Age", min_value=16, max_value=100, value=profile.get('age', 25))
                    new_weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, 
                                               value=float(profile.get('weight', 70.0)), step=0.1)
                    new_height = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, 
                                               value=float(profile.get('height', 170.0)), step=1.0)
                
                with col2:
                    new_gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                            index=["Male", "Female", "Other"].index(profile.get('gender', 'Male')) 
                                            if profile.get('gender') in ["Male", "Female", "Other"] else 0)
                    new_activity = st.selectbox("Activity Level", ["Low", "Moderate", "High", "Very High"],
                                              index=["Low", "Moderate", "High", "Very High"].index(profile.get('activity_level', 'Moderate'))
                                              if profile.get('activity_level') in ["Low", "Moderate", "High", "Very High"] else 1)
                    new_experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"],
                                                index=["Beginner", "Intermediate", "Advanced"].index(profile.get('experience_level', 'Beginner'))
                                                if profile.get('experience_level') in ["Beginner", "Intermediate", "Advanced"] else 0)
                
                new_goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Endurance", "Maintenance"],
                                      index=["Weight Loss", "Muscle Gain", "Endurance", "Maintenance"].index(profile.get('fitness_goal', 'Maintenance'))
                                      if profile.get('fitness_goal') in ["Weight Loss", "Muscle Gain", "Endurance", "Maintenance"] else 3)
                
                if st.form_submit_button("💾 Update Profile", type="primary"):
                    update_data = {
                        "age": new_age,
                        "weight": new_weight,
                        "height": new_height,
                        "gender": new_gender,
                        "activity_level": new_activity,
                        "experience_level": new_experience,
                        "fitness_goal": new_goal
                    }
                    
                    # Make API request to update profile
                    try:
                        response = requests.put(f"{API_BASE_URL}/auth/profile/{user_id}", json=update_data, timeout=30)
                        if response.status_code == 200:
                            result = response.json()
                            if result.get('success'):
                                st.success("✅ Profile updated successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to update profile")
                        else:
                            st.error(f"❌ Update failed: {response.status_code}")
                    except:
                        st.error("❌ Connection error while updating profile")
        
        else:
            st.error("Failed to load profile data")

if __name__ == "__main__":
    main()
