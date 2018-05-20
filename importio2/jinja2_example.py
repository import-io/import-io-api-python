#!/usr/bin/env python
from jinja2 import Template
t = Template("Hello {{ something }}!")

values = {"something": "World"}
print(t.render(values))
