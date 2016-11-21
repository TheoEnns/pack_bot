import unittest
from random import randint
from src.pb_get_json import grab_dict_from
from src.pb_knapsack import KnapSack01Solver

http_suitcase = 'http://pkit.wopr.c2x.io:8000/suitcases/rolly'
http_parts = 'http://pkit.wopr.c2x.io:8000/robots/hey-you/parts'
file_suitcase = 'test/suitcase.json'
file_parts = 'test/parts.json'

class KnapSack01SolverExtended(KnapSack01Solver):
    def pick_items_brute_force(self):
        """
        A terribly inefficient recursive solution for knapsack 0-1 added as a test comparison against
            the pick_items_dp() with small datasets. This function returns total optimal value achieved
            and the list of indices of parts used.

        :return: total_value, index_list
        """
        return self.__pick_items_brute_force(self.num_options-1,self.max_volume)

    def __pick_items_brute_force(self,current_index,available_volume):
        """
        The private recursion function for pick_items_brute_force to solve knapsack 0-1. This is for
            a test comparison to pick_items_dp().

        :return: total_value, index_list
        """
        #If there is no room left or we run out of items
        if available_volume <= 0 or current_index == -1:
            #Return that there is nothing to add
            return 0, []

        #If the remaining volume is smaller than the current item
        if self.parts[current_index]['volume'] > available_volume:
            #then try the next item
            return self.__pick_items_brute_force(current_index-1,available_volume)
        else:
            #We must either pick or not pick the remaining item
            #depending on the relative value of the remaining space given the remaining items
            #versus the value of the space left if we do add the current item given the remaining items
            value_without_current_item, excluded_item_set = \
                self.__pick_items_brute_force(current_index-1,available_volume)
            value_with_current_item, included_item_set = \
                self.__pick_items_brute_force(current_index-1, available_volume - self.parts[current_index]['volume'])
            value_with_current_item += self.parts[current_index]['value']

            # Note: for simplicity sake, in the case of a tie I will choose taking the item.
            if value_without_current_item > value_with_current_item:
                return value_without_current_item, excluded_item_set
            else:
                included_item_set.append(current_index)
                return value_with_current_item, included_item_set

class TestKnapSackSolver(unittest.TestCase):

    def setUp(self):
        pass

    def test_regress_simple_set_from_file(self):
        """
            test_known_subsample_from_file() takes a set of parts
              small enough that I could determine the correct solution
              on sight and verifies that the solution I as a human got matches
              the machine's solution.
          Verifies:
                  human solution and dp solutions match content
                  the value quoted by the solver matches the summation of values for the solution parts
                  the solution volume fits in the mini-suitcase
        """
        suitcase = {'volume':120}
        parts = [{"volume": 81, "id": "part-1", "value": 48},
                 {"volume": 71, "id": "part-2", "value": 32},
                 {"volume": 42, "id": "part-3", "value": 17},
                 {"volume": 44, "id": "part-4", "value": 39}]
        expected_indices = [1,3] #The solution I as a human would expect for the small set of parts
        solver = KnapSack01Solver(parts,suitcase['volume'])
        total_value, indices = solver.pick_items_dp()

        compare_value = 0
        total_volume = 0
        for index in indices:
            compare_value += parts[index]['value']
            total_volume += parts[index]['volume']

        self.assertEqual(compare_value,total_value,"Value achieved failed to match value sum over indices")
        self.assertGreater(suitcase['volume'],total_volume,"Volume picked fails to fit suitcase")
        self.assertItemsEqual(expected_indices,indices,"Solution set does not match expected set")

    def test_regress_full_file(self):
        """
            test_regression_full_file() is regression test against files of known output
            It will raise an alarm if the expected indices or total value no longer match the file's
                known output.
        """
        suitcase = grab_dict_from(file_suitcase)
        parts = grab_dict_from(file_parts)
        solver = KnapSack01Solver(parts,suitcase['volume'])
        total_value, indices = solver.pick_items_dp()
        expected_result = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                           18, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 35, 36,
                           37, 38, 39, 41, 43]

        self.assertEqual(1163,total_value,"Total value achieved failed to match expected regression value")
        self.assertItemsEqual(expected_result ,indices,"Length of indices list does not match regression")

    def test_random_input(self):
        """
            test_random_input() takes a randomized subset from the http sources, and solves the problem using both
                the dynamic and brute force approach against a reduced suitcase.
            Verifies: brute force and dp solutions match value and solution set
                      no index in the solution set is duplicated
                      the solution cumalitve volume fits in the mini-suitcase
        """
        suitcase = grab_dict_from(http_suitcase)
        parts = grab_dict_from(http_parts)
        reduction_factor = randint(5,10)
        suitcase['volume'] = suitcase['volume']/reduction_factor
        parts = parts[:len(parts)/reduction_factor]
        solver = KnapSack01SolverExtended(parts,suitcase['volume'])
        dp_total_value, dp_indices = solver.pick_items_dp()
        bf_total_value, bf_indices = solver.pick_items_brute_force()

        self.assertEqual(bf_total_value, dp_total_value,
                         "DP solution does not match the value of brute force solution")
        self.assertItemsEqual(dp_indices, bf_indices,"dp solution does not match in bf_index list")
        total_volume = 0
        for index in dp_indices:
            self.assertEqual(dp_indices.count(index),1,"Item index is duplicated in solution")
            total_volume += parts[index]['volume']
        self.assertGreater(suitcase['volume'],total_volume, "Volume picked fails to fit suitcase")
        print "\n---Random Input Test---"
        print 'Parts: ', parts, '\nSolution Indices: ', dp_indices
        print 'Suitcase: ', suitcase['volume'], '\nUsed space: ', total_volume, '\n'

if __name__ == '__main__':
    unittest.main()
