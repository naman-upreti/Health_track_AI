
# 🏋️‍♀️ Health Track AI  

**Your Personal AI-Powered Fitness & Nutrition Coach** 🤖💪  

Health Track AI is an intelligent **fitness assistant** that uses **Machine Learning** and **Generative AI (GPT-5)** to analyze your fitness profile and deliver **personalized workout, nutrition, and lifestyle plans** — like having your own virtual coach!  

---

## 🎯 What It Does  

- 🧠 **Understands You:** Takes inputs like age, weight, height, and activity level  
- 📊 **Predicts Goals:** ML model predicts your ideal goal (Weight Loss, Muscle Gain, etc.)  
- 💪 **Personalizes Plans:** AI designs a tailored workout & diet routine  
- 💬 **Coaches You:** GPT-5 acts as your conversational fitness guide  
- 📈 **Tracks Progress:** Visualizes improvements through an interactive dashboard  

---

## ⚙️ How It Works  

1. **Input Data:** User enters physical stats & preferences  
2. **ML Prediction:** A **RandomForest model** classifies the fitness goal  
3. **AI Generation:** **GPT-5** generates personalized workouts, meals & motivation  
4. **Recommendation Engine:** Combines ML outputs + AI responses  
5. **Dashboard Display:** **Streamlit UI** shows results, graphs & progress reports  
6. **API Backend:** **FastAPI** handles predictions and real-time communication  

---

## 🛠 Tech Stack  

| Layer | Tools |
|-------|--------|
| **Frontend** | Streamlit (Interactive Dashboard) |
| **Backend** | FastAPI + Uvicorn |
| **Machine Learning** | Scikit-learn (RandomForest) |
| **AI Integration** | OpenAI GPT-5 |
| **Data & Visualization** | Pandas, NumPy, Matplotlib, Seaborn |

---

## 🚀 Quick Start  

```bash
# Clone repo
git clone https://github.com/your-username/health-track-ai.git
cd health-track-ai

# Install dependencies
pip install -r requirements.txt

# Run backend & frontend
uvicorn backend.main:app --reload
streamlit run app.py
````

---

## 🌟 Why It’s Unique

* Combines **ML predictions + Generative AI coaching**
* Runs on a **modular architecture (FastAPI + Streamlit)**
* Offers **real-time fitness insights** & **adaptive recommendations**
* Easy to extend with wearables, gamified challenges, and mobile apps

---

**Built with ❤️ using Python, FastAPI, Streamlit, and GPT-5**
⭐ *Star this repo to support AI-powered fitness innovation!*

```
