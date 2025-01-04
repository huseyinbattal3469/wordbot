import json 
# from difflib import get_close_matches
import random as rnd
import pandas as pd
from textdistance import levenshtein 
import os

# Load knowledge base
def load_knowledge_base(file_path: str, language: str):
    if not os.path.exists(file_path):
        print(f"database is not found, creating a new database and adding {language} language...\n")
        data = {
            "languages": [
                {
                    "name": language,
                    "words": [
                    ]
                }
            ]
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return data
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not any(lang["name"] == language for lang in data["languages"]):
        print(f"{language} language does not exist in database, adding...\n")
        data["languages"].append({
            "name": language,
            "words": [
            ]
        })

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        print(f"{language} language is already available, loading...\n")   
    return data

def save_knowledge_base(file_path:str, data:dict):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def find_best_match(word:str, words:list[str]) -> str | None:
    potentials = []
    for w in words:
        match = levenshtein.normalized_similarity(word, w)
        print(word, w, match)
        if match  >= 0.6:
            potentials.append(match)
    return potentials[0] if potentials else None
    #matches = get_close_matches(question, questions, n=1, cutoff=0.6)
    #return matches[0] if matches else None

def find_match(word:str, words:list[str]) -> str | None:
    for w in words:
        match = levenshtein.normalized_similarity(word, w)
        print(word, w, match)       
        if match == 1.0:
            return w
    # matches = get_close_matches(question, questions, n=1, cutoff=1.0)
    # return matches[0] if matches else None

def get_answer_for_question(word:str, current_language_base:dict) -> str | None:
    for w in current_language_base["words"]:
        print(word, w["question"])
        if w["question"] == word:
            return w["answer"]
        
def word_bot():
    while True:
        user_input = input("\nPlease type a language you want to learn or type 'exit' to close the program: ")
        if user_input == 'exit':
            print("Thank you for using the WordBot by huseyinbattal3469. See you next time :)")
            break
        knowledge_base = load_knowledge_base("database.json", user_input)
        index, current_language_base  = next(((i ,lang) for i, lang in enumerate(knowledge_base["languages"]) if lang["name"] == user_input), None)
        while True:
            user_input = int(input("Welcome to the Language Learning Program! What would you like to do?\nTrain(1), Teach Words to Bot(0), Show the Learning Summary(3), Exit and Return to the Language Selection(2): "))
            if user_input == 2:
                break
            if user_input == 1:
                if current_language_base["words"] == []:
                        print("Please select the 'Teach Words to Bot(0)' option before the training...\n") 
                        continue
                while True:                        
                    below_zero_questions = [w for w in current_language_base["words"] if w["token"] < 0]
                    equal_zero_questions = [w for w in current_language_base["words"] if w["token"] == 0]
                    above_zero_questions = [w for w in current_language_base["words"] if w["token"] > 0]

                    if equal_zero_questions:
                        question = rnd.choice(equal_zero_questions)
                    elif below_zero_questions:
                        question = rnd.choice(below_zero_questions)
                    elif above_zero_questions:
                        question = rnd.choice(above_zero_questions)         

                    word = question['question']
                    meaning = question['answer']
                    token = question['token']

                    current_language_base["words"].remove(question)

                    print("Bot: What is '{}({})' means?".format(word,token))
                    user_input = input('You: ').lower().strip()
                    if user_input == "back":
                        current_language_base["words"].append(question)
                        print("\n"*20)
                        break
                    result = levenshtein.normalized_similarity(user_input, meaning) >= 0.5 #get_close_matches(user_input, [meaning],n=1,cutoff=0.5)
                    if user_input.startswith("to ") and meaning.startswith("to "):
                            user_input = user_input.split(" ")[-1]
                            meaning = meaning.split(" ")[-1]
                            result = levenshtein.normalized_similarity(user_input, meaning) >= 0.5 #get_close_matches(user_input, [meaning],n=1,cutoff=0.5)
                            user_input = "to "+user_input
                            meaning = "to "+meaning
                    
                    if user_input == meaning:
                        print("Bot: That's correct! {}: {}".format(word, meaning))
                        question['token'] +=1 if (question['token'] + 1) != 0 else 2
                    elif result:
                        print("Bot: That's ALMOST correct! You've typed '{}', but it should be '{}'".format(user_input, meaning))
                        question['token'] +=0.5 if (question['token'] + 0.5) != 0 else 1
                    else:
                        print("Bot: The answer is incorrect :( It should be '{}'".format(meaning))
                        question['token'] -= 1 if (question['token'] - 1) != 0 else 2                                       
                    current_language_base["words"].append(question)
                    knowledge_base["languages"][index] = current_language_base
                    save_knowledge_base("database.json", knowledge_base)
                    print("\n************")

            elif user_input == 0:
                while True:
                    word = input("Bot: Please enter your word to learn: ").lower().strip()
                    if word == "back":
                        print("\n"*20)
                        break
                    best_match = find_match(word, [q["question"] for q in current_language_base["words"]])
                    if best_match:
                        meaning = get_answer_for_question(best_match, current_language_base)
                        print(f"Bot: I already know the same word: {word} = {meaning}\n************")
                    else:
                        meaning = input("Bot: I don't know that word. Can you teach me?: ").lower().strip()
                        if meaning != "skip":
                            current_language_base["words"].append({"question":word, "answer":meaning,"token":0})
                            knowledge_base["languages"][index] = current_language_base
                            save_knowledge_base("database.json", knowledge_base)
                            print("Bot: Thank you! I learned a new word!\n************")
                        elif meaning == "skip":                
                            print("Skipped...")
                            
            elif user_input == 3:
                print("**********\n'-' = Bad. More away from 0 means worse.\n'0' = Fresh Words.\n'+' = Good. More away from 0 means better.\n")
                with open("database.json","r") as f:
                    words = current_language_base['words']
                df = pd.DataFrame(words)
                print("WORST 5 WORD BY MISS")
                df_worst = df.sort_values(by="token",ascending=True).head(5).to_string(index=False) 
                print(df_worst, end="\n\n")
                print("BEST 5 WORD BY STRIKE")
                df_best = df.sort_values(by="token",ascending=False).head(5).to_string(index=False)   
                print(df_best, end="\n**********\n")
if __name__ == "__main__":
    word_bot()