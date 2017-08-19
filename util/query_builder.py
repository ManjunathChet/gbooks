import requests
import json


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
            print key + " : " + value

        self.base_address = 'https://www.googleapis.com/books/v1/volumes?q='
        self.full_query = self.base_address + self.q
        self.get_dict()

    def get_dict(self):
        """
        get_dict takes the response data and translates it to a dictionary
        """
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


def construct_dict(book):
    """
    Helper function to construct the book library
    :param book: Dictionary; contains induvidual book data
    :return: cleaned dictionary with uniform keys and values
    """
    final_dict = {}
    for key in book.keys():
        value = book[key]
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