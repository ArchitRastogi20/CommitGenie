import os
import subprocess
import requests
import json
from openai import OpenAI

# Set your OpenAI API key
OPENAI_API_KEY = "Enter API key"
client = OpenAI(api_key=OPENAI_API_KEY)
url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

def generate_commit_message_ollama(diff: str, style: str = "concise and clear") -> str:
    prompt = f"""
You are a highly skilled AI specialized in generating concise and descriptive git commit messages.
Analyze the following git diff and craft a meaningful commit message that clearly summarizes the changes.
Ensure the message is succinct and formatted in one or two sentences.
Git diff:
{diff}
"""
    data = {
        "model": "llama3.2:1b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data['response']  
        return actual_response
    else:
        raise Exception("Request failed with status code:", response.status_code, response.text)

def extract_code_block(text: str) -> str:
    """Extracts code block from the AI response."""
    if text.startswith("```") and text.endswith("```"):
        return text[3:-3].strip()
    return text.strip()

def generate_commit_message_chatgpt(diff: str, style: str = "concise and clear") -> str:
    prompt = f"""
You are a highly skilled AI specialized in generating concise and descriptive git commit messages.
Analyze the following git diff and craft a meaningful commit message that clearly summarizes the changes.
Ensure the message is succinct and formatted in one or two sentences.
Git diff:
{diff}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in generating clear and useful commit messages."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )
    return extract_code_block(response.choices[0].message.content.strip())

def get_current_branch() -> str:
    """Returns the current git branch name."""
    try:
        return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def list_branches() -> list:
    """Lists available git branches."""
    try:
        branches = subprocess.check_output(["git", "branch", "--all"]).decode().strip().split("\n")
        branches = [branch.strip().replace("* ", "").replace("remotes/origin/", "") for branch in branches]
        return sorted(set(branches))  # Remove duplicates
    except subprocess.CalledProcessError:
        return []

def merge_branch():
    """Handles merging branches."""
    current_branch = get_current_branch()
    if not current_branch:
        print("\n⚠️ Could not determine the current branch.")
        return

    merge_to_develop = input("\nDo you want to merge into 'develop'? (y/N): ").strip().lower()
    
    if merge_to_develop != "y":
        branches = list_branches()
        print("\nAvailable branches:")
        for i, branch in enumerate(branches, 1):
            print(f"{i}. {branch}")
        
        target_branch = input("\nEnter the branch name you want to merge into: ").strip()
        if target_branch not in branches:
            print("\n⚠️ Invalid branch selected. Aborting merge.")
            return
    else:
        target_branch = "develop"

    print(f"\n🚀 Merging '{current_branch}' into '{target_branch}'...")
    try:
        subprocess.run(["git", "checkout", target_branch], check=True)
        subprocess.run(["git", "merge", current_branch], check=True)
        subprocess.run(["git", "push", "origin", target_branch], check=True)
        print(f"\n✅ Successfully merged '{current_branch}' into '{target_branch}'!")
    except subprocess.CalledProcessError:
        print("\n❌ Merge failed. Resolve conflicts and try again.")

def main(model_choice=None):
    make_commit = input("\nDo you want to make a commit? (y/N): ").strip().lower()
    
    if make_commit == "y":
        diff_output = subprocess.check_output(
            ["git", "diff", "--cached"],
            encoding="utf-8",
            errors="replace"
        )
        if not diff_output.strip():
            print("No staged changes found. Please stage your changes with 'git add'.")
            return

        # Model selection
        if model_choice is None:
            model_choice = input("\nSelect model (0 for Ollama, 1 for ChatGPT): ").strip().lower()
        if model_choice in ["0", "ollama"]:
            generate_commit_message = generate_commit_message_ollama
        elif model_choice in ["1", "gpt", "chatgpt"]:
            generate_commit_message = generate_commit_message_chatgpt
        else:
            print("Invalid model selection. Defaulting to ChatGPT.")
            generate_commit_message = generate_commit_message_chatgpt

        # Loop until a commit message is accepted
        while True:
            commit_msg = generate_commit_message(diff_output, style="concise and clear")
            print("\nSuggested Commit Message:\n")
            print(commit_msg)
            confirm = input("\nType 'y' to accept this commit message, or press Enter to regenerate: ").strip().lower()
            if confirm in ["y", "yes"]:
                break
            else:
                print("\nRegenerating commit message...\n")

        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        print("\n✅ Committed successfully!")

        branch_name = get_current_branch()
        if branch_name:
            push_confirm = input(f"\nDo you want to push to branch '{branch_name}'? (y/N): ").strip().lower()
            if push_confirm == "y":
                subprocess.run(["git", "push", "origin", branch_name], check=True)
                print(f"\n🚀 Changes pushed to '{branch_name}' successfully!")
            else:
                print("\n🚫 Push skipped.")
        else:
            print("\n⚠️ Could not determine the current branch. Please push manually if needed.")
    else:
        merge_confirm = input("\nDo you want to do a merge? (y/N): ").strip().lower()
        if merge_confirm == "y":
            merge_branch()

if __name__ == "__main__":
    model_choice = "" # 0 for Ollama, 1 for ChatGPT
    main(model_choice)
