# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class HoverCardTarget(Component):
    """A HoverCardTarget component.
erCardTarget

Keyword arguments:

- children (a list of or a singular dash component, string or number; required):
    Content.

- boxWrapperProps (dict; optional):
    Target box wrapper props.

    `boxWrapperProps` is a dict with keys:

    - bd (string | number; optional):
        border.

    - bg (boolean | number | string | dict | list; optional):
        background, theme key: theme.colors.

    - bga (boolean | number | string | dict | list; optional):
        backgroundAttachment.

    - bgp (string | number; optional):
        backgroundPosition.

    - bgr (boolean | number | string | dict | list; optional):
        backgroundRepeat.

    - bgsz (string | number; optional):
        backgroundSize.

    - bottom (string | number; optional)

    - c (boolean | number | string | dict | list; optional):
        color.

    - className (string; optional):
        Class added to the root element, if applicable.

    - darkHidden (boolean; optional):
        Determines whether component should be hidden in dark color
        scheme with `display: none`.

    - display (boolean | number | string | dict | list; optional)

    - ff (boolean | number | string | dict | list; optional):
        fontFamily.

    - flex (string | number; optional)

    - fs (boolean | number | string | dict | list; optional):
        fontStyle.

    - fw (boolean | number | string | dict | list; optional):
        fontWeight.

    - fz (number; optional):
        fontSize, theme key: theme.fontSizes.

    - h (string | number; optional):
        height, theme key: theme.spacing.

    - hiddenFrom (boolean | number | string | dict | list; optional):
        Breakpoint above which the component is hidden with `display:
        none`.

    - inset (string | number; optional)

    - left (string | number; optional)

    - lh (number; optional):
        lineHeight, theme key: lineHeights.

    - lightHidden (boolean; optional):
        Determines whether component should be hidden in light color
        scheme with `display: none`.

    - lts (string | number; optional):
        letterSpacing.

    - m (number; optional):
        margin, theme key: theme.spacing.

    - mah (string | number; optional):
        maxHeight, theme key: theme.spacing.

    - maw (string | number; optional):
        maxWidth, theme key: theme.spacing.

    - mb (number; optional):
        marginBottom, theme key: theme.spacing.

    - me (number; optional):
        marginInlineEnd, theme key: theme.spacing.

    - mih (string | number; optional):
        minHeight, theme key: theme.spacing.

    - miw (string | number; optional):
        minWidth, theme key: theme.spacing.

    - ml (number; optional):
        marginLeft, theme key: theme.spacing.

    - mod (string; optional):
        Element modifiers transformed into `data-` attributes, for
        example, `{ 'data-size': 'xl' }`, falsy values are removed.

    - mr (number; optional):
        marginRight, theme key: theme.spacing.

    - ms (number; optional):
        marginInlineStart, theme key: theme.spacing.

    - mt (number; optional):
        marginTop, theme key: theme.spacing.

    - mx (number; optional):
        marginInline, theme key: theme.spacing.

    - my (number; optional):
        marginBlock, theme key: theme.spacing.

    - opacity (boolean | number | string | dict | list; optional)

    - p (number; optional):
        padding, theme key: theme.spacing.

    - pb (number; optional):
        paddingBottom, theme key: theme.spacing.

    - pe (number; optional):
        paddingInlineEnd, theme key: theme.spacing.

    - pl (number; optional):
        paddingLeft, theme key: theme.spacing.

    - pos (boolean | number | string | dict | list; optional):
        position.

    - pr (number; optional):
        paddingRight, theme key: theme.spacing.

    - ps (number; optional):
        paddingInlineStart, theme key: theme.spacing.

    - pt (number; optional):
        paddingTop, theme key: theme.spacing.

    - px (number; optional):
        paddingInline, theme key: theme.spacing.

    - py (number; optional):
        paddingBlock, theme key: theme.spacing.

    - right (string | number; optional)

    - style (optional):
        Inline style added to root component element, can subscribe to
        theme defined on MantineProvider.

    - ta (boolean | number | string | dict | list; optional):
        textAlign.

    - td (string | number; optional):
        textDecoration.

    - top (string | number; optional)

    - tt (boolean | number | string | dict | list; optional):
        textTransform.

    - visibleFrom (boolean | number | string | dict | list; optional):
        Breakpoint below which the component is hidden with `display:
        none`.

    - w (string | number; optional):
        width, theme key: theme.spacing."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dongjak_dash_components'
    _type = 'HoverCardTarget'
    @_explicitize_args
    def __init__(self, children=None, boxWrapperProps=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'boxWrapperProps']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'boxWrapperProps']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        if 'children' not in _explicit_args:
            raise TypeError('Required argument children was not specified.')

        super(HoverCardTarget, self).__init__(children=children, **args)
