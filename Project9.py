###############################################################
# CSE 231 project #9
#
# program that deals with data from the NYSE.
# this program will read data from the prices file as well as data from the securities file
# 
#function to open the 2 files.
#function to read the securities file and create a master dictionary.
#function to add pricing data to the master dictionary.
#function to get the max price of a given company symbol.
#function to find the max price of all the given companies.
#function to get the avg price of a given company symbol.
#function to display a given list in 3 columns.
#main function to call all other functions and interact with the user/options.
###############################################################

import csv

#initialize all constant variables
MENU = '''\nSelect an option from below:
            (1) Display all companies in the New York Stock Exchange
            (2) Display companies' symbols
            (3) Find max price of a company
            (4) Find the company with the maximum stock price
            (5) Find the average price of a company's stock
            (6) quit
    '''
WELCOME = "Welcome to the New York Stock Exchange.\n"
    
#function to open the 2 files.
def open_file():
    '''FUnction to open the two different files for manipulation
    Parameters: None
    Returns: prices fp and securities fp'''
    
    #prompt for a prices filename
    prompt_prices = input("\nEnter the price's filename: ")
    
    #loop to handle all error inputs
    while True:
        try:
            #try opening the name of the file given
            prices_file_pointer = open(prompt_prices)
            #return that file if it is found
            #return prices_file_pointer
            break
        except FileNotFoundError:
            #if file is not found, try asking again
            print("\nFile not found. Please try again.")
            prompt_prices = input("\nEnter the Prices file name: ")
            
    #prompt for security filename
    prompt_security = input("\nEnter the security's filename: ")
    
    #loop to handle all error inputs
    while True:
        try:
           #try opening the name of the file given
            securities_file_pointer = open(prompt_security)
            #return that file if it is found
            #return securities_file_pointer
            break
        except FileNotFoundError:
            #if file is not found, try asking again
            print("\nFile not found. Please try again.")
            prompt_security = input("\nEnter the Prices file name: ")
    #return the two filepointers
    return prices_file_pointer, securities_file_pointer

#function to read the securities file and create a master dictionary.
def read_file(securities_fp):
    '''Function to read the securities file and create a master dictionary
    Parameters: securities fp
    Returns: Master dictionary'''
    
    #initialize empty dictionary
    master_dictionary = {}
    #initialize empty set
    name_set = set()
    
    #read the file using csv reader
    reader = csv.reader(securities_fp)
    #skip header line
    next(reader)
    for line in reader:

        #add each name to the set
        name_set.add(line[1])
        
        #gather company symbol as the key for the dictionary
        the_key = line[0]
        
        #gather all necessary information for the values list
        comp_name = line[1]
        comp_sector = line[3]
        comp_subsector = line[4]
        comp_address = line[5]
        comp_date = line[6]

        #assign each piece of information to the master dictionary
        master_dictionary[the_key] = [comp_name, comp_sector, comp_subsector, comp_address, comp_date, []]
        
    #return the set and master dictionary
    return name_set, master_dictionary
        
#function to add pricing data to the master dictionary.        
def add_prices (master_dictionary, prices_file_pointer):
    '''Function to add pricing data to the master dictionary
    Parameters: Master dictionary and prices filepointer
    Returns: Nothing'''
    
    #read the file using csv reader and skip header line
    reader = csv.reader(prices_file_pointer)
    next(reader)
    for index,line in enumerate(reader):
        
        #gather all necessary information and assign floats when needed
        the_date = line[0]
        the_symbol = line[1]
        the_open = line[2]
        the_open_flt = float(the_open)
        the_close = line[3]
        the_close_flt = float(the_close)
        the_low = line[4]
        the_low_flt = float(the_low)
        the_high = line[5]
        the_high_flt = float(the_high)
        
        #add each piece of info to the pricing list
        price_list = [the_date, the_open_flt, the_close_flt, the_low_flt,the_high_flt]
        
        #add the list to the dictionary if it exists, continue otherwise
        try:
            master_dictionary[the_symbol][5].append(price_list)
        except KeyError:
            continue
        
#function to get the max price of a given company symbol.        
def get_max_price_of_company (master_dictionary, company_symbol):
    '''Function to get the max price of a given company symbol
    Parameters: Master dictionary and company symbol
    Returns: a tuple of company symbol and max price for the company symbol.'''
    
    #initialize empty list and empty tuple for companies with no data available
    empty_list = []
    empty_tuple = (None, None)
    
    #get the necessary information that is within the lists within the dictionary
    try:
        for i,x in enumerate(master_dictionary[company_symbol][5]):
            the_date = x[0]
            high_price = x[4]
            #add the necessary information into a tuple
            a_tuple = (high_price, the_date)
            #append each tuple to the empty list
            empty_list.append(a_tuple)
        #if nothing is available, return the empty tuple
        if len(empty_list) == 0:
            return (empty_tuple)
        #return the max tuple of the list
        else:
            return (max(empty_list))
    #if the symbol doesn't exist, return the empty tuple
    except KeyError:
        return (empty_tuple)
                                              
#function to find the max price of all the given companies.
def find_max_company_price (master_dictionary):
    '''Function to find the max company price
    Parameters: Master dictionary
    Returns: tuple containing the max price and the compan symbol'''
    
    #initialize empty list
    a_list = []
    # loop through each key in the dictionary
    for symb in master_dictionary:
        #make the symbol a string
        symb_str = str(symb)
        #use the get_max_price_of_company function to get the max price of each company
        max_price = get_max_price_of_company(master_dictionary, symb_str)
        #add the max price and company symbol to a tuple
        the_price = max_price[0]
        if max_price[0] != None:
            a_tup = (the_price, symb_str)
        #if the price is not equal to None, then append the tuple to empty list
            a_list.append(a_tup)
        #find the max price of all the prices and return the max price along with company name
        the_max = max(a_list)
    return (the_max[1], the_max[0])

#function to get the avg price of a given company symbol.
def get_avg_price_of_company (master_dictionary, company_symbol):
    '''function to get the avg price of a given company symbol
    Parameters: master dictionary and company symbol
    Returns: average price of a given company'''
    
    #initialize empty lists
    empty_list = []
    
    #try to loop through the pricing lists of a given symbol
    try:
        for i,x in enumerate(master_dictionary[company_symbol][5]):
            #find high prices, add them to a list, sum the high prices and divide by the num of prices
            high_price = x[4]
            empty_list.append(high_price)
        the_sum = sum(empty_list)
        numbers = len(empty_list)
        #dont divide by 0
        if numbers != 0:
            #return the average
            the_avg = round(the_sum/numbers, 2)
            return the_avg
        #return 0 otherwise
        else:
            return 0.0
    except KeyError:
        return 0.0
#function to display a given list into 3 columns            
def display_list (lst):  # "{:^35s}"
    '''Function to display a given list into 3 columns
    Parameters: lst
    Returns: Nothing'''
    indx = 0
    while indx < len(lst):
        print("{:^35s}{:^35s}{:^35s}".format(lst[indx], lst[indx+1], lst[indx+2]))
        indx+=3
    print('\n')
def main():
    #print welcome message
    print(WELCOME)
    
    #call all necessary functions needed
    the_open_file = open_file()
    the_read_file = read_file(the_open_file[1])
    master_dictionary = the_read_file[1]
    the_add_prices = add_prices(the_read_file[1], the_open_file[0])
    the_max_company_price = find_max_company_price(the_read_file[1])
    
    #print the menu and prompt for an option
    print(MENU)
    prompt = input("\nOption: ")
    #if given prompt is not in given menu options, print error message
    while prompt not in "123456":
        print("\nInvalid option. Please try again.")
        prompt = input("\nOption: ")
    #main loop  
    while prompt != '6':
        if prompt == '1':
            #if the prompt is equal to 1, print the set of all companies
            print("\n{:^105s}".format("Companies in the New York Stock Market from 2010 to 2016"))
            #sort the companies
            companies_set = sorted(the_read_file[0])
            #print(companies_set)
            display_list(companies_set)

        #if the prompt is equal to 2, print all company symbols    
        elif prompt == '2':
            print("\ncompanies' symbols:")
            the_symbols = master_dictionary.keys()
            #sort the symbols
            sorted_symbols = sorted(the_symbols)
            #print(sorted_symbols)
            display_list(sorted_symbols)
            
        #if the prompt is equal to 3, prompt for a company symbol, then print max price for the symbol    
        elif prompt == '3':
            symbol_prompt = input("\nEnter company symbol for max price: ")
            #if the symbol doesn't exist, print error message and reprompt
            while True:
                if symbol_prompt in the_read_file[1]:
                    break
                else:
                    print("\nError: not a company symbol. Please try again.")
                    symbol_prompt = input("\nEnter company symbol for max price: ")
            #call max price function to get the max price to display
            the_max_p = get_max_price_of_company(the_read_file[1], symbol_prompt)
            if the_max_p == (None, None):
                print("\nThere were no prices.")
            else:
                print("\nThe maximum stock price was ${:.2f} on the date {:s}/\n".format(the_max_p[0], the_max_p[1]))
            
        #if the prompt is equal to 4, print the company with the high stock price in the data 
        elif prompt == '4':
            print("\nThe company with the highest stock price is {:s} with a value of ${:.2f}\n".format(the_max_company_price[0], the_max_company_price[1]))
        
        #if the option is equal to 5, prompt for a symbol and print the average stock price for the given symbol
        elif prompt == '5':
            prompt_symbol = input("\nEnter company symbol for average price: ")
            while True:
                if prompt_symbol in the_read_file[1]:
                    break
                else:
                    print("\nError: not a company symbol. Please try again.")
                    prompt_symbol = input("\nEnter company symbol for average price: ")
            #call the averge price company function in order to get the average price and print it
            the_avg = get_avg_price_of_company(the_read_file[1], prompt_symbol)
            if the_avg == 0.0:
                print("\nThere were no prices.")
            else:
                print("\nThe average stock price was ${:.2f}.\n".format(the_avg))
        #print the menu again and rempromt, if not a valid option, then print error message and reprompt
        print(MENU)
        prompt = input("\nOption: ")
        while prompt not in "123456":
            print("\nInvalid option. Please try again.")
            prompt = input("\nOption: ")
       
if __name__ == "__main__": 
    main() 