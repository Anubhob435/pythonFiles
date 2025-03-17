from collections import Counter

#Write a python code to arrange the elements of an array based on the rand( frequency of their appearence.)

arr = [1, 2, 3, 2, 4, 3, 2]
freq = Counter(arr)
result = sorted(arr, key=lambda x: freq[x], reverse=True)
print(result)