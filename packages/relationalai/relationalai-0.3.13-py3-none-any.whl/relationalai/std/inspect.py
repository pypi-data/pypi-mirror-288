from .. import dsl
from . import aggregates as aggs
from rich import box as rich_box
from rich.console import Console
from rich.table import Table

def print_dataframe(df):
    console = Console()
    table = Table(show_header=True, border_style="dim", header_style="", box=rich_box.SIMPLE)

    # Add columns
    for column in df.columns:
        table.add_column(column)

    # Add rows
    for _, row in df.iterrows():
        table.add_row(*row.astype(str))

    console.print(table)

def _type(type:dsl.Type|dsl.TypeUnion|dsl.TypeIntersection, props=[], limit=20, silent=False):
    model = dsl.get_graph()
    props = props or type.known_properties()
    with model.query(dynamic=True) as select:
        obj = type()
        aggs.top(20, obj)
        res = select(obj, *[getattr(obj, p) for p in props])
    if not silent:
        print_dataframe(res.results)
    return res.results

def inspect(object, props=[], limit=20, silent=False):
    if isinstance(object, dsl.Type) or isinstance(object, dsl.TypeUnion) or isinstance(object, dsl.TypeIntersection):
        return _type(object, props=props, limit=limit, silent=silent)
    else:
        print("Unknown object type: ", object)