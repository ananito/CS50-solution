import re


# Get text from the user
text = input("Text: ")


# Split text into words
words = text.split()

# Use regex to to find all letters of a the text
letters = re.findall("[A-Z]|[a-z]", text)
# Use regex to find each punctuation so that it is a sentence
sentences = re.findall("[.!?]", text)

# Calculate average letter per word
l = (len(letters) / len(words)) * 100

#  Calculate avrage sentences per words
s = (len(sentences) / len(words)) * 100

# Find the level of the book
index = round(0.0588 * l - 0.296 * s - 15.8)

if index < 0:
    print("Before Grade 1")
elif index > 0 and index < 16:
    print(f"Grade {index}")
else:
    print("Grade 16+")