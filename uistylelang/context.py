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


# This contains wxPython PseudoDC-specific code
# For consistency with the wxPython methods, title-case is used in this file


# HOW THIS WORKS:

# PDC Init
# 1. Creates the Element objects from the parsed stylesheet data
# * Each style set is accessible via the id selector and pseudo id selectors
# 2. Assigns a wxPython id and the declared id selector and pseudo id selectors

# Elem Init
# 1. The element is updated with a type hint, content and styles
# * The type hint tells the context draw method what to treat the element as
# 2. The element is drawn

# Elem Update
# 1. Gets the id selector and pseudo id selector (e.g: 'elem:active')
# 2. Get any updates to the image file path, text, inline styles, etc.
# 3. Inline styles get added to/merged with the current styles
# 4. The element is drawn

# You can now call:
# >> dc.InitElem('elem')
# >> dc.UpdateElem('elem:active', styles="background-color: red;")


import copy

import wx
import wx.adv

from .lang import UIStyleLangParser
from .utils import ReadRawFile


# Note: "type" gets set on runtime; no need to put it in here
SUPPORTED_PROPERTIES = {
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


class Element(object):
    """ Represents an abstract element object drawn on the DC. """
    def __init__(self, elem_id):
        self.id_selector = elem_id
        self.wx_id = wx.NewIdRef()
        self.elem_type = "SHAPE"
        self.current_styles = {}
        self.rect = wx.Rect(0, 0, 0, 0)
        self.content = "" # holds file path/text values

    def InitStyles(self, styles):
        self.current_styles = styles
        for pseudo_id in self.current_styles:
            for prop in SUPPORTED_PROPERTIES.keys():
                if prop not in self.current_styles[pseudo_id].keys():
                    self.current_styles[pseudo_id][prop] = copy.copy(SUPPORTED_PROPERTIES[prop])

    def GetId(self):
        return self.id_selector

    def GetWxId(self):
        return self.wx_id

    def SetType(self, elem_type):
        if elem_type in ["SHAPE", "TEXT", "IMAGE"]:
            self.elem_type = elem_type
        else:
            raise RuntimeError("Invalid element type. Must be one of: SHAPE, TEXT, IMAGE") 

    def GetType(self):
        if self.elem_type != "":
            return self.elem_type
        else:
            raise RuntimeError("Element was not initilized with the 'InitElem' method!")

    def SetStyles(self, styles):
        self.current_styles = styles

    def GetStyles(self, pseudo_id=""):
        if pseudo_id == "":
            return self.current_styles
        return self.current_styles[pseudo_id]

    def SetRect(self, rect):
        self.rect = rect

    def GetRect(self):
        return self.rect

    def SetContent(self, content=""):
        if content != "":
            self.content = content

    def GetContent(self):
        return self.content

    def MergeStyles(self, pseudo_id, new_styles):
        """ Merge new styles and the current styles.
        
        :param pseudo_id: pseudo id of this element of which to update with the new styles
        :param new_styles: new styles to merge with the current styles
        """

        if new_styles != "":
            # We only apply styles to this pseudo-id selector
            for prop in new_styles:
                # Make a copy so that we don't overwrite
                new_prop_val = copy.copy(new_styles[prop])

                # Merge the UI Style Lang properties. Any styles that are not 
                # specified will automatically be the default ones.
                self.current_styles[pseudo_id][prop] = new_prop_val


class UIStylePDC(wx.adv.PseudoDC):
    def __init__(self, parent, file):
        wx.adv.PseudoDC.__init__(self)

        self._parent_window = parent
        self._raw_stylesheet = ReadRawFile(file)
        self._lang_parser = UIStyleLangParser(self.GetRawStyleSheet())
        self._parsed_styles_data = self.LangParser.parse()
        self._uisl_elements = {}

        self._InitDeviceContext()

    def _InitDeviceContext(self):
        """ Create Element objects for each element declared in the stylesheet and assign the parsed styles to them.

        For internal use only.
        """
        for id_selector in self.ParsedStyles:

            styles = self.ParsedStyles[id_selector]
            elem = Element(id_selector)
            elem.InitStyles(styles)
            self._uisl_elements[id_selector] = elem
 
    def GetRawStyleSheet(self):
        return self._raw_stylesheet

    @property
    def ParsedStyles(self):
        return self._parsed_styles_data

    @property
    def LangParser(self):
        return self._lang_parser

    def CleanProperty(self, prop):
        return self.LangParser.clean_property(prop)


    def GetWxRect(self, elem_id):
        """ Get the wxPython Rect of the element.

        :param str elem_id: id to of the element (must be already declared in the intial stylesheet)
        :returns: `wx.Rect`
        """
        elem = self._uisl_elements[elem_id]

        return elem.GetRect()

    def GetWxId(self, elem_id):
        """ Returns the assigned wxPython id of the element. Useful for situations when you need to mess with the wxPython ids yourself.

        :param str elem_id: id to of the element (must be already declared in the intial stylesheet)
        :returns: `wx.IdRef`
        """
        elem = self._uisl_elements[elem_id]

        return elem.GetWxId()

    def DrawElem(self, elem_id, pseudo_id):
        """ Draws the current element on the PDC. """
        elem = self._uisl_elements[elem_id]
        wx_id = elem.GetWxId()

        self.ClearId(wx_id)
        self.SetId(wx_id)

        #print(elem.GetStyles(pseudo_id))

        try:
            styles_dict = copy.copy(elem.GetStyles(pseudo_id))
        except KeyError:
            raise RuntimeError("Invalid psuedo selector, '{}'".format(pseudo_id))

        elem_type = elem.GetType()
        elem_content = elem.GetContent()

        # Clean property values
        for prop in styles_dict:
            styles_dict[prop] = self.CleanProperty(styles_dict[prop])

        # Define styles 
        uiss_background_color = styles_dict["background-color"] 
        uiss_color = styles_dict["color"] 
        uiss_background = styles_dict["background"] 
        uiss_border_radius = styles_dict["border-radius"] 
        uiss_border_width = styles_dict["border-width"]
        uiss_border_color = styles_dict["border-color"]
        uiss_top = styles_dict["top"]
        uiss_left = styles_dict["left"]
        uiss_width = styles_dict["width"] 
        uiss_height = styles_dict["height"] 
        uiss_text_decoration = styles_dict["text-decoration"]
        uiss_font_weight = styles_dict["font-weight"]
        uiss_font_style = styles_dict["font-style"]
        uiss_font_size = styles_dict["font-size"]
        uiss_transform_rotate = styles_dict["transform-rotate"]
        uiss_text_transform = styles_dict["text-transform"] 

        # Set the rect of the element
        elem.SetRect(wx.Rect(uiss_left, uiss_top, uiss_width, uiss_height))

        # Draw
        if elem_type == "SHAPE":

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


        elif elem_type == "TEXT":
            text = elem_content

            # Use styles
            fnt = self._parent_window.GetFont()

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


        elif elem_type == "IMAGE":
            img_path = elem_content
            image = wx.Image(img_path)

            #if uiss_height != 0 and uiss_width != 0:
            #img_center = wx.Point(uiss_left+(image.GetWidth()/2), uiss_top+(image.GetHeight()/2))
            #print(img_center)
    
            if uiss_transform_rotate > 0:

                image = wx.Image.Rotate(
                    image, uiss_transform_rotate, wx.Point(uiss_left, uiss_top)
                    )

            bitmap = wx.Image.ConvertToBitmap(image)

            self.DrawBitmap(bitmap, uiss_left, uiss_top, True)


    def InitElem(self, id_statement, type_hint="SHAPE", content=""):
        """ Initilizes and draws the element with the same id selector and pseudo-id selector declared in the stylesheet. 

        :param str id_statement: id selector and pseudo-id selector to draw (must be already declared in the intial stylesheet)
        :param str type_hint: one of: ``"SHAPE"``, ``"TEXT"`` or ``"IMAGE"`` hinting to the context what type to treat this element as. Defaults to ``"SHAPE"``.
        :param str content: This could be either text or an image path to override the current text or image path to be drawn and displayed. This must agree with the `type_hint` value. 

        See also: ``UpdateElem``
        """
        ids = self.LangParser.get_statement_ids(id_statement)
        elem = self._uisl_elements[ids[0]]
        elem.SetType(type_hint)
        elem.SetContent(content)
        self.DrawElem(ids[0], ids[1])

 
    def UpdateElem(self, id_statement, content="", styles=""):
        """ Updates and draws the element with the same id selector and pseudo-id selector declared in the stylesheet. 

        Example:

        .. code-block::

            >> dc.InitElem('my-elem', "TEXT", "This is the text to be displayed")
            >> dc.UpdateElem('my-elem:active', content="This is the updated text", styles="color: red;")
        
        These methods together can be thought of as an equivelant to the following pseudo HTML: 
        
        .. code-block::

            <div class="{{ id_statement }}" style="{{ styles }}">{{ content }}</div>


        :param str id_statement: id selector and pseudo-id selector to draw (must be already declared in the intial stylesheet)
        :param str content: This could be either text or an image path to override the current text or image path to be drawn and displayed. This must agree with the `type_hint` value set in `InitElem`. 
        :param str styles: inline styles to update and override style properties of the element. Please note that inline styles WILL overwrite values declared in the intial stylesheet.
        """

        ids = self.LangParser.get_statement_ids(id_statement)
        new_styles = self.LangParser.parse_inline(styles)
        #print("\n style ", new_styles)
        elem = self._uisl_elements[ids[0]]
        elem.SetContent(content)
        elem.MergeStyles(ids[1], new_styles)
        self.DrawElem(ids[0], ids[1])
