'''
Created on May 6, 2016

@author: jivan
'''
from HTMLParser import HTMLParser, HTMLParseError


class HTMLTableStripper(HTMLParser):
    ''' | *brief*: Collects values from html tables.
        | *author*: Jivan
        | *created*: 2016-01-22
        This class parses HTML and provides the content of any tables as a list of
        string values for each row.

        Example:
            table_stripper = HTMLTableStripper()
            table_stripper.feed('<tr><td>1</td><td>2</td></tr>')
            r = table_stripper.get_table_contents()
            r is [ ['1','2'] ]

        get_table_contents() returns the data of the results (the content between <td></td> tags)
        as a list of lists where each list is a data row from the html.  You cannot feed
        any more html to the class after calling get_table_contents().

        Use a new instance for each separate piece of html you would like to parse.
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        # List of python object results, built up as html is parsed.
        self._results = []
        # Stack of tags of interest indicating their nesting as they are encountered.
        self._previous_tag = []

    def handle_starttag(self, tag, attrs):
        # Ignore all tags besides tr & td.
        if tag in ['tr', 'th', 'td']:
            # We don't expect any nested tables or other tags in result tables.
            if self._previous_tag == 'tr' and tag not in ['th', 'td']:
                raise Exception('Invalid HTML.  <TR> tags should only contain <TH> & <TD> tags.')
            # A new row, make an empty list to store its values.
            if tag == 'tr':
                self._current_row = []

            self._previous_tag.append(tag)

    def handle_data(self, data):
        # Store data if it comes from a <td> tag.
        if self._previous_tag and self._previous_tag[-1] in ['th', 'td']:
            self._current_row.append(data)

    def handle_endtag(self, tag):
        # Ignore all tags besides tr & td.
        if tag in ['tr', 'th', 'td']:
            pt = self._previous_tag.pop()
            if tag != pt:
                raise HTMLParseError('Mismatched tag <{}></{}>'.format(pt, tag))
            if pt == 'tr':
                self._results.append(self._current_row)
                self._current_row = []

    def get_table_contents(self):
        self.close()
        return self._results
