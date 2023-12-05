#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ���� �Լ��� ����ϸ鼭 �ִ��� �����ϴ� �Լ�
int computeFailureFunction(char pattern[], int m) {
    int i = 1, j = 0;
    int max = 0;
    // �������� �Ҵ�� �迭
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
            max = (j > max) ? j : max; // �ִ� ����
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

    // ���� �Ҵ�� �޸� ����
    free(failure);

    return max;
}


int main() {
    // �˻��� ������ �ִ� ����
    const int MAX_PATTERN_LENGTH = 100;

    // ����ڷκ��� ������ ���� �Է�
    int m;
    scanf_s("%d", &m);

    // ����ڷκ��� ���� �Է�
    char pattern[100];
    scanf_s("%s", pattern);

    // �ִ� ���� �� ���
    int maxFailure = computeFailureFunction(pattern, m);

    // ��� ���
    printf("%d", maxFailure);

    return 0;
}
