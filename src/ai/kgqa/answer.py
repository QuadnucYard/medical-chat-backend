import random
from dataclasses import dataclass
from operator import itemgetter
from typing import Any

from more_itertools import first

from .search import Search


@dataclass
class AnswerResult:
    entity: str
    items: list[str]
    text: str
    marked_text: str


def mark_answer(text: str):
    return text.replace("\n", "<br>")


class Answer:
    def __init__(self) -> None:
        self.searcher = Search()
        self.answer_formats = {
            "disease_accompany": ["{0}的并发症有：{1}等", "{0}可能会并发这些疾病：{1}", "{1}是{0}的并发症"],
            "disease_cause": ["{0}可能的成因有以下几种：{1}", "{0}的病因大致为：{1}", "{0}有以下几种致病原因{1}"],
            "disease_check": ["患有{0}应该检查{1}等项目", "得了{0}应该做这些检查：{1}", "{0}需要的检查有：{1}等项目"],
            "disease_cureprob": [
                "{0}的治愈概率约为：{1}",
                "治好{0}的概率约为：{1}",
            ],
            "disease_cureway": ["{0}的治疗方式有：{1}", "{0}可以采取的治疗方式有：{1}", "患上{0}应该尝试以下方式治疗：{1}"],
            "disease_desc": ["{0}的简介：{1}", "{0}的相关信息如下：{1}", "{0}的主要特征为：{1}"],
            "disease_do_food": [
                "患有{0}建议食用{1}等食物",
                "得了{0}要多吃：{1}等食物",
                "对{0}的患者，请注意在饮食方面多摄入这些食物：{1}",
            ],
            "disease_drug": ["治疗{0}应该吃：{1}等药物", "{0}要服用{1}来治疗", "患有{0}要服用这些药物：{1}"],
            "disease_easyget": ["{0}的易发人群有：{1}", "{1}容易患上{0}"],
            "disease_lasttime": ["{0}治疗需要的时间大致为：{1}", "{0}的持续时间大致为{1}", "{0}大约需要{1}来治疗"],
            "disease_not_food": ["患有{0}不宜食用{1}等食物", "患有{0}最好不要吃{1}等食物", "{0}的忌口有：{1}等食物"],
            "disease_prevent": ["{0}的预防措施有：{1}", "预防{0}可以做这些措施：{1}", "可以采用以下方法：{1}来预防{0}"],
            "disease_symptom": ["{0}的大致症状如下：{1}", "得了{0}会出现这些症状：{1}", "{0}的可能症状有：{1}"],
            "symptom_disease": ["{0}症状会导致的疾病有：{1}", "{0}症状可能预示着这些疾病{1}"],
        }
        self.answer_fallback = ["暂时没有{0}相关信息"]
        self.answer_none = ["您的问题并不明确，请换个问法再说一遍，谢谢。"]
        self.answer_unk = [
            "您的问题好像超出了我的回答范围，请问一个合适的问题",
            "这个问题似乎与医学无关，请重新考虑",
            "我是医药问答机器人，无法回答与医疗无关的问题，请重新提问",
        ]

    def search_answer(self, question_type: str, entity: str) -> list[dict[str, Any]]:
        """根据问题类型调用Search类查询neo4j数据库，并将直接查询结果返回"""
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
            case "disease_accompany":  # 查询疾病的并发症
                return self.searcher.entity_relation(entity, "accompany_with")
            case "disease_not_food":  # 查询疾病的忌口
                return self.searcher.entity_relation(entity, "no_eat")
            case "disease_do_food":  # 查询疾病建议吃的东西
                return self.searcher.entity_relations(entity, ["do_eat", "recommend_eat"])
            case "disease_drug":  # 查询疾病常用药品
                return self.searcher.entity_relations(entity, ["common_drug", "recommend_drug"])
            case "disease_check":  # 查询疾病应该进行的检查
                return self.searcher.entity_relation(entity, "need_check")
        print("Unknown", question_type)
        assert False

    def extract_search_results(self, answers: list[dict[str, Any]]) -> list[str]:
        if not answers:
            return []
        if "y.name" in answers[0]:
            # 一堆{x.name, y.name}
            return list(map(itemgetter("y.name"), answers))
        else:
            key = first((k for k in answers[0].keys() if k != "x.name"))
            val = answers[0][key]
            return val if isinstance(val, list) else [val]

    def create_answer(self, question_type: str, entity: str) -> AnswerResult:
        """调用serach_answer函数，获得查询结果，依据结果生成对应的自然语言回答的字符串"""
        results = self.search_answer(question_type, entity)
        extracted = self.extract_search_results(results)
        txt = (
            random.choice(self.answer_formats[question_type]).format(entity, "、".join(extracted))
            if extracted
            else random.choice(self.answer_fallback).format(entity)
        )
        return AnswerResult(entity=entity, items=extracted, text=txt, marked_text=mark_answer(txt))

    def create_answer_multi(self, question_type: str, entitys: list[str]) -> list[AnswerResult]:
        return [self.create_answer(question_type, entity) for entity in entitys]

    def get_answer_none(self):
        return random.choice(self.answer_none)
    
    def get_answer_unk(self):
        return random.choice(self.answer_unk)


if __name__ == "__main__":
    a = Answer()
    print(a.create_answer("disease_cureprob", "感冒"))
    print(a.create_answer("disease_prevent", "急腹症"))
    print(a.create_answer("disease_do_food", "感冒"))
    print(a.create_answer_multi("disease_cureprob", ["感冒", "急腹症", "中风"]))
