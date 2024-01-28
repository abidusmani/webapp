import pandas as pd
import numpy as np
import matplotlib as mp
from numpy import random
# from python_script import matrix_json

# input_data = np.matrix("3,5,2,9,8,7;2,6,8,2,1,7;7,3,9,6,5,6;1,9,10,2,3,4;8,7,5,3,2,6");
# print(input_data)

#upload dataset 

# input_data = matrix_json
def topsis(input_data):
# convert data into dataframe
    df = pd.DataFrame(input_data , columns = ['c1','c2','c3','c4','c5','c6'])
    df

    #normalized matrix to calculate weights
    df.sum(axis=0)
    df_n = df/df.sum(axis=0)
    df_n

    #calculate h value
    h = 1/np.log(df.shape[1])
    h = np.round(h,5)
    h

    # entropy calculation
    df_m = df_n*(np.log(df_n))
    df_m
    df_o = df_m.sum(axis = 0)
    ej = df_o*(-h)
    ej_1 = (1-ej)
    q = ej_1.sum()
    wj = ej_1/q
    print(wj.round(4))

    #calculate the normalized matrix
    df_l = np.power(df,2)
    df_l
    df_p = np.round(df/(np.sqrt(df_l.sum(axis=0))),4)
    df_p = df_p.mul(wj,axis = 1)

    #calculating the non-beneficial ideal best and ideal worst
    pos_ideal = []
    neg_ideal = []
    # c2,c3 are the non-beneficial

    a = []
    a = df_p.min(axis = 'index')
    b = []
    b = df_p.max(axis = 'index')

    # c1, c4, c5, c6 are the beneficial criteria

    p_ = a.to_numpy()
    n_ = b.to_numpy()
    pos_ideal = []
    neg_ideal = []

    for i in range(0,6):
        if(i==1 or i==2):
            aa = np.round(p_[i],5)
            pos_ideal.append(aa)
            bb = np.round(n_[i],5)
            neg_ideal.append(bb)
        else:
            cc = np.round(n_[i],5)
            pos_ideal.append(cc)
            dd = np.round(p_[i],5)
            neg_ideal.append(dd)

    df_e = df_p.copy(deep= True)
    df_o = df_p.copy(deep = True)
    df_pp = df_p.copy(deep = True)

    i = 0
    for column in df_pp:
        df_pp[column] = pos_ideal[i] - df_pp[column]
    i = i+1

    j = 0
    for column in df_e:
        df_e[column] = df_e[column] - neg_ideal[j]
    j = j + 1


    print(df_o)
    df_o['s_plus'] = np.sqrt(np.power(df_pp.sum(axis = 1),2))
    df_o['s_minus'] = np.sqrt(np.power(df_e.sum(axis = 1),2))
    df_o['RC'] = df_o['s_minus']/(df_o['s_plus']+df_o['s_minus'])
    df_o['rank'] = df_o['RC'].rank(ascending = False)
    print(df_o)
    return df_o

def topsis_gre(input_data):
    
    p = 0.5
    m = len(neg_ideal)
    k = 0
    r_minus = df_p.copy(deep= True)
    for column in r_minus:
        A = np.abs(np.min(neg_ideal)-df_p[column])
        B = np.abs(np.max(neg_ideal)-df_p[column])
        C = np.abs(neg_ideal[k]-df_p[column])
        D = B.mul(p)
        E = (C.add(D)).div(A.add(D))
        k = k + 1
        r_minus[column] = E
    r_minus['g_minus'] = (r_minus.sum(axis = 1)).div(m)
    print(r_minus)

    #evaluating the value  of 'p' using bes optimization method
    x=random.rand(5,6)
    p_ = pd.DataFrame(x,columns = ['p1','p2','p3','p4','p5','p6'],index = [0,1,2,3,4])
    # print("hello")
    print(p_)

    p = 0.5
    m = len(pos_ideal)
    k = 0
    r_plus = df_p.copy(deep= True)
    for column in r_plus:
        A = np.abs(np.min(pos_ideal)-df_p[column])
        B = np.abs(np.max(pos_ideal)-df_p[column])
        C = np.abs(neg_ideal[k]-df_p[column])
        D = B.mul(p)
        E = (C.add(D)).div(A.add(D))
        k = k + 1
        r_plus[column] = E

    r_plus['g_plus'] = (r_plus.sum(axis = 1)).div(m)
    print(r_plus)
    df_o['g_min'] = r_minus['g_minus'].copy(deep = True)
    df_o['g_plus'] = r_plus['g_plus'].copy(deep = True)
    df_o['score'] = (df_o['g_min']).div(df_o['g_min'].add(df_o['g_plus']))
    df_o['rank_new']= df_o['score'].rank(ascending = False)
    print(df_o)
    return df_o
