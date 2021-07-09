#include<stdio.h>
#include<string.h>


long long int calculate()
{
    short int stop = 0;
    long long int result[2] = {1, 1};
    int now = 0;
    printf("stop: ");
    scanf("%hd", &stop);
    if (stop == 0 || stop == 1) {
        return 1;
    }
    if (stop < 0) {
        stop = 32767;
    }
    for (int i = 1; i != stop; ++i) {
        result[now^1] += result[now];
        now ^= 1;
    }
    return result[now];
}

long long int new_calculate()
{   short int stop = 0;
    long long int result[2] = {1, 1};
    int now = 0;
    printf("stop: ");
    scanf("%hd", &stop);
    if (stop == 0 || stop == 1) {
        return 1;
    }
    if (stop < 0) {
        stop = 32767;
    }
    for (int i = 1; i != stop; ++i) {
        result[now^1] += result[now];
        now ^= 1;
    }
    return result[now];
}

void service() {
    int choice;
    long long int result;
    while (1) {
        printf("Your choice: ");
        scanf("%d", &choice);
        if (choice == 1) {
            result = calculate();
        } else if (choice == 2) {
            printf("Sending result %lld to %s\n", result);
        } else if (choice == 3) {
            return;
        } else {
            printf("Please input 1 or 2 or 3\n");
        }
    }
}

int main(){
    printf("%lld", new_calculate());
}