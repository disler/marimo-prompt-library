# Marimo Reactive Notebook Prompt Library
> Starter codebase to use Marimo reactive notebooks to build a reusable, customizable, Prompt Library.
>
> Take this codebase and use it as a starter codebase to build your own personal prompt library.
>
> Marimo reactive notebooks & Prompt Library [walkthrough](https://youtu.be/PcLkBkQujMI)
>
> Run multiple prompts against multiple models (SLMs & LLMs) [walkthrough](https://youtu.be/VC6QCEXERpU)

<img src="./images/multi_slm_llm_prompt_and_model.png" alt="multi llm prompting" style="max-width: 750px;">

<img src="./images/marimo_prompt_library.png" alt="marimo promptlibrary" style="max-width: 750px;">

## 1. Understand Marimo Notebook
> This is a simple demo of the Marimo Reactive Notebook
- Install hyper modern [UV Python Package and Project](https://docs.astral.sh/uv/getting-started/installation/)
- Install dependencies `uv sync`
- Install marimo `uv pip install marimo`
- To Edit, Run `uv run marimo edit marimo_is_awesome_demo.py`
- To View, Run `uv run marimo run marimo_is_awesome_demo.py`
- Then use your favorite IDE & AI Coding Assistant to edit the `marimo_is_awesome_demo.py` directly or via the UI.

## 2. Ad-hoc Prompt Notebook
> Quickly run and test prompts across models
- 🟡 Copy `.env.sample` to `.env` and set your keys (minimally set `OPENAI_API_KEY`)
    - Add other keys and update the notebook to add support for additional SOTA LLMs
- 🟡 Install Ollama (https://ollama.ai/) and pull the models you want to use
    - Update the notebook to use Ollama models you have installed
- To Edit, Run `uv run marimo edit adhoc_prompting.py`
- To View, Run `uv run marimo run adhoc_prompting.py`

## 3. ⭐️ Prompt Library Notebook
> Build, Manage, Reuse, Version, and Iterate on your Prompt Library
- 🟡 Copy `.env.sample` to `.env` and set your keys (minimally set `OPENAI_API_KEY`)
    - Add other keys and update the notebook to add support for additional SOTA LLMs
- 🟡 Install Ollama (https://ollama.ai/) and pull the models you want to use
    - Update the notebook to use Ollama models you have installed
- To Edit, Run `uv run marimo edit prompt_library.py`
- To View, Run `uv run marimo run prompt_library.py`

## 4. Multi-LLM Prompt
> Quickly test a single prompt across multiple language models
- 🟡 Ensure your `.env` file is set up with the necessary API keys for the models you want to use
- 🟡 Install Ollama (https://ollama.ai/) and pull the models you want to use
    - Update the notebook to use Ollama models you have installed
- To Edit, Run `uv run marimo edit multi_llm_prompting.py`
- To View, Run `uv run marimo run multi_llm_prompting.py`

## 5. Multi Language Model Ranker
> Compare and rank multiple language models across various prompts
- 🟡 Ensure your `.env` file is set up with the necessary API keys for the models you want to compare
- 🟡 Install Ollama (https://ollama.ai/) and pull the models you want to use
    - Update the notebook to use Ollama models you have installed
- To Edit, Run `uv run marimo edit multi_language_model_ranker.py`
- To View, Run `uv run marimo run multi_language_model_ranker.py`

## General Usage
> See the [Marimo Docs](https://docs.marimo.io/index.html) for general usage details

## Personal Prompt Library Use-Cases
- Ad-hoc prompting
- Prompt reuse
- Prompt versioning
- Interactive prompts
- Prompt testing & Benchmarking
- LLM comparison
- Prompt templating
- Run a single prompt against multiple LLMs & SLMs
- Compare multi prompts against multiple LLMs & SLMs
- Anything you can imagine!

## Advantages of Marimo

### Key Advantages
> Rapid Prototyping: Seamlessly transition between user and builder mode with `cmd+.` to toggle. Consumer vs Producer. UI vs Code. 

> Interactivity: Built-in reactive UI elements enable intuitive data exploration and visualization.

> Reactivity: Cells automatically update when dependencies change, ensuring a smooth and efficient workflow.

> Out of the box: Use sliders, textareas, buttons, images, dataframe GUIs, plotting, and other interactive elements to quickly iterate on ideas.

> It's 'just' Python: Pure Python scripts for easy version control and AI coding.


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
- https://youtu.be/PcLkBkQujMI
- https://github.com/BuilderIO/gpt-crawler
- https://github.com/simonw/llm
- https://ollama.com/
- https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/
- https://qwenlm.github.io/