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


# This contains wxPython PseudoDC-specific code
# For consistency with the wxPython methods, title-case is used in this file


import copy

import wx
import wx.adv

from .lang import UIStyleLangParser


DEFAULT_PROPERTIES = {
    "color": "transparent",
    "background": "transparent",
    "background-color": "transparent",
    "border-radius": "0px",
    "border-width": "0px",
    "border-color": "transparent",
    "top": "0px",
    "left": "0px",
    "width": "0px",
    "height": "0px",
    "font-size": "medium",
    "font-weight": "normal",
    "font-style": "normal",
    "text-decoration": "none",
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


class ImageID(object):
    def __init__(self, _id, path=""):
        self.uisl_id = _id
        self.wx_id = wx.NewIdRef()
        self.image_path = path

    def GetId(self):
        return self.uisl_id

    def GetWxId(self):
        return self.wx_id

    def GetPath(self):
        return self.image_path

    def SetPath(self, path):
        self.image_path = path


class UIStylePDC(wx.adv.PseudoDC):
    def __init__(self, parent, file):
        wx.adv.PseudoDC.__init__(self)

        self.parent_window = parent
        self.raw_stylesheet = self.ReadRawFile(file)
        self.lang_parser = UIStyleLangParser(self.GetRawStyleSheet())
        self.sdc_shape_style_ids = {}
        self.sdc_text_style_ids = {}
        self.sdc_image_style_ids = {}
        self.current_styles = {}

        self._InitDeviceContext()

    
    def _InitDeviceContext(self):
        for _id in self.ParsedStyles:
            # Set the style type
            try:
                style_type = self.ParsedStyles[_id]["type"]
            except KeyError:
                # Default to "shape"
                style_type = self.ParsedStyles[_id]["type"] = "shape"
               
            #print(_id, "->", style_type)

            # Create the id objects
            if style_type == "text":
                obj = TextID(_id)
                self.sdc_text_style_ids[_id] = obj

            elif style_type == "image":
                obj = ImageID(_id)
                self.sdc_image_style_ids[_id] = obj

            else:
                obj = ShapeID(_id)
                self.sdc_shape_style_ids[_id] = obj

            #print(obj.GetId(), '->', obj.GetWxId())

            # The style type is obviously not saved here
            self.current_styles[obj.GetWxId()] = DEFAULT_PROPERTIES

    def _MergeParsedStyles(self, _id, styles):
        # Make a copy so that we don't overwrite
        styles_dict = copy.copy(self.current_styles[_id])

        # Merge the UI Style Lang properties. Any styles that are not 
        # specified will automatically be the default ones.
        for prop in styles:
            styles_dict[prop] = styles[prop]

        # At this point, set the current styles to be the new styles 
        self.current_styles[_id] = styles_dict
        return styles_dict

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


    def GetRawStyleSheet(self):
        return self.raw_stylesheet

    def GetLangParser(self):
        return self.lang_parser

    @property
    def ParsedStyles(self):
        styles = self.lang_parser.parse()
        return styles

    def CleanProperty(self, prop):
        return self.lang_parser.clean_property(prop)


    def InitShapeStyles(self, _id):
        """ Draws the shape with the same id declared in the stylesheet. This can be thought of like the following pseudo-HTML: *<div class="{{_id}}"></div>*

        :param str _id: id to draw (must be already declared in the intial stylesheet)
        """
        styles = self.ParsedStyles[_id]
        style_id_obj = self.sdc_shape_style_ids[_id]
        self.UpdateShape(style_id_obj.GetWxId(), styles)
        #print('-> DrawShape')


    def InitTextStyles(self, _id, text=""):
        """ Draws the text with the same id declared in the stylesheet. This can be thought of like the following pseudo-HTML: *<p class="{{_id}}">{{text}}</p>*

        :param str _id: id to draw (must be already declared in the intial stylesheet)
        :param str text: text to be drawn and displayed
        """
        styles = self.ParsedStyles[_id]
        style_id_obj = self.sdc_text_style_ids[_id]
        style_id_obj.SetText(text)
        self.UpdateText(style_id_obj.GetWxId(), text, styles)
        #print('-> DrawText')


    def UpdateShape(self, _id, styles):
        self.ClearId(_id)
        self.SetId(_id)

        styles_dict = self._MergeParsedStyles(_id, styles)

        # Define styles 
        uiss_background_color = self.CleanProperty(styles_dict["background-color"]) 

        uiss_border_radius = self.CleanProperty(styles_dict["border-radius"]) 
        uiss_border_width = self.CleanProperty(styles_dict["border-width"]) 
        uiss_border_color = self.CleanProperty(styles_dict["border-color"]) 

        uiss_top = self.CleanProperty(styles_dict["top"]) 
        uiss_left = self.CleanProperty(styles_dict["left"]) 
        uiss_width = self.CleanProperty(styles_dict["width"]) 
        uiss_height = self.CleanProperty(styles_dict["height"]) 

        # Use styles
        self.SetPen(wx.Pen(wx.Colour(uiss_border_color), uiss_border_width))
        self.SetBrush(wx.Brush(wx.Colour(uiss_background_color), wx.SOLID))

        if uiss_border_radius > 0:
            if uiss_width == uiss_height and uiss_border_radius == uiss_height/2:
                # Correct the coordinates so that the circle's "corner" is 
                # placed at the uiss_top and uiss_left position
                half = uiss_width/2
                self.DrawCircle(uiss_top+half, uiss_left+half, uiss_border_radius)
            else:
                self.DrawRoundedRectangle(uiss_top, uiss_left, uiss_width, uiss_height, uiss_border_radius)

        else:
            self.DrawRectangle(uiss_top, uiss_left, uiss_width, uiss_height)


    def UpdateText(self, _id, text, styles):

        self.ClearId(_id)
        self.SetId(_id)

        styles_dict = self._MergeParsedStyles(_id, styles)

        # Define styles
        uiss_color = self.CleanProperty(styles_dict["color"]) 
        uiss_background = self.CleanProperty(styles_dict["background"]) 
        uiss_text_decoration = self.CleanProperty(styles_dict["text-decoration"])

        uiss_top = self.CleanProperty(styles_dict["top"]) 
        uiss_left = self.CleanProperty(styles_dict["left"]) 

        uiss_font_weight = self.CleanProperty(styles_dict["font-weight"]) 
        uiss_font_style = self.CleanProperty(styles_dict["font-style"]) 
        uiss_font_size = self.CleanProperty(styles_dict["font-size"])

        # Use styles
        fnt = self.parent_window.GetFont()

        # Text decoration
        if uiss_text_decoration == "underline":
            fnt.MakeUnderlined()

        # Font size
        if uiss_font_size == "medium":
            pass

        elif uiss_font_size == "smaller":
            fnt.MakeSmaller()

        elif uiss_font_size == "larger":
            fnt.MakeLarger()

        # Font weight
        if uiss_font_weight in ["normal", "400"]:
            fnt.SetWeight(wx.FONTWEIGHT_NORMAL)

        elif uiss_font_weight in ["bold", "700"]:
            fnt.SetWeight(wx.FONTWEIGHT_BOLD)

        elif uiss_font_weight == "100":
            fnt.SetWeight(wx.FONTWEIGHT_THIN)

        elif uiss_font_weight == "200":
            fnt.SetWeight(wx.FONTWEIGHT_EXTRALIGHT)

        elif uiss_font_weight == "300":
            fnt.SetWeight(wx.FONTWEIGHT_LIGHT)

        elif uiss_font_weight == "500":
            fnt.SetWeight(wx.FONTWEIGHT_MEDIUM)

        elif uiss_font_weight == "600":
            fnt.SetWeight(wx.FONTWEIGHT_SEMIBOLD)

        elif uiss_font_weight == "800":
            fnt.SetWeight(wx.FONTWEIGHT_EXTRABOLD)

        elif uiss_font_weight == "900":
            fnt.SetWeight(wx.FONTWEIGHT_HEAVY)

        elif uiss_font_weight == "1000":
            fnt.SetWeight(wx.FONTWEIGHT_EXTRAHEAVY)

        # Font style
        if uiss_font_style == "normal":
            fnt.SetStyle(wx.FONTSTYLE_NORMAL)

        elif uiss_font_style == "italic":
            fnt.SetStyle(wx.FONTSTYLE_ITALIC)

        self.SetFont(fnt)
        self.SetTextForeground(wx.Colour(uiss_color))
        self.SetTextBackground(wx.Colour(uiss_background))
        self.DrawText(text, uiss_top, uiss_left)


    def UpdateShapeStyles(self, _id, styles=""):
        """ Updates and draws the shape with the same id declared in the stylesheet. This can be thought of like the following pseudo-HTML: *<div class="{{_id}}" style="{{styles}}"></div>*

        :param str _id: id to draw (must be already declared in the intial stylesheet)
        :param str styles: inline styles to update and override style properties of the shape
        """
        style_id_obj = self.sdc_shape_style_ids[_id]
        #print(style_id_obj.GetId())
        uiss_style = self.lang_parser.parse_inline(styles)
        self.UpdateShape(style_id_obj.GetWxId(), uiss_style)


    def UpdateTextStyles(self, _id, text="", styles=""):
        """ Updates and draws the text with the same id declared in the stylesheet. This can be thought of like the following pseudo-HTML: *<p class="{{_id}}" style="{{styles}}">{{text}}</p>*

        :param str _id: id to draw (must be already declared in the intial stylesheet)
        :param str text: update and override the text to be drawn and displayed
        :param str styles: inline styles to update and override style properties of the text
        """
        style_id_obj = self.sdc_text_style_ids[_id]
        #print(style_id_obj.GetId())
        uiss_style = self.lang_parser.parse_inline(styles)

        if text == "":
            text = style_id_obj.GetText()
        else:
            style_id_obj.SetText(text)
            
        self.UpdateText(style_id_obj.GetWxId(), text, uiss_style)
