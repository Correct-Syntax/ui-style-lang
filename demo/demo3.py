# Demo for UI Style Lang
# ======================

# This demo file (demo3.py) is MIT licensed - (C) 2020 Noah Rahm, Correct Syntax

# Usage:
# It's a custom button...click it!

# This demo is up-to-date


import wx

from uistylelang import UIStylePDC, UIStyleApp, UIStyleFrame


class MainApplication(UIStyleFrame):
    def __init__(self):
        UIStyleFrame.__init__(self, None, title="UI Style Lang Demo", pos=(0, 0), size=(1000, 800), name="main-frame")

        # Create the DC
        self._pdc = UIStylePDC(
            self,
            './custom-widget-demo.uiss'
            ) 

        self.DrawDrawing(self._pdc)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)


    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc = wx.GCDC(dc)

        # We need to clear the dc BEFORE calling PrepareDC.
        dc.Clear()

        # Draw to the dc using the calculated clipping rect.
        self._pdc.DrawToDCClipped(
            dc, wx.Rect(0, 0, self.Size[0], self.Size[1])
            )

    def OnMotion(self, event):
        pnt = event.GetPosition()
        elem_rect = self._pdc.GetWxRect('button')
        mouse_pnt = wx.Rect(pnt[0], pnt[1], 1, 1)
        
        if mouse_pnt.Intersects(elem_rect) == True:
            self._pdc.UpdateElem('button:hover')
        else:
            self._pdc.UpdateElem('button')

        self.RefreshDemo()


    def OnLeftDown(self, event):
        pnt = event.GetPosition()
        elem_rect = self._pdc.GetWxRect('button')

        # Create a 1x1 rect for the mouse pointer
        mouse_pnt = wx.Rect(pnt[0], pnt[1], 1, 1) 
        
        if mouse_pnt.Intersects(elem_rect) == True:
            self._pdc.UpdateElem('button:press')
            self._pdc.UpdateElem('button-text:hover')

        self.RefreshDemo()

    def OnLeftUp(self, event):
        pnt = event.GetPosition()
        elem_rect = self._pdc.GetWxRect('button')

        # Create a 1x1 rect for the mouse pointer
        mouse_pnt = wx.Rect(pnt[0], pnt[1], 1, 1) 
        
        if mouse_pnt.Intersects(elem_rect) == True:
            self._pdc.UpdateElem('button')
            self._pdc.UpdateElem('button-text')
            self.ButtonCallback()
            
        self.RefreshDemo()

    def DrawDrawing(self, dc):

        # Initial
        dc.InitElem('button')
        dc.InitElem('button-text', "TEXT", "UI Style Lang Demo")
        dc.InitElem('text', "TEXT", "UI Style Lang Demo")


    def RefreshDemo(self):
        rect = wx.Rect(0, 0, self.Size[0], self.Size[1])
        self.RefreshRect(rect, False)
        self.Refresh()

    def ButtonCallback(self):
        notify = wx.adv.NotificationMessage(
            title="Button Clicked",
            message="You clicked the UI Style Lang custom button",
            parent=None, flags=wx.ICON_INFORMATION)
        notify.Show(timeout=2) # 1 for short timeout, 100 for long timeout



if __name__ == '__main__':
    # Create the app and startup
    app = UIStyleApp(file='./custom-widget-demo.uiss', redirect=False)
    frame = MainApplication()
    frame.Show()
    app.SetTopWindow(frame)
    app.MainLoop()

