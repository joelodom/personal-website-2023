#!/usr/bin/env python3

import joel_utils.renderer as renderer

rendered = renderer.render_jinja('../templates/new-user.jinja2')
print(rendered)
