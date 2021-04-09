"""
    CS051P Lab Assignments: Babies

    Author: Chuck Rak
    Partner: Vikrant Goel

    Date:   3 November 2020

    The goal of this assignment is to give you more practice with functions,
    including testing functions.
"""
import matplotlib.pyplot as plt
import sys

def parse_names(fname):
    """
    parse a name file
    :param fname:  name (full path) of the file to read and parse
    :return d: a name dictionary
    """
    # Opens file
    in_file = open(fname, "r")
    # Empty dictionary assigned
    d = dict()
    # Iterate through each line of given file
    for line in in_file:
        # Line contains following elements in this order(State, Gender, Year, Name, # of occurences)
        info_list = line.split(",")
        year = int(info_list[2])
        name = info_list[3]
        count = int(info_list[4])
        # Checks if year is already in the dictionary
        if year in d:
            if name in d[year]:
                # Adds the counts together if the name has already occured
                d[year][name] += count
            else:
                # Assigns value of inner dictionary to number of occurences of name
                d[year][name] = count
        # If year isn't already in dictionary it becomes a new element of the dictionary
        else: 
            d[year] = {name : count}
    return d
    

def extract_data(name_dict,match_string):
    """
    Takes a name dictionary  { year : {name : count}} and a string to match (strings like abc* are special case)
    and creates a result dictionary { year : count }
    :param name_dict: name dictionary
    :param match_string: string to match
    :return extracted_d: dictionary of form { year : count } that match the strings
    """
    # Empty dictionary assigned
    extracted_d = dict()
    # search_all_names tells computer whether to search all names in case of match_string = "*"
    search_all_names = False
    # If wildcard parameter is in string, then it does not have to exactly equal the striing 
    must_equal = True
    # Checks for wildcard parameter in string
    if "*" in match_string:
        if(len(match_string) > 1):
            # If wildcard is in string, the string is shortened by one to eliminate the wildcard
            # and the rest of the string is used to search through the dictiornary
            match_string = match_string[:len(match_string)-1]
            must_equal = False
        else:
            # sets search_all_names to true because "*" is in match_string and len !> 1 so match_string = "*"
            search_all_names = True    
    # Iterates through keys of given dictionary
    for year in name_dict:
        count = 0
        # Addresses case when match_string only contains "*", thus all names match
        if search_all_names:
            # Iterates through different names in each year 
            for name in name_dict[year]:
                count += name_dict[year][name]
            extracted_d[year] = count
        # Addresses all other cases where match_string is either a name or part of a name combined with a "*"
        else:
            # Cycles through the different names in each year
            for name in name_dict[year]:
                
                if not must_equal:
                    # Checks to see if match_string is in name
                    if match_string in name:
                        # Adds value of name if it matches match_string
                        count += name_dict[year][name]
                # Accounts for case where user only wants to search for a certain name (ex: "Jeff")
                # so the computer checks to see if string is equal to name instead of in name, 
                # to prevent names such as "Jeffery" from being counted. This would only happen if "Jeff*"
                # was entered
                else:
                    if match_string == name:
                        count += name_dict[year][name]
            extracted_d[year] = count
    return extracted_d

    
def normalize_data(data):
    """
    Normalize data by dividing by average value computed
    over years.  Be careful of /0 bugs !
    :param data: a dictionary with the data
    """
    # Initializes years and total count to 0
    years_count = 0
    total_name_count = 0
    # cycles through each year, counts how many years and adds up total count
    for year in data: 
        years_count += 1
        total_name_count += data[year]
    # Coumputes average
    average_appearance = total_name_count / years_count
    # Cycles through each year and assigns each value to the normalized values
    for year in data:
        data[year] = data[year] / average_appearance


def scatter_plot(data,format,name):
    """
    Create a scatterplot (but don't draw the final plot).  The plotted data will need to be normalized
    :param data:  a dictionary of the form { year : count }
    :param format: format string for matplotlib
    :param name: name of this plot for legend
    """
    # Normalization of given data
    normalize_data(data)
    # List comprehensions that iterate through x and y data lists
    x = [year for year in data]
    y = [count for count in data.values()]

    # plot the data
    plt.plot(x,y, format, label=name)


def close_plot(title):
    """
    This function should add the legend, title, and labels to the graph
    :param title: title for whole plot (a string))
    """
    # Generates labels for graph, legend, and title
    plt.xlabel("Year")
    plt.ylabel("Normalized Count")
    plt.legend()
    plt.title(title)

def main(filedir):
    """
    Interactive input to specify plot
    Creates plots for the requested pattern for each of the 
    requested states
    :param filedir: the path to directory with data files
    """
    count = 0
    # Asks use for matching string
    matching_string = input("Enter a pattern to match:")
    # Creates four different formats that will be used for each state's data
    formats = ('b.', 'gx', 'ro', 'ms')
    # Prompts for state name
    state = input("Enter the two letter abbreviation for a state (TX,IN,...):")
    # cycles through a max of four states' data, adding it to the plot and doing the necessary manipulations, 
    # ending when there is an empty string entered
    while(not state == "" and count < 4):
        data = extract_data(parse_names(filedir+ "/" + state + ".TXT"), matching_string)
        normalize_data(data)
        scatter_plot(data, formats[count], state)
        state = input("Enter the two letter abbreviation for a state (TX,IN,...):")
        count += 1
    close_plot(matching_string)


if __name__ == '__main__':   
    # change the directory path as needed
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('namesbystate')
    # plt.show is here so that we can
    # automate testing do not call it in your code
    plt.show()