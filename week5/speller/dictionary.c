// Implements a dictionary's functionality

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 49999;

// Hash table
node *table[N];

// Dictionariry word count
int wordcount = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    /*
    *   The use of prime numbers was taken from
    *   https://computinglife.wordpress.com/2008/11/20/why-do-hash-functions-use-prime-numbers/
    */

    // hash word to find location
    int hash_key = hash(word);


    //node *temp = table[key];

    // treverse the list while it is not null
    while (table[hash_key] != NULL)
    {
        // compare the word in the current node with word
        if (strcasecmp(table[hash_key]->word, word) == 0)
        {
            //printf("word compared: %s\n", temp->word);
            return true;
        }
        else
        {
            table[hash_key] = table[hash_key]->next;
        }


    }



    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int key = 0;

    for (int i = 0, n = (strlen(word) + 1); i < n ; i++)
    {
        key = 31 * key + tolower(word[i]);
    }
    key = key % N;
    return key;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open the file
    FILE *input = fopen(dictionary, "r");


    // check if file opened
    if (input == NULL)
    {
        return false;
    }

    char words[LENGTH + 1];

    while (fscanf(input, "%s", words) != EOF)
    {

        // create a new node for each word
        node *new_word = malloc(sizeof(node));

        // check if malloc was succesfull
        if (new_word == NULL)
        {

            free(new_word);
            return false;
        }

        // set linked list next to NULL for security purpose
        new_word->next = NULL;

        // copy string to new_word
        strcpy(new_word->word, words);

        // get hash key
        int hkey = hash(words);


        // check if the table is not already full
        if (table[hkey] == NULL)
        {
            table[hkey] = new_word;
        }
        else
        {
            new_word->next = table[hkey];

            table[hkey] = new_word;
        }
        wordcount++;

    }
    //printf("Word count:%i\n", wordcount);

    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < (N + 1); i++)
    {
        node *list = table[i];
        node *temp = list;

        while (list != NULL)
        {
            list = list->next;
            free(temp);
            temp = list;
        }

    }

    return true;
}
