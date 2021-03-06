LF = "\n"


def render(obj):
    output = []
    for field in obj:
        output.append(field.render())
    return LF.join(output)


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
<div class="label">
    {self.name}:
</div>
"""

    def render_input(self):
        "Default input widget asks for string."
        return f"""\
<div class="value">
    <input name={self.name}/>
</div>
"""


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


form_fields = [Field("First")]
