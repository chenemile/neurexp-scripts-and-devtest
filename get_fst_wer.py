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

from statistics import median


def get_aprf(true_pos, false_neg, false_pos, total):
    '''
    '''
    if true_pos == -1:
        true_pos = total - false_neg - false_pos

    accuracy  = (true_pos)/float(total) * 100
    precision = (true_pos)/float(true_pos + false_pos) * 100
    recall    = (true_pos)/float(true_pos + false_neg) * 100
    fmeasure  = (2 * precision * recall)/(precision + recall)

    return accuracy, precision, recall, fmeasure


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pred', help='itemquulteki\'s output file of predicted analyses')
    parser.add_argument('gold', help='devtest\'s gold analyses')
    args = parser.parse_args()

    unique     = [] # count as correct if FST outputs one and only one analysis and it is correct
    rndm       = [] # randomly select an analysis and count as correct if selected analysis is correct
    fewest     = [] # count as correct if the *first* fewest analysis is correct
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
                fewest.append("+?")
                anycorrect.append("+?")

            # check unique
            elif data_dict["words"][0]["count"] == 1:
                unique.append(data_dict["words"][0]["analyses"]["analyses"][0]["underlyingForm"].lower())
                rndm.append(data_dict["words"][0]["analyses"]["analyses"][0]["underlyingForm"].lower())
                fewest.append(data_dict["words"][0]["analyses"]["analyses"][0]["underlyingForm"].lower())
                anycorrect.append(data_dict["words"][0]["analyses"]["analyses"][0]["underlyingForm"].lower())

            # word was predicted to have multiple analyses
            else:
                unique.append("+?")
                
                for analysis in data_dict["words"][0]["analyses"]["analyses"]:
                    predicted_analyses.append(analysis["underlyingForm"].lower())

                # randomly select an analysis
                rndm.append(random.choice(predicted_analyses).lower())

                # select first fewest analysis
                fewest.append(min(predicted_analyses, key=len).lower())

                # append all analyses to 'anycorrect'
                anycorrect.append(predicted_analyses)
             
    gold_analyses = []
    with open(args.gold, 'r') as f:
        for line in f:
            gold_analyses.append(line.strip().lower())

    # check for correctness
    #     false negatives +1 for every word analyzer fails to analyze
    #     false positives +1 for every wrong analysis 
    #     true positives  +1 for every word analyzer successfully analyzes 
    #         needed only for anycorrect, since true positives for all other
    #         heuristics = total - false negatives - false postives
    false_neg_unique = []
    false_pos_unique = []

    false_neg_random = [] 
    false_pos_random = []

    false_neg_fewest = []
    false_pos_fewest = []

    true_pos_anycorrect  = []
    false_neg_anycorrect = []
    false_pos_anycorrect = []

    for i in range(len(gold_analyses)):

        if unique[i] == "+?":
            false_neg_unique.append(words[i])
        elif gold_analyses[i] != unique[i]:
            false_pos_unique.append(words[i])

        if rndm[i] == "+?":
            false_neg_random.append(words[i])
        elif gold_analyses[i] != rndm[i]:
            false_pos_random.append(words[i])

        if fewest[i] == "+?":
            false_neg_fewest.append(words[i])
        elif gold_analyses[i] != fewest[i]:
            false_pos_fewest.append(words[i])

        # analyzer returned multiple analyses
        if type(anycorrect[i]) == list:
            found_match = False

            for analysis in anycorrect[i]:
                if gold_analyses[i] == analysis:
                    found_match = True
                    break

            # add all returned analyses as false positives (except the correct one)
            num_returned_analyses = len(anycorrect[i])
            if found_match == True:
                true_pos_anycorrect.append(words[i])
                false_pos_anycorrect.extend([words[i]] * (num_returned_analyses-1))
            else:
                false_pos_anycorrect.extend([words[i]] * num_returned_analyses) 
        else:
            if anycorrect[i] == "+?":
                false_neg_anycorrect.append(words[i])
            elif gold_analyses[i] != anycorrect[i]:
                false_pos_anycorrect.append(words[i])
            else:
                true_pos_anycorrect.append(words[i])

    num_items_tok = len(gold_analyses)
    num_items_typ = len(set(gold_analyses))

    # get average, precision, recall, f-measure
    unique_aprf_typ     = get_aprf(-1, len(set(false_neg_unique)), len(set(false_pos_unique)), num_items_typ)
    random_aprf_typ     = get_aprf(-1, len(set(false_neg_random)), len(set(false_pos_random)), num_items_typ)
    fewest_aprf_typ     = get_aprf(-1, len(set(false_neg_fewest)), len(set(false_pos_fewest)), num_items_typ)
    anycorrect_aprf_typ = get_aprf(len(set(true_pos_anycorrect)), len(set(false_neg_anycorrect)), len(set(false_pos_anycorrect)), num_items_typ)

    unique_aprf_tok     = get_aprf(-1, len(false_neg_unique), len(false_pos_unique), num_items_tok)
    random_aprf_tok     = get_aprf(-1, len(false_neg_random), len(false_pos_random), num_items_tok)
    fewest_aprf_tok     = get_aprf(-1, len(false_neg_fewest), len(false_pos_fewest), num_items_tok)
    anycorrect_aprf_tok = get_aprf(len(true_pos_anycorrect), len(false_neg_anycorrect), len(false_pos_anycorrect), num_items_tok)

    # get avg, median num analyses and word with most analyses
    analyses_count = {}
    for i in range(len(anycorrect)):
        analyses_count[words[i]] = len(anycorrect[i]) 

    word_with_most       = max(analyses_count, key=analyses_count.get) 
    word_with_most_count = analyses_count[word_with_most]

    average_num_analyses = "{:.2f}".format(sum(analyses_count.values()) / float(len(analyses_count)))
    median_num_analyses  = median(list(analyses_count.values()))

    print("================")
    print("fst analyzer WER")
    print("================")

    print("----------------")
    print("problem children")
    print("----------------")
    pprint.pprint(false_neg_anycorrect + list(set(false_pos_anycorrect)))

    print()

    print("-----")
    print("types")
    print("-----")
    print("unique:")
    print("  coverage  = {:.2f}".format((num_items_typ - len(set(false_neg_unique)))/float(num_items_typ) * 100))
    #print("  accuracy  = {:.2f}".format(unique_aprf_typ[0]))
    print("  precision = {:.2f}".format(unique_aprf_typ[1]))
    print("  recall    = {:.2f}".format(unique_aprf_typ[2]))
    print("  f-measure = {:.2f}".format(unique_aprf_typ[3]))
    print()

    print("random:")
    print("  coverage  = {:.2f}".format((num_items_typ - len(set(false_neg_random)))/float(num_items_typ) * 100))
    #print("  accuracy  = {:.2f}".format(random_aprf_typ[0]))
    print("  precision = {:.2f}".format(random_aprf_typ[1]))
    print("  recall    = {:.2f}".format(random_aprf_typ[2]))
    print("  f-measure = {:.2f}".format(random_aprf_typ[3]))
    print()

    print("fewest:")
    print("  coverage  = {:.2f}".format((num_items_typ - len(set(false_neg_fewest)))/float(num_items_typ) * 100))
    #print("  accuracy  = {:.2f}".format(fewest_aprf_typ[0]))
    print("  precision = {:.2f}".format(fewest_aprf_typ[1]))
    print("  recall    = {:.2f}".format(fewest_aprf_typ[2]))
    print("  f-measure = {:.2f}".format(fewest_aprf_typ[3]))
    print()

    print("any correct:")
    print("  coverage  = {:.2f}".format((num_items_typ - len(set(false_neg_anycorrect)))/float(num_items_typ) * 100))
    #print("  accuracy  = {:.2f}".format(anycorrect_aprf_typ[0]))
    print("  precision = {:.2f}".format(anycorrect_aprf_typ[1]))
    print("  recall    = {:.2f}".format(anycorrect_aprf_typ[2]))
    print("  f-measure = {:.2f}".format(anycorrect_aprf_typ[3]))

    print()

    print("------")
    print("tokens")
    print("------")
    print("unique:")
    print("  coverage  = {:.2f}".format((num_items_tok - len(false_neg_unique))/float(num_items_tok) * 100))
    #print("  accuracy  = {:.2f}".format(unique_aprf_tok[0]))
    print("  precision = {:.2f}".format(unique_aprf_tok[1]))
    print("  recall    = {:.2f}".format(unique_aprf_tok[2]))
    print("  f-measure = {:.2f}".format(unique_aprf_tok[3]))
    print()

    print("random:")
    print("  coverage  = {:.2f}".format((num_items_tok - len(false_neg_random))/float(num_items_tok) * 100))
    #print("  accuracy  = {:.2f}".format(random_aprf_tok[0]))
    print("  precision = {:.2f}".format(random_aprf_tok[1]))
    print("  recall    = {:.2f}".format(random_aprf_tok[2]))
    print("  f-measure = {:.2f}".format(random_aprf_tok[3]))
    print()

    print("fewest:")
    print("  coverage  = {:.2f}".format((num_items_tok - len(false_neg_fewest))/float(num_items_tok) * 100))
    #print("  accuracy  = {:.2f}".format(fewest_aprf_tok[0]))
    print("  precision = {:.2f}".format(fewest_aprf_tok[1]))
    print("  recall    = {:.2f}".format(fewest_aprf_tok[2]))
    print("  f-measure = {:.2f}".format(fewest_aprf_tok[3]))
    print()

    print("any correct:")
    print("  coverage  = {:.2f}".format((num_items_tok - len(false_neg_anycorrect))/float(num_items_tok) * 100))
    #print("  accuracy  = {:.2f}".format(anycorrect_aprf_tok[0]))
    print("  precision = {:.2f}".format(anycorrect_aprf_tok[1]))
    print("  recall    = {:.2f}".format(anycorrect_aprf_tok[2]))
    print("  f-measure = {:.2f}".format(anycorrect_aprf_tok[3]))

    print()


    print("-----------")
    print("other stats")
    print("-----------")
    print("word with most analyses: " + word_with_most)
    print("  num analyses: " + str(word_with_most_count))
    print()

    print("average number of analyses: " + average_num_analyses)
    print("median number of analyses:  " + str(median_num_analyses))

    print()

if __name__ == "__main__":
    main()
