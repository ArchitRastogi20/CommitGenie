# CommitGenie

CommitGenie is an AI-powered Git commit message generator designed to automate and streamline your commit workflow. It automatically analyzes your staged changes and generates clear, concise commit messages based on your code differences. In addition to generating commit messages, CommitGenie can push your commit to the current branch and perform branch merges interactively.

## Project Overview

Before using CommitGenie, you need to stage your changes using the `git add` command. For example:

```
git add <file name>
```

CommitGenie reads your staged changes (using `git diff --cached`) and sends the diff output to an AI model. The model then generates a succinct, descriptive commit message summarizing your changes. You can review and accept the message or regenerate a new one. Once accepted, the commit is created and, if desired, pushed to your current branch. Additionally, CommitGenie offers an interactive merge option that lets you merge your current branch into any available branch.

## How to Use

### 1. Clone the Repository and Navigate to the Project Directory

```
git clone https://github.com/yourusername/CommitGenie.git
cd CommitGenie
```

### 2. Stage Your Changes

Stage the files you want to commit:

```
git add <file name>
```

### 3. Activate Your Python Virtual Environment (Optional but Recommended)

For Windows Command Prompt:

```
.venv\Scripts\activate
```

For PowerShell:

```
.\.venv\Scripts\activate
```

### 4. Install Dependencies

You have two options:

- **Using a requirements.txt file (not preferred):**

```
pip install -r requirements.txt
```

- **Manually Install Dependencies:**

For ChatGPT functionality:

```
pip install openai
```

For Ollama functionality:

```
pip install requests
```

### 5. Configuration

- **ChatGPT Users:**  
  Open the script and set your OpenAI API key in the `OPENAI_API_KEY` variable.

- **Ollama Users:**  
  Ensure Ollama is installed on your system. The default model is set to `llama3.2:1b` in the code. To use a different model, modify the `model` parameter in the `generate_commit_message_ollama` function.

### 6. Run CommitGenie

Execute the script from the repository root:

```
python commit.py
```

Upon running, you will be prompted to choose an action:

- **Commit Message Creation ( c):**  
  The tool generates a commit message based on your staged changes. You can review the suggested message and type 'y' (or 'yes') to accept it. The commit is then created, and you will be asked if you wish to push it to the current branch.

- **Merge Operation (m):**  
  The tool displays a list of available branches. Enter the name of the branch you want to merge into, and the script will check out the target branch, merge your current branch into it, and push the changes.

## Dependencies

- **Python Version:** Python 3.11 or higher

- **ChatGPT Users:**  
  - `openai` (install via `pip install openai`)

- **Ollama Users:**  
  - `requests` (install via `pip install requests`)

- **Other:**  
  - Git (for version control and executing Git commands)

## Contact

For any questions, issues, or suggestions regarding CommitGenie, please feel free to reach out:

- **Email:** architrastogi26@gmail.com
- **GitHub:** [ArchitRastogi20](https://github.com/ArchitRastogi20)