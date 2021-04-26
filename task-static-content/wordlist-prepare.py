with open('wordlist.txt', 'r') as file:
    content = file.read()

result = set()
for line in content.replace(' ', '\n').split('\n'):
    if len(line) == 0:
        continue
    if line.isalpha():
        result.add(line.lower())
        continue

    word = ''
    for char in line:
        if char.isalpha():
            word += char
    result.add(word.lower())

with open('wordlist.txt', 'w') as file:
    print(*list(result), sep='\n', file=file)