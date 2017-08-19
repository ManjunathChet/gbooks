import csv
import os
from util.query_builder import QueryBuilder, Library, is_valid_query, is_valid_filter


if __name__== "__main__":

    # --------------------
    #   PROMPTS
    # ____________________

    while True:
        query = raw_input('Enter search query (required): ')
        if not is_valid_query(query):
            continue
        else:
           break
    # Loop for prompt

    valid_filters = ["averageRating", "ratingsCount", "publishedDate", "pageCount", "title"]
    # Supported fields for sorting

    while True:
        sort_input = raw_input('Sort? Options are {} \n Leave blank for unsorted values: '.format(valid_filters))
        if not is_valid_filter(sort_input, valid_filters):
            continue
        else:
           break
    # Loop for prompt that asks for sort

    # --------------------
    #   BUILD RESPONSE DICTIONARY
    # ____________________

    qb = QueryBuilder(q=query)
    # TO-DO: Add more elements to the query (MaxResults, filters, etc.)

    book_library = Library(qb.get_dict()).books
    # Construct a dictionary from the specified query

    # --------------------
    # SORT
    # ____________________

    if sort_input:
        try:
            book_library.sort(key=lambda x:x[sort_input], reverse=True)
        except KeyError:
            print "Some books don't have " + sort_input
    # If a sort field is specified, then perform a sort and modify the library

    # --------------------
    #   OUTPUT RESULTS
    # ____________________

    for book in book_library:
        if (not sort_input) or (sort_input == "title"):
            print book['title']
        else:
            try:
                print '{0:>40} | {1:>5}: {2}'.format(book['title'], sort_input, book[sort_input])
            except KeyError:
                print book['title'] + " doesn't have " + sort_input

    # --------------------
    #   SAVE CSV FILE
    # ____________________

    filename = "results/" + query + '.csv'
    with open(filename, 'wb') as csv_file:
        book_library_writer = csv.writer(csv_file, delimiter='|')
        for book in book_library:
            book_library_writer.writerow([book[key] for key in book])
        print "Library written to " + str(os.path.abspath(filename))

    # TO-DO:
    # Extend the app to load from a CSV file and perform sort functions
    #   - The following comments are modules under construction for CSV loading

    #with open(filename, 'rb') as csv_file:
    #    book_reader = csv.reader(csv_file, delimiter='|')
    #    for row in book_reader:
    #       print "  ;  ".join(row)
    #        print "\n"
