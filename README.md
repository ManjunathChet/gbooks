# gbooks
A console line application that interacts with the google books API

#### How to Run

From this directory, run:
`python gbooks.py`

#### Behavior

The console app will prompt the user for 2 inputs:
* query
* sort

After the input is provided, the app will display the results, and save a copy in a
CSV file that can be found in the 'results' folder.

#### Validated Tests

###### Input Validation
* Empty query input
* Empty sort input
* Long query input

###### Sort Tests
* publishedDate sort
* averageRating sort
* publishedDate sort
* title sort

###### Output Tests
* Data is written out to CSV
* Fields are parsed as expected
* Missing fields are omitted

#### Known Issues
* Prompt for loading CSV is still in progress. The user can only start new queries and save them.
* Sorts for counts is currently broken (ex. ratingsCount ranks 10 > 98)
* Sorts for missing fields is broken
* Paths for output files are absolute
* No file validation is done prior to writing files
* No file locks are implemented yet
