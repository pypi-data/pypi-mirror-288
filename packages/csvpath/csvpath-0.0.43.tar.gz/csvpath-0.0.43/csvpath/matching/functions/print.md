
# Print

Prints to std.out. The function is helpful for debugging. It is good for writing validation results. Print can also be a quick way to create an output .csv or in another way capture the data generated during a run.

Print takes a value and a string. The value indicates if the print() is activated. The string is the output to write to sys.out.

Print strings can include the following variables.

| Variable name     | Description                                                           |
|-------------------|-----------------------------------------------------------------------|
|name               | The name of the file. E.g. for `$file.csv[*][no()]` it is `file`.     |
|delimiter          | The file's delimiter                                                  |
|quotechar          | The quote character the file uses to quote columns                    |
|match_count        | The current number of matches                                         |
|line_count         | The current line being processed                                      |
|scan_count         | The current number of lines scanned                                   |
|headers            | The list of header values                                             |
|headers.headername | The value of the named header                                         |
|scan_part          | The scan pattern                                                      |
|match_part         | The match pattern                                                     |
|variables          | The value of variables                                                |
|variables.varname  | The value of the named variable                                       |
|match_json         | A JSON dump of the match part parse tree                              |
|line               | The list of values that is the current line being processed           |
|last_row_time      | Time taken for the last row processed                                 |
|rows_time          | Time taken for all rows processed so far                              |

A variable is indicated as a qualifier off the root. The root is `$`, so the `delimiter` variable is referred to like this:

    $.delimiter

The print string must match this regular expression:

    r'"[\$A-Za-z0-9\.%_|\s :\\/,]+"'

I.e. it must be quoted with double quotes and be composed of only:
- Alphanums
- Dollar signs
- Periods
- Percents
- Underscores
- Pipes (the `|`)
- Spaces
- Colons
- Forward slashes
- Commas

It would obviously be better to have more special characters. The grammar may improve in the future, but for now that what we get. Any value contained by a header or variable will print just fine, even if it doesn't match this limited set of characters.

## Examples

    "$.name's delimiter is $.delimiter."

    "The match part JSON was parsed into this tree:\n
        $.match_json"

