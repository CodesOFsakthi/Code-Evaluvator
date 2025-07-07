import pandas as pd
import os

# Make sure 'data' folder exists
os.makedirs("data", exist_ok=True)

# Sample coding questions
data = [
    {"QID": "Q1", "Question": "Write a function to reverse a list."},
    {"QID": "Q2", "Question": "Check if a number is prime."},
    {"QID": "Q3", "Question": "Write a function to sort a list using bubble sort."},
    {"QID": "Q4", "Question": "Implement a stack using an array."},
    {"QID": "Q5", "Question": "Write a program to check if a string is a palindrome."},
]

# Create DataFrame and save as Excel
df = pd.DataFrame(data)
df.to_excel("data/questions.xlsx", index=False)

print("✅ questions.xlsx created in /data folder.")
