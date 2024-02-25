import re
pattern = r"\d,\d"

text = '01.01 100.1,02.01.30'

print(re.search(pattern, text))
if re.search(pattern, text):
    print('Работает')
else:
    print('Не работает')
