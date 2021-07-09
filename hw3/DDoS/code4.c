#include <stdio.h>
#include <regex.h>
#include <string.h>
#include <stdlib.h>
#include <seccomp.h>

void addSeccomp();
void initialize();
char *readEmail();
void service(const char *);
long long int calculate();

int main() {
    char *email = NULL;
    initialize();
    printf("Give me your email: ");
    email = readEmail();
    if (!email) {
        _Exit(0);
    }
    service(email);
}

void addSeccomp() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_load(ctx);
}

void initialize() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    addSeccomp();
}

// <__start_CNS_readEmail>
char *readEmail() {
    int status = REG_NOMATCH;
    regex_t regex;
    int notSuccess = 0;
    const char *namePattern = "^[a-zA-Z]+([a-zA-Z0-9\\-]?[a-zA-Z]+)+@([a-zA-Z0-9\\-]+\\.)+[a-zA-Z0-9]+$";
    regmatch_t matchPointer[1];
    char *email = calloc(100, 1);
    if (!fgets(email, 99, stdin) || strlen(email) < 1) {
        printf("Error while reading email\n");
        return NULL;
    }
    email[strlen(email)-1] = '\0';

    notSuccess = regcomp(&regex, namePattern, REG_EXTENDED);
    if (notSuccess) {
        char *buf = calloc(100, 1);
        size_t bufSize = 100;
        size_t size = regerror(notSuccess, &regex, buf, bufSize);
        printf("Regex compile error\n");
        printf("%s, %lu\n", buf, size);
        return NULL;
    }

    status = regexec(&regex, email, 1, matchPointer, 0);
    regfree(&regex);
    if (status == REG_NOMATCH) {
        printf("Your email does not match the regex\n");
        return NULL;
    } else if (status == 0) {
        email[matchPointer[0].rm_eo] = '\0';
    } else {
        printf("regexec error, unknown return value %d\n", status);
        return NULL;
    }

    return email;
}
// <__end_CNS_readEmail>

// <__start_CNS_service>
void service(const char *email) {
    {
    int choice;
    long long int result;
    while (1) {
        printf("Your choice: ");
        if(!scanf("%d", &choice)){
            printf("Input A NUMBER!!!!!!!!!!!!\n");
            return;
            }
        if (choice == 1) {
            result = calculate();
        } else if (choice == 2) {
            printf("Sending result %lld to %s\n", result, email);
        } else if (choice == 3) {
            return;
        } else {
            printf("Please input 1 or 2 or 3\n");
        }
    }
}

// <__end_CNS_service>

// <__start_CNS_calculate>
long long int calculate() {
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
}
// <__end_CNS_calculate>

                                  