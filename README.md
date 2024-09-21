# Marimo Reactive Notebook Prompt Library

## Get Started Notebook
> This is a simple demo of the Marimo Reactive Notebook
- Install hyper modern [UV Python Package and Project](https://docs.astral.sh/uv/getting-started/installation/)
- Install dependencies `uv sync`
- Install marimo `uv pip install marimo`
- Copy `.env.sample` to `.env` and set your keys
- To Edit, Run `uv run marimo edit marimo_is_awesome_demo.py.py`
- To View, Run `uv run marimo run marimo_is_awesome_demo.py.py`
- Then use your favorite IDE & AI Coding Assistant to edit the `marimo_is_awesome_demo.py.py` directly or via the UI.

## Ad-hoc Prompt Notebook
> Quickly run and test prompts across models
- To Edit, Run `uv run marimo edit adhoc_prompting.py`
- To View, Run `uv run marimo run adhoc_prompting.py`

## Prompt Library Notebook
> Manage your prompt library
- To Edit, Run `uv run marimo edit prompt_library.py`
- To View, Run `uv run marimo run prompt_library.py`

## General Usage
> See the [Marimo Docs](https://docs.marimo.io/index.html) for more details
- `uv pip install marimo` - install marimo
- `uv run marimo` - open the Marimo app in your default browser
- `uv run marimo edit marimo_is_awesome_demo.py.py` - create or edit an existing notebook
- `uv run marimo run marimo_is_awesome_demo.py.py` - run a notebook as a script

## Prompt Library Use-Cases
- Ad-hoc prompting
- Prompt reuse
- Prompt versioning
- Interactive prompts
- Multi-model comparison
- Prompt templating

## Advantages of Marimo

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

## Resources
- https://docs.astral.sh/uv/
- https://docs.marimo.io/index.html
- 