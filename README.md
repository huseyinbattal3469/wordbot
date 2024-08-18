# Word Learning Bot

This project is a **Language Learning Bot** designed to help users learn and reinforce vocabulary. The bot uses a simple algorithm to test the user's knowledge of words, track their progress, and adaptively select words based on past performance.

## Project Files

- `main.py`: The main Python script that runs the bot.
- `database.json`: A JSON file where the bot stores learned words and their associated tokens.

## Features

- **Interactive Learning**: The bot interacts with the user to test their vocabulary knowledge. It asks the user for the meaning of a word, provides feedback based on the user's response, and adjusts its learning algorithm accordingly.
- **Adaptive Learning**: The bot tracks the user's progress with each word using a token system:
  - Positive tokens indicate that the user knows the word well.
  - Negative tokens indicate that the user struggles with the word.
  - A token value of `0` indicates a new or fresh word.
- **Word Teaching Mode**: Users can add new words and their meanings to the bot's knowledge base.
- **Learning Summary**: The bot can display a summary of the user's learning progress, showing the best and worst-performing words.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/huseyinbattal3469/word-learning-bot.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd word-learning-bot
   ```
3. **Install required packages**:
   ```bash
   pip install pandas
   ```
4. **Create or update `database.json`**:
   - Ensure that you have a `database.json` file in the project directory. This file stores the words and their tokens.

## Usage

1. **Run the Bot**:
   ```bash
   python main.py
   ```

2. **Options**:
   - **Train (1)**: The bot will ask you the meaning of words it has learned. Your responses will influence the token values for those words.
   - **Teach Words to Bot (0)**: Add new words and their meanings to the bot's knowledge base.
   - **Show the Learning Summary (3)**: Display the best and worst words based on your learning history.
   - **Exit (2)**: Exit the program.

3. **Commands**:
   - **"back"**: Exit the current mode and return to the main menu.

## Example Interaction

```plaintext
Welcome to the Language Learning Program! What would you like to do?
Train(1), Teach Words to Bot(0), Show the Learning Summary(3), Exit(2): 1
Bot: What is 'apple(0)' means?
You: fruit
Bot: That's correct! apple: fruit
************
```

## License

This project is developed by Hüseyin Battal.

GitHub: [https://github.com/huseyinbattal3469](https://github.com/huseyinbattal3469)  
LinkedIn: [https://www.linkedin.com/in/huseyin-battal/](https://www.linkedin.com/in/huseyin-battal/)

---

This `README.md` provides a clear and concise overview of your word learning bot project. Let me know if you need any further adjustments!
