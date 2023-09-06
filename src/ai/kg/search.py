from py2neo import Graph, Node


class Search:
    # 数据库链接
    def __init__(self):
        self.g = Graph("http://10.203.163.86:7474/", auth=("neo4j", "Citrus130649"), name="neo4j")
        # self.g = Graph('http://localhost:7474/', auth=("neo4j", "Citrus130649" ),name='neo4j')

    # 给定实体与特定的关系查找其他实体
    def search_entity_relation(self, entity: str, relation: str):
        sql = "match(x)-[r:{1}]-(y) where x.name='{0}' return x.name,y.name".format(
            entity, relation
        )
        res = self.g.run(sql).data()
        return res

    # 给定实体的名称查找实体的属性
    def search_entity(self, entity: str, properties: str):
        sql = "match (x:Disease) where x.name = '{0}' return x.name, x.{1}".format(
            entity, properties
        )
        res = self.g.run(sql).data()
        return res


if __name__ == "__main__":
    s = Search()
    # print(s.search_entity_relation("急腹症","has_symptom"))
    print(s.search_entity("急腹症", "cure_way"))
