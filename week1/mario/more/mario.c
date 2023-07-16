#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    // get the height of the pyramid fro the user
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    //first loop through the row
    for (int i = 1; i <= h; i++)
    {
        // print spaces
        for (int j = 1; j <= h - i; j++)
        {
            printf(" ");
        }
        //print #tags
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        // print space bewteen the triangles
        printf("  ");
        // make the second triangle
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }

        printf("\n");

    }
}