import django.dispatch as dispatch

render_navbar = dispatch.Signal(providing_args=['urls'])
render_navbar_admin = dispatch.Signal(providing_args=['urls'])
