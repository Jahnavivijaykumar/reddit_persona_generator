# Reddit User Persona Generator 🧠

This project generates user personas based on Reddit user activity using Reddit API and OpenAI's language model.

## 📌 What It Does
- Takes a Reddit username/profile URL as input
- Scrapes up to 50 comments and 50 posts
- Sends the data to GPT-3.5/4 to generate a detailed persona
- Outputs persona and citations into a `.txt` file

---

## 📂 Folder Contents
- `persona_generator.py`: Python script
- `kojied_persona.txt`: Output sample for Reddit user `kojied`
- `Hungry-Move-6603_persona.txt`: Output sample for Reddit user `Hungry-Move-6603`

---

## 🛠️ How to Run

1.Clone the Repo
```bash
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
2.Set Up Python Environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
3.Configure .env
Create a .env file with:
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=your_app
OPENAI_API_KEY=your_openai_key
4. Run Script
```bash
python persona_generator.py
