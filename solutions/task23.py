def _solve(text: str) -> str:
    with open('chemlist.txt', 'r') as chemlist:
        chem = [i[:-1].lower().split(',') for i in chemlist.readlines()]
    chem.sort(key=lambda x: len(x[1]), reverse=True)
    print(chem)
    for elem in chem:
        text = text.replace(elem[1], elem[0])
    print(text)
    return text