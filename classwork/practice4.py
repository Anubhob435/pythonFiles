def move_hashes_to_front(s):
    hash_count = s.count('#')
    s = s.replace('#', '')
    result = '#' * hash_count + s
    return result

# Test case
input_string = "move#hash#to#the#front"
output_string = move_hashes_to_front(input_string)
print(output_string)  