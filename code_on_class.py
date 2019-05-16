#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#######################################
#defaultdict给输入的key值赋默认值，defaultdict(int)表示默认value值为0
from collections import defaultdict
original_price = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
price = defaultdict(int)
for i, p in enumerate(original_price):
    price[i+1] = p
assert price[1] == 1#断言函数判断
#print(price[123])



def func_1(n):
    for i in range(n):
        print(n)
import time
def call_time(func_1, arg): # 脚手架程序
    start = time.time()
    #调用func_1之前的时间
    func_1(arg)
    print('used time: {}'.format(time.time() - start))
    #time.time()是这时的时间，也就是调用func_1之后的时间

#call_time(func_1, 5)


##########################################
# 下面是写了一个装饰器get_call_time，但是好像有点问题


from functools import wraps
function_called_time = defaultdict(int)
def get_call_time(func):
    #写一个decorator的时候，最好在实现之前加上functools的wrap
    # ，它能保留原有函数的名称和docstring
    @wraps(func)
    def _inner(arg): ## *args, **kwargs
        """It's inner function"""
        global function_called_time#说明是全局变量
        function_called_time[func.__name__] += 1
        result = func(arg)
        print('function called time is : {}'.format(function_called_time[func.__name__]))
        return result
    return _inner

'''
call_time(func_1, 10)
func_1 = get_call_time(func_1)
func_1(10)
'''
###############################################这里有问题，装饰器@get_call_time出了问题
@get_call_time
def func_1(n):
    """
     @param n: is the number of customers
     @return int: the customers value point
     """
    for i in range(n):
        print(n)
    return 0
'''
help(func_1)
func_1(10)
'''


#############################################
def func_slow(n):
    for i in range(n):
        time.sleep(0.2)
        print(n)
#call_time(func_slow, 1)
#func_slow(5)

#这里也是@get_call_time装饰器出了问题
@get_call_time
def func_slow(n):
    for i in range(n):
        time.sleep(0.2)#延迟0.2s
        print(n)
#func_slow(1)


######################################################
def memo(func):
    cache = {}
    @wraps(func)
    def _wrap(n): ## ? *args, **kwargs
        if n in cache: result = cache[n]
        else:
            result = func(n)
            cache[n] = result
        return result
    return _wrap

#########################max函数没看懂，装饰器工作原理也还是不清楚
solution = {}
@memo
def r(n):
    #max函数key=lambda x: x[0]以key函数返回值为比较依据，取最大的那个
    max_price, split_point = max(
        [(price[n], 0)] + [(r(i) + r(n - i), i) for i in range(1, n)], key=lambda x: x[0]
    )
    solution[n] = (split_point, n - split_point)#更新solution{}
    return max_price
#print(r(231))
########
'''
Dynamic Programming
不断查表的意思
分析子问题的重复性
子问题进行存储
Solution 要进行解析
'''

'''

print(solution[2])
print(solution[16])
print(solution[6])
print(solution[10])
print(solution)
'''
r(213)
#通过递归，进一步细分
def not_cut(split): return split == 0
def parse_solution(target_length, revenue_solution):
    left, right = revenue_solution[target_length]
    if not_cut(left): return [right]
    return parse_solution(left, revenue_solution) + parse_solution(right, revenue_solution)

#print(parse_solution(19, solution))


#######################
'''
Edit Distance
定义得到类似汉明权重的距离参数的函数
'''

solution = {}
from functools import lru_cache
@lru_cache(maxsize=2 ** 10)
#@lru_cache(maxsize=1, typed=True)
#加了缓存会减少重复运算，加快速度
#maxsize 代表能缓存几个函数执行的结果 typed=True代表参数类型改变时重新缓存
def edit_distance(string1, string2):
    if len(string1) == 0: return len(string2)
    if len(string2) == 0: return len(string1)
    tail_s1 = string1[-1]
    tail_s2 = string2[-1]
    candidates = [
        (edit_distance(string1[:-1], string2) + 1, 'DEL {}'.format(tail_s1)),  # string 1 delete tail
        (edit_distance(string1, string2[:-1]) + 1, 'ADD {}'.format(tail_s2)),  # string 1 add tail of string2
    ]

    if tail_s1 == tail_s2:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 0, '')
    else:
        both_forward = (edit_distance(string1[:-1], string2[:-1]) + 1,
                        'SUB {} => {}'.format(tail_s1, tail_s2))
    candidates.append(both_forward)
    min_distance, operation = min(candidates, key=lambda x: x[0])
    #返回candidates[0]最小的那个
    solution[(string1, string2)] = operation#更新global变量solution
    return min_distance#返回distance
'''
print(edit_distance('ABCDE', 'ABCCEF'))
print(solution)
print(edit_distance('beijing', 'biejin'))
print(solution)
print(edit_distance('1010', '11100'))
print(solution)
'''
