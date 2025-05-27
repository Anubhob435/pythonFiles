lst_alphabets = []
lst_num = []
lst_2 = []
lst_print = []
dictionary_1 = {
    1: "a", 2: "b", 3: "c", 4: "d", 5: "e",
    6: "f", 7: "g", 8: "h", 9: "i", 10: "j",
    11: "k", 12: "l", 13: "m", 14: "n", 15: "o",
    16: "p", 17: "q", 18: "r", 19: "s", 20: "t",
    21: "u", 22: "v", 23: "w", 24: "x", 25: "y", 26: "z", 27: " "
}

keys = list(dictionary_1.keys())
values = list(dictionary_1.values())

word = input("Enter word: ").lower()

print("OH I USED TO SAY !!")
for i in word:
    lst_alphabets.append(i)

for k in lst_alphabets:
    index = values.index(k)
    Key = keys[index]
    lst_num.append(Key)

def programme():
    count = 0
    for x in lst_num:
        for z in range(0, x):
            tempv = values[z]
            lst_print.append(tempv)
            print("".join(lst_print))
            if tempv != lst_alphabets[count]:
                lst_print.pop()
            else:
                count +=1

programme()
print("I FOUND YOU !!! :)")