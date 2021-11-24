from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
import csv
# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph("http://localhost:7474", username="neo4j", password='zhao')
graph.delete_all()

with open('Metal material.csv', 'r') as f:
    reader = csv.reader(f)
    data = list(reader)
    print(data[1])
# ['2A12铝合金', ' 固溶', ' 高温、高湿、高盐', ' 14个月', '点腐蚀，蚀坑357μm']
for i  in  range(1, len(data)):

    node = Node('MetallicMateria',name=data[i][1],id = data[i][0])
    graph.create(node)

    relation = Node('TreatmentProc', name=data[i][2])
    relation1 = Node(' EnvTest', name=data[i][3])
    relation2 = Node('TestTime', name=data[i][4])
    relation3 = Node('Performance', name=data[i][5])
    matcher = NodeMatcher(graph)
    nodelist = list(matcher.match('Performance', name=data[i][5]))
    if len(nodelist) > 0:  # 表示节点存在，不需创建新的节点
        relation3 = nodelist[0]
        Performance = Relationship(node, relation1.__name__, relation3)
        graph.create(Performance)
    else:
        #创建节点
        graph.create(relation3)
        #创建关系
        Performance = Relationship(node,relation1.__name__,relation3)
        graph.create(Performance)

    TreatmentProc = Relationship(node, '处理工艺', relation)
    EnvTest = Relationship(node, '试验周期', relation2)
    #Performance = Relationship(node, relation1.__name__, relation3)
    graph.create(TreatmentProc)
    graph.create(EnvTest)
    #graph.create(Performance)
