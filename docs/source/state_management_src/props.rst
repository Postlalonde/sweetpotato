Props
======


:class:`~sweetpotato.management.Props`
***************************************

.. code-block:: python

   from sweetpotato.management import State, Props

   state = State({"isAuthenticated": False})
   props = Props(state)
   print(props["isAuthenticated"])
