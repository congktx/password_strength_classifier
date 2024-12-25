import random
import json
from zxcvbn import zxcvbn
import csv
import pandas as pd

lowercases = "abcdefghijklmnopqrstuvwxyz"
uppercases = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
special_characters = "~!@#$%^&*()_-=+\/|?.<>,;:"
all_characters = lowercases + uppercases + digits + special_characters
max_characters = 12

data = []
num_len = []
eng_words = ["ace","big","cat","dog","elf","fun","hut","jaw","key","mix","owl","pig","rat","van","zip"]
array_5d = [[[[[0 
                for _ in range(max_characters + 1)] 
                for _ in range(max_characters + 1)] 
                for _ in range(max_characters + 1)] 
                for _ in range(max_characters + 1)]
                for _ in range(max_characters + 1)]

def generate_password(lower, upper, digit, special, words):
    password = ""
    for i in range(words):
        password += random.choice(eng_words)
        lower -= 3
    numbers = [lower, upper, digit, special]
    for i in range(lower + upper + digit + special):
        type = random.randint(0, 3)
        while numbers[type] == 0:
            type = random.randint(0, 3)
        numbers[type] -= 1
        if type == 0:
            password += random.choice(lowercases)
        elif type == 1:
            password += random.choice(uppercases)
        elif type == 2:
            password += random.choice(digits)
        elif type == 3:
            password += random.choice(special_characters)
    return password

def add_lack_sample_data(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        for i in range(max_characters, -1, -1):
            for j in range(max_characters-i, -1, -1):
                for k in range(max_characters-i-j, -1, -1):
                    for l in range(max_characters-i-j-k, -1, -1):
                        for h in range(i//3, -1, -1):
                            if (i+j+k+l == 0 or array_5d[i][j][k][l][h] > 0):
                                continue
                            array_5d[i][j][k][l][h] = 1
                            password = generate_password(i,j,k,l,h)
                            analysis = zxcvbn(password)
                            strength = float(analysis['score'])
                            new_row = [password, i+j+k+l, i, j, k, l, h, strength]
                            writer.writerow(new_row)

if __name__ == "__main__":
    # add_lack_sample_data("./data/processed_data.csv")
    df = pd.read_csv('./data/processed_data.csv')
    print(df['strength'].value_counts())


# password,length,lowers,uppers,digits,specials,words,strength