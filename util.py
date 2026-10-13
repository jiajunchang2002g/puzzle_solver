import ipywidgets as widgets
from IPython.display import display

def grid_selector(size=8, cell_size=25):
    selected = set()
    buttons = {}

    grid = widgets.GridBox(
        layout=widgets.Layout(
            grid_template_columns=f"repeat({size}, {cell_size}px)",
            grid_gap="0px",
            width="max-content"
        )
    )

    def on_click(r, c):
        cell = (r, c)
        if cell in selected:
            selected.remove(cell)
        else:
            selected.add(cell)
        buttons[cell].button_style = (
            "danger" if cell in selected else ""
        )

    for r in range(size):
        for c in range(size):
            btn = widgets.Button(
                description="",
                layout=widgets.Layout(
                    width=f"{cell_size}px",
                    height=f"{cell_size}px",
                    min_width="0px",
                    padding="0px",
                    margin="0px",
                    border="1px solid gray"
                )
            )
            btn.on_click(lambda b, r=r, c=c: on_click(r, c))
            buttons[r, c] = btn
            grid.children += (btn,)

    def clear(b):
        selected.clear()
        for btn in buttons.values():
            btn.button_style = ""

    clear_btn = widgets.Button(description="Clear")
    clear_btn.on_click(clear)

    display(grid, clear_btn)
    return selected

selected = grid_selector(8)
