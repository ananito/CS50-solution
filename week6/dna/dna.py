import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("USAGE: ./database.csv ./sequences.txt")

    #  Read database file into a variable

    database = []

    with open(sys.argv[1], "r") as file:
        db = csv.DictReader(file)
        # This is the subsequences
        sequences = db.fieldnames
        for row in db:
            database.append(row)
    sequences.pop(0)

    # Read DNA sequence file into a variable

    with open(sys.argv[2], "r") as file:
        sequence = file.read()
    # print(sequence)

    # Find longest match of each STR in DNA sequence
    results = {}
    for subs in sequences:
        total = longest_match(sequence, subs)
        results[subs] = str(total)
    # print(results)

    # TODO: Check database for matching profiles
    for i in range(len(database)):
        # Make a copy of the database
        dbcopy = database[i].copy()
        # remove name from the copy so we can compare the copy and the result
        dbcopy.pop("name")
        if dbcopy == results:
            print(database[i]["name"])
            break
    else:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
