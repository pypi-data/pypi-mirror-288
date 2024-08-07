"""
Module for calculating the chance to one-shot monsters in D&D 3.5.
"""

import pandas as pd
from one_shot_calculator.discrete_dists import *

def min_one(dist):
    """Returns dist, changed so that any outcomes below one are set to one.
       This is the rule for damage in D&D 3.5."""
    return {list(dist)[i]: dist[list(dist)[i]] if list(dist)[i]>1 else 0 for i in range(len(list(dist))) } | {1: sum(dist[list(dist)[i]] if list(dist)[i]<=1 else 0 for i in range(len(list(dist)))) } 

def attack_dist(attack_bonus,armor_class,damage_dist,crit_range=(20,20),crit_mult=2,confirm_bonus=0,crit_effect={0:1}):
    """Returns the probability distribution for damage dealt by attacks with attack_bonus against
       armor_class which if they hit deal damage_dist damage.
       
       Optional arguments:
       crit_range is a two-element tuple
       crit_mult is the critical multiplier. In D&D 3.5 one rolls an attack's original damage multiple times on a crit.
       confirm_bonus is any bonus to confirm critical hits. Confirming crits is an oft-forgotten rule.
       crit_effect is any bonus damage on a critical hit, such as a flaming burst weapon"""
    hit_chance=prob_between(basic_die_dist(20),min(max(2,armor_class-attack_bonus),20),20)
    confirm_chance=prob_between(basic_die_dist(20),min(max(2,armor_class-attack_bonus-confirm_bonus),20),20)
    crit_chance=prob_between(basic_die_dist(20),min(max(crit_range[0],armor_class-attack_bonus),20),20)*confirm_chance
    zerodist={0: prob_between(basic_die_dist(20),1,min(max(1,armor_class-attack_bonus-1),20))}
    nonzerodist={i: (hit_chance-crit_chance)*prob_get(min_one(damage_dist),i)+crit_chance*prob_get(min_one(add_dists(multiple_dist(crit_mult,damage_dist),crit_effect)),i) for i in range(min_dist(min_one(damage_dist)),max_dist(min_one(add_dists(multiple_dist(crit_mult,damage_dist),crit_effect)))+1)}
    return nonzerodist | zerodist

def save_chance(save_bonus,difficulty_class):
    """Returns the chance to save with save_bonus against difficulty_class"""
    return prob_at_least(basic_die_dist(20),max(2,min(difficulty_class-save_bonus,20)))

def save_for_half_dist(save_bonus,difficulty_class,damage_dist):
    """Returns the probability distribution for damage if one takes half damage on a successful save.
       Rolls with save_bonus against difficulty_class, on a failed save takes damage_dist"""
    return {i: save_chance(save_bonus,difficulty_class)*prob_get(min_one(mult_dist_by_const(min_one(damage_dist),0.5)),i)+(1-save_chance(save_bonus,difficulty_class))*prob_get(min_one(damage_dist),i) for i in range(max(1,int(0.5*min_dist(damage_dist)//1)),max_dist(damage_dist)+1)}

def one_shot_histogram(dataframe,low_CR,high_CR,one_shot_function):
    """Returns a histogram of the chance that an attack one-shots monsters in a given CR range.

       dataframe should be the result of a process_csv command
       low_CR is the lowest CR included, high_CR is the highest
       one_shot_function is a function that acts on the dataframe and gives a chance of one-shotting a monster
       """
    return dataframe.loc[(dataframe["CR"]>=low_CR) & (dataframe["CR"]<=high_CR)].apply(one_shot_function,axis=1).round(3).hist(bins=list(map(lambda x: x/20,range(21))))