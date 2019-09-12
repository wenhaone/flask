def getLCString(str1,str2):
    maxlen = len(str1) if len(str1) < len(str2) else len(str2)
    print(maxlen)
    example = str1 if len(str1) < len(str2) else str2
    print(example)
    other = str2 if str1 == example else str1
    print(other)
    l = []
    for i in range(maxlen):
        for j in range(maxlen, i, -1):
            if other.find(example[i:j]) != -1 :
                print(example[i:j])
                # if example[i:j] !="":

                l.append(example[i:j])

    return l

if __name__ == "__main__":
    str1 = "asdfgfd"
    str2 = "derdfgfrew"
    print("666")
    print(getLCString(str1,str2))