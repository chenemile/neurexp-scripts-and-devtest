'''
:author: Emily Chen
:date:   2021

'''
import argparse
import csv
import json
import pprint
import random
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pred', help='itemquulteki\'s output file of predicted analyses')
    parser.add_argument('gold', help='devtest\'s gold analyses')
    args = parser.parse_args()

    unique     = [] # count as correct if FST outputs one and only one analysis and it is correct
    rndm       = [] # randomly select an analysis and count as correct if selected analysis is correct
    shortest   = [] # count as correct if the *first* shortest analysis is correct
    anycorrect = [] # count as correct if any of the FST's analyses are correct

    words      = []

    with open(args.pred, 'r') as f:
        data = json.load(f)

        for data_dict in data["analyzedSentences"]:
            words.append(data_dict["tokens"][0])

            predicted_analyses = []

            # check for failure
            if data_dict["words"][0]["count"] == 0:
                unique.append("+?")
                rndm.append("+?")
                shortest.append("+?")
                anycorrect.append("+?")

            # check unique
            elif data_dict["words"][0]["count"] == 1:
                unique.append(data_dict["words"][0]["analyses"]["analyses"][0]["underlyingForm"].lower())
                rndm.append(data_dict["words"][0]["analyses"]["analyses"][0]["underlyingForm"].lower())
                shortest.append(data_dict["words"][0]["analyses"]["analyses"][0]["underlyingForm"].lower())
                anycorrect.append(data_dict["words"][0]["analyses"]["analyses"][0]["underlyingForm"].lower())

            # word was predicted to have multiple analyses
            else:
                unique.append("+?")
                
                for analysis in data_dict["words"][0]["analyses"]["analyses"]:
                    predicted_analyses.append(analysis["underlyingForm"].lower())

                # randomly select an analysis
                rndm.append(random.choice(predicted_analyses).lower())

                # select first shortest analysis
                shortest.append(min(predicted_analyses, key=len).lower())

                # append all analyses to 'anycorrect'
                anycorrect.append(predicted_analyses)
             
    gold_analyses = [] # presumed gold analyses for devtest (aren't actually)
    with open(args.gold, 'r') as f:
        for line in f:
            gold_analyses.append(line.strip().lower())

    # check for correctness
    num_wrong_unique     = 0
    num_wrong_random     = 0
    num_wrong_shortest   = 0
    num_wrong_anycorrect = 0

    items_wrong_anycorrect = []

    for i in range(len(gold_analyses)):

        if gold_analyses[i] != unique[i]:
            num_wrong_unique += 1

        if gold_analyses[i] != rndm[i]:
            num_wrong_random += 1

        if gold_analyses[i] != shortest[i]:
            num_wrong_shortest += 1

        if type(anycorrect[i]) == list:
            found_match = False

            for analysis in anycorrect[i]:
                if gold_analyses[i] == analysis:
                    found_match = True
                    break

            if found_match == False:
                num_wrong_anycorrect += 1
                items_wrong_anycorrect.append(words[i])
        else:
            if gold_analyses[i] != anycorrect[i]:
                num_wrong_anycorrect += 1
                items_wrong_anycorrect.append(words[i])

    num_items = len(gold_analyses)

    print("================")
    print("fst analyzer WER")
    print("================")

    print("----------------")
    print("problem children")
    print("----------------")
    pprint.pprint(items_wrong_anycorrect)

    print()

    print("---------------")
    print("word error rate")
    print("---------------")
    print("unique:")
    print("  wer = {:.2f}".format(num_wrong_unique/float(num_items) * 100))
    print("  acc = {:.2f}".format((num_items - num_wrong_unique)/float(num_items) * 100))
    print()

    print("random:")
    print("  wer = {:.2f}".format(num_wrong_random/float(num_items) * 100))
    print("  acc = {:.2f}".format((num_items - num_wrong_random)/float(num_items) * 100))
    print()

    print("shortest:")
    print("  wer = {:.2f}".format(num_wrong_shortest/float(num_items) * 100))
    print("  acc = {:.2f}".format((num_items - num_wrong_shortest)/float(num_items) * 100))
    print()

    print("any correct:")
    print("  wer = {:.2f}".format(num_wrong_anycorrect/float(num_items) * 100))
    print("  acc = {:.2f}".format((num_items - num_wrong_anycorrect)/float(num_items) * 100))

    print()

if __name__ == "__main__":
    main()
