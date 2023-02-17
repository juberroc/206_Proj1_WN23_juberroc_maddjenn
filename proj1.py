
# Your names: Julio Berrocal Alvarez, Madison Jennings
# Your student id: 14797142, 48980758
# Your emails: juberroc@umich.edu , maddjenn@umich.edu
# List who you have worked with on this project: Madison Jennings (maddjenn)

import io
import sys
import csv
import unittest


def load_csv(filename):
    file = open(filename)  
    
    content = file.readlines() #list of strings of each row
    data = {}

    headers = content[0].strip().split(",") # list of strings of first row
    headers.pop(0)

    midwest = content[1].strip().split(",") # list of string of second row
    midwest.pop(0)
    northeast = content[2].strip().split(",") # list of string of third row
    northeast.pop(0)
    south = content[3].strip().split(",") # list of string of fourth row
    south.pop(0)
    west = content[4].strip().split(",") # list of string of fifth row
    west.pop(0)
   
    region_counts = {"midwest": midwest, "northeast": northeast, "south": south, "west": west} 
    
    for i in range(len(headers)): #switching values from str to int
       midwest[i] = int(midwest[i])
       northeast[i] = int(northeast[i])
       south[i] = int(south[i])
       west[i] = int(west[i])
        

    for row in content[1:]: #looping through the rows (regions)
        column = row.split(',')
        region = column[0]
        data[region] = {}
        counter = 0
        for item in headers: #looping through the heards
            data[region][item] = region_counts[region][counter] 
            counter += 1
    
    file.close()
    return data

def calc_pct(data):
    '''
    Calculates the percentage of each demographic using this
    formula: (demographic / total people) * 100

    Parameters
    ----------
    data: dict
        Either SAT or Census data

    Returns
    -------
    pcts: dict
        the dictionary that represents the data in terms of percentage share
        for each demographic for each region in the data set
    '''
    pcts = {}
    for region, region_data in data.items():
        total_people = region_data.get("Region Totals")
        region_pcts = {}
        for demographic, count in region_data.items():
            pct = (count / total_people) * 100
            region_pcts[demographic] = round(pct, 2)
        pcts[region] = region_pcts
    return pcts

def calc_diff(sat_dict, census_dict):
    '''
    Takes the absolute value, rounded to 2 decimal places,
    of the difference between each demographic's percentage
    value in census_dict from sat_dict

    Parameters
    ----------
    sat_dict: dict
        SAT data
    census_dict: dict
        Census data

    Returns
    -------
    pct_dif: dict
        the dictionary of the percent differences
    '''
    pct_dif = {}
    for region in sat_dict.keys():
        pct_dif[region] = {}
        for demographic in sat_dict[region]:
            if demographic in census_dict[region].keys():
                diff = abs(sat_dict[region][demographic] - census_dict[region][demographic])
                diff = round(diff, 2)
                pct_dif[region][demographic] = diff
    return pct_dif

def write_csv(data, file_name):
    '''
    Writes the data to csv, adding the header as
    the first row

    Parameters
    ----------
    data: dict
        dictionary with percent differences

    file_name: str
        the name of the file to write

    Returns
    -------
        None. (Doesn't return anything)
    '''
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['region'] + list(data[list(data.keys())[0]].keys())
        writer.writerow(header)

        for region, values in data.items():
            row = [region] + list(values.values())
            writer.writerow(row)

def min_max_mutate(data, col_list):
    # Do not change the code in this function
    '''
    Mutates the data to simplify the implementation of
    `min_max` by moving the race/ethnicity key to the outside
    of the nested dictionary and the region key to the inside
    nested dictionary like so:
    {'race/ethnicity': {'region': pct, 'region': pct, ...}...}

    Parameters
    ----------
    data : dict
        dictionary of data passed in.
    col_list : list
        list of columns to mutate to.

    Returns
    -------
    demo_vals: dict
    '''
    
    # Do not change the code in this function
    demo_vals = {}
    for demo in col_list:
        demo_vals.setdefault(demo, {})
        for region in data:
            demo_vals[demo].setdefault(region, data[region][demo])
    return demo_vals

def min_max(data):
    '''
    Finds the max and min regions and vals for each demographic,
    filling a dictionary in the following format:
    {"min": {"demographic": {"region": value}, ...},
     "max": {"demographic": {"region": value}, ...}...}

    Parameters
    ----------
    data: dict
        the result of min_max_mutate

    Returns
    -------
    min_max: dict
        a triple nested dictionary
    '''
    min_max = {"min": {}, "max": {}}
    for demographic in data:
        min_region = min(data[demographic], key=data[demographic].get)
        min_val = data[demographic][min_region]
        max_region = max(data[demographic], key=data[demographic].get)
        max_val = data[demographic][max_region]
        min_max["min"][demographic] = {min_region: min_val}
        min_max["max"][demographic] = {max_region: max_val}
    return min_max

#Extra Credit

def nat_pct(data, col_list):
    '''
    EXTRA CREDIT
    Uses either SAT or Census data dictionaries
    to sum demographic values, calculating
    national demographic percentages from regional
    demographic percentages

    Parameters
    ----------
    data: dict
        Either SAT or Census data
    col_list: list
        list of the columns to loop through. helps filter out region totals columns

    Returns
    -------
    data_totals: dict
        dictionary of the national demographic percentages

    '''
    data_totals = {}    
    for col in col_list:
        if not col.endswith("_total"):
            for region in data:
                value = data[region].get(col, 0)
                data_totals[col] = data_totals.get(col, 0) + value
    total_population = sum(data_totals.values())
    for col, total in data_totals.items():
        percentage = (total / total_population) * 100
        data_totals[col] = percentage
    
    return data_totals

def nat_diff(sat_data, census_data):
    '''
    EXTRA CREDIT
    Calculates the difference between SAT and Census
    data on a national scale
    Parameters
    ----------
    sat_data: dict
        national SAT data
    census_data: dict
        national Census data

    Returns
    nat_difference: dict
        the dictionary consisting of the demographic
        difference on national level
    '''
    nat_difference = {}
    for col in sat_data:
        census_pct = census_data.get(col)
        if col in census_data.keys():
            diff = sat_data[col] - census_pct
            nat_difference[col] = diff
    return nat_difference

def main():
    '''
    Fill out main per the comments below; 
    You don't have to print anything here, 
    but your code should run write_csv()
    on your computed dict of differences
    '''   
    # read in the data
    census_var = load_csv("census_data.csv")
    sat_var = load_csv("sat_data.csv")

    # compute demographic percentages
    sat_pct = calc_pct(sat_var)
    census_pct = calc_pct(census_var)

    # compute the difference between test taker and state demographics
    pct_diff = calc_diff(sat_pct, census_pct)
    #rint(pct_diff)

    # output the csv
    output = write_csv(pct_diff, "proj1-Berrocal-Jennings.csv")

    # create a list from the keys of inner dict
    demographics = list(pct_diff['midwest'].keys())[0:8] #excluded Region Totals

    # mutate the data using the provided 'min_max_mutate' function
    dic_mutate = min_max_mutate(pct_diff, demographics)

    # calculate the max and mins using `min_max`
    min_max_dic = min_max(dic_mutate)

    # print 'min_max' as well 
    print(min_max_dic)

    # extra credit here

    # if you did the EC, print the dict you get from nat_diff

    pass

main()

# unit testing
class HWTest(unittest.TestCase):

    def setUp(self):
        # surpressing output on unit testing
        suppress_text = io.StringIO()
        sys.stdout = suppress_text

        # setting up the data we'll need here
        # basically, redoing all the stuff we did in the main function
        self.sat_data = load_csv("sat_data.csv")
        self.census_data = load_csv("census_data.csv")

        self.sat_pct = calc_pct(self.sat_data)
        self.census_pct = calc_pct(self.census_data)

        self.pct_dif_dict = calc_diff(self.sat_pct, self.census_pct)

        self.col_list = list(self.pct_dif_dict["midwest"].keys())

        self.mutated = min_max_mutate(self.pct_dif_dict, self.col_list)

        self.min_max_val = min_max(self.mutated)

        # extra credit
        # providing a list of col vals to cycle through
        #self.col_list = self.census_data["midwest"].keys()

        # computing the national percentages
        #self.sat_nat_pct = nat_pct(self.sat_data, self.col_list)
        #self.census_nat_pct = nat_pct(self.census_data, self.col_list)

        #self.dif = nat_diff(self.sat_nat_pct, self.census_nat_pct)

    '''

    Create test functions for the functions you wrote here!

    '''
    def test_load_csv(self):
        self.assertEqual(len(self.sat_data), 4, "Testing that length of SAT dictionary is 4")
        self.assertEqual(len(self.census_data), 4, "Testing that length of Census dcitionary is 4 ")
        self.assertEqual(self.sat_data["midwest"]["ASIAN"], 14664, "Testing number of Asian test-takers in the midwest")
        self.assertEqual(self.census_data["northeast"]["ASIAN"], 3635499, "Testing Asian population in the northeast")

    def test_calc_pct(self):
        self.assertAlmostEqual(self.sat_pct["midwest"]["AMERICAN INDIAN/ALASKA NATIVE"], 0.8039, 2, "Testing SAT pct of American Indian/Alaska white in midwest region")
        self.assertAlmostEqual(self.sat_pct["midwest"]["ASIAN"], 5.873 , 2, "Testing SAT pct of Asians in midwest region")
        self.assertAlmostEqual(self.census_pct["midwest"]["AMERICAN INDIAN/ALASKA NATIVE"], 0.5251, 2,  "Testing census pct of American Indian/Alaska white in midwest region")
        self.assertAlmostEqual(self.census_pct["west"]["ASIAN"], 10.7708 , 2, "Testing census pct of Asian in west region")

    def test_calc_diff(self):
        self.assertAlmostEqual(self.pct_dif_dict["midwest"]["ASIAN"], 3.11 , 2, "Testing pct difference for Asian in midwest")
        self.assertAlmostEqual(abs(self.pct_dif_dict["south"]["BLACK"]), 3.26, 2, "Testing pct difference for Black in south" )

    def test_min_max(self):
        self.assertEqual(list(self.min_max_val["max"]["WHITE"].keys())[0], "midwest", "Testing that max region for White is midwest")
        self.assertEqual(list(self.min_max_val["min"]["WHITE"].keys())[0], "west", "Testing that min region for White is west")
        self.assertEqual(list(self.min_max_val["min"]["BLACK"].keys())[0], "midwest", "Testing that min region for Black is midwest")
        self.assertEqual(list(self.min_max_val["max"]["BLACK"].keys())[0], "south", "Testing that max region for Black is south")
      


    # # testing the nat_pct extra credit function
    # def test_nat_pct(self):
    #    self.assertEqual(
    #    nat_pct({"region":{"demo":5,"Region Totals":10}},["demo", "Region Totals"]),
    #    {'Region Totals': 100.0, 'demo': 50.0})

    # # second test for the nat_pct extra credit function
    # def test2_nat_pct(self):
    #     self.assertEqual(
    #         self.sat_nat_pct["AMERICAN INDIAN/ALASKA NATIVE"],
    #         0.73)

    # # testing the nat_dif extra credit function
    # def test_nat_diff(self):
    #     self.assertEqual(
    #         nat_diff({"demo":0.53, "Region Totals": 1},{"demo":0.5, "Region Totals": 1}),
    #         {'Region Totals': 0, "demo":0.03}
    #         )

    # # second test for the nat_diff extra credit function
    # def test2_nat_diff(self):
    #     self.assertEqual(
    #         self.dif["ASIAN"],
    #         3.32)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    pass
