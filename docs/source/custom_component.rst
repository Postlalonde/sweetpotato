Custom Components 🦄
=====================

Build a Custom Component ⚒️
--------------------------

Instructions for building custom components to be added.


Customizing a component can be as simple as:

.. code-block:: pycon

   >>> from sweetpotato.core.base import RootComponent
   >>> component = RootComponent(component_name="Name of your component")
   >>> print(component)
   <NameOfYourComponent />

but this doesn't add or change anything, other than the name. For actual customization, read on.

Let's say we want to add our own props to a component.

.. code-block:: python

   from sweetpotato.core.base import RootComponent
   from sweetpotato.core.utils import CustomMixin

   custom_props = {"custom_prop_one", "custom_prop_two"}

   # Name the class something relevant and unique
   class CustomComponent(RootComponent, CustomMixIn):
       """My first custom component."""
       extra_props = custom_props


.. code-block:: pycon

   >>> custom_component = CustomComponent(custom_prop_one="a custom prop")
   >>> print(custom_component)
   <CustomComponent custom_prop_one="a custom prop"/>


We can now use this component in our main application, like so:

.. code-block:: python

   from sweetpotato.app import App
   from sweetpotato.components import View, Text, StyleSheet
   from my_project import CustomComponent
