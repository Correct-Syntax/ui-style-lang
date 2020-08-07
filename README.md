UI Style Lang (Language)
========================

!["UI Style Lang"](https://github.com/Correct-Syntax/ui-style-lang/blob/master/logo.png?raw=true "UI Style Lang")


UI Style Lang is a simple CSS-like language which allows for drawing and styling wxPython elements. Many UI Style Lang properties are the same as the normal (not short-hand) CSS3 properties. This provides a familiar syntax, especially for those with experience with CSS3.


# WIP/ TODO

* SVG support(?).
* More widget styling support

# Features

* **Written in pure Python with minimal dependancies (just wxPython and the standard library)**

* **Drawing API**
    * Includes the ``UIStylePDC`` UI Style Lang class which is a powerful extension of the wxPython ``wx.PseudoDC``
    * Over 15 stylesheet properties already supported
    * Draw circles, rectangles, squares, images, & text
    * Translate & rotate objects
    * Load styles from inline styles and an external stylesheet
    * Auto-handles IDs, with support for manual-handling of IDs

* **Widget Styling API**
    * Supports loading from a stylesheet for easy theming
    * Support for styling panels, frames (currently)


# Development 

Pull requests and/or feature suggestions are welcome!

# Usage

See the [docs](https://github.com/Correct-Syntax/ui-style-lang/tree/master/docs) and [full demos](https://github.com/Correct-Syntax/ui-style-lang/tree/master/demo) for information on usage...

# License

UI Style Lang is licensed under the BSD 3-Clause license