# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FunctionCall(Component):
    """A FunctionCall component.


Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

- data-* (string; optional):
    Wild card data attributes.

- docs (a list of or a singular dash component, string or number; optional)

- inputs (a list of or a singular dash component, string or number; optional)

- outputs (a list of or a singular dash component, string or number; optional)

- tabIndex (number; optional):
    tab-index."""
    _children_props = ['inputs', 'outputs', 'docs']
    _base_nodes = ['inputs', 'outputs', 'docs', 'children']
    _namespace = 'dongjak_dash_components'
    _type = 'FunctionCall'
    @_explicitize_args
    def __init__(self, inputs=Component.UNDEFINED, outputs=Component.UNDEFINED, docs=Component.UNDEFINED, id=Component.UNDEFINED, tabIndex=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'aria-*', 'data-*', 'docs', 'inputs', 'outputs', 'tabIndex']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['id', 'aria-*', 'data-*', 'docs', 'inputs', 'outputs', 'tabIndex']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(FunctionCall, self).__init__(**args)
