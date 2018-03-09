import numpy as np
import collections

en_list = []
he_list = []
hewv_list = []

with open("he-en/en.train.txt", encoding='utf-8', newline='') as fen:
    for en_line in fen:
        en_list.append(en_line)
		
with open("he-en/he.train.txt", encoding='utf-8', newline='') as fhe:
    for he_line in fhe:
        he_list.append(he_line)
		
with open("he-en/hewv.train.txt", encoding='utf-8', newline='') as fhewv:
    for hewv_line in fhewv:
        hewv_list.append(hewv_line)

en_counter=collections.Counter(en_list)
he_counter=collections.Counter(he_list)
hewv_counter=collections.Counter(hewv_list)

print("En:")		
print("Strings in list: %s" % len(en_list))
print("Unique string in list: %s" % len(set(en_list)))
print(en_counter.most_common(10))

print("He:")
print("Strings in list: %s" % len(he_list))
print("Unique string in list: %s" % len(set(he_list)))
print(he_counter.most_common(10))

print("Hewv:")
print("Strings in list: %s" % len(hewv_list))
print("Unique string in list: %s" % len(set(hewv_list)))
print(hewv_counter.most_common(10))