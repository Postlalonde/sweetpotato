State
======

To utilize state management in sweetpotato, initialize a :class:`~sweetpotato.management.State` object and register the
instance with the desired class. To use hooks (read about hooks `here <https://reactjs.org/docs/hooks-intro.html>`_),
call the :meth:`~sweetpotato.core.base_management.State.use_state` or :meth:`~sweetpotato.core.base_management.State.use_effect` methods,
passing a name and other optional arguments.


:class:`~sweetpotato.management.State`
***************************************

.. code-block:: python

   from sweetpotato.core.base import RootComponent
   from sweetpotato.management import State
   from sweetpotato.components import Button

   class MyButton(RootComponent):
       pass

   state = State({"pressed": 0})
   MyButton.register(state)
   set_pressed, pressed = state.use_state("pressed", increment=1)


   component = MyButton(
       state=state,
       children=[
           Button(
               title=f"Pressed: {pressed}",
               onPress=set_pressed
               )
           )
       ]
   )


