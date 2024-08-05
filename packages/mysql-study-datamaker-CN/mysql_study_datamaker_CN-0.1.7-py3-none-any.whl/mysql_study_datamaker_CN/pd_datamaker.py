import numpy as np
import pandas as pd
import random as rd


def __set_seed(seed=None):
    if not isinstance(seed, int) and seed != None:
        raise ValueError('seed must be an integer or None')

    if seed != None:
        np.random.seed(seed)
        rd.seed(seed)


def to_DataFrame_maker(n: int,
                       types: str = "subject",
                       low: int = 0,
                       high: int = 1,
                       seed: int | None = None,
                       people: int = 10,
                       names: tuple | list | None = None,
                       items: tuple | None = None,
                       write: bool = False) -> pd.DataFrame | None:
    """
    这只是一个为了方便生成一个随机访问的 DataFrame 数据而做的方法；
    现在只是实现了一些比较基础的功能，不要对这个方法报有过多的想法；
    目前的版本只能生成一个随机的成绩和姓名相关的 DataFrame对象；
    你可以扩大学科的种类或者更改学科的种类，在items参数中；
    下面的参数说明：
    :param n: 要生成的 column的数量
    :param types: 现在只有 subject 一种类型，向正常运行它，不要去更改这个参数！
    :param low: 目前是随机的最高分和最低分中的最低分，默认为0，不支持非int类型和小于0的数
    :param high: 最高分，不支持小于low
    :param people: row的数量
    :param names: index的索引项，可以不给，默认从 0 开始
    :param items: column的值，默认是学科，并放置了 9 个学科（语数外物化生史地政）
    :param write: 默认为False，如果是True，则写一个csv文件，该文件也是 x类型，如果存在则报错
    :return: pd.DataFrame 或 None
    """
    assert isinstance(n, int) and n > 0
    assert high > low >= 0 and isinstance(low, int) and isinstance(high, int)
    __set_seed(seed)
    if types == "subject":
        assert isinstance(people, int) and people > 0
        if items is None:
            items: tuple = ("Chinese",
                            "Math",
                            "English",
                            "Physics",
                            "Chemistry",
                            "Biology",
                            "History",
                            "Geography",
                            "Polity")
        if len(items) <= high:
            subjects = items[0:n]
        else:
            assert len(items) == n
            subjects = items

        if names is None:
            dic = {}
            for subject in subjects:
                score = [rd.randint(low, high) for _ in range(people)]
                dic[subject] = score
            result = pd.DataFrame(dic)
            if write:
                with open("dataFrame_maker.csv", "x") as file:
                    file.write(str(result))
            return result
        else:
            assert len(names) == people
            dic = {}
            for subject in subjects:
                score = [rd.randint(low, high) for _ in range(people)]
                dic[subject] = score
            result = pd.DataFrame(dic, index=names)
            if write:
                with open("dataFrame_maker.csv", "x") as file:
                    file.write(str(result))
            return result

    return None


def get_demo():
    content = """if __name__ == '__main__':
    names = ["Tom",
             "Bob",
             "Jerry",
             "Lucy",
             "Lily",
             "Mike",
             "Tony",
             "Amber",
             "Kevin",
             "Peter"]
    r = to_DataFrame_maker(n=3, low=80, high=150, people=10, names=names, write=True)
    print(r)"""
    print(content)


if __name__ == '__main__':

    names = ["Tom",
             "Bob",
             "Jerry",
             "Lucy",
             "Lily",
             "Mike",
             "Tony",
             "Amber",
             "Kevin",
             "Peter"]
    r = to_DataFrame_maker(n=3, low=80, high=150, people=10, names=names,seed=10)
    print(r)
