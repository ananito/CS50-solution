#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);


int main(void)
{

    string text = get_string("Text: ") ;
    //int text_lenght = strlen(text);
    int word = count_words(text);
    int sentences = count_sentences(text);
    int letters = count_letters(text);

    /*The equatiion for finding the grade level is (0.0588 * L - 0.296 * S - 15.8) where
    L is the average letters per 100 words and S is the average sentences per 100 word*/


    // l =L letter/word*100
    float l = ((float) letters / word) * 100;


    float s = ((float) sentences / word)  * 100;

    int grade_level = round(0.0588 * l - 0.296 * s - 15.8);


    if (grade_level < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade_level > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade_level);
    }



    //printf("l: %i\n", grade_level);
    // printf("s : %f\n", s);


}

int count_letters(string text)
{
    int total_letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // check if it the char is an alphabatical char
        if (isalpha(text[i]))
        {
            total_letters++;
        }

    }
    return total_letters;

}

int count_words(string text)
{
    int word_count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isblank(text[i]) || text[i + 1] == 0)
        {
            word_count++;
            //printf("%i\n", word);
        }
    }
    return word_count;

}

int count_sentences(string text)
{
    int sentences_count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            sentences_count++;
        }

    }
    return sentences_count;

}