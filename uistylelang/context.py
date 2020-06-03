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



#font-weight

#normal bold 100 200 300 400 500 600 700 800 900 1000

# wx.FONTWEIGHT_THIN
	

# Thin font (weight = 100).

# wx.FONTWEIGHT_EXTRALIGHT
	

# Extra Light (Ultra Light) font (weight = 200).

# wx.FONTWEIGHT_LIGHT
	

# Light font (weight = 300).

# wx.FONTWEIGHT_NORMAL
	

# Normal font (weight = 400).

# wx.FONTWEIGHT_MEDIUM
	

# Medium font (weight = 500).

# wx.FONTWEIGHT_SEMIBOLD
	

# Semi Bold (Demi Bold) font (weight = 600).

# wx.FONTWEIGHT_BOLD
	

# Bold font (weight = 700).

# wx.FONTWEIGHT_EXTRABOLD
	

# Extra Bold (Ultra Bold) font (weight = 800).

# wx.FONTWEIGHT_HEAVY
	

# Heavy (Black) font (weight = 900).

# wx.FONTWEIGHT_EXTRAHEAVY
	

# Extra Heavy font (weight = 1000).

# wx.FONTWEIGHT_MAX



# This contains wxPython PseudoDC-specific code
# For consistency with the wxPython methods, title-case is used in this file


import copy

import wx
import wx.adv

from .lang import UIStyleLangParser


DEFAULT_PROPERTIES = {
    "color": "transparent",
    "background-color": "transparent",
    "border-radius": "0px",
    "border-width": "0px",
    "border-color": "transparent",
    "top": "0px",
    "left": "0px",
    "width": "0px",
    "height": "0px",
    "color": "black",
    "font-size": "regular",
    "font-weight": "normal", # light, normal, semibold, bold
    "font-style": "normal", # normal, italic
    "background": "transparent"
}





class ShapeID(object):
    def __init__(self, _id):
        self.uisl_id = _id
        self.wx_id = wx.NewIdRef()

    def GetId(self):
        return self.uisl_id

    def GetWxId(self):
        return self.wx_id

class TextID(object):
    def __init__(self, _id, text="default"):
        self.uisl_id = _id
        self.wx_id = wx.NewIdRef()
        self.text = text

    def GetId(self):
        return self.uisl_id

    def GetWxId(self):
        return self.wx_id

    def GetText(self):
        return self.text

    def SetText(self, text):
        self.text = text


class UIStylePDC(wx.adv.PseudoDC):
    def __init__(self, parent, file):
        wx.adv.PseudoDC.__init__(self)


        self.parent_window = parent

        self.raw_stylesheet = self.ReadRawFile(file)
        self.lang_parser = UIStyleLangParser(self.GetRawStyleSheet())
        self.sdc_shape_style_ids = {}
        self.sdc_text_style_ids = {}
        self.current_styles = {}# = DEFAULT_PROPERTIES

        self.InitContext()

    
    def ReadRawFile(self, raw_file):
        """ Reads the raw file from the system.
        Supports .CSS and .UISS stylesheets
        """

        if raw_file.endswith(".css") or raw_file.endswith(".uiss"):
            raw_text = open(raw_file, "r").read()
            return raw_text

        else:
            msg = 'Invalid file type! Only .uiss and .css filetype extensions are supported.'
            raise Exception(msg)

        
        


    def InitContext(self):


        # Create the id objects
        for _id in self.ParsedStyles:
            print(_id, "...")
            if _id.endswith("-text"):

                obj = TextID(_id)
                self.sdc_text_style_ids[_id] = obj
            else:
                obj = ShapeID(_id)
                self.sdc_shape_style_ids[_id] = obj

            self.current_styles[obj.GetWxId()] = DEFAULT_PROPERTIES

            #print(obj.GetId(), '->', obj.GetWxId())

        #print( self.sdc_shape_style_ids)


    def GetRawStyleSheet(self):
        return self.raw_stylesheet

    def GetLangParser(self):
        return self.lang_parser

    @property
    def ParsedStyles(self):
        styles = self.lang_parser.parse()
        return styles

    def GetParsedInlineStyles(self, _id):#REMOVE
        styles = self.lang_parser.parse_inline(_id)
        return styles


    def HandleStylesDict(self, _id, css_style):
        # Make a copy so that we don't overwrite
        styles_dict = copy.copy(self.current_styles[_id])

        # Merge the css properties. Any css styles that are not 
        # specified will automatically be the default ones.
        for css_property in css_style:
            #print(css_property)
            styles_dict[css_property] = css_style[css_property]

        # At this point, set the current styles to be the new styles 
        self.current_styles[_id] = styles_dict
        return styles_dict


    def DrawShapeStyles(self, _id):
        
        styles = self.ParsedStyles[_id]
        style_id_obj = self.sdc_shape_style_ids[_id]
        print('DrawShape')
        self.UpdateShape(style_id_obj.GetWxId(), styles)



    def UpdateShape(self, _id, css_style):
        print(_id, 'update _id' )

        self.ClearId(_id)
        self.SetId(_id)

        styles_dict = self.HandleStylesDict(_id, css_style)

        print(styles_dict, '<___')

        css_color = self.CleanCSSProp(styles_dict["color"]) 
        css_background_color = self.CleanCSSProp(styles_dict["background-color"]) 

        css_border_radius = self.CleanCSSProp(styles_dict["border-radius"]) 
        css_border_width = self.CleanCSSProp(styles_dict["border-width"]) 
        css_border_color = self.CleanCSSProp(styles_dict["border-color"]) 

        css_top = self.CleanCSSProp(styles_dict["top"]) 
        css_left = self.CleanCSSProp(styles_dict["left"]) 
        css_width = self.CleanCSSProp(styles_dict["width"]) 
        css_height = self.CleanCSSProp(styles_dict["height"]) 


        #print("//", css_background_color)
        self.SetPen(wx.Pen(wx.Colour(css_border_color), css_border_width))
        self.SetBrush(wx.Brush(wx.Colour(css_background_color), wx.SOLID))

        if css_border_radius > 0:
            if css_width == css_height and css_border_radius == css_height/2:
                # Correct the coordinates so that the circle's "corner" is 
                # placed at the css_top and css_left position
                half = css_width/2
                self.DrawCircle(css_top+half, css_left+half, css_border_radius)
            else:
                self.DrawRoundedRectangle(css_top, css_left, css_width, css_height, css_border_radius)

            
        else:
            self.DrawRectangle(css_top, css_left, css_width, css_height)


    def DrawTextStyles(self, _id, text=""):
        styles = self.ParsedStyles[_id]
        style_id_obj = self.sdc_text_style_ids[_id]
        print('DrawText')
        style_id_obj.SetText(text)
        self.UpdateText(style_id_obj.GetWxId(), text, styles)


    def UpdateText(self, _id, text, styles):

        self.ClearId(_id)
        self.SetId(_id)

        styles_dict = self.HandleStylesDict(_id, styles)


        css_color = self.CleanCSSProp(styles_dict["color"]) 
        css_background = self.CleanCSSProp(styles_dict["background"]) 

        css_top = self.CleanCSSProp(styles_dict["top"]) 
        css_left = self.CleanCSSProp(styles_dict["left"]) 

        css_font_weight = self.CleanCSSProp(styles_dict["font-weight"]) 
        css_font_style = self.CleanCSSProp(styles_dict["font-style"]) 

        fnt = self.parent_window.GetFont()

        #MakeItalic MakeLarger MakeSmaller MakeStrikethrough MakeUnderlined Scaled


        
        if css_font_weight == "bold":
            fnt.SetWeight(wx.FONTWEIGHT_BOLD)



        if css_font_style == "normal":
            fnt.SetStyle(wx.FONTSTYLE_NORMAL)

        elif css_font_style == "italic":
            fnt.SetStyle(wx.FONTSTYLE_ITALIC)


        self.SetFont(fnt)
        self.SetTextForeground(wx.Colour(css_color))
        self.SetTextBackground(wx.Colour(css_background))
        self.DrawText(text, css_top, css_left)


    def CleanCSSProp(self, css_prop):
        #print('type:', css_prop, type(css_prop))
        if css_prop == type(int):
            cleaned_css_prop = css_prop
        elif css_prop.endswith("px"):
            # Remove the "px" on the end and 
            # convert to the proper type.
            if "." in css_prop:
                cleaned_css_prop = float(css_prop[:-2])
            else:
                cleaned_css_prop = int(css_prop[:-2])
        else:
            cleaned_css_prop = css_prop

        return cleaned_css_prop


    def UpdateShapeStyles(self, _id, styles=""):

        style_id_obj = self.sdc_shape_style_ids[_id]
        #print(style_id_obj.GetId())

        css_style = self.lang_parser.parse_inline(styles)

        #print(css_style, "<<<<<<<<------")

        self.UpdateShape(style_id_obj.GetWxId(), css_style)


    def UpdateTextStyles(self, _id, text="", styles=""):

        style_id_obj = self.sdc_text_style_ids[_id]
        #print(style_id_obj.GetId())

        css_style = self.lang_parser.parse_inline(styles)

        #print(css_style, "<<<<<<<<------")

        if text == "":
            text = style_id_obj.GetText()
        else:
            style_id_obj.SetText(text)
            
        self.UpdateText(style_id_obj.GetWxId(), text, css_style)

        #style = #self.GetParsedInlineStyles(style_id_obj.GetId())
        #print(style)
        
            

