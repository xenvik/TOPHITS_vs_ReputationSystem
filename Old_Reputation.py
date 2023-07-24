# We need to find the leaders by mentions.
# We need to rank leaders by weight given to them by mentions.
# Initial weight to all mentions is given as equal.
# Calculate score on basis of above, iterations, updating, also mentions of feed owners
# should be considered while scoring.

import re
# import itertools
import operator
import math

import numpy as np
import pandas as pd
from collections import Counter
df = pd.read_csv('Crypto_twitter_full.csv', usecols=['type', 'link', 'time', 'text', 'sen', 'pos', 'neg'], encoding='latin1', low_memory=False, dtype={'pos': str})
df = df[df.type == 'twitter']  # only twitter data


# Finding mentions in data by feed owners
def feedomen(feedo):
    flist = []
    df = pd.read_csv('Crypto_twitter_full.csv', usecols=['type', 'link', 'time', 'text', 'sen', 'pos', 'neg'], encoding='latin1', low_memory=False, dtype={'pos': str})
    df = df[df.type == 'twitter']
    df.link = df.link.str.replace('https://twitter.com/', '@', regex=True)
    df = df[df.link == feedo]
    df.text = df.text.fillna('')
    for row in df.text:
        if row[0] == 'R' and row[1] == 'T':
            continue
        else:
            for word in row.split():
                if word[0] == '@':
                    word = word.split("'")[0]
                    flist.append(word.lower())

# Cleaning mentions from extra characters
    omentions = []
    for row in flist:
        for char in "[#!$%^&*()-+|:;,<>?./…]":
            row = row.replace(char, '')
        omentions.append(row)

# Counter for mentions
    dct = Counter(omentions)
    cist = sorted(dct.items(), key=operator.itemgetter(1), reverse=True)
    #map(float,cist)
    return(cist)

# Raters List
cmlist = []
df.link = df.link.fillna('')
df.link = df.link.str.replace('https://twitter.com/', '@', regex=True)
for link in df.link:
    if link in cmlist:
        continue
    else:
        cmlist.append(link)


def default_weight(raters):
    ranking = []
    for feedo in cmlist:
        ranking.append(feedomen(feedo))
    return ranking


def new_ranker(ratrw, rated):
    wt = list(ratrw)
    new_rated = []
    for lqr in rated:
        rt = list(lqr)
        rt[1] = (rt[1] * wt[1]) + 1
        new_rated.append(rt)
    #print(new_rated)
    return new_rated


def weights(ranking):
    new_weights = []
    for i in cmlist:
        i = i.lower()
        new_weights.append([i, 0])
    for rater in ranking:
        for ratrw in rater:
            for ratrwm in new_weights:
                if ratrw[0] == ratrwm[0] and ratrw[1] > ratrwm[1]:
                    ratrwm[1] = ratrw[1]
    #print(new_weights)
    return new_weights


def normalisation(ranking):
    max = float()
    for rater in ranking:
        for rated in rater:
            value = float(rated[1])
            #print('value= ', value)
            #if value > 1.0 :
            valuelog = math.log((rated[1]+1), 10)
            #print('valuelog= ', valuelog)
            if max < valuelog:
                max = valuelog
            if value > max:
                max = value
            print (max)

    for rater in ranking:
        for rated in rater:
            #print('rated',rated[1])
            value = float(rated[1]) / max
            if value == 0:
                v = 0.1
            rated[1] = value
            #print('value updated', value)
    return ranking


iterations=9 #sanity check
for check in range(iterations):
    new_ranking = []
    if check == 0:
        ranking = default_weight(cmlist)
    else:
        weight = weights(ranking)
        i = 0
        for rated in ranking:
            new_ranking.append(new_ranker(weight[i], rated))
            i += 1
        ranking = normalisation(new_ranking)

#print(ranking)

def counter(ranking):
    final_list = []
    for final in ranking:
        for descend in final:
            if descend[0] in final_list:
                continue
            else:
                final_list.append([descend[0], 0])
    return final_list


def counter_add(ranking, final_list):
    for ranked in ranking:
        for individual in ranked:
            for rated in final_list:
                if individual[0] == rated[0]:
                    rated[1] += individual[1]
    return final_list


final_list = counter(ranking)
liquid_ranking = counter_add(ranking, final_list)

#print(liquid_ranking)

import operator # Descending order

peanuts = dict(liquid_ranking)
list = sorted(peanuts.items(), key=operator.itemgetter(1), reverse=True)
dfm = dict(list)

dfm = pd.DataFrame.from_dict(data=dfm, orient='index')
print(dfm)

#saving the dataframe
dfm.to_csv('Mentions_LiquidRank.csv', header=['Mentions'])




