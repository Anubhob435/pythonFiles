# Python Function Reference

## Basic Functions

### `print()`
- `sep=""` - separator between items
- `end=""` - what to print at the end

### `help()`
Get help documentation for objects

### `range(a, b, c)`
- `a` = start value
- `b` = end value (not included)
- `c` = step value

### `list()`
Create a new list

## Higher-Order Functions

### `map()`
Applies a function to each item in a list

**Using lambda:**
```python
map(lambda x: x + "s", strings)
```

**Using custom function:**
```python
def add_s(string):
    return string + "s"

map(add_s, strings)
```

### `filter()`
Filters items in a list based on a condition

**Example:**
```python
x = filter(longer_than_4, strings)
# or with lambda
x = filter(lambda x: condition, strings)
```

### `sum(numbers, start=0)`
Sum all numbers in a list with optional start value

### `sorted()`
Returns a sorted list

**Parameters:**
- `reverse=True` - sort in descending order
- `key` - custom function to specify sorting criteria

**Example:** Sort list of dictionaries by specific key
```python
sorted(list_of_dicts, key=lambda x: x['key_name'])
```

## Iteration Functions

### `enumerate()`
Enhanced for loop with index

```python
for index, task in enumerate(tasks):
    print(f"{index + 1}. {task}")
```

### `zip()`
Combines multiple iterables (stops at shortest length)

## File Operations

### `open()`
Open a file with specified permissions
- `"r"` - read
- `"w"` - write
- `"a"` - append
- `"wr"` - read/write

### File Handling Best Practice
```python
with open("filename.txt", "w") as file:
    file.write("content")
    # file automatically closes
```

**Manual closing:**
```python
file.close()
```


pprint()