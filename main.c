#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 실패 함수를 계산하면서 최댓값을 추적하는 함수
int computeFailure(char pattern[], int m) {
    int i = 1, j = 0;
    int max = 0;
    int failure[m];
    failure[0] = 0;

    while (i < m) {
        if (pattern[i] == pattern[j]) {
            j++;
            failure[i] = j;
            if (j > max){
                max = j;
            }
            i++;
        } else {
            if (j != 0) {
                j = failure[j - 1];
            } else {
                failure[i] = 0;
                i++;
            }
        }
    }

    return max;
}

int main() {
    // 검색할 패턴의 최대 길이
    const int MAX_PATTERN_LENGTH = 100;

    // 사용자로부터 패턴의 길이 입력
    int m;
    scanf("%d", &m);

    // 사용자로부터 패턴 입력
    char pattern[MAX_PATTERN_LENGTH];
    scanf("%s", pattern);

    // 최대 실패 값 계산
    int maxFailure = computeFailure(pattern, m);

    printf("%d\n", maxFailure);

    return 0;
}

