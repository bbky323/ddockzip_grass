#include <stdio.h>



int main()
{
    char s1[13];    // ũ�Ⱑ 13�� char�� �迭�� ����
    int i = 0;
    int num = 0;
    int sum = 0;
    
    printf("���ڿ��� �Է��ϼ���: ");
    scanf_s("%13s", s1, sizeof(s1)); // ���� �����÷ο� ������ ���� ũ�� ����

    for (i = 0; i < sizeof(s1);i++) {
        if (s1[i] == 'I') {
            if (s1[i + 1] == 'I') {
                if (s1[i + 2] == 'V') {
                    i = i + 2; //IIV�̹Ƿ� 3��° �ε������� �ϳ��� ��
                    num = 3;
                }
                else if (s1[i + 2] == 'X') {
                    i = i + 2; //IIX�̹Ƿ� 3��° �ε������� �ϳ��� ��
                    num = 8;
                }
                else {
                    num = 1;
                }
            }
            else if (s1[i + 1] == 'V') {
                i = i + 1; //IV�̹Ƿ� 2��° �ε������� �ϳ��� ��
                num = 4;
            }
            else if (s1[i + 1] == 'X') {
                i = i + 1; //IX�̹Ƿ� 2��° �ε������� �ϳ��� ��
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