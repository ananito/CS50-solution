from cs50 import get_int

# Get card number from the user
card = get_int("Card Number: ")
main = [int(x) for x in str(card)]

checksum = 0

# Copy list
others = [int(x) for x in str(card)]

# Copy list
underlined = [int(x) for x in str(card)]
# Reverse he list and get ever other list
underlined.reverse()
underlined = underlined[1::2]
# print(underlined)
# print(others)

for i in underlined:

    if i in main:
        others.remove(i)

    # Chech if the underlined *2 is less than 2 digits
    if i * 2 <= 9:
        checksum = checksum + i*2
    # Chech if the underlined *2 is more than 2 digits
    elif i * 2 > 9:
        # first digit
        a = i*2//10

        # second digit
        b = i*2 % 10
        checksum = checksum + a + b
# print(others)

# final checksum
checksum = checksum + sum(others)
# print(checksum)

# Check if card num is valid
if checksum % 10 == 0:

    # Check if the card length is between 13 and 16
    if len(str(card)) >= 13 and len(str(card)) <= 16:
        # Check if the first 2 digits are 34 or 37 for AMEX
        if int(str(card)[0:2]) == 34 or int(str(card)[0:2]) == 37:
            print("AMEX")
        # Check if the first 2 digits is between 51 and 57 for Mastercard
        elif int(str(card)[0:2]) >= 51 and int(str(card)[0:2]) < 56:
            print("MASTERCARD")
        # Check if the first digit is 4 for visa
        elif int(str(card)[0:1]) == 4:
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")
else:
    print("INVALID")
# print(len(main))