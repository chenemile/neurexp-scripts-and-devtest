'''
:author: Emily Chen
:date:   2021

'''
import argparse
import csv
import pprint
import random
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('guesses', help='itemquulteki\'s output file')
    parser.add_argument('gold', help='devtest\'s gold analyses')
    args = parser.parse_args()

    unique = [] # count as correct if FST outputs one and only one analysis and it is correct
    rndm   = [] # randomly select an analysis and count as correct if selected analysis is correct
    shortest   = [] # count as correct if the *first* shortest analysis is correct
    anycorrect = [] # count as correct if any of the FST's analyses are correct

    with open(args.guesses, 'r') as f:
        lines = csv.reader(f, delimiter='\t')

        line_num = 1

        for line in lines:

            # check for failure
            if int(line[0]) == 0:
                unique.append("+?")
                rndm.append("+?")
                shortest.append("+?")
                anycorrect.append("+?")
                line_num += 1

            # check unique
            elif int(line[0]) == 1:
                unique.append(line[5])
                rndm.append(line[5])
                shortest.append(line[5])
                anycorrect.append(line[5])
                line_num += 1

            else:
                unique.append("+?")

                # randomly select an analysis
                rndm.append(random.choice(line[5:]))

                # select first shortest analysis
                shortest.append(min(line[5:], key=len))

                anycorrect.append(line[5:])

                line_num += 1


    gold_analyses = [] # presumed gold analyses for devtest (aren't actually)
    with open(args.gold, 'r') as f:
        for line in f:
            gold_analyses.append(line.strip())


    # check for correctness
    num_wrong_unique     = 0
    num_wrong_random     = 0
    num_wrong_shortest   = 0
    num_wrong_anycorrect = 0

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
        else:
            if gold_analyses[i] != anycorrect[i]:
                num_wrong_anycorrect += 1

    num_items = len(gold_analyses)

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


if __name__ == "__main__":
    main()
