from pprint import pprint
from typing import Any
from py2neo import Graph
from ..config import settings


class Search:
    # 数据库链接
    def __init__(self):
        self.g = Graph(
            settings.NEO_PROFILE,
            auth=(settings.NEO_USER, settings.NEO_PASSWORD),
            name=settings.NEO_DB_NAME,
        )

    # 给定实体与特定的关系查找其他实体
    def entity_relation(self, entity: str, relation: str) -> list[dict[str, Any]]:
        sql = "match(x)-[r:{1}]-(y) where x.name='{0}' return x.name,y.name"
        return self.g.run(sql.format(entity, relation)).data()

    def entity_relations(self, entity: str, relations: list[str]) -> list[dict[str, Any]]:
        return sum((self.entity_relation(entity, relation) for relation in relations), [])

    # 给定实体的名称查找实体的属性
    def entity(self, entity: str, properties: str) -> list[dict[str, Any]]:
        sql = "match (x:Disease) where x.name = '{0}' return x.name, x.{1}"
        return self.g.run(sql.format(entity, properties)).data()


if __name__ == "__main__":
    s = Search()
    pprint(s.entity_relation("急腹症", "has_symptom"))
    pprint(s.entity("急腹症", "cure_way"))
    pprint(s.entity("感冒", "cure_way"))
    pprint(s.entity("感冒", "prevent"))
