import pandas as pd
import csv
import math
import re
from imblearn.over_sampling import SMOTE
from nltk.corpus import words

english_words = set(words.words())

def clean_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        csvreader = csv.reader(infile)
        csvwriter = csv.writer(outfile)
        
        headers = next(csvreader)
        csvwriter.writerow(headers)
        
        for row in csvreader:
            if len(row) == 2 and len(row[0]) > 0 and len(row[0]) < 40:
                csvwriter.writerow(row)

def extract_count_lowercase(password):
    s = str(password) if pd.notnull(password) else ""
    count = len([char for char in s if char.islower()])
    return count

def extract_count_uppercase(password):
    s = str(password) if pd.notnull(password) else ""
    count = len([char for char in s if char.isupper()])
    return count

def extract_count_digits(password):
    s = str(password) if pd.notnull(password) else ""
    count = len([char for char in s if char.isdigit()])
    return count

def extract_count_special(password):
    s = str(password) if pd.notnull(password) else ""
    count = len([char for char in s if not char.isalnum()])
    return count

def extract_length(password):
    s = str(password) if pd.notnull(password) else ""
    count = len([char for char in s])
    return count

def calculate_entropy(password):
    password = str(password)
    length = len(password)
    entropy = 0

    for i in range(0, length):
        if password[i].islower():
            entropy += 1 * (i/(i+1))
        elif password[i].isupper():
            entropy += 2 * (i/(i+1))
        elif password[i].isdigit():
            entropy += 3 * (i/(i+1))
        elif not password[i].isalnum():
            entropy += 4 * (i/(i+1))
    
    return entropy

def count_continous(password):
    s = str(password) if pd.notnull(password) else ""
    continous = re.findall(r'(012|123|234|345|456|567|678|789|890|abc|4321|321|1234|asdf|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|qwerty)', s.lower())
    return len(continous)

def count_words(text, dictionary):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    dictionary_words = [word for word in words if word in dictionary]
    return len(dictionary_words)

def calculate_entropys(s):
    s = str(s) if pd.notnull(s) else ""
    prob = [float(s.count(c)) / len(s) for c in set(s)]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

if __name__ == '__main__':
    input_file = './data/data.csv'
    output_file = './data/clean_data.csv'
    clean_csv(input_file, output_file)

    df = pd.read_csv('./data/clean_data.csv')

    df['length'] = df['password'].apply(extract_length)
    df['lowers'] = df['password'].apply(extract_count_lowercase)
    df['uppers'] = df['password'].apply(extract_count_uppercase)
    df['digits'] = df['password'].apply(extract_count_digits)
    df['specials'] = df['password'].apply(extract_count_special)
    df['entropy'] = df['password'].apply(calculate_entropy)
    df['continous'] = df['password'].apply(count_continous)
    df['words'] = df['password'].apply(lambda x: count_words(str(x), english_words))

    df1 = df.copy()
    df1 = df1.drop('password', axis = 1)
    df1 = df1.drop_duplicates()
    print(df1["strength"].value_counts())
    
    df1.to_csv('./data/processed_data.csv', index=False)