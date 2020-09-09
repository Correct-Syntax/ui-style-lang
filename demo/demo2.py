# Widget Styling Demo for UI Style Lang
# =====================================

# This demo file (demo2.py) is MIT licensed - (C) 2020 Noah Rahm, Correct Syntax

# Usage:
# Run the demo and see the custom styling of the widgets (if
# your platform supports it).

import os
import wx

from uistylelang import UIStyleApp, UIStyleFrame, UIStylePanel, UIStyleStaticText


uiss_string = """
/* !uistylelangstr */

@style main-frame {
  background-color: #444;
}

@style main-panel {
  background-color: transparent;
}

@style static-text {
  color: orange;
  background-color: #fff;
}

"""


if __name__ == '__main__':
    # Create the app via the special UIStyleApp class
    app = UIStyleApp(file=uiss_string)
    # Uncomment to load from stylesheet:
    #app = UIStyleApp(file="demo-styles2.uiss")

    # Create the UIStyleFrame (Frame)
    frm = UIStyleFrame(None,
                       title="Hello World!",
                       size=(400,275),
                       name="main-frame"
                       )

    # Create a UIStylePanel (Panel)
    pnl = UIStylePanel(frm,
                       name="main-panel"
                       )

    # Labels
    st = UIStyleStaticText(pnl, -1, 'Hello World!', (15,10), name="static-text")
    st.SetFont(wx.FFont(14, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD))

    st = wx.StaticText(pnl, pos=(15,40),
            label='This is wxPython')
    st.SetFont(wx.FFont(10, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD))

    # Bitmap label
    bmp = wx.Bitmap(os.path.join(os.path.dirname(__file__), './test-img.png'))
    sb = wx.StaticBitmap(pnl, bitmap=bmp, pos=(15,85))

    frm.Show()
    app.MainLoop()


