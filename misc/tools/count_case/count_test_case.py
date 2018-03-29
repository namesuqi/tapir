# coding=utf-8
# author: zengyuetian
# count test case number via keyword "@reviewer"


import os


def count_keyword(file_name, word):
    count = 0
    f = open(file_name)
    lines = f.readlines()
    for line in lines:
        if line.find(word) >= 0:
            count += 1
    return count


if __name__ == "__main__":
    python_file_num = 0
    test_case_num = 0
    for root, dirs, files in os.walk("../../testsuite"):
        for fi in files:
            if fi.find('.py') > -1:
                python_file_num += 1
                # print fi
                full_path = os.path.join(root, fi)
                test_case_num += count_keyword(full_path, "@reviewer")

    print("\nTotal python file number is {0}.".format(python_file_num))
    print("\nTotal test case number is {0}.".format(test_case_num))
