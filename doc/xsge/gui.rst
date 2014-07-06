********
xsge.gui
********

.. automodule:: xsge.gui

xsge.gui Classes
================

xsge.gui.Handler
----------------

.. autoclass:: xsge.gui.Handler

xsge.gui.Handler Methods
~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.gui.Handler.get_mouse_focused_window

xsge.gui.Window
---------------

.. autoclass:: xsge.gui.Window

xsge.gui.Window Methods
~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.gui.Window.show

.. automethod:: xsge.gui.Window.hide

.. automethod:: xsge.gui.Window.move_to_front

.. automethod:: xsge.gui.Window.move_to_back

.. automethod:: xsge.gui.Window.destroy

.. automethod:: xsge.gui.Window.redraw

.. automethod:: xsge.gui.Window.refresh

.. automethod:: xsge.gui.Window.get_mouse_on_titlebar

.. automethod:: xsge.gui.Window.get_mouse_focused_widget

xsge.gui.Window Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.gui.Window.event_step

.. automethod:: xsge.gui.Window.event_key_press

.. automethod:: xsge.gui.Window.event_key_release

.. automethod:: xsge.gui.Window.event_mouse_button_press

.. automethod:: xsge.gui.Window.event_mouse_button_release

.. automethod:: xsge.gui.Window.event_titlebar_mouse_button_press

.. automethod:: xsge.gui.Window.event_titlebar_mouse_button_release

.. automethod:: xsge.gui.Window.event_global_key_press

.. automethod:: xsge.gui.Window.event_global_key_release

.. automethod:: xsge.gui.Window.event_global_mouse_button_press

.. automethod:: xsge.gui.Window.event_global_mouse_button_release

.. automethod:: xsge.gui.Window.event_close

xsge.gui.Dialog
---------------

.. autoclass:: xsge.gui.Dialog

xsge.gui.Dialog Methods
~~~~~~~~~~~~~~~~~~~~~~~

In addition to methods inherited from :class:`xsge.gui.Window`, the
following methods are also available:

.. automethod:: xsge.gui.Dialog.show

xsge.gui.Widget
---------------

.. autoclass:: xsge.gui.Widget

xsge.gui.Widget Methods
~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.gui.Widget.destroy

.. automethod:: xsge.gui.Widget.redraw

.. automethod:: xsge.gui.Widget.refresh

xsge.gui.Widget Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.gui.Widget.event_step

.. automethod:: xsge.gui.Widget.event_key_press

.. automethod:: xsge.gui.Widget.event_key_release

.. automethod:: xsge.gui.Widget.event_mouse_button_press

.. automethod:: xsge.gui.Widget.event_mouse_button_release

.. automethod:: xsge.gui.Widget.event_global_key_press

.. automethod:: xsge.gui.Widget.event_global_key_release

.. automethod:: xsge.gui.Widget.event_global_mouse_button_press

.. automethod:: xsge.gui.Widget.event_global_mouse_button_release

xsge.gui.Label
--------------

.. autoclass:: xsge.gui.Label

xsge.gui.Button
---------------

.. autoclass:: xsge.gui.Button

xsge.gui.Button Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge.gui.Widget`, the following event methods are also
available:

.. automethod:: xsge.gui.Button.event_press

xsge.gui.CheckBox
-----------------

.. autoclass:: xsge.gui.CheckBox

xsge.gui.CheckBox Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge.gui.Widget`, the following event methods are also
available:

.. automethod:: xsge.gui.CheckBox.event_toggle

xsge.gui.RadioButton
--------------------

.. autoclass:: xsge.gui.RadioButton

xsge.gui.RadioButton Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge.gui.Widget`, the following event methods are also
available:

.. automethod:: xsge.gui.RadioButton.event_toggle

xsge.gui.ProgressBar
--------------------

.. autoclass:: xsge.gui.ProgressBar

xsge.gui.TextBox
----------------

.. autoclass:: xsge.gui.TextBox

xsge.gui.TextBox Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge.gui.Widget`, the following event methods are also
available:

.. automethod:: xsge.gui.TextBox.event_change_text

xsge.gui.MessageDialog
----------------------

.. autoclass:: xsge.gui.MessageDialog

xsge.gui.TextEntryDialog
------------------------

.. autoclass:: xsge.gui.TextEntryDialog

xsge.gui Functions
==================

.. autofunction:: xsge.gui.init

.. autofunction:: xsge.gui.show_message

.. autofunction:: xsge.gui.get_text_entry
