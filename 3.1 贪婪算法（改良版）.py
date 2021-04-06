# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:28:40 2021

@author: EldenBob
"""
import pandas as pd

#建立需求节点
class demand_node(object):

    def __init__(self, t, a, v):
        self.tag = t
        self.amount = a
        self.value = v

    def get_tag(self):
        return self.tag

    def get_amount(self):
        return self.amount

    def get_value(self):
        return self.value

    def __repr__(self):
                return repr((self.tag, self.amount, self.value))

def demand_list(d_tags, d_amounts, d_values):

    list = []

    for i in range(len(d_tags)):
        list.append(demand_node(d_tags[i], d_amounts[i],
                         d_values[i]))
    return list

#建立供给节点
class supply_node(object):

    def __init__(self, t, a):
        self.tag = t
        self.amount = a

    def get_tag(self):
        return self.tag

    def get_amount(self):
        return self.amount

    def __repr__(self):
                return repr((self.tag, self.amount))

def supply_list(s_tags, s_amounts):

    list = []

    for i in range(len(s_tags)):
        list.append(supply_node(s_tags[i], s_amounts[i]))
    return list


#定义贪婪算法
def greedy(demand_total, supply_total, key_function):

    demand_total_sorted = sorted(demand_total,  key = key_function, reverse=True) #排序

    #分别用来储存详细的分配情况，收入情况和分配总表，
    distribute = ""
    income = 0
    result = []

    for i in range(len(supply_total)):
        result.append([])
    for i in range(len(demand_total_sorted)):
        for x in range(len(supply_total)):
            result[x].append(0)

    for d in demand_total_sorted:
        for s in supply_total:
            while d.tag in s.tag and s.amount > 0 and d.amount > 0:
                count = s.amount - d.amount

                if count >= 0:
                    income += d.amount * d.value * 1000
                    result[supply_total.index(s)][demand_total.index(d)] += d.amount
                    distribute += (
                                    "   将 {}k 个 Demand_node{} 分配给 Supply_node{} \n".format(d.amount, demand_total.index(d) + 1, supply_total.index(s) + 1)
                                       )
                    s.amount = count
                    d.amount = 0

                if count < 0:
                    income += s.amount * d.value * 1000
                    result[supply_total.index(s)][demand_total.index(d)] += s.amount
                    distribute += (
                                    "   将 {}k 个 Demand_node{} 分配给 Supply_node{} \n".format(s.amount, demand_total.index(d) + 1, supply_total.index(s) + 1)
                                       )
                    d.amount = d.amount - s.amount
                    s.amount = 0

    #筛选出未被满足的节点
    demand_surplus_print = ""
    demand_surplus = 0
    for d in demand_total:
        demand_surplus += d.amount
    if demand_surplus == 0:
        demand_surplus_print = "没有未被满足的需求。\n"
    else:
        demand_surplus_print += "以下需求节点未被满足：\n"
        for d in demand_total:
            if d.amount > 0:
                demand_surplus_print += "   Demand_node{}  {}\n".format(demand_total.index(d) + 1, d.amount)

    return (income, result, distribute, demand_surplus_print)

#主函数
def testGreedy(demand_total, supply_total, key_function):
    income_total, disresult, detial, demand_surplus_print = greedy(demand_total, supply_total, key_function)

    result_df = pd.DataFrame(disresult)
    result_df.columns = ['Demand_node1','Demand_node2','Demand_node3']
    result_df.index = ['Supply_node1','Supply_node2','Supply_node3','Supply_node4','Supply_node5','Supply_node6']

    print("\n最终分配结果：(单位：K)")
    print(result_df)
    print("\n总获利为 {} 元\n".format(income_total))
    print(demand_surplus_print)
    print("详细分配情况如下：\n" + detial)


d_tags = ['Male', 'CA', 'Age']
d_amounts = [200,200,1000]
d_values = [1,3,0.1]

s_tags = [['Male','Age'],['Male','WA','Age'], ['Male','CA','Age'],['CA', 'Age'],['NV', 'Age'],['Age']]
s_amounts = [400,400,100,100,500,300]

demand_total = demand_list(d_tags, d_amounts, d_values)
supply_total = supply_list(s_tags, s_amounts)
testGreedy(demand_total, supply_total, demand_node.get_value)
