import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def create_enhanced_dataset():
    """Create an enhanced fitness dataset with more features"""
    np.random.seed(42)
    
    # Base data
    ages = np.random.randint(18, 65, 1000)
    weights = np.random.normal(70, 15, 1000)
    heights = np.random.normal(170, 10, 1000)
    
    # Ensure realistic ranges
    weights = np.clip(weights, 40, 150)
    heights = np.clip(heights, 150, 200)
    
    # Generate other features
    genders = np.random.choice(['Male', 'Female'], 1000)
    activity_levels = np.random.choice(['Low', 'Moderate', 'High', 'Very High'], 1000)
    experience_levels = np.random.choice(['Beginner', 'Intermediate', 'Advanced'], 1000)
    
    # Calculate BMI
    bmis = weights / ((heights / 100) ** 2)
    
    # Generate fitness goals based on logical rules
    fitness_goals = []
    for i in range(1000):
        bmi = bmis[i]
        age = ages[i]
        activity = activity_levels[i]
        
        if bmi > 28:
            goal = 'Weight Loss'
        elif bmi < 20 and age < 30:
            goal = 'Muscle Gain'
        elif activity in ['High', 'Very High'] and age < 40:
            goal = 'Endurance'
        else:
            goal = np.random.choice(['Weight Loss', 'Muscle Gain', 'Endurance', 'Maintenance'])
        
        fitness_goals.append(goal)
    
    # Create DataFrame
    data = {
        'age': ages,
        'weight': weights,
        'height': heights,
        'gender': genders,
        'activity_level': activity_levels,
        'fitness_goal': fitness_goals,
        'bmi': bmis,
        'experience_level': experience_levels
    }
    
    return pd.DataFrame(data)

def train_fitness_model():
    """Train the fitness goal prediction model"""
    print("Creating enhanced dataset...")
    df = create_enhanced_dataset()
    
    # Save the dataset
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/fitness_data.csv', index=False)
    print("Dataset saved to data/fitness_data.csv")
    
    # Prepare features
    le_gender = LabelEncoder()
    le_activity = LabelEncoder()
    le_experience = LabelEncoder()
    
    df['gender_encoded'] = le_gender.fit_transform(df['gender'])
    df['activity_encoded'] = le_activity.fit_transform(df['activity_level'])
    df['experience_encoded'] = le_experience.fit_transform(df['experience_level'])
    
    # Features for training
    feature_columns = ['age', 'weight', 'height', 'bmi', 'gender_encoded', 'activity_encoded', 'experience_encoded']
    X = df[feature_columns]
    y = df['fitness_goal']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train RandomForest model
    print("Training RandomForest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model and encoders
    os.makedirs('ml', exist_ok=True)
    model_data = {
        'model': model,
        'le_gender': le_gender,
        'le_activity': le_activity,
        'le_experience': le_experience,
        'feature_columns': feature_columns
    }
    
    joblib.dump(model_data, 'ml/fitness_model.pkl')
    print("Model saved to ml/fitness_model.pkl")
    
    return model_data

def predict_fitness_goal(age, weight, height, gender, activity_level, experience_level):
    """Predict fitness goal for new user"""
    try:
        # Load the trained model
        model_data = joblib.load('ml/fitness_model.pkl')
        model = model_data['model']
        le_gender = model_data['le_gender']
        le_activity = model_data['le_activity']
        le_experience = model_data['le_experience']
        
        # Calculate BMI
        bmi = weight / ((height / 100) ** 2)
        
        # Encode categorical features
        gender_encoded = le_gender.transform([gender])[0]
        activity_encoded = le_activity.transform([activity_level])[0]
        experience_encoded = le_experience.transform([experience_level])[0]
        
        # Create feature array
        features = np.array([[age, weight, height, bmi, gender_encoded, activity_encoded, experience_encoded]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        # Get class probabilities
        classes = model.classes_
        prob_dict = dict(zip(classes, probability))
        
        return {
            'predicted_goal': prediction,
            'confidence': max(probability),
            'probabilities': prob_dict
        }
    
    except Exception as e:
        print(f"Error in prediction: {e}")
        return {
            'predicted_goal': 'Maintenance',
            'confidence': 0.5,
            'probabilities': {'Maintenance': 0.5}
        }

if __name__ == "__main__":
    # Train the model
    train_fitness_model()
    
    # Test prediction
    print("\nTesting prediction...")
    result = predict_fitness_goal(25, 70, 175, 'Male', 'Moderate', 'Beginner')
    print(f"Prediction result: {result}")
