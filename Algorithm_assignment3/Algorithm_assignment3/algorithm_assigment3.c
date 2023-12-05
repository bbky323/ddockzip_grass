#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 실패 함수를 계산하면서 최댓값을 추적하는 함수
int computeFailureFunction(char pattern[], int m) {
    int i = 1, j = 0;
    int max = 0;
    // 동적으로 할당된 배열
    int* failure = (int*)malloc(m * sizeof(int));
    if (failure == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    failure[0] = 0;

    while (i < m) {
        if (pattern[i] == pattern[j]) {
            j++;
            failure[i] = j;
            max = (j > max) ? j : max; // 최댓값 갱신
            i++;
        }
        else {
            if (j != 0) {
                j = failure[j - 1];
            }
            else {
                failure[i] = 0;
                i++;
            }
        }
    }

    // 동적 할당된 메모리 해제
    free(failure);

    return max;
}


int main() {
    // 검색할 패턴의 최대 길이
    const int MAX_PATTERN_LENGTH = 100;

    // 사용자로부터 패턴의 길이 입력
    int m;
    scanf_s("%d", &m);

    // 사용자로부터 패턴 입력
    char pattern[100];
    scanf_s("%s", pattern);

    // 최대 실패 값 계산
    int maxFailure = computeFailureFunction(pattern, m);

    // 결과 출력
    printf("%d", maxFailure);

    return 0;
}
