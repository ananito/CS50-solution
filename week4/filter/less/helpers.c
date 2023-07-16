#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int avrg = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            avrg = (float)(image[i][j].rgbtBlue) + (image[i][j].rgbtGreen) + (image[i][j].rgbtRed);
            avrg =  round((float) avrg / 3);
            image[i][j].rgbtRed = avrg;
            image[i][j].rgbtGreen = avrg;
            image[i][j].rgbtBlue = avrg;
        }

    }

    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int red, blue, green;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            red = round((float)(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue));
            green = round((float)(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue));
            blue = round((float)(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue));
            if (red > 255)
            {
                red = 255;
            }
            if (green > 255)
            {
                green = 255;
            }
            if (blue > 255)
            {
                blue = 255;
            }


            image[i][j].rgbtRed = red;
            image[i][j].rgbtGreen = green;
            image[i][j].rgbtBlue = blue;
        }

    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int temp;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2); j++)
        {
            temp = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][(width - j - 1)].rgbtRed;
            image[i][(width - j - 1)].rgbtRed = temp;

            temp = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][(width - j - 1)].rgbtBlue;
            image[i][width - j - 1].rgbtBlue = temp;


            temp = image [i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][(width - j - 1)].rgbtGreen;
            image[i][(width - j - 1)].rgbtGreen = temp;

        }

    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    int average = 0;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }

    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = 0;
            int blue = 0;
            int green = 0;
            int total = 0;

            for (int k = -1; k < 2 ; k++)
            {
                for (int l = -1; l < 2; l++)
                {
                    if (i + k >= 0 && i + k < (height) && j + l >= 0 && j + l < (width))
                    {
                        /*
                              0 1 2 3 4 5
                            0 A B C D E F
                            1 G H I J K L
                            2 M N O P Q R
                            3 S T U V W X

                            if i is 0 and k is -1 then i+k = -1 therfore it is invalid but if i is 3 and k = 1 then i+k = 4 which is invalid
                            if j is 0 and l is minus  j+l = -1 however if it is in the middle then no problem

                        */



                        red = red + copy[i + k][j + l].rgbtRed;
                        green = green + copy[i + k][j + l].rgbtGreen;
                        blue = blue + copy[i + k][j + l].rgbtBlue;
                        total++;
                    }
                }

            }
            image[i][j].rgbtRed = round((float) red / total);
            image[i][j].rgbtBlue = round((float) blue / total);
            image[i][j].rgbtGreen = round((float) green / total);



        }

    }





    return;
}
