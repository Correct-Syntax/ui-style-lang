UI Style Lang (Language)
========================

!["UI Style Lang"](https://github.com/Correct-Syntax/ui-style-lang/blob/master/assets/logo.png?raw=true "UI Style Lang")


[![Documentation Status](https://readthedocs.org/projects/ui-style-lang/badge/?version=latest)](https://ui-style-lang.readthedocs.io/en/latest/?badge=latest)

UI Style Lang is a simple CSS-like language which allows for drawing and styling wxPython elements. Many UI Style Lang properties are the same as the normal (not short-hand) CSS3 properties. This provides a familiar syntax, especially for those with experience with CSS3.

If you are looking for an easy way to:

* **Draw shapes, text and/or images** in wxPython without worrying so much about ids, brushes, pens, etc.
* **Style the native wxPython widgets** from a stylesheet
* **Create your own custom widgets in wxPython** that can be styled with a CSS-like stylesheet

...then UI Style Lang is likely the module you're looking for.


# Direction of this project

The direction of this project will mainly focus towards creating custom widgets which are styl-able via the UI Style Language. The aim is to imitate how (Qt Style Sheets) qss is to Qt except with wxPython custom-made widgets and UI Style Language.

If you would like to help out or have ideas, feel free to open a Github issue or contact me directly via my email. :)


# WIP/ TODO

* Custom widgets (spinbox, slider, buttons, etc)
* SVG support(?)


# Features

* **Written in pure Python with minimal dependancies (just wxPython and the standard library)**

* **Drawing API**
    * Includes the ``UIStylePDC`` UI Style Lang class which is a powerful extension of the wxPython ``wx.PseudoDC``
    * Over 15 stylesheet properties already supported
    * Draw circles, rectangles, squares, images, & text
    * Translate & rotate elements
    * Load styles from inline styles, string and/or an external stylesheet
    * Auto-handles wxPython IDs, with support for manual-handling of IDs

* **Native Widget Styling API**
    * Supports loading from a stylesheet for easy theming
    * Support for styling app, panels, frames and static text widgets

...and more.


# Usage and Examples

See the [documentation](https://ui-style-lang.readthedocs.io/en/latest/) at Read the Docs and [full demo examples](https://github.com/Correct-Syntax/ui-style-lang/tree/master/demo) for information on usage...


# What does the syntax look like?

UI Style Lang (Stylesheet API) example:

```
/* My custom button styles */
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
```

Python API example:

```python

# Intilizing the element: <div id="button"></div>
>> dc.InitElem("button")

# Editing the style with inline styles: <div id="button" style="border-color: red; border-width: 4px;"></div>
>> dc.UpdateElem('button', styles="border-color: red; border-width: 4px;")

# Update the element with the 'hover' styles: <div id="button" class="hover"></div>
>> dc.UpdateElem('button:hover')

```

# Development

Pull requests and/or feature suggestions are welcome!


# License

UI Style Lang is licensed under the BSD 3-Clause license