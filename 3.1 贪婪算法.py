# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 10:55:05 2021

@author: EldenBob
"""
import pandas as pd
import time

#输入供给端节点标签,并将各节点储存在一个列表

Supply_node1_tag = ['Male','Age=5']
Supply_node2_tag = ['Male','WA','Age=5']
Supply_node3_tag = ['Male','CA','Age=5']
Supply_node4_tag = ['CA','Age=5']
Supply_node5_tag = ['NV','Age=5']
Supply_node6_tag = ['Age=5']

Supply_node = [Supply_node1_tag,Supply_node2_tag,Supply_node3_tag,Supply_node4_tag,Supply_node5_tag,Supply_node6_tag]

#输入供给端各节点数量

Supply_amount = {'Supply_node1':400,'Supply_node2':400,'Supply_node3':100,'Supply_node4':100,'Supply_node5':500,'Supply_node6':300}

#输入需求端各节点标签

Demand_node1_tag = ['Male']
Demand_node2_tag = ['CA']
Demand_node3_tag = ['Age=5']

Demand_node = [Demand_node1_tag,Demand_node2_tag,Demand_node3_tag]

#输入供给端各节点数量

Demand_amount = {'Demand_node1':200,'Demand_node2':200,'Demand_node3':1000}

#输入标签CPM

tag_CPM = {'Male':1,'CA':3,'Age=5':0.1}

#为缩小遍历次数，给定一个最小分配数量单位

minUnit = 100
#minUnit = eval(input("输入最小分配数量单位"))

#预先建立一个列表以存储分配情况

result= []
for i in range(len(Supply_node)):
    result.append([])
for i in range(len(Demand_node)):
    for x in range(len(Supply_node)):
        result[x].append(0)

#功能实现

#0 加入计算运算时间的功能
time_start = time.time()

#1.1 为实现当前最优，需要优先考虑CPM最贵的标签，故首先将标签CPM进行排序

tag_CPM_sorted = sorted(tag_CPM.items(), key=lambda item:item[1], reverse=True)

#1.2 加入计算总收入的功能

income = 0

#2 套了一大堆if和while来做

distribute = ""    #建立一个空字符串用来储存分配情况

#究极嵌套开始！

n = 0
while n < len(Demand_node):
    for i in Demand_node:           #依次提取需求节点
        if tag_CPM_sorted[n][0] in i:       #判断提取的需求节点是否为最高优先级
            key_demand = "Demand_node" + str(Demand_node.index(i) + 1)   #建立一个key字符串以用来从需求数量字典中提出tag
            for x in Supply_node:                                    #遍历供给节点，寻找有对应tag并且剩余数量大于最小单位数量的节点
                if tag_CPM_sorted[n][0] in x:
                    key_supply = "Supply_node" + str(Supply_node.index(x) + 1)
                    while Supply_amount[key_supply] >= minUnit and Demand_amount[key_demand] >= minUnit :
                        Supply_amount[key_supply] -= minUnit         #减去已经被分配的数量
                        Demand_amount[key_demand] -= minUnit
                        income += tag_CPM_sorted[n][1] * 100000      #计算获利
                        #将分配情况写入结果列表
                        result[Supply_node.index(x)][Demand_node.index(i)] += 100000
                        #输出分配情况
                        distribute += (
                                       "将 " + str(minUnit) + "k 个 " +
                                       str(key_demand) + " 分配给 " +
                                       str(key_supply) + '\n'
                                       )
            distribute += "\n"
    n += 1

print("最小分配数量单位为：" + str(minUnit) + "k\n")

#统计并输出计算时间

time_end = time.time()
use_time = time_end - time_start
print("所用时间为：" + ('%.20f' % use_time) + "s\n" )

#输出总获利

print("总获利：" + str(income) + "元\n")

#统计剩余的需求情况

key_list=[]
value_list=[]
for key,value in Demand_amount.items():
    key_list.append(key)
    value_list.append(value)
account = 0
for i in value_list:
    account += i
if account != 0:
    print("需求情况：以下需求节点未被满足")
    for i in value_list:
        if i != 0:
            print("         " + str(key_list[value_list.index(i)]) + "  " + str(i))
else:
    print("需求情况：无未被满足的需求")

#用Dataframe呈现最终分配结果

result_df = pd.DataFrame(result)
result_df.columns = ['Demand_node1','Demand_node2','Demand_node3']
result_df.index = ['Supply_node1','Supply_node2','Supply_node3','Supply_node4','Supply_node5','Supply_node6']
print("\n最终分配结果：")
print(result_df)
print("\n详细分配方案：\n")
print(distribute)

print(
      '''程序存在的问题：
      1.只能在需求都被满足的情况下正常运行，尝试解决这个问题但是失败了(后来成功了）；
      2.究竟是否实现贪婪算法已达到减少计算量的目的存疑；
      3.最小分配数量单位在面临不规整的数据时，会极大地增加计算量；
      4.一些功能的实现略有复杂；
      5.代码语言不够规范。
      ''')
#print(Supply_amount)       #统计供给端余量
#print(Demand_amount)       #统计需求端端余量
