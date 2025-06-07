print()
sep = ""
end = ""

help()


range(a, b, c)
a = start
b = end (not included)
c = step value

list()



map(lambd x: x + "s", strings )

map function adds custom function to each and every items in a list

lambda x: is a custum function

lambda x: x + "s" means add a s to each an every item in that list

insted of writeing a single inline function, you can define custom
user define dfunction and then call that

def add_s(string):
    return string + "s"

map(add_s, strings)


filter()

iterates throug a list and applies the mentioned filter, if ok
keeps it else not

example 
x = filter(longer_than_4, strings) 

lambda x: {condition } is also valid

sum(numbers, start = start value)

