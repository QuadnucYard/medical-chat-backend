from typing import Any, cast

import jieba.analyse


class SimpleNLP:
    def __init__(self) -> None:
        ...

    def __call__(self, text: str):
        return cast(list[str], jieba.analyse.extract_tags(text, withWeight=False))


if __name__ == "__main__":
    from pprint import pprint
    nlp = SimpleNLP()
    sents = [
        "查询预防感冒的措施。",
        "了解如何预防高血压。",
        "想知道预防糖尿病的方法。",
        "请告诉我防止中暑的措施。",
        "想了解预防心脏病的建议。",
        "请问有没有预防流感的方法。",
        "想知道预防哮喘的措施。",
        "了解骨折的恢复时间。",
        "查询癌症的持续时间。",
        "请告诉我脑卒中的持续时间。",
        "查询感冒时建议吃的东西。",
        "了解高血压时建议吃的东西。",
        "想知道糖尿病时建议吃的东西。",
        "请告诉我中暑时建议吃的东西。",
        "想了解心脏病时建议吃的东西。",
        "请问流感时建议吃的东西有哪些。",
        "想知道哮喘时建议吃的东西。",
        "了解骨折时建议吃的东西。",
        "查询癌症时建议吃的东西。",
        "请告诉我中风时建议吃的东西。",
        "晓美焰来到北京立方庭参观自然语义科技公司",
    ]
    pprint(list(map(nlp, sents)))
