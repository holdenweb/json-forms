def render(obj):
    output = []
    for field in obj:
        output.append(field.render)

class Field:
    def __init__(self, name: str):
        self.name = name
    def render(self):
        return f"""\
<div>
    {self.render_label()}
    {self.render_input()}
</div>
"""

    def render_label(self):
        return f"""\
<div>
    {self.name}:
</div>
"""

    def render_input(self):
        "Default input widget asks for string."
        return f"""\
<div>
    <input name={self.name}/>
</div>
"""

LF = '\n'

class ObjField(Field):
    def __init__(self, name: str, fields: list):
        self.fields = fields
        super().__init__(self, name)
    def render_input(self):
        for field in self.fields:
            output.append(Field(field).render())
        return f"""\
<div>
    {LF.join(output)}
</div>
"""
