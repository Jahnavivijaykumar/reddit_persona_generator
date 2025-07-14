import praw
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Configure OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_reddit_data(username, limit=50):
    user = reddit.redditor(username)
    posts = []
    comments = []

    for submission in user.submissions.new(limit=limit):
        posts.append({
            "title": submission.title,
            "body": submission.selftext,
            "url": submission.url
        })

    for comment in user.comments.new(limit=limit):
        comments.append({
            "body": comment.body,
            "link": f"https://www.reddit.com{comment.permalink}"
        })

    return posts, comments

def build_prompt(posts, comments):
    prompt = "You are an AI persona builder. Based on the following Reddit posts and comments, generate a detailed user persona including interests, personality, tone, political/religious beliefs (if any), writing style, etc. For each trait, cite which post or comment was used.\n\n"

    prompt += "### Posts:\n"
    for i, post in enumerate(posts):
        prompt += f"[Post {i+1}] Title: {post['title']}\nBody: {post['body']}\nURL: {post['url']}\n\n"

    prompt += "### Comments:\n"
    for i, comment in enumerate(comments):
        prompt += f"[Comment {i+1}] {comment['body']}\nLink: {comment['link']}\n\n"

    return prompt

def generate_persona(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_output(username, persona_text):
    filename = f"{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"✅ Persona for {username} saved to {filename}")

if __name__ == "__main__":
    reddit_url = input("Enter Reddit profile URL: ").strip()
    if reddit_url.endswith("/"):
        reddit_url = reddit_url[:-1]
    username = reddit_url.split("/")[-1]

    print(f"Fetching data for u/{username}...")
    posts, comments = fetch_reddit_data(username)

    print(f"Collected {len(posts)} posts and {len(comments)} comments.")
    prompt = build_prompt(posts, comments)

    print("Generating user persona using GPT...")
    with open(f"{username}_rawdata.txt", "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"✅ Raw Reddit data saved to {username}_rawdata.txt")

