#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    int i;

    int N=10;
    for (i = 0; i < N; i++) {
        fork();
    }
    sleep(120);
    return 0;
}

