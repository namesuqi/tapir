# coding=utf-8
# author: zengyuetian


class People(object):
    def get_name(self):
        print self.name


if __name__ == "__main__":
    my_name = "name"
    p = People()
    p.__setattr__(my_name, "alex")
    p.get_name()