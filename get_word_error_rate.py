# -*- coding: utf-8 -*-
'''
:author: Emily Chen
:date:   2021

USAGE:  python2.7 scripts/get_word_error_rate.py /nas/data/yupik/finite_state_morphology/uppercase.fomabin devset/src-dev.txt devset/tgt-dev.txt [PREDICTIONS.TXT] 

'''
import argparse
import pprint

from sys import exit
from foma import *


parser = argparse.ArgumentParser()

parser.add_argument('fst', help='file path to fst analyzer')
parser.add_argument('surface_forms', help='file path to surface forms')
parser.add_argument('gold', help='file path to gold analyses')
parser.add_argument('pred', help='file path to predicted eanalyses')
args = parser.parse_args()

gold_analyses = []
predicted_analyses = []
surface_forms = []

with open(args.gold, 'r') as f:
    for line in f:
        analysis = line.replace(" ","").strip().decode('utf-8')
        gold_analyses.append(analysis)

with open(args.pred, 'r') as f:
    for line in f:
        analysis = line.replace(" ","").strip().decode('utf-8')
        predicted_analyses.append(analysis)

with open(args.surface_forms, 'r') as f:
    for line in f:
        sf = line.replace(" ","").strip().decode('utf-8')
        surface_forms.append(sf)


if len(gold_analyses) != len(predicted_analyses):
    print("WARNING: number of gold standard items does not match the " + \
          "number of items being analyzed")
    exit()
else:
    t = FST.load(args.fst)

    print(args.pred)

    num_wrong = 0
    num_items = len(gold_analyses)
    items_wrong = []

    for i in range(len(gold_analyses)):

        # if gold analysis does not match predicted analysis,
        # compare their surface forms generated by the FST analyzer
        # (possible syncretism)
        if gold_analyses[i] != predicted_analyses[i]:
            gold_analysis = gold_analyses[i][0].lower() + gold_analyses[i][1:]

            if predicted_analyses[i]:
                predicted_analysis = predicted_analyses[i][0].lower() + predicted_analyses[i][1:]

            gold_surface_forms = t[gold_analysis]
            predicted_surface_forms = t[predicted_analysis]

            sf_in_common = set(gold_surface_forms).intersection(predicted_surface_forms)

            if len(sf_in_common) == 0:
                num_wrong += 1
                items_wrong.append("item ID " + str(i) + ": " + surface_forms[i])

    #print("----------------")
    #print("problem children")
    #print("----------------")
    #pprint.pprint(items_wrong)

    print("---------------")
    print("word error rate")
    print("---------------")
    print("  wer = {:.2f}".format(num_wrong/float(num_items) * 100))
    print("  acc = {:.2f}".format((num_items - num_wrong)/float(num_items) * 100))
