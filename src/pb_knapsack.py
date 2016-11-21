"""
    pb_get_json.py
        Author: Theodore Enns
        Brief: A basic recursive 0-1 knapsack approach.

           Profiling the data sets from the server showed that parts typically numbered
           about 38 to 44, with values and weights range 1 to 100 and the
           suitcase volume was 1584. Therefore, in choosing between the
           a dynamic programming approach (cost of O( len(parts)*Volume) ~ 70000) and the
           meet-in-the-middle (cost of O( len(parts)*2^(len(parts)/2)) ~ 185000000), I concluded
           the dynamic programming approach was better.
"""

class KnapSack01Solver(object):

    def __init__(self, parts, volume):
        """
        Class for solving 0-1 knapsacks

        :param parts: list of parts where each parts is a dict of id, volume, and value fields
        :param volume: positive integer for maximum capacity of knapsack
        """
        self.max_volume = volume
        self.num_options = len(parts)
        self.parts = parts

    def pick_items_dp(self):
        """
        Standard dynamic programming solution to knapsack 0-1. Returns total optimal value
            achieved and the list of indices of parts used.

        :return: total_value, index_list
        """
        if self.max_volume == 0 or self.num_options ==0:
            return 0, [] # Trivial scenario catch; no space or no parts means nothing to pack

        #  The dynamic programing approach calls for a value_table stores maximum packable
        #       values for the first i-th items given j container space where i is the
        #       row index (with i=0 corresponding to no items) and j is the column index
        #       (with j=0 being no space and iterating up to the actual container space
        #  However, in the interest of saving memory footprint, we shall stick to holding
        #       only the last row and current row in memory.

        # value_list represents the row-1 entries of the value table
        value_list = [0 for col in range(self.max_volume+1)]
        # selection_list holds the lists of parts indices used to get the values in row-1 of the value table
        selection_list = [[] for col in range(self.max_volume+1)]

        # If row is zero, there are no options and if col is zero, there is no room
        #  so we leave row==0 aor col==0 location at value zero
        for row in range(1,self.num_options+1):
            # Create the new selection_list and value_list for the the current row
            new_selection_list = [[] for col in range(self.max_volume+1)]
            new_value_list = [0 for col in range(self.max_volume+1)]
            for col in range(1,self.max_volume+1):

                # If the part would fit at the container size col
                if self.parts[row-1]['volume'] <= col:

                    # Get best cumulative value if I include the part and the value if I exclude instead
                    remainder_volume = col-self.parts[row-1]['volume']
                    value_including_item = self.parts[row-1]['value'] + value_list[remainder_volume]
                    value_excluding_item = value_list[col]

                    # Find which value is better
                    # Note: for simplicity sake, in the case of a tie I will choose taking the item. Normally,
                    #  I would inquire with the interviewer whether multiple optimal solutions would be worth
                    #  reporting, but with this being Thanksgiving vacation time, I will lean to the literal
                    #  return format of the prompt.
                    if value_including_item < value_excluding_item:
                        # Then do not to include part at parts[row-1]
                        new_value_list[col] = value_excluding_item
                        new_selection_list[col] = selection_list[col]
                    else:
                        # Otherwise include part at parts[row-1]
                        new_value_list[col] = value_including_item
                        new_selection_list[col] = selection_list[remainder_volume] + [row-1]
                else:
                    # If the part cannot fit, then the solution from the subset of options
                    #   without that part is still valid
                    new_value_list[col] = value_list[col]
                    new_selection_list[col] = selection_list[col]

            # Move the current row results to the contianers for the last row
            selection_list = new_selection_list
            value_list = new_value_list

        # The last entry of the last row is the solution
        return value_list[self.max_volume], selection_list[self.max_volume]
