from util.query_builder import QueryBuilder, \
    Library, \
    is_valid_query, \
    is_valid_filter, \
    check_if_query_is_stored_locally, \
    build_library_from_csv, \
    save_library_to_csv

def gbooks():
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

    query_is_in_csv = check_if_query_is_stored_locally(query)

    if query_is_in_csv:
        book_library = build_library_from_csv(query)
    else:
        qb = QueryBuilder(q=query)
        # TO-DO: Add more elements to the query (MaxResults, filters, etc.)
        book_library = Library(qb.get_dict()).books
        # Construct a list of books from the specified query

    # --------------------
    # SORT
    # ____________________
    for book in book_library:
        if sort_input not in book.keys():
            book[sort_input] = None

    if "count" in sort_input.lower() or "date" in sort_input.lower() or "rating" in sort_input.lower():
        # If the specified field is a count/date, then reverse the sort (higher/latest at the top)
        book_library.sort(key=lambda x: x[sort_input], reverse=True)
        # Sort 1-liner from StackOverflow; source:
        # https://stackoverflow.com/a/73050
    elif sort_input:
        # If its not a "count" type field, then we use a regular sort
        book_library.sort(key=lambda x: x[sort_input])

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

    save_library_to_csv(query, book_library)

if __name__== "__main__":
    gbooks()

