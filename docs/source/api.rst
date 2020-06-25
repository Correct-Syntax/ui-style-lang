=================
UI Style Lang API
=================

UI Style Lang is a simple CSS-like language which allows for drawing and styling wxPython elements. Many UI Style Lang properties are the same as the normal (not short-hand) CSS3 properties. This provides a familiar syntax, especially for those with experience with CSS3.


Style Sheet API
===============

The UI Style Lang language is declared in a .uiss or .css file. It has a simple, CSS3-like syntax and an id based structure.

.. note::
   It should be noted that not all of the properties supported in the drawing API are supported by the API for styling elements. Thus, the drawing API is much more powerful (at the moment, at least) and the usage will differ greatly.

Basic Syntax Rules
^^^^^^^^^^^^^^^^^^

UI Style Lang language is much like CSS in it's syntax. However, UI Style Lang differs in certain areas, especially in the strictness of spacing.

Declarations
------------

Declare an element style with ``@style`` and assign an id like below:

.. code-block:: css

   @style element-id {

   }

An id can include alphabetical characters A-Z and numbers, separated by dashes.

Properties
----------

Properties are written much like in CSS:

.. code-block:: css

   @style element-id {
      border-width: 2px;
   }

Values, such as "2px" in the above example, *must include the suffix "px" or "deg"*, depending on the property.


Spacing
-------

UI Style Lang enforces proper spacing around ids and property values. 


For example:

**RIGHT**

.. code-block:: css

   // This is correct syntax

   @style tester {
      border-color: grey;
      border-width: 2px;
      background-color: red;
   }

**WRONG**

.. code-block:: css

   // This is WRONG syntax and will result in an error!

   @style tester{ // Bad spacing here...
      border-color:grey; // and here...
      border-width: 2 px; // and here.
      background-color: red; // This is good, though.
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

Style Sheet Properties
^^^^^^^^^^^^^^^^^^^^^^

type
----

Sets the property type of the element. **(Specific to UI Style Lang)**

.. warning::
   Be sure to set this property when drawing text or images with the Drawing API!

.. method:: type: shape|text|image

   :shape (default):
      This element is to be treated as a shape (circle, square, rectangle, etc)

   :text:
      This element is to be treated as text

   :image:
      This element is to be treated as an image


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

The "HTML equivelent" in UI Style Lang is the Python method API. The HTML + CSS feel is most pronounced in the ``UIStyleDC`` drawing API.

Drawing API
^^^^^^^^^^^

The drawing API is an abstraction of wxPython DCs. UIStyleDC is implemented as an enhanced wrapper of ``wx.adv.PseudoDC``. Other wxPython DCs may be supported in the future, but are not planned.

UIStyleDC
---------

The ``UIStyleDC`` class is an enhanced wrapper for the ``wx.adv.PseudoDC``, making it possible to use UI Style Lang to draw on any ``wx.Window``. 

.. note::
   The normal methods from the ``PseudoDC`` are still accessible from ``UIStyleDC``. 

.. py:class:: UIStyleDC(parent, file)

   initilizes the DC and styles

   :param parent: an instance of ``wx.Frame``
   :param file: path to the stylesheet with intial styles declared (supports a .uiss or .css file) 


   .. py:method:: InitShapeStyles(_id)

      Draws the shape with the same id declared in the stylesheet. This can be thought of like the following pseudo-HTML: *<div class="{{_id}}"></div>*

      :param str _id: Id of the element to be drawn declared in the initial stylesheet


   .. py:method:: UpdateShapeStyles(_id, styles="")

      Updates and draws the shape with the same id declared in the stylesheet. This can be thought of like the following pseudo-HTML: *<div class="{{_id}}" style="{{styles}}"></div>*

      :param str _id: id to draw (must be already declared in the intial stylesheet)
      :param str styles: inline styles to update and override style properties of the shape


   .. py:method:: InitTextStyles(_id, text)

      Draws the text with the same id declared in the stylesheet. This can be thought of like the following pseudo-HTML: *<p class="{{_id}}">{{text}}</p>*

      :param str _id: id to draw (must be already declared in the intial stylesheet)
      :param str text: text to be drawn and displayed


   .. py:method:: UpdateTextStyles(_id, text="", styles="")

      Updates and draws the text with the same id declared in the stylesheet. This can be thought of like the following pseudo-HTML: *<p class="{{_id}}" style="{{styles}}">{{text}}</p>*

      :param str _id: id to draw (must be already declared in the intial stylesheet)
      :param str text: update and override the text to be drawn and displayed
      :param str styles: inline styles to update and override style properties of the text