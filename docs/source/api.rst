=================
UI Style Lang API
=================

UI Style Lang is a simple CSS-like language which allows for drawing and styling wxPython elements. Many UI Style Lang properties are the same as the normal (non short-hand) CSS3 properties. This provides a familiar syntax, especially for those with experience with CSS3.

It also has a Python API which can be thought of like what HTML+JS is to CSS.


Style Sheet API
===============

The UI Style Lang language can be declared in a .uiss or .css file or as a string. It has a simple, CSS3-like syntax and an id based structure.

.. note::
   It should be noted that not all of the properties supported in the Drawing API are supported by the Native Widget API for styling elements. Thus, the Drawing API is much more powerful (at the moment, at least) and the usage will differ greatly.

Loading Styles Via String
^^^^^^^^^^^^^^^^^^^^^^^^^

Normally, UI Style Lang is declared in a .uiss or .css file. However, there are times when it is helpful to write the styles in a string directly in the python (.py) file.

Comment-Header
--------------

A special comment-header is required when loading styles from a string. The comment-header is declared at the very top of the string as ``/* !uistylelangstr */``.

Example
-------

.. code-block:: python

   uiss_str = """
   /* !uistylelangstr */
   
   .button {
      background-color: white;
   }
   ...

   """

   # load just like you would a file

.. versionadded:: 8.5


Basic Syntax Rules
^^^^^^^^^^^^^^^^^^

UI Style Lang language is much like CSS in it's syntax. However, UI Style Lang differs in certain areas, especially in the strictness of spacing.

Declaration Syntax
------------------

Declare an element style with the ``@style`` keyword and assign an *id selector* and/or a *pseudo-id selector* like below:

.. code-block:: css

   @style id-selector:pseudo-id-selector {
      ...
   }


Id Selectors
************

An *id selector* **represents a single element**, much like an HTML id. It can include alphabetical characters A-Z and numbers, separated by dashes.

.. code-block:: css

   @style my-element {
      ...
   }


If a *pseudo-id selector* (See below for more on pseudo-id selectors) is not declared, by default it will be called "init".

Therefore, writing:

.. code-block:: css

   @style my-element {
      ...
   }

...is the same as writing:

.. code-block:: css

   @style my-element:init {
      ...
   }

...and vice-versa.


Pseudo-id Selectors
*******************

Declarations can also have *pseudo-id selectors* which **represent a unique style of an element an any time**, much like an HTML class.

Like *id selectors*, it can include alphabetical characters A-Z and numbers, separated by dashes.

*Id selectors* and *pseudo-id selectors* are separated by a single colon with no spacing:

.. code-block:: css

   @style my-element:hover {
      ...
   }


This is a very powerful feature of UI Style Lang as it allows you to declare style changes to your element in the stylesheet. 

It is useful especially for creating custom widgets where styles change depending on events as in this example:

.. code-block:: css

   /* button */
   @style button {
      background-color: #F4F4F4;
      top: 20px;
      left: 40px;
      width: 115px;
      height: 35px;
      border-color: #D1D1D1;
      border-size: 2px;
   }

   @style button:hover {
      background-color: #FDFDFD;
      top: 20px;
      left: 40px;
      width: 115px;
      height: 35px;
      border-color: #D1D1D1;
      border-size: 2px;
   }

   @style button:press {
      background-color: #D1D1D1;
      top: 20px;
      left: 40px;
      width: 115px;
      height: 35px;
      border-color: #D1D1D1;
      border-size: 2px;
   }

   @style button-text {
      color: black;
      top: 30px;
      left: 47px;
   }

   @style button-text:hover {
      color: #444;
      top: 30px;
      left: 47px;
   }


.. versionadded:: 0.8


Properties
----------

Properties are written much like in CSS:

.. code-block:: css

   @style element-id {
      border-width: 2px;
   }

Values, such as "2px" in the above example, *must include the suffix "px" or "deg"*, depending on the property.


Comments
--------

UI Style Lang has support for single-line comments in the stylesheet. Multi-line comments may be supported in the future.

.. code-block:: css

   /* An element with a comment */
   @style element-id {
      border-width: 2px;
      background-color: blue;
   }

.. versionadded:: 0.6

Spacing
-------

UI Style Lang enforces proper spacing around ids and property values. 


For example:

**RIGHT**

.. code-block:: css

   /* This is correct syntax */

   @style tester {
      border-color: grey;
      border-width: 2px;
      background-color: red;
   }

**WRONG**

.. code-block:: css

   /* This is WRONG syntax and will result in an error! */

   @style tester{ /* Bad spacing here... */
      border-color:grey; /* and here... */
      border-width: 2 px; /* and here. */
      background-color: red; /* This is good, though. */
   }


Style Sheet Example
^^^^^^^^^^^^^^^^^^^

Below is a minimal example of the UI Style Lang language declaring a 200 x 200px rectangle with a 2px grey border and red background placed at 400, 500 on the window.

.. code-block:: css

   @style rect-example {
      width: 200px;
      height: 200px;
      top: 500px;
      left: 400px;
      border-color: grey;
      border-width: 2px;
      background-color: red;
   }

.. note::

   You will not see anything drawn unless you specify the `top`, `left`, `bottom` and `top` properties. It is easy to forget, but be sure to do so!


Style Sheet Properties
^^^^^^^^^^^^^^^^^^^^^^

top
---

Sets the top left corner Y coordinate of the element

.. method:: top: length

   :length:
      Value defining the position (in pixels) of the element along the Y axis


left
----

Sets the top left corner X coordinate of the element

.. method:: left: length

   :length:
      Value defining the position (in pixels) of the element along the X axis


width
-----

Sets the width of the element

.. method:: width: length

   :length:
      Value defining the width (in pixels) of the element


height
------

Sets the height of the element

.. method:: height: length

   :length:
      Value defining the height (in pixels) of the element


color
-----

Sets the color of the text

.. method:: color: color

   :color:
      Hexadecimal colors or any color name supported by wxPython (e.g: red, #C7C729)


background
----------

Sets the background color of the text

.. method:: background: color

   :color:
      Hexadecimal colors or any color name supported by wxPython (e.g: red, #C7C729)


background-color
----------------

Sets the background color of the current element

.. method:: background-color: color

   :color:
      Hexadecimal colors or any color name supported by wxPython (e.g: red, #C7C729)


border-radius
-------------

Sets the shape of the border of the element

.. method:: border-radius: length

   :length:
      Pixel value defining the shape of the border (e.g: 10px). If set to exactly 1/2 the height of the element, the shape will be a circle.


border-width
------------

Sets the width of the border of the element

.. method:: border-width: length

   :length:
      Pixel value defining the thickness of the border (e.g 2px)


border-color
------------

Sets the color of the border of the element

.. method:: border-color: color

   :color:
      Hexadecimal colors or any color name supported by wxPython (e.g: red, #C7C729)


font-size
---------

Sets the size of the text font

.. method:: font-size: medium|smaller|larger

   :medium (default):
      Sets the font-size to a medium size

   :smaller:
      Sets the current font size to be divided by 1.2 , the factor of 1.2 being inspired by the W3C CSS specification

   :larger:
      Sets the current font size to be multiplied by 1.2 , the factor of 1.2 being inspired by the W3C CSS specification


font-style
----------

Sets the text font style

.. method:: font-style: normal|italic

   :normal (default):
      Normal font style

   :italic:
      Italic font style


font-weight
-----------

Sets how thick or thin characters in the text should be displayed

.. method:: font-weight: normal|bold|100|200|300|400|500|600|700|800|900|1000

   :normal (default):
      Normal font weight

   :bold: 
      Bold font weight

   :100 200 300 400 500 600 700 800 900 1000:
      Thickness of characters, from thin to thick. 400 is the same as normal, and 700 is the same as bold.


text-decoration
---------------

Specifies the decoration added to the text

.. method:: text-decoration: none|underline

   :none (default):
      Sets the text to normal

   :underline:
      Sets a line below the text



Python API
==========

The "HTML equivelent" in UI Style Lang is the Python method API. The HTML + CSS feel is most pronounced in the ``UIStylePDC`` Drawing API.

Drawing API
^^^^^^^^^^^

The drawing API is an abstraction of wxPython DCs. ``UIStylePDC`` is implemented as an enhanced wrapper of ``wx.adv.PseudoDC``. Other wxPython DCs may be supported in the future, but are not planned.

UIStylePDC
----------

The ``UIStylePDC`` class is an enhanced wrapper for the ``wx.adv.PseudoDC``, making it possible to use UI Style Lang to draw on any ``wx.Window``. 

.. note::
   The normal methods from the ``wx.adv.PseudoDC`` are still accessible from ``UIStylePDC``. 

.. py:module:: uistylelang.context.UIStylePDC
.. py:currentmodule:: uistylelang.context.UIStylePDC

.. autoclass:: uistylelang.UIStylePDC

.. automethod:: uistylelang.UIStylePDC.GetWxId
.. automethod:: uistylelang.UIStylePDC.GetWxRect
.. automethod:: uistylelang.UIStylePDC.InitElem

.. warning::

   Content as defined by the ``content`` variable is shared between ALL pseudo-id selectors. This means that an element with ``content`` will still be the same no matter which pseudo selector for that element you use.

   For example:

   .. code-block:: python

         >> dc.InitElem('my-elem', "TEXT", "This is the text to be displayed") # Initial
         ...
         >> dc.UpdateElem('my-elem:active', content="This is the updated text", styles="color: red;") # Updated
         ...
         >> dc.UpdateElem('my-elem:active') # content will be "This is the updated text"
         >> dc.UpdateElem('my-elem:hover') # content will also be "This is the updated text"

   This may change in the future, but keep this in mind when updating an element's content.

.. automethod:: uistylelang.UIStylePDC.UpdateElem


Native Widget API
^^^^^^^^^^^^^^^^^

.. note::

   The Native Widget API can be used *with* or *without* the Drawing API and vice-versa. UI Style Lang does not force usage of both as the same time.

The Native Widget API is an abstraction of a few of the native wxPython widgets. The widgets here are implemented as an enhanced wrappers of the corresponding widget to allow for styling (if the platform supports it). 

Widgets are styled using the ``name`` parameter as the *id selector*.

Example:

.. code-block:: css

   # In the stylesheet.uiss file
   @style main-panel {
     background-color: #444;
   }

.. code-block:: python

   # In the Python file
   app = UIStyleApp(file="stylesheet.uiss")

   ...
   
   pnl = UIStylePanel(frm,
                     name="main-panel"
                     )
  

UIStyleApp
----------

.. autoclass:: uistylelang.UIStyleApp

UIStyleFrame
------------

.. autoclass:: uistylelang.UIStyleFrame

UIStylePanel
------------

.. autoclass:: uistylelang.UIStylePanel

UIStyleStaticText
-----------------

.. autoclass:: uistylelang.UIStyleStaticText
