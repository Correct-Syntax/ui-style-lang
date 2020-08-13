===============
Troubleshooting 
===============

Here are some common problems and solutions you can try when working with the UI Style Lang API and you're having issues.


Drawn Elements Do Not Show Up
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**1. Check to make sure you have specified the `top`, `left`, `bottom` and `top` properties in your element declaration in the stylesheet.**

.. code-block:: css

   @style example {
      width: 200px;
      height: 200px;
      top: 500px;
      left: 400px;
      border-color: grey;
      border-width: 2px;
      background-color: red;
   }


**2. Check to see if you intialized the element in the Python API.**

.. code-block:: python

    # "dc" here refers to the `UIStylePDC`
    dc.InitElem('example')


You will not see anything drawn unless you did both of the above. It is easy to forget, but be sure you have done so!


Styled Widgets Are Not Changing Styles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**1. Styling of the native wxPython widgets (used as the backend for the UI Style Lang's Styled Widgets) may not be supported on your platform.** 

UI Style Lang uses the wxPython native widgets as a backend for the styled widgets. Check to see if the given widget succeeded in styling the widget on your platform via the `ConfigureStyle` method:

.. code-block:: python

   ..
   >> frm = UIStyleFrame(None,
                       title="Hello World!",
                       size=(400,275),
                       name="main-frame")
   ..
   >> frm.ConfigureStyle()
   >> False 

By default, the exampe above will return False because the default background color for UIStyleFrame (transparent) is not supported on most platforms.


**2. Make sure the widget is visible.**

The `UIStyleApp` background, `UIStyleFrames` and even `UIStylePanels` can be hidden from view by the `UIStylePDC` and other widgets placed inside them. Thus, any styling applied to them cannot be seen.