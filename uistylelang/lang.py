# UI Style Lang Copyright (c) 2020 Noah Rahm, Correct Syntax.

# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:

#     1. Redistributions of source code must retain the above copyright notice, 
#        this list of conditions and the following disclaimer.
    
#     2. Redistributions in binary form must reproduce the above copyright 
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.

#     3. The names of Noah Rahm, Correct Syntax and any contributers may not be 
#        used to endorse or promote products derived from this software without 
#        specific prior written permission.  

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re


class UIStyleLangParser(object):
    def __init__(self, uislang_str):
        self.uistylelang_str = uislang_str

    def get_lang_string(self):
        return self.uistylelang_str

    def parse(self, styles="", inline=False):
        """ Parses the UI Style Language text and formats the data into a dictionary.
        
        Return format:

            parsed_data = {
                "rect (ID)": {
                    "border-width (PROPERTY)": "1px (VALUE)",
                    "border-color (PROPERTY)": "red (VALUE)",
                }
            }
        """
        parsed_data = {}

        if styles == "":
            uiss_styles = self.get_lang_string()
        else:
            uiss_styles = styles

        token_specification = [
            ('ID', r'@style [A-Za-z\-:]+'), #  Identifiers
            ('BEGIN', r'{'), # Statement begin
            ('PROPERTY', r'[A-Za-z0-9\-]+'), # Properties
            ('VALUE', r': [A-Za-z0-9#\.]+;'), # Property values
            ('END', r'}'), # Statement terminator
            ('NEWLINE', r'\n'), # Line endings
            ('SKIP', r'[ \t]+'), # Skip over spaces and tabs
            ('MISMATCH', r'.'), # Any other (invalid) character
        ]
        
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        line_num = 1
        line_start = 0

        for mo in re.finditer(tok_regex, uiss_styles):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start

            if kind == "NEWLINE":
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise RuntimeError(f'{value!r} unexpected on line {line_num}, column {column}')

            elif kind == "BEGIN":
                pass

            elif kind == "ID":
                if inline == False:
                    # Get the id
                    style_id = value[7:]
                    prop_dict = {} # inner properties

            elif kind == "PROPERTY":
                if inline == False:
                    property_selector = value
                    prop_dict[str(property_selector)] = None
                else:
                    property_selector = value
                    parsed_data[str(property_selector)] = None

            elif kind == "VALUE":
                if inline == False:
                    property_val = value[2:][:-1]
                    prop_dict[str(property_selector)] = property_val
                else:
                    property_val = value[2:][:-1]
                    parsed_data[str(property_selector)] = property_val

            elif kind == "END":
                if inline == False:
                    parsed_data[style_id] = prop_dict

            #print(kind, value, "\n")

        #print(parsed_data, "<<<")
        return parsed_data


    def parse_inline(self, styles):
        """ Parses inline styles of the UI Style Language and formats 
        the data into a dictionary. 

        Return format:

            parsed_data = {
                "border-width (PROPERTY)": "1px (VALUE)",
                "border-color (PROPERTY)": "red (VALUE)",
            }

        """
        return self.parse(styles, inline=True)


    def clean_property(self, uiss_prop):
        """ Cleans the given UI Style Lang property and 
        converts it to the best type.
        """
        if uiss_prop == type(int):
            cleaned_uiss_prop = uiss_prop
        elif uiss_prop.endswith("px"):
            # Remove the "px" on the end and 
            # convert to the proper type.
            if "." in uiss_prop:
                cleaned_uiss_prop = float(uiss_prop[:-2])
            else:
                cleaned_uiss_prop = int(uiss_prop[:-2])

        elif uiss_prop.endswith("deg"):
            # Remove the "deg" on the end and 
            # convert to the proper type.
            cleaned_uiss_prop = float(uiss_prop[:-3]) # Must be a float!

        else:
            cleaned_uiss_prop = uiss_prop

        return cleaned_uiss_prop





if __name__ == "__main__":
    string = """

    @style rect {
      border-radius: 1.5px;
      border-color: red;
    }

    """
    parser = UIStyleLangParser(string)
    parsed_str = parser.parse()
    print(parsed_str)
