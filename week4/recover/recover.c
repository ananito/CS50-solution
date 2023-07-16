#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const int BLOCK_SIZE = 512;

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recorver FILE\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("File not Found!\n");
        return 1;
    }

    BYTE blocks[BLOCK_SIZE];

    char filename[10];

    int filenum = 0;

    FILE *output;

    int jpg_num = 0;


    while (fread(blocks, 1, BLOCK_SIZE, input) == BLOCK_SIZE)
    {
        sprintf(filename, "%03i.jpg", filenum);


        //if block header is the conditions below then start a new pic
        if (blocks[0] == 0xff && blocks[1] == 0xd8 && blocks[2] == 0xff && (blocks[3] & 0xf0) == 0xe0)
        {
            // check if output is open
            if (jpg_num != 0)
            {
                jpg_num = 0; // if it is a new jpg then set jpg_num = 0
                fclose(output);
            }


            if (jpg_num == 0) // if jpg_num is zero then open a write to file
            {
                jpg_num = 1; // change jpg_num value to one so that i know it is not a new pi
                output = fopen(filename, "w");
                fwrite(blocks, 1, BLOCK_SIZE, output);
                filenum++;
                //printf("Hel2\n");
            }

        }
        else if (jpg_num == 1)
        {
            fwrite(blocks, 1, BLOCK_SIZE, output);
        }




    }

    fclose(output);

    fclose(input);


    return 0;
}