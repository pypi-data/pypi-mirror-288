import re
import importlib.resources

from jinja2 import Environment
from jinja2 import BaseLoader

from .sql import ADISQLGenerator

jinja_environment = Environment(loader=BaseLoader)
strip_quote = lambda x: re.sub('"', '', x)
jinja_environment.filters["stripquote"] = strip_quote

from .log_formats import colorized_logger
logger = colorized_logger(__name__)

with importlib.resources.path('adilib.templates', 'schema.d2.jinja') as file:
    with open(file, 'rt') as f:
        db_d2_template = f.read()


from .log_formats import colorized_logger
logger = colorized_logger(__name__)


class D2Generator:
    def __init__(self, tables, token, prefix, version):
        sql_generator = ADISQLGenerator(tables, token, version)
        self.form_tables = sql_generator.get_tables(readable_labels=True)
        self.form_fields = sql_generator.get_fields(readable_labels=True)

    def get_source(self):
        template = jinja_environment.from_string(db_d2_template)
        d2 = template.render(
            tables = self.form_tables,
            fields = self.form_fields,
        )
        return d2
