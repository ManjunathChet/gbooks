import requests
import json
import os


class QueryBuilder(object):
    """
    QueryBuilder contains all the elements of building a request that interacts with the
    Google books API.
    """
    def __init__(self, *args, **kwargs):
        """

        :param args: The expected values are filters for the query
        :return: Nothing returned, class variables are set
        """
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        self.base_address = 'https://www.googleapis.com/books/v1/volumes?q='
        self.full_query = self.base_address + self.q
        self.get_dict()

    def get_dict(self):
        """
        get_dict takes the response data and translates it to a dictionary
        """

        print "Querying " + self.full_query + " ..."
        response = requests.get(self.full_query)
        response_json = json.loads(response.text)
        return response_json


class Library(object):
    """
    Library translates the dictionary returned by the request into a dictionary that can
     be indexed for various values.
    """
    def __init__(self, query_dict):
        self.books = []
        self.query_dict = query_dict
        self.build_books_dict()

    def build_books_dict(self):
        for book in self.query_dict["items"]:
            items_dict = construct_dict(book["volumeInfo"])
            sale_dict = construct_dict(book["saleInfo"])

            merged_dict = items_dict.copy()
            merged_dict.update(sale_dict)

            self.books.append(merged_dict)

            #break


def construct_dict(book):
    """
    Helper function to construct the book library
    :param book: Dictionary; contains induvidual book data
    :return: cleaned dictionary with uniform keys and values
    """
    final_dict = {}
    for key in book.keys():
        value = book[key]
        #print "KEY: " + key
        #print "VALUE: " + str(value)

        if type(value) is dict:
            #print "TYPE IS DICT"
            merge_dict = final_dict.copy()
            merge_dict.update(construct_dict(value))
            # If the value of a certain key is a dictionary, then add that dictionary to the book info
            # by recursively calling this function
        if type(value) is int or type(value) is float:
            #print "TYPE IS NUM"
            final_dict[key] = value
            # If a value is a number, then keep its value as an int or float.
            #
            # If we dont do this step, then sorting these values will fail, since they will be cast as
            # strings.
            # ex.) 98 will be greater than 1200, because of lexicographical sort.
        else:
            try:
                final_dict[key] = str(value)
            except UnicodeEncodeError:
                continue

    return final_dict

def is_valid_query(query):
    """
    Prompt input verification

    :param query: string from input
    :return: True if valid, False if not
    """
    if len(query) > 30:
        print "Query: {}".format(query)
        print "is too long, please try a shorter query"
        return False
    if len(query) <= 0:
        print "Please enter a valid query"
        return False
    else:
        return True


def is_valid_filter(sort_input, valid_filters):
    """
    Sort input validation

    :param sort_input: string, from second input prompt
    :param valid_filters: list, hardcoded strings that are supported fields
    :return: True if valid, False if not
    """
    if sort_input and sort_input not in valid_filters:
        print "{} is not a valid sort option.".format(sort_input)
        return False
    else:
        return True


def check_if_query_is_stored_locally(query):
    """
    Check if a CSV file is already created for this query
    :param query: string; input from user
    :return: True if CSV file exists, False if not
    """

    filename = "results/" + query + '.csv'

    if os.path.isfile(filename):
        print "Query is already stored locally."
        return True
    else:
        print "Query is not stored locally."
        return False


def build_library_from_csv(query):
    """
    Construct book library from stored file
    :param query: string; input from user, only used for filename
    :return: list of book dictionaries; library
    """

    filename = "results/" + query + '.csv'
    library = []

    print "Reading from " + filename

    with open(filename, 'rb') as csv_file:
        book_list = csv_file.readlines()
        for book in book_list:
            library.append(json.loads(book))

    return library


def save_library_to_csv(query, book_library):
    """
    Function that creates CSV file
    :param query: string, input from user
    :param book_library: list, all books (dictionaries)
    :return: Nothing, a file is created in "results"
    """
    filename = "results/" + query + '.csv'

    print "Saving library to " + filename + " ..."

    with open(filename, 'wb') as csv_file:
        for book in book_library:
            book_json = json.dumps(book)
            csv_file.write(book_json)
            csv_file.write('\n')

        print "Library written to " + str(os.path.abspath(filename))
