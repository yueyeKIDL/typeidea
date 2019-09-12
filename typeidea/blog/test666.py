def my_make(temp, counter_list):
    res = ''.join('{}{}'.format(v, k) for k, v in temp.items() if temp)
    counter_list.append(res)
    temp.clear()


def string_zip(words):
    temp = {}
    counter_list = []
    count = 0
    for word in words:
        if word not in temp:
            my_make(temp, counter_list)
            count = 1
        else:
            count += 1
        temp[word] = count
    my_make(temp, counter_list)
    return ''.join(counter_list).replace('1', '')


if __name__ == '__main__':
    words = 'ccddttttecc'
    print(string_zip(words))
