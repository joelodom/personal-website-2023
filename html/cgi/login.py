#!/usr/bin/env python3

import joel_utils.renderer as renderer

rendered = renderer.render_jinja('../templates/login.jinja2', name='fooooo')
print(rendered)
