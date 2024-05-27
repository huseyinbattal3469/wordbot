import json 
from difflib import get_close_matches
import random as rnd
import pandas as pd
# Load knowledge base

def load_knowledge_base(file_path:str):
    with open(file_path,"r") as f:
        data = json.load(f)
    return data


def save_knowledge_base(file_path:str, data:dict):
    with open(file_path,"w") as f:
        json.dump(data, f, indent=2)


def find_best_match(question:str, questions:list[str]) -> str | None:
    matches = get_close_matches(question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def find_match(question:str, questions:list[str]) -> str | None:
    matches = get_close_matches(question, questions, n=1, cutoff=1.0)
    return matches[0] if matches else None

def get_answer_for_question(question:str, knowledge_base:dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        

def word_bot():
    knowledge_base = load_knowledge_base("database.json")
    while True:
        user_input = int(input("Welcome to the Language Learning Program! What would you like to do?\nTrain Italian(1), Teach Italian Words to Bot(0), Show the Learning Summary(3), Exit(2): "))
        if user_input == 2:
            break
        if user_input == 1:      
            while True:  
                below_zero_questions = [q for q in knowledge_base["questions"] if q["token"] < 0]
                equal_zero_questions = [q for q in knowledge_base["questions"] if q["token"] == 0]
                above_zero_questions = [q for q in knowledge_base["questions"] if q["token"] > 0]

                if equal_zero_questions:
                    question = rnd.choice(equal_zero_questions)
                elif below_zero_questions:
                    question = rnd.choice(below_zero_questions)
                elif above_zero_questions:
                    question = rnd.choice(above_zero_questions)          
                word = question['question']
                meaning = question['answer']
                token = question['token']

                knowledge_base["questions"].remove(question)

                print("Bot: What is '{}({})' means?".format(word,token))
                user_input = input('You: ').lower().strip()
                if user_input == "back":
                    print("\n"*20)
                    break
                result = get_close_matches(user_input, [meaning],n=1,cutoff=0.5)
                if user_input.startswith("to ") and meaning.startswith("to "):
                        user_input = user_input.split(" ")[-1]
                        meaning = meaning.split(" ")[-1]
                        result = get_close_matches(user_input, [meaning],n=1,cutoff=0.5)
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
                    
                
                knowledge_base["questions"].append(question)
                save_knowledge_base("database.json",knowledge_base)
                print("\n************")
        elif user_input == 0:
            while True:
                word = input("Bot: Please enter your word to learn: ").lower().strip()
                if word == "back":
                    print("\n"*20)
                    break
                best_match = find_match(word, [q["question"] for q in knowledge_base["questions"]])
                if best_match:
                    meaning = get_answer_for_question(best_match, knowledge_base)
                    print(f"Bot: I already know the same word: {word} = {meaning}\n************")
                else:
                    meaning = input("Bot: I don't know that word. Can you teach me?: ").lower().strip()
                    if meaning != "skip":
                        knowledge_base["questions"].append({"question":word, "answer":meaning,"token":0})
                        save_knowledge_base("database.json",knowledge_base)
                        print("Bot: Thank you! I learned a new word!\n************")
                    elif meaning == "skip":                
                        print("Skipped...")
        elif user_input == 3:
            print("**********\n'-' = Bad. More away from 0 means worse.\n'0' = Fresh Words.\n'+' = Good. More away from 0 means better.\n")
            with open("database.json","r") as f:
                questions = json.load(f)['questions']
            df = pd.DataFrame(questions)
            print("WORST 5 WORD BY MISS")
            df_worst = df.sort_values(by="token",ascending=True).head(5).to_string(index=False) 
            print(df_worst, end="\n\n")
            print("BEST 5 WORD BY STRIKE")
            df_best = df.sort_values(by="token",ascending=False).head(5).to_string(index=False)   
            print(df_best, end="\n**********\n")
if __name__ == "__main__":
    word_bot()