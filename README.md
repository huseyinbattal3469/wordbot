# WordBot

**WordBot** is a simple console-based language learning program. It maintains a JSON database of words across multiple languages, allowing you to:

- Create or load a language database (`database.json`).
- Teach new words to the bot.
- Practice (train) on already-entered words.
- View summaries of your best- and worst-learned words.

This README provides steps to install, run, and extend WordBot on your local machine.

---

## Table of Contents
1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Configuration Details](#configuration-details)
6. [How It Works](#how-it-works)
7. [Dependencies](#dependencies)
8. [Contributing](#contributing)
9. [License](#license)

---

## Features

1. **Language Selection**  
   - Prompts you to choose or create a language in `database.json`.  
   - If your chosen language does not exist, it will be added with an empty word list.  
   - If it already exists, the bot loads that language.

2. **Teach Words**  
   - Input new words and their translations (“meaning”) to expand the bot’s knowledge.  
   - The bot stores these words with an initial `token = 0`.

3. **Training (Quiz) Mode**  
   - Randomly picks a word to ask for its meaning, prioritizing words that have lower (or zero) `token` values (i.e., words you’re weak on).  
   - Evaluates your answer using the [TextDistance (Levenshtein)](https://pypi.org/project/textdistance/) library.  
   - Increments or decrements tokens based on correctness.

4. **Summaries**  
   - Shows a quick summary of your “Best 5” and “Worst 5” words by sorting on `token` values in ascending or descending order.

5. **Persistence with JSON**  
   - Saves and loads a JSON file named `database.json`.  
   - If the file does not exist, the bot will create one.

---

## Project Structure

```
.
├── .venv/
│   └── ...           # (Optional) Python virtual environment
├── main.py           # Entry-point script containing 'word_bot()'
├── run_wordbot.bat   # Windows batch file for quick execution
├── WordBot           # Shortcut file (Windows .lnk)
└── README.md         # This file
```

- **`.venv/`**: Optional virtual environment folder (recommended for dependency isolation).  
- **`main.py`**: Main Python script containing the `word_bot()` function and logic.  
- **`run_wordbot.bat`**: A Windows batch file to activate the virtual environment and run `main.py` directly.  
- **`WordBot`**: A shortcut file (on Windows) that may also launch the bot.

---

## Installation

1. **Clone or Download** this repository to your local machine.
2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv .venv
   ```
3. **Activate the Virtual Environment**:
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
4. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Or manually:
   ```bash
   pip install textdistance pandas
   ```

5. **(Optional) Adjust `run_wordbot.bat`:**  
   If you’re on Windows and want to use the batch file, ensure it activates the correct virtual environment path and runs `main.py`.

---

## Usage

1. **Run with Python**  
   From within the project folder (and active virtual environment), execute:
   ```bash
   python main.py
   ```
   The program will launch and guide you via console prompts.

2. **Run with `run_wordbot.bat`** (Windows Only)  
   Double-click **`run_wordbot.bat`** or run it from Command Prompt:
   ```bash
   run_wordbot.bat
   ```
   This batch file should:
   - Activate the `.venv` environment.
   - Launch `main.py`.

3. **Choose or Create a Language**  
   - The bot will ask which language you want to learn. Enter something like `"english"` or `"german"`.
   - If the language is not found, it will be added to `database.json`.
   - If it exists, the bot will load its words.

4. **Select an Action**  
   - **Train (1):** The bot quizzes you on words already in `database.json`.
   - **Teach Words to Bot (0):** Add new words to the current language.
   - **Show Learning Summary (3):** View top 5 and bottom 5 words by `token` value.
   - **Exit / Return to Language Selection (2):** Jump back to selecting a new language or close the app.

---

## Configuration Details

- **`database.json`**  
  Stores the entire knowledge base of languages and words. If the file doesn’t exist, it’s automatically created.

- **`token` Value**  
  Each word has a `token` value indicating how well you know it:
  - `token < 0`: Struggling with the word.
  - `token = 0`: Fresh / newly learned word.
  - `token > 0`: Word is at least somewhat familiar.

- **Token Adjustments**  
  - **Correct answer**: Increase token by 1.  
  - **Incorrect answer**: Decrease token by 1.  
  - **Partially correct**: Increase token by 0.5.  

  Special logic ensures you don’t remain stuck at 0; if you do an operation that would keep you at 0, it gets adjusted to 2 (for correct) or 1 (for partial).

- **Similarity**  
  - [Levenshtein normalized similarity](https://pypi.org/project/textdistance/) is used to compare user input with known answers.
  - A `SIMILARITY_THRESHOLD` is set to `0.6`.

---

## How It Works

1. **Loading Knowledge Base**  
   - `load_knowledge_base(file_path, language)` checks if `database.json` exists.
     - If not, creates a new one with the chosen language.
     - If it does exist, loads the JSON and checks if that language is listed.  
   - Returns a Python `dict`.

2. **Saving Knowledge Base**  
   - `save_knowledge_base(file_path, data)` writes updated data back to `database.json`.

3. **Training / Quizzing**  
   - Words are randomly picked from one of three “difficulty” pools, based on their `token` values:
     - **`< 0`**: Words you struggle with.  
     - **`= 0`**: New or untested words.  
     - **`> 0`**: Words that you have answered correctly at least once.  
   - The bot prompts you for the correct meaning. If you type `"back"`, you exit that training session.

4. **Evaluation**  
   - The bot uses `levenshtein.normalized_similarity(user_input, correct_answer)`.  
   - If it’s exactly 1.0, you’re fully correct.  
   - If it’s above `SIMILARITY_THRESHOLD`, you’re “almost correct.”  
   - Otherwise, you’re incorrect.

5. **Teaching New Words**  
   - If you choose “Teach Words to Bot (0),” you can provide new words (`question`) and their meanings (`answer`).  
   - The bot adds them to the `current_language_base["words"]` list.

---

## Dependencies

- **Python 3.9+** (recommended)
- **[textdistance](https://pypi.org/project/textdistance/)**
- **pandas** (for summary sorting and display)
- **json** (standard library)
- **os** (standard library)
- **random** (standard library)

If you have a `requirements.txt`, install everything with:
```bash
pip install -r requirements.txt
```

---

## Contributing

Feel free to submit pull requests, open issues, or suggest new features. All contributions are welcome!

**Potential improvements** might include:
- Adding a GUI for user interaction.
- Extending the code to multiple-choice quizzes.
- Storing synonyms or example sentences for each word.
- Integrating a speech recognition engine to practice pronunciation.

---

## License

No explicit license is provided in this repository. For questions regarding usage, distribution, or contributions, please contact the repository owner.
