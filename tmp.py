from zxcvbn import zxcvbn

password = "abczz!!!!!!!"
analysis = zxcvbn(password)
print(analysis['score'])