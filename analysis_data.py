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
max_characters = 15

data = []
num_len = []
eng_words = ["ace","big","cat","dog","elf","fun","hut","jaw","key","mix","owl","pig","rat","van","zip"]
array_5d = [[[[[0 
                for _ in range(max_characters + 1)] 
                for _ in range(max_characters + 1)] 
                for _ in range(max_characters + 1)] 
                for _ in range(max_characters + 1)]
                for _ in range(max_characters + 1)]

def generate_password(lower, upper, digit, special, sets):
    password = ""
    numbers = [lower, upper, digit, special]
    l_lower = '-'
    l_upper = '-'
    l_digit = '-'
    l_special = '0'
    lowers = lowercases
    uppers = uppercases
    digitss = digits
    specials = special_characters
    for i in range(lower + upper + digit + special):
        type = random.randint(0, 3)
        while numbers[type] == 0:
            type = random.randint(0, 3)
        numbers[type] -= 1
        if type == 0:
            char = random.choice(lowers)
            lowers = lowers.replace(char, '')
            if (lowers == ""):
                lowers = lowercases
            l_lower = char
        elif type == 1:
            char = random.choice(uppers)
            uppers = uppers.replace(char, '')
            if (uppers == ""):
                uppers = uppercases
            l_upper = char
        elif type == 2:
            char = random.choice(digitss)
            digitss = digitss.replace(char, '')
            if (digitss == ""):
                digitss = digits
            l_digit = char
        elif type == 3:
            char = random.choice(specials)
            specials = specials.replace(char, '')
            if (specials == ""):
                specials = special_characters
            l_special = char
        password += char

    if (lower > 0 and l_lower not in lowercases):
        return ""
    if (upper > 0 and l_upper not in uppercases):
        return ""
    if (digit > 0 and l_digit not in digits):
        return ""
    if (special > 0 and l_special not in special_characters):
        return ""
    
    sets = len(set(password)) - sets
    new_pass = ""
    for index in range(len(password)):
        if (sets <= 0):
            new_pass += password[index]
        elif (password[index] in lowercases and password[index] != l_lower):
            new_pass += l_lower
            sets -= 1
        elif (password[index] in uppercases and password[index] != l_upper):
            new_pass += l_upper
            sets -= 1
        elif (password[index] in digits and password[index] != l_digit):
            new_pass += l_digit
            sets -= 1
        elif (password[index] in special_characters and password[index] != l_special):
            new_pass += l_special
            sets -= 1
    if (sets != 0):
        return ""
    return new_pass

def add_lack_sample_data(filename):
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        for i in range(max_characters, -1, -1):
            for j in range(max_characters-i, -1, -1):
                for k in range(max_characters-i-j, -1, -1):
                    for l in range(max_characters-i-j-k, -1, -1):
                        for h in range(i+j+k+l, -1, -1):
                            if (i+j+k+l == 0 or array_5d[i][j][k][l][h] > 0):
                                continue
                            array_5d[i][j][k][l][h] = 1
                            password = generate_password(i,j,k,l,h)
                            if password == "":
                                continue
                            analysis = zxcvbn(password)
                            strength = float(analysis['score'])
                            new_row = [password, i+j+k+l, i, j, k, l, h, strength]
                            writer.writerow(new_row)

def extract_features(password):
    lowercase_count = sum(1 for c in password if c in lowercases)
    uppercase_count = sum(1 for c in password if c in uppercases)
    digits_count = sum(1 for c in password if c in digits)
    special_count = sum(1 for c in password if c in special_characters)

    return [lowercase_count, uppercase_count, digits_count, special_count]

def add_password_data(start_line, line_cap):
    with open("./data/production.csv", "a", newline="") as file:
        writer = csv.writer(file)

        with open("./data/rockyou.txt", 'r', encoding='latin-1') as file:
            lines = file.readlines()[start_line:]
            line_cnt = start_line - 1
            for line in lines:
                line_cnt += 1
                if line_cnt >= line_cap:
                    break 

                password = line.strip()
                leng = len(password)

                if (leng > max_characters or leng == 0):
                    continue

                lowercase_count, uppercase_count, digits_count, special_count = extract_features(password)

                if (lowercase_count + uppercase_count + digits_count + special_count) != leng:
                    continue

                sets = len(set(password))

                if (array_5d[lowercase_count][uppercase_count][digits_count][special_count][sets] > 0):
                    continue
                array_5d[lowercase_count][uppercase_count][digits_count][special_count][sets] = 1

                analysis = zxcvbn(password)
                score = analysis['score']

                new_row = [password, leng, lowercase_count, uppercase_count, digits_count, special_count, sets, score]

                writer.writerow(new_row)

if __name__ == "__main__":
    # add_password_data(0, 15000000)
    # add_lack_sample_data("./data/production.csv")
    df = pd.read_csv('./data/production.csv')
    print(df['strength'].value_counts())


# password,length,lowers,uppers,digits,specials,sets,strength