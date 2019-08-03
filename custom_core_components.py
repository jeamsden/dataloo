import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Overview", href="/cycling_overview"),
            ],
            nav=True,
            in_navbar=True,
            label="Cycling",
        ),
    ],
    brand="Dataloo",
    brand_href="/",
    color='primary',
    dark=True,
    sticky='top'
)