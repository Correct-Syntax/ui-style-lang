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
from .utils import ReadRawFile


# Note: "type" gets set on runtime; no need to put it in here
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
    "transform-rotate": "0deg",
    "text-transform": "none",
}



class ShapeID(object):
    """ Represents a shape element. """
    def __init__(self, _id):
        self.uisl_id = _id
        self.wx_id = wx.NewIdRef()
        self.rect = wx.Rect(0, 0, 0, 0)

    def GetId(self):
        return self.uisl_id

    def GetWxId(self):
        return self.wx_id

    def SetRect(self, rect):
        self.rect = rect

    def GetRect(self):
        return self.rect


class TextID(object):
    """ Represents a text element. """
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
    """ Represents an image element. """
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
        self.raw_stylesheet = ReadRawFile(file)
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
        """ Merge new styles and the current styles dicts.
        
        :param str _id: element id to merge styles for
        :param str styles: new styles to merge with the current styles
        """
        # Make a copy so that we don't overwrite
        styles_dict = copy.copy(self.current_styles[_id])

        # Merge the UI Style Lang properties. Any styles that are not 
        # specified will automatically be the default ones.
        for prop in styles:
            styles_dict[prop] = styles[prop]

        # At this point, set the current styles to be the new styles 
        self.current_styles[_id] = styles_dict
        return styles_dict
    
    def GetRawStyleSheet(self):
        return self.raw_stylesheet

    def GetLangParser(self):
        return self.lang_parser

    def GetWXId(self, _id, style_type="shape"):
        """ Returns the assigned wxPython id of the element. Useful for 
        situations when you need to mess with the wxPython ids yourself.

        :param str _id: id to of the element (must be already declared in 
        the intial stylesheet)
        :param str style_type: type of the element - can be one of: text, image, shape
        """
        if style_type == "text":
            id_obj = self.sdc_text_style_ids[_id]
        elif style_type == "image":
            id_obj = self.sdc_image_style_ids[_id]
        else:
            id_obj = self.sdc_shape_style_ids[_id]

        return id_obj.GetWxId()


    def GetWXRect(self, _id, style_type="shape"):
        """ Get the wxPython Rect of the element.

        :param str _id: id to of the element (must be already declared in 
        the intial stylesheet)
        :param str style_type: type of the element - can be one of: text, image, shape
        
        :returns: `wx.Rect`
        """
        if style_type == "text":
            id_obj = self.sdc_text_style_ids[_id]
        elif style_type == "image":
            id_obj = self.sdc_image_style_ids[_id]
        else:
            id_obj = self.sdc_shape_style_ids[_id]

        return id_obj.GetRect()

    @property
    def ParsedStyles(self):
        styles = self.lang_parser.parse()
        return styles

    def CleanProperty(self, prop):
        return self.lang_parser.clean_property(prop)


    def InitShapeStyles(self, _id):
        """ Draws the shape with the same id declared in the 
        stylesheet. This can be thought of like the following 
        pseudo-HTML: *<div class="{{_id}}"></div>*

        :param str _id: id to draw (must be already declared in 
        the intial stylesheet)
        """
        styles = self.ParsedStyles[_id]
        style_id_obj = self.sdc_shape_style_ids[_id]
        self.UpdateShape(style_id_obj.GetWxId(), style_id_obj, styles)


    def InitTextStyles(self, _id, text=""):
        """ Draws the text with the same id declared in the 
        stylesheet. This can be thought of like the following 
        pseudo-HTML: *<p class="{{_id}}">{{text}}</p>*

        :param str _id: id to draw (must be already declared in 
        the intial stylesheet)
        :param str text: text to be drawn and displayed
        """
        styles = self.ParsedStyles[_id]
        style_id_obj = self.sdc_text_style_ids[_id]
        style_id_obj.SetText(text)
        self.UpdateText(style_id_obj.GetWxId(), text, styles)


    def InitImageStyles(self, _id, img_path=""):
        """ Draws the image with the same id declared in the 
        stylesheet. This can be thought of like the following 
        pseudo-HTML: *<img class="{{_id}}" src="{{img_path}}">*

        :param str _id: id to draw (must be already declared in 
        the intial stylesheet)
        :param str img_path: path of the image to be drawn and displayed
        """
        styles = self.ParsedStyles[_id]
        style_id_obj = self.sdc_image_style_ids[_id]
        style_id_obj.SetPath(img_path)
        self.UpdateImage(style_id_obj.GetWxId(), img_path, styles)


    def UpdateShape(self, _id, id_obj, styles):
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

        # Set the rect of the element
        id_obj.SetRect(wx.Rect(uiss_left, uiss_top, uiss_width, uiss_height))

        # Use styles
        self.SetPen(wx.Pen(wx.Colour(uiss_border_color), uiss_border_width))
        self.SetBrush(wx.Brush(wx.Colour(uiss_background_color), wx.SOLID))

        if uiss_border_radius > 0:
            if uiss_width == uiss_height and uiss_border_radius == uiss_height/2:
                # Correct the coordinates so that the circle's "corner" is 
                # placed at the uiss_top and uiss_left position
                half = uiss_width/2
                self.DrawCircle(uiss_left+half, uiss_top+half, uiss_border_radius)
            else:
                self.DrawRoundedRectangle(
                    uiss_left, uiss_top, uiss_width, uiss_height, uiss_border_radius
                    )

        else:
            self.DrawRectangle(uiss_left, uiss_top, uiss_width, uiss_height)


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

        uiss_transform_rotate = self.CleanProperty(styles_dict["transform-rotate"])
        uiss_text_transform = self.CleanProperty(styles_dict["text-transform"]) 


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

        # Text transform
        if uiss_text_transform == "none":
            text = text # Do nothing

        if uiss_text_transform == "lowercase":
            text = text.lower()

        elif uiss_text_transform == "uppercase":
            text = text.upper()

        elif uiss_text_transform == "capitalize":
            text = text.capitalize()

        if uiss_transform_rotate == 0:
            self.DrawText(text, uiss_left, uiss_top)
        else:
            self.DrawRotatedText(text, uiss_left, uiss_top, uiss_transform_rotate)
            

    def UpdateImage(self, _id, img_path, styles):
        self.ClearId(_id)
        self.SetId(_id)

        styles_dict = self._MergeParsedStyles(_id, styles)

        # Define styles 
        uiss_top = self.CleanProperty(styles_dict["top"]) 
        uiss_left = self.CleanProperty(styles_dict["left"]) 
        #uiss_width = self.CleanProperty(styles_dict["width"]) 
        #uiss_height = self.CleanProperty(styles_dict["height"]) 

        uiss_transform_rotate = self.CleanProperty(styles_dict["transform-rotate"])

        # Use styles
        image = wx.Image(img_path)

        #if uiss_height != 0 and uiss_width != 0:
        #img_center = wx.Point(uiss_left+(image.GetWidth()/2), uiss_top+(image.GetHeight()/2))
        #print(img_center)
 
        if uiss_transform_rotate > 0:
            #print(uiss_transform_rotate)

            # There could be a bug with this code since it doesn't seem to have
            # the correct rotation all the time.
            image = wx.Image.Rotate(
                image, uiss_transform_rotate, wx.Point(uiss_left, uiss_top)
                )

        bitmap = wx.Image.ConvertToBitmap(image)

        self.DrawBitmap(bitmap, uiss_left, uiss_top, True)


    def UpdateShapeStyles(self, _id, styles=""):
        """ Updates and draws the shape with the same id 
        declared in the stylesheet. This can be thought of like the 
        following pseudo-HTML: *<div class="{{_id}}" style="{{styles}}"></div>*

        :param str _id: id to draw (must be already declared in the intial stylesheet)
        :param str styles: inline styles to update and override style properties of the shape
        """
        style_id_obj = self.sdc_shape_style_ids[_id]
        #print(style_id_obj.GetId())
        uiss_style = self.lang_parser.parse_inline(styles)
        self.UpdateShape(style_id_obj.GetWxId(), style_id_obj, uiss_style)


    def UpdateTextStyles(self, _id, text="", styles=""):
        """ Updates and draws the text with the same id declared 
        in the stylesheet. This can be thought of like the following 
        pseudo-HTML: *<p class="{{_id}}" style="{{styles}}">{{text}}</p>*

        :param str _id: id to draw (must be already declared in the 
        intial stylesheet)
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


    def UpdateImageStyles(self, _id, img_path="", styles=""):
        """ Updates and draws the image with the same id declared in the 
        stylesheet. This can be thought of like the following 
        pseudo-HTML: *<img class="{{_id}}" src="{{img_path}}" style="{{styles}}">*

        :param str _id: id to draw (must be already declared in the intial stylesheet)
        :param str img_path: update and override the image path to be drawn and displayed
        :param str styles: inline styles to update and override style properties of the image
        """
        style_id_obj = self.sdc_image_style_ids[_id]
        #print(style_id_obj.GetId())
        uiss_style = self.lang_parser.parse_inline(styles)

        if img_path == "":
            img_path = style_id_obj.GetPath()
        else:
            style_id_obj.SetPath(img_path)
            
        self.UpdateImage(style_id_obj.GetWxId(), img_path, uiss_style)
