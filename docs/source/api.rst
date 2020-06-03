=================
UI Style Lang API
=================

UI Style Lang is a simple CSS-like language which allows for drawing and styling wxPython elements. Many UI Style Lang properties are the same as the normal (not short-hand) CSS3 properties. This provides a familiar syntax, especially for those with experience with CSS3.


Style Sheet API
===============

The UI Style Lang language is declared in a .uiss or .css file. It has a simple, CSS3-like syntax and an id based structure.

.. note::
   It should be noted that not all of the properties supported in the drawing API are supported by the API for styling elements. Thus, the drawing API is much more powerful (at the moment, at least) and the usage will differ greatly.

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

.. function:: font-weight

   :normal: 

      normal font weight

   :bold: 

      bold font weight



Python API
==========

The "HTML equivelent" in UI Style Lang is the Python method API. The HTML + CSS feel is most pronounced in the ``UIStyleDC`` drawing API.

UIStyleDC
---------

The ``UIStyleDC`` class is an enhanced wrapper for the ``wx.adv.PseudoDC``. The normal methods from the ``PseudoDC`` are still accessible from ``UIStyleDC``. 

.. py:class:: UIStyleDC(parent, file)

   initilizes the DC and styles

   :param parent: an instance of ``wx.Frame``
   :param file: path to the stylesheet with intial styles declared (supports a .uiss or .css file) 

   .. py:method:: DrawShapeStyles(id)

      Draws the shape with the same id declared in the stylesheet. This can be thought of like the following pseudo-HTML: ``<div class="{{id}}"></div>``

      :param str id: Id of the element to be drawn declared in the initial stylesheet

