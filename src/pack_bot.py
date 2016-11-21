#!/usr/bin/env python

"""
    pack_bot.py
        Author: Theodore Enns
        Brief: A executable python script that solves 0-1 knapsack.

        usage: pack_bot.py [-h] [-v] [-s] [-r REDUCTION_FACTOR] suitcase_source parts_source

        Returns a json object with an optimal parts list that the robot can pack

        positional arguments:
          suitcase_source       the source for the suitcase (file path or http)
          parts_source          the source for the parts list (file path or http)

        optional arguments:
          -h, --help            show this help message and exit
          -v, --verbose         provides a basic breakdown of input and additional output stats
          -s, --save_inputs     saves input files to suitcase.json and parts.json
          -r REDUCTION_FACTOR,
          --reduction_factor REDUCTION_FACTOR
                                reduces input by division factor (must be int >0)
"""

import argparse
import json

from pb_get_json import grab_dict_from
from pb_knapsack import KnapSack01Solver

def main():
    # parse args
    parser = argparse.ArgumentParser(description=
                                     "Returns a json object with an optimal parts list that the robot can pack")
    parser.add_argument("-v", "--verbose", action="store_true", required=False, default=False,
                        help="provides a basic breakdown of input and additional output stats")
    parser.add_argument("-s", "--save_inputs", action="store_true", required=False, default=False,
                        help="saves input files to suitcase.json and parts.json")
    parser.add_argument("-r", "--reduction_factor", type=int, required=False, default=1,
                        help="reduces input by division factor (must be int >0)")
    parser.add_argument("suitcase_source", type=str, help="the source for the suitcase (file path or http)")
    parser.add_argument("parts_source", type=str, help="the source for the parts list (file path or http)")
    args = parser.parse_args()

    # grab input data
    suitcase = grab_dict_from(args.suitcase_source)
    parts = grab_dict_from(args.parts_source)
    if args.save_inputs:
        with open('suitcase.json', 'w') as outfile:
            json.dump(suitcase, outfile)
        with open('parts.json', 'w') as outfile:
            json.dump(parts, outfile)

    # Apply data reduction if desired (for testing)
    if args.reduction_factor > 1:
        suitcase['volume'] = suitcase['volume']/args.reduction_factor
        parts = parts[0:1 + (len(parts)/args.reduction_factor)]


    if args.verbose:
        print 'Volume: ', suitcase['volume'], ' with #items: ', len(parts)
        sumVolume = 0
        for part in parts:
            sumVolume += part['volume']
        print 'Out of total part volume: ', sumVolume
        print 'Parts: ', parts, '\n'

    #Run solver
    solver = KnapSack01Solver(parts,suitcase['volume'])
    total_value, indices = solver.pick_items_dp()
    if args.verbose:
        print 'Total Value: ', total_value
        print 'Indices: ', indices

    # Collate solution
    sumVolume = 0
    if len(indices) ==0:
        result = {"part_ids":None,"value":0}
    else:
        result = {"part_ids":[],"value":total_value}
        for index in indices:
            result["part_ids"].append(parts[index]["id"])
            sumVolume += parts[index]['volume']
    if args.verbose:
        print 'Used volume: ', sumVolume,'\n'
    output = json.dumps(result, indent=4)

    # Output final result
    print output
    return 0

if __name__ == '__main__':
    main()
