from py2neo import Graph, Node
from search import Search


class Answer:
    # 提供问题类型与实体
    def __init__(self, question_type: str, entity: str) -> None:
        self.searcher = Search()
        self.question_type = question_type
        self.entity = entity
        self.numlimit: int = 20

    # 改变要查询问题
    def change_question(self, question_type, entity):
        self.question_type = question_type
        self.entity = entity

    # 根据问题类型调用Search类查询neo4j数据库，并将直接查询结果返回
    def search_answer(self) -> list:
        # 查询疾病的原因
        if self.question_type == "disease_cause":
            return self.searcher.search_entity(self.entity, "cause")

        # 查询疾病的防御措施
        elif self.question_type == "disease_prevent":
            return self.searcher.search_entity(self.entity, "prevent")

        # 查询疾病的持续时间
        elif self.question_type == "disease_lasttime":
            return self.searcher.search_entity(self.entity, "cure_lasttime")

        # 查询疾病的治愈概率
        elif self.question_type == "disease_cureprob":
            return self.searcher.search_entity(self.entity, "cured_prob")

        # 查询疾病的治疗方式
        elif self.question_type == "disease_cureway":
            return self.searcher.search_entity(self.entity, "cure_way")

        # 查询疾病的易发人群
        elif self.question_type == "disease_easyget":
            return self.searcher.search_entity(self.entity, "easy_get")

        # 查询疾病的相关介绍
        elif self.question_type == "disease_desc":
            return self.searcher.search_entity(self.entity, "desc")

        # 查询疾病有哪些症状
        elif self.question_type == "disease_symptom":
            return self.searcher.search_entity_relation(self.entity, "has_symptom")

        # 查询症状会导致哪些疾病
        elif self.question_type == "symptom_disease":
            return self.searcher.search_entity_relation(self.entity, "has_symptom")

        # 查询疾病的并发症
        elif self.question_type == "disease_acompany":
            return self.searcher.search_entity_relation(self.entity, "acompany_with")

        # 查询疾病的忌口
        elif self.question_type == "disease_not_food":
            return self.searcher.search_entity_relation(self.entity, "no_eat")

        # 查询疾病建议吃的东西
        elif self.question_type == "disease_do_food":
            ans1 = self.searcher.search_entity_relation(self.entity, "do_eat")
            ans2 = self.searcher.search_entity_relation(self.entity, "recommand_eat")
            return ans1 + ans2

        # 查询疾病常用药品
        elif self.question_type == "disease_drug":
            ans1 = self.searcher.search_entity_relation(self.entity, "common_drug")
            ans2 = self.searcher.search_entity_relation(self.entity, "recommand_drug")
            return ans1 + ans2

        # 查询疾病应该进行的检查
        elif self.question_type == "disease_check":
            return self.searcher.search_entity_relation(self.entity, "need_check")

    # 调用serach_answer函数，获得查询结果，依据结果生成对应的自然语言回答的字符串
    def create_answer(self) -> str:
        answers = self.search_answer()
        if not answers:
            return "暂时没有相关信息"
        # 查询疾病的原因
        if self.question_type == "disease_cause":
            res = ""
            for item in answers[0]["x.cause"]:
                res += item
            natural_language_answer = "{0}可能的成因有以下几种：{1}".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病的预防措施
        elif self.question_type == "disease_prevent":
            res = ""
            for item in answers[0]["x.prevent"]:
                res += item
            natural_language_answer = "{0}的预防措施有：{1}".format(answers[0]["x.name"], res)
            return natural_language_answer
        # 查询疾病的持续时间
        elif self.question_type == "disease_lasttime":
            res = ""
            for item in answers[0]["x.cure_lasttime"]:
                res += item
            natural_language_answer = "{0}治疗需要的时间大致为：{1}".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病的治愈概率
        elif self.question_type == "disease_cureprob":
            res = ""
            for item in answers[0]["x.cured_prob"]:
                res += item
            res = res[3:]
            natural_language_answer = "{0}的治愈概率约为：{1}".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病的治疗方式
        elif self.question_type == "disease_cureway":
            res = ""
            for item in answers[0]["x.cure_way"]:
                res += item
                res += "、"
            res = res[:-1]
            natural_language_answer = "{0}的治疗方式有：{1}".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病的易发人群
        elif self.question_type == "disease_easyget":
            res = ""
            for item in answers[0]["x.easy_get"]:
                res += item
            natural_language_answer = "{0}的易发人群有：{1}".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病的相关介绍
        elif self.question_type == "disease_desc":
            res = ""
            for item in answers[0]["x.desc"]:
                res += item
            natural_language_answer = "{0}的简介：{1}".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病有哪些症状
        elif self.question_type == "disease_symptom":
            res = ""
            for i in answers:
                res += i["y.name"]
                res += "、"
            res = res[:-1]
            natural_language_answer = "{0}的大致症状如下：{1}".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询症状会导致哪些疾病
        elif self.question_type == "symptom_disease":
            res = ""
            for i in answers:
                res += i["y.name"]
                res += "、"
            res = res[:-1]
            natural_language_answer = "{0}症状会导致的疾病有：{1}".format(answers[0]["x.name"], res)
            return natural_language_answer
        # 查询疾病的并发症
        elif self.question_type == "disease_acompany":
            res = ""
            for i in answers:
                res += i["y.name"]
                res += "、"
            res = res[:-1]
            natural_language_answer = "{0}的并发症有：{1}等".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病的忌口
        elif self.question_type == "disease_not_food":
            res = ""
            for i in answers:
                res += i["y.name"]
                res += "、"
            res = res[:-1]
            natural_language_answer = "患有{0}不宜食用{1}等食物".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病建议吃的东西
        elif self.question_type == "disease_do_food":
            res = ""
            for i in answers:
                res += i["y.name"]
                res += "、"
            res = res[:-1]
            natural_language_answer = "患有{0}建议食用{1}等食物".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病常用药品
        elif self.question_type == "disease_drug":
            res = ""
            for i in answers:
                res += i["y.name"]
                res += "、"
            res = res[:-1]
            natural_language_answer = "治疗{0}应该吃：{1}等药物".format(answers[0]["x.name"], res)
            return natural_language_answer

        # 查询疾病应该进行的检查
        elif self.question_type == "disease_check":
            res = ""
            for i in answers:
                res += i["y.name"]
                res += "、"
            res = res[:-1]
            natural_language_answer = "患有{0}应该检查{1}等项目".format(answers[0]["x.name"], res)
            return natural_language_answer


if __name__ == "__main__":
    a = Answer("prevent", "急腹症")
    print(a.create_answer())
