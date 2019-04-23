# import requests
# from spiders.settings import get_response, conn, cur
# from spiders.storage import stored_books
# from lxml import etree
#
# response = get_response('https://www.qu.la/')
# html = etree.HTML(response.text)
# b = html.xpath('//*[@id="newscontent"]/div[2]/ul/li[1]/span[2]/a/@href')[0].split('/')[2]
# print(b)
# if __name_ == '__main__':
# def main():
#     n = int(input())
#     s = input()
#     ans = 'yes'
#     if n==0 or n==1:
#         print('yes')
#         return 0
#     for i in range(1, n):
#         if s[i]=='1' and s[i]==s[i-1]:
#             ans = 'no'
#             break
#     print(ans)
#
#
# if __name__ == '__main__':
#     main()

# 3
# n, m = map(int, input().split())
# nm = []
# for i in range(n):
#     k = input().split()
#     nm.append(k)
# for i in range(n):
#     for j in range(m):
#         if i == 0:
#             if j == 0:

# s = input()
#
# a = 'MADASDsdasdh655'
# ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# abc = 'abcdefghijklmnopqrstuvwxyz'
# A_a = dict(zip(ABC, abc))
# for i in a:
#     if i in A_a:
#         a = a.replace(i, A_a.get(i))
# print(a)


# def main():
#     n = int(input())
#     s = input()
#     yes = 'Yes'
#     no = 'No'
#     is_0 = 0
#     if n == 0 or n == 1:
#         print(yes)
#         return 0
#
#     if s[0] == s[1] == 0 or s[-1] == s[-2] == 0:
#         print(no)
#         return 0
#     for i in range(1, n):
#         if s[i] == '1' and s[i] == s[i - 1]:
#             print(no)
#             return 0
#         if s[i] == '1':
#             is_0 = 0
#         else:
#             is_0 += 1
#         if is_0 == 3:
#             print(no)
#             return 0
#     print(yes)
#
#
# if __name__ == '__main__':
#     main()

'''
def main():
    n, m = map(int, input().split())
    nm = []
    for i in range(n):
        k = input().split()
        nm.append(k)
    for i in range(n):
        for j in range(m):
            if nm[i][j] == '*':
                if j != 0:
                    if nm[i][j - 1] == '.':
                        print('No')
                        return 0
                    elif nm[i][j - 1] != '*':
                        nm[i][j - 1] = int(nm[i][j - 1]) - 1
                        if nm[i][j - 1] < 0:
                            print('No')
                            return 0
                    if i != 0:
                        if nm[i - 1][j] == '.':
                            print('No')
                            return 0
                        elif nm[i - 1][j] != '*':
                            nm[i - 1][j] = int(nm[i - 1][j]) - 1
                            if nm[i - 1][j] < 0:
                                print('No')
                                return 0

                        if nm[i - 1][j - 1] == '.':
                            print('No')
                            return 0
                        elif nm[i - 1][j - 1] != '*':
                            nm[i - 1][j - 1] = int(nm[i - 1][j - 1]) - 1
                            if nm[i - 1][j - 1] < 0:
                                print('No')
                                return 0

                    if i != (n - 1):
                        if nm[i + 1][j] == '.':
                            print('No')
                            return 0
                        elif nm[i + 1][j] != '*':
                            nm[i + 1][j] = int(nm[i + 1][j]) - 1
                            if nm[i + 1][j] < 0:
                                print('No')
                                return 0
                        if nm[i + 1][j - 1] == '.':
                            print('No')
                            return 0
                        elif nm[i + 1][j - 1] != '*':
                            nm[i + 1][j - 1] = int(nm[i + 1][j - 1]) - 1
                            if nm[i + 1][j - 1] < 0:
                                print('No')
                                return 0
                if j != m - 1:
                    if nm[i][j + 1] == '.':
                        print('No')
                        return 0
                    elif nm[i][j + 1] != '*':
                        nm[i][j + 1] = int(nm[i][j + 1]) - 1
                        if nm[i][j + 1] < 0:
                            print('No')
                            return 0
                    if i != 0:
                        if nm[i - 1][j] == '.':
                            print('No')
                            return 0
                        elif nm[i - 1][j] != '*':
                            nm[i - 1][j] = int(nm[i - 1][j]) - 1
                            if nm[i - 1][j] < 0:
                                print('No')
                                return 0
                    if i != (n - 1):
                        if nm[i + 1][j + 1] == '.':
                            print('No')
                            return 0
                        elif nm[i + 1][j + 1] != '*':
                            nm[i + 1][j + 1] = int(nm[i + 1][j + 1]) - 1
                            if nm[i + 1][j + 1] < 0:
                                print('No')
                                return 0
    print('Yes')
'''

from selenium import webdriver

browser = webdriver.Firefox()

browser.get("http://www.baidu.com")
print(browser.page_source)
browser.close()
