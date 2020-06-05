# Demo for UI Style Lang
# ======================

# This demo file (demo.py) is MIT licensed - (C) 2020 Noah Rahm, Correct Syntax

# Usage:
# Run the demo and click the right and left mouse buttons back and forth
# to see the styles change.

# TODO:
# Comments!!!

import random

import wx

from uistylelang import UIStylePDC


class MainApplication(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="UI Style Lang Demo",
                          pos=(0, 0), size=(1000, 800))

        # Create the DC
        self._pdc = UIStylePDC(
            self,
            './demo-styles.uiss'# Change file to .css for different styles!
            ) 

        self.DrawDrawing(self._pdc)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)


    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)

        # We need to clear the dc BEFORE calling PrepareDC.
        dc.SetBackground(wx.Brush(wx.Colour('#ECECEC')))
        dc.Clear()

        # Draw to the dc using the calculated clipping rect.
        self._pdc.DrawToDCClipped(
            dc, wx.Rect(0, 0, self.Size[0], self.Size[1])
            )


    def OnLeftDown(self, event):
        self._pdc.UpdateShapeStyles('rect', styles="background-color: blue;")

        self._pdc.UpdateTextStyles('black-text', text="Hello there!")

        self._pdc.UpdateShapeStyles('grey-box',
                                    styles="background-color: red; top: 300px; left: 50px;"
                                    )
        self.RefreshDemo()

    def OnRightDown(self, event):
        self._pdc.UpdateShapeStyles('rect', styles="background-color: pink;")

        self._pdc.UpdateTextStyles('black-text', styles="color: black;")

        # Showing off the inline style abilities here...
        styles = """
        border-width: {0}px;
        background-color: white;
        top: {1}px;
        left: {2}px;
        border-color: black;
        """.format(
            random.randint(1, 3),
            random.randint(1, 500),
            random.randint(1, 300)
            )
        
        self._pdc.UpdateShapeStyles('grey-box', styles=styles)

        self._pdc.UpdateTextStyles('black-text', styles="color: red; text-decoration: underline; font-size: larger; font-style: italic; font-weight: bold;")
        self.RefreshDemo()

    def DrawDrawing(self, dc):

        # Initial
        dc.InitShapeStyles('grey-box')
        dc.InitShapeStyles('rect')
        dc.InitTextStyles('black-text', text="UI Style Lang Demo")

        # Change styles
        dc.UpdateShapeStyles('rect', styles="border-color: blue; border-width: 3px;")


    def RefreshDemo(self):
        rect = wx.Rect(0, 0, self.Size[0], self.Size[1])
        self.RefreshRect(rect, False)
        self.Refresh()




if __name__ == '__main__':
    # Create the app and startup
    app = wx.App(redirect=False)
    frame = MainApplication()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()
