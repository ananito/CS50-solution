#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

void cipher(string key, string text);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    if (strlen(argv[1]) != 26)
    {
        printf("Key must be 26 characters.\n");
        return 1;
    }
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        for (int j = 0; j < i; j++)
        {
            if (toupper(argv[1][j]) == toupper(argv[1][i]))
            {
                // if the same character is in the key twice then break
                printf("Invalid Key! Can't use the same letter twice.\n");
                return 1;
            }

        }

        // check if char is an alphabets
        if (!isalpha(argv[1][i]))
        {
            printf("Key must only contain letters!\n");
            return 1;
        }

    }

    string plain_text = get_string("Plain Text: ");

    printf("ciphertext: ");

    cipher(argv[1], plain_text); // call the cypher function
    return 0;

}

void cipher(string key, string text)
{
    int alphabets[26];
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        alphabets[i] = key[i];
    }

    // to keep the same case sensetivity
    for (int i = 0, j = strlen(text); i < j; i++)
    {
        if (isblank(text[i]))
        {
            printf(" ");
        }
        else
        {
            if (isdigit(text[i]) || ispunct(text[i]))
            {
                printf("%c", text[i]);
            }
            else
            {
                if (isupper(text[i]))
                {
                    printf("%c", toupper(alphabets[text[i] - 65]));
                    /* since the uppercase letter start with 65 by
                    subtracting it from the other upper vaur we get an index to locate in the array*/
                }
                else if (islower(text[i]))
                {
                    printf("%c", tolower(alphabets[text[i] - 97]));
                }

            }

        }

    }
    printf("\n");
}