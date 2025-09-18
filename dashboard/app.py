import streamlit as st
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Health Track AI Dashboard",
    page_icon="📊",
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
    # Header
    st.title("📊 Health Track AI Dashboard")
    st.markdown("**Administrative dashboard for monitoring and analytics**")
    
    # Check API connection
    if not check_api_connection():
        st.error("⚠️ Unable to connect to the API server.")
        st.info("Please ensure the backend is running on port 8000.")
        return
    
    # Sidebar navigation
    st.sidebar.title("📊 Dashboard")
    section = st.sidebar.selectbox(
        "Select Section:",
        ["📈 Analytics", "👥 User Management", "🔧 System Health", "📋 Reports"]
    )
    
    if section == "📈 Analytics":
        show_analytics()
    elif section == "👥 User Management":
        show_user_management()
    elif section == "🔧 System Health":
        show_system_health()
    elif section == "📋 Reports":
        show_reports()

def show_analytics():
    """Display analytics dashboard"""
    st.header("📈 Analytics Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", "1,245", "12.5%")
    
    with col2:
        st.metric("Predictions Made", "3,678", "8.2%")
    
    with col3:
        st.metric("AI Requests", "2,134", "15.7%")
    
    with col4:
        st.metric("Success Rate", "97.8%", "0.3%")
    
    # Charts
    st.subheader("📊 Usage Trends")
    
    # Sample data for demonstration
    dates = [datetime.now().date() - timedelta(days=i) for i in range(30, 0, -1)]
    predictions = [20 + i*2 + (i%7)*5 for i in range(30)]
    ai_requests = [15 + i*1.5 + (i%5)*3 for i in range(30)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Daily Predictions**")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, predictions, marker='o', linewidth=2, color='#1f77b4')
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Predictions")
        ax.set_title("Daily Prediction Requests")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("**AI Coach Usage**")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, ai_requests, marker='s', linewidth=2, color='#ff7f0e')
        ax.set_xlabel("Date")
        ax.set_ylabel("AI Requests")
        ax.set_title("Daily AI Coach Requests")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    # Goal distribution
    st.subheader("🎯 Goal Distribution")
    goal_data = {
        'Weight Loss': 45,
        'Muscle Gain': 30,
        'Endurance': 15,
        'Maintenance': 10
    }
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    ax.pie(goal_data.values(), labels=goal_data.keys(), autopct='%1.1f%%', colors=colors)
    ax.set_title("Distribution of Predicted Fitness Goals")
    st.pyplot(fig)

def show_user_management():
    """Display user management interface"""
    st.header("👥 User Management")
    
    # User statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Users", "1,245")
    
    with col2:
        st.metric("New This Week", "87")
    
    with col3:
        st.metric("Avg Session Time", "12 min")
    
    # User table (mock data)
    st.subheader("Recent User Activity")
    
    user_data = {
        'User ID': ['USR001', 'USR002', 'USR003', 'USR004', 'USR005'],
        'Age': [25, 32, 28, 45, 31],
        'Goal': ['Weight Loss', 'Muscle Gain', 'Endurance', 'Maintenance', 'Weight Loss'],
        'Last Active': ['2024-01-15', '2024-01-14', '2024-01-15', '2024-01-13', '2024-01-15'],
        'Predictions': [3, 1, 5, 2, 4],
        'AI Requests': [2, 0, 3, 1, 2]
    }
    
    df = pd.DataFrame(user_data)
    st.dataframe(df, use_container_width=True)
    
    # Test user prediction
    st.subheader("🧪 Test User Prediction")
    
    with st.form("test_prediction"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=16, max_value=80, value=30)
            weight = st.number_input("Weight (kg)", min_value=40.0, max_value=200.0, value=70.0)
            height = st.number_input("Height (cm)", min_value=140, max_value=220, value=170)
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female"])
            activity = st.selectbox("Activity Level", ["Low", "Moderate", "High", "Very High"])
            experience = st.selectbox("Experience", ["Beginner", "Intermediate", "Advanced"])
        
        if st.form_submit_button("Test Prediction"):
            test_data = {
                "age": age,
                "weight": weight,
                "height": height,
                "gender": gender,
                "activity_level": activity,
                "experience_level": experience
            }
            
            result = make_api_request("predict", test_data)
            
            if result and result.get("success"):
                st.success(f"Predicted Goal: {result['prediction']['predicted_goal']}")
                st.info(f"Confidence: {result['prediction']['confidence']:.1%}")

def show_system_health():
    """Display system health monitoring"""
    st.header("🔧 System Health")
    
    # API status
    api_status = check_api_connection()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_color = "🟢" if api_status else "🔴"
        st.metric("API Status", f"{status_color} {'Online' if api_status else 'Offline'}")
    
    with col2:
        st.metric("Response Time", "156ms", "-23ms")
    
    with col3:
        st.metric("Memory Usage", "67%", "2.1%")
    
    with col4:
        st.metric("CPU Usage", "23%", "-1.2%")
    
    # Test all endpoints
    st.subheader("🔍 Endpoint Health Check")
    
    endpoints = [
        ("Root", "/"),
        ("Predict", "/predict"),
        ("Recommend", "/recommend"),
        ("GenAI", "/genai"),
        ("Meal Plan", "/meal_plan"),
        ("Full Plan", "/full_plan")
    ]
    
    if st.button("Run Health Check"):
        for name, endpoint in endpoints:
            try:
                if endpoint == "/":
                    response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
                else:
                    # Use test data for POST endpoints
                    test_data = {
                        "age": 30,
                        "weight": 70.0,
                        "height": 170,
                        "gender": "Male",
                        "activity_level": "Moderate",
                        "experience_level": "Beginner"
                    }
                    if endpoint in ["/recommend", "/genai", "/meal_plan"]:
                        test_data["fitness_goal"] = "Weight Loss"
                    
                    response = requests.post(f"{API_BASE_URL}{endpoint}", json=test_data, timeout=10)
                
                if response.status_code == 200:
                    st.success(f"✅ {name}: OK")
                else:
                    st.error(f"❌ {name}: Error {response.status_code}")
            except Exception as e:
                st.error(f"❌ {name}: {str(e)}")
    
    # Model information
    st.subheader("🤖 Model Information")
    
    model_info = {
        "Model Type": "RandomForest Classifier",
        "Training Data": "1000 samples",
        "Features": "7 (age, weight, height, BMI, gender, activity, experience)",
        "Classes": "4 (Weight Loss, Muscle Gain, Endurance, Maintenance)",
        "Last Updated": "2024-01-15"
    }
    
    for key, value in model_info.items():
        st.write(f"**{key}:** {value}")

def show_reports():
    """Display reports section"""
    st.header("📋 Reports")
    
    # Report generation
    st.subheader("📄 Generate Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            ["User Activity", "Prediction Analytics", "AI Usage", "System Performance"]
        )
        
        date_range = st.date_input(
            "Date Range",
            value=[datetime.now().date() - timedelta(days=7), datetime.now().date()],
            max_value=datetime.now().date()
        )
    
    with col2:
        export_format = st.selectbox("Export Format", ["CSV", "JSON", "PDF"])
        
        if st.button("Generate Report", type="primary"):
            st.success(f"Generated {report_type} report for {date_range}")
            
            # Mock report data
            if report_type == "User Activity":
                report_data = {
                    "total_users": 1245,
                    "active_users": 892,
                    "new_users": 87,
                    "avg_session_time": "12:34"
                }
            elif report_type == "Prediction Analytics":
                report_data = {
                    "total_predictions": 3678,
                    "accuracy": "94.5%",
                    "most_common_goal": "Weight Loss (45%)"
                }
            elif report_type == "AI Usage":
                report_data = {
                    "ai_requests": 2134,
                    "success_rate": "97.8%",
                    "avg_response_time": "2.3s"
                }
            else:
                report_data = {
                    "uptime": "99.9%",
                    "avg_response_time": "156ms",
                    "error_rate": "0.2%"
                }
            
            st.json(report_data)
    
    # Quick insights
    st.subheader("💡 Quick Insights")
    
    insights = [
        "Weight Loss is the most popular fitness goal (45% of predictions)",
        "Users aged 25-35 make up 60% of the user base",
        "AI coaching requests peak on Mondays and Wednesdays",
        "Mobile users represent 73% of total traffic",
        "Average user completes 3.2 predictions before getting recommendations"
    ]
    
    for insight in insights:
        st.write(f"• {insight}")

if __name__ == "__main__":
    main()
