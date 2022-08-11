State
======



:class:`~sweetpotato.management.State`
***************************************

.. code-block:: python

   from sweetpotato.core.base import RootComponent
   from sweetpotato.management import State
   from sweetpotato.components import Button

   class MyButton(RootComponent):
       pass

   state = State({"pressed": False})
   MyButton.register(state)
   set_pressed, pressed = state.use_state(name="pressed", default_value=False)


   component = MyButton(
       state=state,
       children=[
           Button(
               title=pressed,
               onPress=f"() => {set_pressed}(!{pressed})")
           )
       ]
   )


