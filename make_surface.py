# -*- coding: utf-8 -*-

'''
:author: Emily Chen
:date:   2021

'''
import argparse

from foma import *


def convert_to_fst_input(sample):
    '''
    :param sample: sampled underlying string
    :type  sample: str

    :return: str

    Reformats an analysis from the FST format that is
    conducive to sampling to actual FST output format:
       FROM = qiya(V)^[Ind.Intr.3Sg]
       TO   = qiya(V)^[Ind.Intr]^[3Sg]

    '''
    fused_infl = ["[Opt.Pres.Intr.2Sg]",
                  "[Opt.Pres.Trns.2Sg.3Sg]",
                  "[Opt.Neg.Pres.Trns.2Sg.3Pl]",
                  "[Opt.Neg.Pres.Trns.2Pl.3Pl]",
                  "[Opt.Neg.Pres.Trns.2Du.3Pl]",
                  "[Intrg.Intr.2Sg]",
                  "[Intrg.Intr.2Pl]",
                  "[Intrg.Intr.2Du]"
                 ]

    converted = sample

    if "Intr" in sample or "Trns" in sample:
        if not any(infl in sample for infl in fused_infl):
            converted = sample.replace("Intr.", "Intr]^["). \
                               replace("Trns.", "Trns]^[")
            sample = converted

    if "Anaphor" in sample:
        converted = sample.replace("Anaphor]", "Anaphor]^")
        sample = converted

    if "[DEM" in sample:
        converted = sample.replace("[DEM", "(DEM")
        sample = converted

    if "(DEM.PRO)" in sample:
        if "Poss" in sample:
            converted = sample[:-12] + sample[-4:]
            sample = converted
        elif "[Abs.Pl]" in sample or "[Abs.Du]" in sample:
            converted = sample.replace("[Abs", "[AbsRel") \
                              .replace("[Rel", "[AbsRel")
            sample = converted

    if "ingagh(POS)" in sample:
        converted = sample.replace("ingagh(POS)","ingagh*(POS)")
        sample = converted

    if "=" in sample:
        converted = sample.replace("^=", "=")
        sample = converted

    return converted


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--underlying', help='file with underlying forms')
    parser.add_argument('--surface', help='file for surface forms')
    parser.add_argument('--analyzer', help='fomabin file')
    args = parser.parse_args()

    t = FST.load(args.analyzer)

    inputfile  = args.underlying
    outputfile = args.surface 

    with open(inputfile, 'r') as infile:
        with open(outputfile, 'w') as outfile:
            for line in infile:

                # prep sample for fst input
                underlying_form = convert_to_fst_input(line).strip()
    
                # use the fst analyzer and generate the surface forms
                surface_forms = t[underlying_form]
    
                if len(surface_forms) > 0:
                    for surface_form in surface_forms:
                        outfile.write(str(underlying_form) + "\t" + str(surface_form) + "\n")


if __name__ == "__main__":
    main()
