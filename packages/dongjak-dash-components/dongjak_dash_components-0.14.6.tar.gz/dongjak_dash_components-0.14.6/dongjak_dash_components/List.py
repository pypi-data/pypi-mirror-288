# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class List(Component):
    """A List component.
t

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    `List.Item` components only.

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- aria-* (string; optional):
    Wild card aria attributes.

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

- center (boolean; optional):
    Determines whether items must be centered with their icon, `False`
    by default.

- className (string; optional):
    Class added to the root element, if applicable.

- classNames (dict; optional):
    Adds class names to Mantine components.

- darkHidden (boolean; optional):
    Determines whether component should be hidden in dark color scheme
    with `display: none`.

- data-* (string; optional):
    Wild card data attributes.

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

- icon (a list of or a singular dash component, string or number; optional):
    Icon that replaces list item dot.

- inset (string | number; optional)

- left (string | number; optional)

- lh (number; optional):
    lineHeight, theme key: lineHeights.

- lightHidden (boolean; optional):
    Determines whether component should be hidden in light color
    scheme with `display: none`.

- listStyleType (boolean | number | string | dict | list; optional):
    Controls `list-style-type`, by default inferred from `type`.

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

- size (a value equal to: 'xs', 'sm', 'md', 'lg', 'xl'; optional):
    Controls `font-size` and `line-height`, `'md'` by default.

- spacing (number; optional):
    Key of `theme.spacing` or any valid CSS value to set spacing
    between items, `0` by default.

- style (boolean | number | string | dict | list; optional):
    Inline style added to root component element, can subscribe to
    theme defined on MantineProvider.

- styles (boolean | number | string | dict | list; optional):
    Mantine styles API.

- ta (boolean | number | string | dict | list; optional):
    textAlign.

- tabIndex (number; optional):
    tab-index.

- td (string | number; optional):
    textDecoration.

- top (string | number; optional)

- tt (boolean | number | string | dict | list; optional):
    textTransform.

- type (a value equal to: 'ordered', 'unordered'; optional):
    List type: `ol` or `ul`, `'unordered'` by default.

- unstyled (boolean; optional):
    Remove all Mantine styling from the component.

- variant (string; optional):
    variant.

- visibleFrom (boolean | number | string | dict | list; optional):
    Breakpoint below which the component is hidden with `display:
    none`.

- w (string | number; optional):
    width, theme key: theme.spacing.

- withPadding (boolean; optional):
    Determines whether list items should be offset with padding,
    `False` by default."""
    _children_props = ['icon']
    _base_nodes = ['icon', 'children']
    _namespace = 'dongjak_dash_components'
    _type = 'List'
    @_explicitize_args
    def __init__(self, children=None, type=Component.UNDEFINED, withPadding=Component.UNDEFINED, size=Component.UNDEFINED, icon=Component.UNDEFINED, spacing=Component.UNDEFINED, center=Component.UNDEFINED, listStyleType=Component.UNDEFINED, id=Component.UNDEFINED, tabIndex=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, hiddenFrom=Component.UNDEFINED, visibleFrom=Component.UNDEFINED, lightHidden=Component.UNDEFINED, darkHidden=Component.UNDEFINED, mod=Component.UNDEFINED, m=Component.UNDEFINED, my=Component.UNDEFINED, mx=Component.UNDEFINED, mt=Component.UNDEFINED, mb=Component.UNDEFINED, ms=Component.UNDEFINED, me=Component.UNDEFINED, ml=Component.UNDEFINED, mr=Component.UNDEFINED, p=Component.UNDEFINED, py=Component.UNDEFINED, px=Component.UNDEFINED, pt=Component.UNDEFINED, pb=Component.UNDEFINED, ps=Component.UNDEFINED, pe=Component.UNDEFINED, pl=Component.UNDEFINED, pr=Component.UNDEFINED, bd=Component.UNDEFINED, bg=Component.UNDEFINED, c=Component.UNDEFINED, opacity=Component.UNDEFINED, ff=Component.UNDEFINED, fz=Component.UNDEFINED, fw=Component.UNDEFINED, lts=Component.UNDEFINED, ta=Component.UNDEFINED, lh=Component.UNDEFINED, fs=Component.UNDEFINED, tt=Component.UNDEFINED, td=Component.UNDEFINED, w=Component.UNDEFINED, miw=Component.UNDEFINED, maw=Component.UNDEFINED, h=Component.UNDEFINED, mih=Component.UNDEFINED, mah=Component.UNDEFINED, bgsz=Component.UNDEFINED, bgp=Component.UNDEFINED, bgr=Component.UNDEFINED, bga=Component.UNDEFINED, pos=Component.UNDEFINED, top=Component.UNDEFINED, left=Component.UNDEFINED, bottom=Component.UNDEFINED, right=Component.UNDEFINED, inset=Component.UNDEFINED, display=Component.UNDEFINED, flex=Component.UNDEFINED, classNames=Component.UNDEFINED, styles=Component.UNDEFINED, unstyled=Component.UNDEFINED, variant=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'center', 'className', 'classNames', 'darkHidden', 'data-*', 'display', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'icon', 'inset', 'left', 'lh', 'lightHidden', 'listStyleType', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'right', 'size', 'spacing', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'type', 'unstyled', 'variant', 'visibleFrom', 'w', 'withPadding']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'bd', 'bg', 'bga', 'bgp', 'bgr', 'bgsz', 'bottom', 'c', 'center', 'className', 'classNames', 'darkHidden', 'data-*', 'display', 'ff', 'flex', 'fs', 'fw', 'fz', 'h', 'hiddenFrom', 'icon', 'inset', 'left', 'lh', 'lightHidden', 'listStyleType', 'lts', 'm', 'mah', 'maw', 'mb', 'me', 'mih', 'miw', 'ml', 'mod', 'mr', 'ms', 'mt', 'mx', 'my', 'opacity', 'p', 'pb', 'pe', 'pl', 'pos', 'pr', 'ps', 'pt', 'px', 'py', 'right', 'size', 'spacing', 'style', 'styles', 'ta', 'tabIndex', 'td', 'top', 'tt', 'type', 'unstyled', 'variant', 'visibleFrom', 'w', 'withPadding']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(List, self).__init__(children=children, **args)
