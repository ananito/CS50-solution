from cs50 import get_int

# Get the height from the user
while True:
    height = get_int("Height: ")
    if height > 0 and height <= 8:
        break

for i in range(1, height+1):

    # Prints the first half pyramid
    print(" " * (height - i) + "#" * i)