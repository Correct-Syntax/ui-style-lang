# UI Style Lang Copyright 2020-2023 Noah Rahm

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

# Utility functions
# For consistency with the wxPython methods, title-case is used in this file

import copy


def ReadRawFile(raw_file):
    """ Reads the raw file from the system. If the comment-header is 
    declared, the ``raw_file`` param will be treated as a string.

    String example with comment-header:

        /* !uistylelangstr */
        
        .button {
          background-color: white;
        }

        ...

    Supports .CSS and .UISS stylesheets
    """ 
    # Whether there is a line break before the 
    # header or not we accept it.
    if raw_file.startswith("/* !uistylelangstr */"): 
        return raw_file
    
    elif raw_file.startswith("\n/* !uistylelangstr */"):
        return raw_file

    # Only accept .css or .uiss files
    elif raw_file.endswith(".css") or raw_file.endswith(".uiss"):
        raw_text = open(raw_file, "r").read()
        return raw_text

    else:
        msg = """Invalid file type or string formatting!
        Possible solutions:
        1. Only .uiss and .css filetype extensions are supported.
        2. String must start with the /* !uistylelangstr */ comment-header. """
        raise Exception(msg)


def MergeParsedStyles(_id, styles, current_styles):
    """ Merge new styles and the current styles dicts.
    
    :param str _id: element id to merge styles for
    :param str styles: new styles to merge with the current styles
    :param str current_styles: current styles to merge with the new styles
    """
    # Make a copy so that we don't overwrite
    styles_dict = copy.copy(current_styles)

    # Merge the UI Style Lang properties. Any styles that are not 
    # specified will automatically be the default ones.
    for prop in styles[_id]["init"]:
        styles_dict[prop] = styles[_id]["init"][prop]

    # At this point, set the current styles to be the new styles 
    current_styles[_id] = styles_dict
    return styles_dict
