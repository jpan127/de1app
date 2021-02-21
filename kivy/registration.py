from kivy.factory import Factory

# Register custom elements
_registrar = Factory.register
_registrar("BaseLayout"    , module="base_layout")
_registrar("BrewScreen"    , module="screens")
_registrar("FlushScreen"   , module="screens")
_registrar("GraphLayout"   , module="graph_layout")
_registrar("HomeScreen"    , module="screens")
_registrar("NavigationRail", module="navigation_rail")
_registrar("PlayButton"    , module="play_button")
_registrar("StreamScreen"  , module="screens")
_registrar("WaterScreen"   , module="screens")
_registrar("DurationPicker", module="duration_picker")