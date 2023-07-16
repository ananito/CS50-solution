#include <stdio.h>
#include <math.h>
#include <cs50.h>



int clenght(long c_num);
void checksum(long cardnum);
void type(long c_num, int length, int sum);


int main(void)
{
    long creditnum = get_long("Number: ");
    checksum(creditnum);
}

void checksum(long cardnum)
{
    long cardnumber = cardnum;
    int length = clenght(cardnum);
    int sum;

    // divide length by 2
    for (int i = 0; i < (length / 2) + 1; i++)
    {
        // get the first num starting from the last
        int lastnum = cardnum % 10;
        // print first num
        //printf("lastnum: %i\n", lastnum);
        // divide the card num /10 to decrease the size
        cardnum = cardnum / 10;
        // get the checksum number
        int placeholder = cardnum % 10;
        // shrink the num again
        cardnum = cardnum / 10;
        // multiply the placehoder*2
        placeholder = placeholder * 2;
        //int sum = placeholder*2;
        // check if sum is a 2 dight num
        if (placeholder < 9)
        {
            sum = sum + placeholder;
            //printf("total: %i\n", sum);
        }
        else
        {
            int a = placeholder % 10;

            int b = placeholder / 10;

            sum = sum + a + b;
        }
        // get the final sum
        sum = sum + lastnum;
    }
    // checks if the last num of the sum is 0
    type(cardnumber, length, sum);
}

// gets the length of the credit card number
int clenght(long c_num)
{
    int length = 0;

    while (c_num > 0)
    {
        c_num = c_num / 10;
        length++;
    }
    return length;
}

void type(long cardnum, int length, int sum)
{
    //divide credit card num by 10^length-2 to get the first 2 digits
    long typenum = cardnum / pow(10, length - 2);

    if ((sum % 10) == 0)
    {

        //printf("%li\n", typenum);
        if (length == 15 && (typenum == 34 || typenum == 37))
        {
            printf("AMEX\n");
        }
        else if (length == 16 && (typenum > 50 && typenum < 56))
        {
            printf("MASTERCARD\n");
        }
        else if ((length == 13 || length == 16) && ((typenum / 10) == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

}