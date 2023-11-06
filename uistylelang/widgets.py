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


# This contains wxPython Widget-specific code
# For consistency with the wxPython methods, title-case is used in this file

import wx

from .lang import UIStyleLangParser
from .utils import ReadRawFile, MergeParsedStyles


class UIStyleApp(wx.App):
    """ Wrapper of ``wx.App`` 
    
    :param file: path to stylesheet for the Native Widget API styling

    Please refer to the wxPython docs for the rest of the params.
    """
    def __init__(self, file, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

        self.raw_stylesheet = ReadRawFile(file)
        self.lang_parser = UIStyleLangParser(self.GetRawStyleSheet())
        
    def GetRawStyleSheet(self):
        return self.raw_stylesheet
    
    @property
    def ParsedStyles(self):
        styles = self.lang_parser.parse()
        return styles


class UIStyleFrame(wx.Frame):
    """ Wrapper of ``wx.Frame`` 

    Supported properties: ``background-color``
    """
    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, name="frame"):
        wx.Frame.__init__(self, parent, id, title, pos, size, style, name)
        
        self.default_properties = {
            "background-color": "transparent",
            }
        self.current_styles = self.default_properties

        try:
            self.ConfigureStyle()
        except KeyError:
            print(
"""UISTYLELANG: Styling was not declared for the UIStyleFrame with the id of '{}'.
Please declare it in the stylesheet.""".format(self.GetName())
)
        except Exception as error:
            print(error)
        
    def CleanProperty(self, prop):
        return wx.GetApp().lang_parser.clean_property(prop)
    
    def ConfigureStyle(self):
        """ Configures the styling of the frame. 

        :returns: a boolean value of whether the styling could be applied.
        """ 
        styles_dict = MergeParsedStyles(
            self.GetName(),
            wx.GetApp().ParsedStyles,
            self.current_styles
            )
        
        uiss_background_color = self.CleanProperty(styles_dict["background-color"])

        return self.SetBackgroundColour(wx.Colour(uiss_background_color))
        
        
class UIStylePanel(wx.Panel):
    """ Wrapper of ``wx.Panel`` 

    Supported properties: ``background-color``
    """
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, 
            size=wx.DefaultSize, style=wx.TAB_TRAVERSAL | wx.NO_BORDER, name="panel"):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)
 
        self.default_properties = {
            "background-color": "transparent",
            }
        self.current_styles = self.default_properties
        
        try:
            self.ConfigureStyle()
        except KeyError:
            print(
"""UISTYLELANG: Styling was not declared for the UIStylePanel with the id of '{}'.
Please declare it in the stylesheet.""".format(self.GetName())
)
        except Exception as error:
            print(error)
        
    def CleanProperty(self, prop):
        return wx.GetApp().lang_parser.clean_property(prop)
    
    def ConfigureStyle(self):
        """ Configures the styling of the panel. 

        :returns: a boolean value of whether the styling could be applied.
        """
        
        styles_dict = MergeParsedStyles(
            self.GetName(),
            wx.GetApp().ParsedStyles,
            self.current_styles
            )
        
        uiss_background_color = self.CleanProperty(styles_dict["background-color"])
        return self.SetBackgroundColour(wx.Colour(uiss_background_color))
  

class UIStyleStaticText(wx.StaticText):
    """ Wrapper of ``wx.StaticText`` 

    Supported properties: ``background-color``, ``color``
    """
    def __init__(self, parent, id=-1, label="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name="static-text"):
        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)

        self.default_properties = {
            "background-color": "transparent",
            "color": "transparent",
            }
        self.current_styles = self.default_properties
        
        try:
            self.ConfigureStyle()
        except KeyError:
            print(
"""UISTYLELANG: Styling was not declared for the UIStyleStaticText with the id of '{}'.
Please declare it in the stylesheet.""".format(self.GetName())
)
        except Exception as error:
            print(error)
        
    def CleanProperty(self, prop):
        return wx.GetApp().lang_parser.clean_property(prop)

    def ConfigureStyle(self):
        """ Configures the styling of the static text. """
        
        styles_dict = MergeParsedStyles(
            self.GetName(),
            wx.GetApp().ParsedStyles,
            self.current_styles
            )
        
        uiss_background_color = self.CleanProperty(styles_dict["background-color"])
        uiss_color = self.CleanProperty(styles_dict["color"])

        self.SetBackgroundColour(wx.Colour(uiss_background_color))
        self.SetForegroundColour(wx.Colour(uiss_color))