#include <stdio.h>



int main()
{
    char s1[13];    // 크기가 13인 char형 배열을 선언
    int i = 0;
    int num = 0;
    int sum = 0;
    
    printf("문자열을 입력하세요: ");
    scanf_s("%13s", s1, sizeof(s1)); // 버퍼 오버플로우 방지를 위해 크기 지정

    for (i = 0; i < sizeof(s1);i++) {
        if (s1[i] == 'I') {
            if (s1[i + 1] == 'I') {
                if (s1[i + 2] == 'V') {
                    i = i + 2; //IIV이므로 3번째 인덱스까지 하나의 값
                    num = 3;
                }
                else if (s1[i + 2] == 'X') {
                    i = i + 2; //IIX이므로 3번째 인덱스까지 하나의 값
                    num = 8;
                }
                else {
                    num = 1;
                }
            }
            else if (s1[i + 1] == 'V') {
                i = i + 1; //IV이므로 2번째 인덱스까지 하나의 값
                num = 4;
            }
            else if (s1[i + 1] == 'X') {
                i = i + 1; //IX이므로 2번째 인덱스까지 하나의 값
                num = 9;
            }
            else {
                num = 1;
            }
        }
        else if (s1[i] == 'V') {
            num = 5;
        }
        else if (s1[i] == 'X') {
            num = 10;
        }
        else {
            num = 0;
        }
        sum += num;
    }

    printf("%d", sum);

    return 0;
}