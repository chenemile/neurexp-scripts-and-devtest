# -*- coding: utf-8 -*-
'''
:author: Emily Chen
:date:   2021

'''
import argparse
import json

from add_surface import convert_to_fst_input


def select_shortest_analyses(word2analyses):
    '''
    :param word2analyses: dictionary of the form
                          {word: {'analyses' : [analysis, analysis, analysis, etc.],
                                 'num deriv': [#, #, #, etc.]}
                          }
    :type  word2analyses: nested dict

    :return: dict

    Selects the analysis with the fewest number of morphemes for each word in the
    devtest set. If there are multiple analyses, select the first one.

    Returns:
      * shortest_w2a:     a dict where each key is a word mapped to the analysis
                          with the fewest number of derivational morphemes

    '''
    shortest_w2a = {}

    for word in word2analyses:
        analyses = word2analyses[word]["analyses"]
        deriv_counts = word2analyses[word]["num deriv"]

        # ignore punctuation
        if word and any(char.isalpha() for char in word):

            # get the number of derivational morphemes that the analysis
            # with the fewest number of derivational morphemes has
            min_num_deriv = min(deriv_counts)

            # select the analyses with the fewest number of derivational
            # morphemes and select one at random (uniform dist)
            has_fewest_deriv = []
            for idx, analysis in enumerate(analyses):
                num_deriv = deriv_counts[idx]
                if num_deriv == min_num_deriv:
                    has_fewest_deriv.append(analysis)
            chosen_analysis = has_fewest_deriv[0]

            # update 'shortest_w2a' which tracks the one analysis that
            # was chosen for each word
            shortest_w2a[word] = convert_to_fst_input(analysis)

    return shortest_w2a


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('json', help='file path to devtest\'s word2analyses json')
    parser.add_argument('--output', default="devtest.tsv", help='desired name of output file')
    args = parser.parse_args()

    jsonfile   = args.json
    outputfile = args.output

    with open(jsonfile) as f:
        word2analyses = json.load(f)

        with open(outputfile, 'w') as out:

            shortest_w2a = select_shortest_analyses(word2analyses)

            for key in shortest_w2a:
                # remove the integer appended to each word that tracks its
                # frequency in the devtest set
                word_only = ''.join([char for char in key if not char.isdigit()])

                out.write(shortest_w2a[key] + "\t" + word_only + "\n")


if __name__ == "__main__":
    main()
