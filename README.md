# Marimo Reactive Notebook Prompt Library

## Get Started
- Install hyper modern [UV Python Package and Project](https://docs.astral.sh/uv/getting-started/installation/)
- Install dependencies `uv sync`
- Install marimo `uv pip install marimo`
- To Edit Run `marimo edit marimo_awesome.py`
- To View Run `marimo run marimo_awesome.py`
- Then use your favorite IDE & AI Coding Assistant to edit the `marimo_awesome.py` directly or via the UI.

## General Usage
- `uv pip install marimo` - install marimo
- `marimo` - open the Marimo app in your default browser
- `marimo edit marimo_awesome.py` - create or edit an existing notebook
- `marimo run marimo_awesome.py` - run a notebook as a script

## Advantages of marimo

### In General

- **Reactive Execution**: Run one cell, and marimo automatically updates all affected cells. This eliminates the need to manually manage notebook state.
- **Interactive Elements**: Provides reactive UI elements like dataframe GUIs and plots, making data exploration fast and intuitive.
- **Python-First Design**: Notebooks are pure Python scripts stored as `.py` files. They can be versioned with git, run as scripts, and imported into other Python code.
- **Reproducible by Default**: Deterministic execution order with no hidden state ensures consistent and reproducible results.
- **Built for Collaboration**: Git-friendly notebooks where small changes yield small diffs, facilitating collaboration.
- **Developer-Friendly Features**: Includes GitHub Copilot, autocomplete, hover tooltips, vim keybindings, code formatting, debugging panels, and extensive hotkeys.
- **Seamless Transition to Production**: Notebooks can be run as scripts or deployed as read-only web apps.
- **Versatile Use Cases**: Ideal for experimenting with data and models, building internal tools, communicating research, education, and creating interactive dashboards.

### Advantages Over Jupyter Notebooks

- **Reactive Notebook**: Automatically updates dependent cells when code or values change, unlike Jupyter where cells must be manually re-executed.
- **Pure Python Notebooks**: Stored as `.py` files instead of JSON, making them easier to version control, lint, and integrate with Python tooling.
- **No Hidden State**: Deleting a cell removes its variables and updates affected cells, reducing errors from stale variables.
- **Better Git Integration**: Plain Python scripts result in smaller diffs and more manageable version control compared to Jupyter's JSON format.
- **Import Symbols**: Allows importing symbols from notebooks into other notebooks or Python files.
- **Enhanced Interactivity**: Built-in reactive UI elements provide a more interactive experience than standard Jupyter widgets.
- **App Deployment**: Notebooks can be served as web apps or exported to static HTML for easier sharing and deployment.
- **Advanced Developer Tools**: Features like code formatting, GitHub Copilot integration, and debugging panels enhance the development experience.
- **Script Execution**: Can be executed as standard Python scripts, facilitating integration into pipelines and scripts without additional tools.