from operator import itemgetter
from typing import Any

from more_itertools import first
from .search import Search
from pprint import pprint


class Answer:
    def __init__(self) -> None:
        self.searcher = Search()

    # 根据问题类型调用Search类查询neo4j数据库，并将直接查询结果返回
    def search_answer(self, question_type: str, entity: str) -> list[dict[str, Any]]:
        match question_type:
            case "disease_cause":  # 查询疾病的原因
                return self.searcher.entity(entity, "cause")

            case "disease_prevent":  # 查询疾病的防御措施
                return self.searcher.entity(entity, "prevent")

            case "disease_lasttime":  # 查询疾病的持续时间
                return self.searcher.entity(entity, "cure_lasttime")

            case "disease_cureprob":  # 查询疾病的治愈概率
                return self.searcher.entity(entity, "cured_prob")

            case "disease_cureway":  # 查询疾病的治疗方式
                return self.searcher.entity(entity, "cure_way")

            case "disease_easyget":  # 查询疾病的易发人群
                return self.searcher.entity(entity, "easy_get")

            case "disease_desc":  # 查询疾病的相关介绍
                return self.searcher.entity(entity, "desc")

            case "disease_symptom":  # 查询疾病有哪些症状
                return self.searcher.entity_relation(entity, "has_symptom")

            case "symptom_disease":  # 查询症状会导致哪些疾病
                return self.searcher.entity_relation(entity, "has_symptom")

            case "disease_acompany":  # 查询疾病的并发症
                return self.searcher.entity_relation(entity, "accompany_with")

            case "disease_not_food":  # 查询疾病的忌口
                return self.searcher.entity_relation(entity, "no_eat")

            case "disease_do_food":  # 查询疾病建议吃的东西
                return self.searcher.entity_relations(entity, ["do_eat", "recommend_eat"])

            case "disease_drug":  # 查询疾病常用药品
                return self.searcher.entity_relations(entity, ["common_drug", "recommend_drug"])

            case "disease_check":  # 查询疾病应该进行的检查
                return self.searcher.entity_relation(entity, "need_check")

        assert False

    # 调用serach_answer函数，获得查询结果，依据结果生成对应的自然语言回答的字符串
    def create_answer(self, question_type: str, entity: str) -> str:
        answers = self.search_answer(question_type, entity)
        if not answers:
            return "暂时没有相关信息"
        match question_type:
            case "disease_accompany":
                return self.format_answer(answers, "{0}的并发症有：{1}等")
            case "disease_cause":
                return self.format_answer(answers, "{0}可能的成因有以下几种：{1}")
            case "disease_check":
                return self.format_answer(answers, "患有{0}应该检查{1}等项目")
            case "disease_cureprob":
                # TODO some have prefixes
                return self.format_answer(answers, "{0}的治愈概率约为：{1}")
            case "disease_cureway":
                return self.format_answer(answers, "{0}的治疗方式有：{1}")
            case "disease_desc":
                return self.format_answer(answers, "{0}的简介：{1}")
            case "disease_do_food":
                return self.format_answer(answers, "患有{0}建议食用{1}等食物")
            case "disease_drug":
                return self.format_answer(answers, "治疗{0}应该吃：{1}等药物")
            case "disease_easyget":
                return self.format_answer(answers, "{0}的易发人群有：{1}")
            case "disease_lasttime":
                return self.format_answer(answers, "{0}治疗需要的时间大致为：{1}")
            case "disease_not_food":
                return self.format_answer(answers, "患有{0}不宜食用{1}等食物")
            case "disease_prevent":
                return self.format_answer(answers, "{0}的预防措施有：{1}")
            case "disease_symptom":
                return self.format_answer(answers, "{0}的大致症状如下：{1}")
            case "symptom_disease":
                return self.format_answer(answers, "{0}症状会导致的疾病有：{1}")
        return "暂时没有相关信息"

    def format_answer(self, answers: list[dict[str, Any]], fmt: str, *, sep: str = "、") -> str:
        ans_str = ""
        if answers:
            if "y.name" in answers[0]:
                # 一堆{x.name, y.name}
                ans_str = sep.join(map(itemgetter("y.name"), answers))
            else:
                # answers[0][key]是一个字符串或字符串列表？
                key = first((k for k in answers[0].keys() if k != "x.name"))
                val = answers[0][key]
                ans_str = sep.join(val) if isinstance(val, list) else val
            return fmt.format(answers[0]["x.name"], ans_str)

    def create_answer_multi(self, question_type: str, entitys: list[str]) -> list[str]:
        return [self.create_answer(question_type, entity) for entity in entitys]


if __name__ == "__main__":
    a = Answer()
    # print(a.create_answer("disease_cureprob", "感冒"))
    # print(a.create_answer("disease_prevent", "急腹症"))
    # print(a.create_answer("disease_do_food", "感冒"))
    print(a.create_answer_multi("disease_cureprob", ["感冒", "急腹症", "中风"]))
