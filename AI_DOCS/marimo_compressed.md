import marimo as mo
import random
import pandas as pd
import plotly.express as px
import altair as alt
from vega_datasets import data
import matplotlib.pyplot as plt

# Markdown
mo.md("## This is a markdown heading")

# Inputs

# 1. Array
sliders = mo.ui.array([mo.ui.slider(1, 100) for _ in range(3)])
mo.md(f"Array of sliders: {sliders}")

# 2. Batch
user_info = mo.md(
    """
    - **Name:** {name}
    - **Birthday:** {birthday}
    """
).batch(name=mo.ui.text(), birthday=mo.ui.date())
user_info

# 3. Button
def on_click(value):
    print("Button clicked!", value)
    return value + 1

button = mo.ui.button(on_click=on_click, value=0, label="Click Me")
button

# 4. Checkbox
checkbox = mo.ui.checkbox(label="Agree to terms")
mo.md(f"Checkbox value: {checkbox.value}")

# 5. Code Editor
code = """
def my_function():
  print("Hello from code editor!")
"""
code_editor = mo.ui.code_editor(value=code, language="python")
code_editor

# 6. Dataframe
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
dataframe_ui = mo.ui.dataframe(df)
dataframe_ui

# 7. Data Explorer
data_explorer = mo.ui.data_explorer(data.cars())
data_explorer

# 8. Dates

# Single date
date_picker = mo.ui.date(label="Select a date")
date_picker

# Date and time
datetime_picker = mo.ui.datetime(label="Select a date and time")
datetime_picker

# Date range
date_range_picker = mo.ui.date_range(label="Select a date range")
date_range_picker

# 9. Dictionary
elements = mo.ui.dictionary({
    'slider': mo.ui.slider(1, 10), 
    'text': mo.ui.text(placeholder="Enter text")
})
mo.md(f"Dictionary of elements: {elements}")

# 10. Dropdown
dropdown = mo.ui.dropdown(options=['Option 1', 'Option 2', 'Option 3'], label="Select an option")
dropdown

# 11. File
file_upload = mo.ui.file(label="Upload a file")
file_upload

# 12. File Browser
file_browser = mo.ui.file_browser(label="Browse files")
file_browser

# 13. Form
form = mo.ui.text(label="Enter your name").form()
form

# 14. Microphone
microphone = mo.ui.microphone(label="Record audio")
microphone

# 15. Multiselect
multiselect = mo.ui.multiselect(options=['A', 'B', 'C', 'D'], label="Select multiple options")
multiselect

# 16. Number
number_picker = mo.ui.number(0, 10, step=0.5, label="Select a number")
number_picker

# 17. Radio
radio_group = mo.ui.radio(options=['Red', 'Green', 'Blue'], label="Select a color")
radio_group

# 18. Range Slider
range_slider = mo.ui.range_slider(0, 100, step=5, value=[20, 80], label="Select a range")
range_slider

# 19. Refresh
refresh_button = mo.ui.refresh(default_interval="5s", label="Refresh")
refresh_button

# 20. Run Button
run_button = mo.ui.run_button(label="Run")
run_button

# 21. Slider
slider = mo.ui.slider(0, 100, step=1, label="Adjust value")
slider

# 22. Switch
switch = mo.ui.switch(label="Enable feature")
switch

# 23. Table
table_data = [{'Name': 'Alice', 'Age': 25}, {'Name': 'Bob', 'Age': 30}]
table = mo.ui.table(data=table_data, label="User Table")
table

# 24. Tabs
tab1_content = mo.md("Content for Tab 1")
tab2_content = mo.ui.slider(0, 10)
tabs = mo.ui.tabs({'Tab 1': tab1_content, 'Tab 2': tab2_content})
tabs

# 25. Text
text_input = mo.ui.text(placeholder="Enter some text", label="Text Input")
text_input

# 26. Text Area
text_area = mo.ui.text_area(placeholder="Enter a long text", label="Text Area")
text_area

# 27. Custom UI elements (Anywidget)
# See the documentation on Anywidget for examples.

# Layouts

# 1. Accordion
accordion = mo.ui.accordion({'Section 1': mo.md("This is section 1"), 'Section 2': mo.ui.slider(0, 10)})
accordion

# 2. Carousel
carousel = mo.carousel([mo.md("Item 1"), mo.ui.slider(0, 10), mo.md("Item 3")])
carousel

# 3. Callout
callout = mo.md("Important message!").callout(kind="warn")
callout

# 4. Justify

# Center
centered_text = mo.md("This text is centered").center()
centered_text

# Left
left_aligned_text = mo.md("This text is left aligned").left()
left_aligned_text

# Right
right_aligned_text = mo.md("This text is right aligned").right()
right_aligned_text

# 5. Lazy
def lazy_content():
    mo.md("This content loaded lazily!")

lazy_element = mo.lazy(lazy_content)
lazy_element

# 6. Plain
plain_dataframe = mo.plain(df)
plain_dataframe

# 7. Routes
def home_page():
    return mo.md("# Home Page")

def about_page():
    return mo.md("# About Page")

mo.routes({
    "#/": home_page,
    "#/about": about_page
})

# 8. Sidebar
sidebar_content = mo.vstack([mo.md("## Menu"), mo.ui.button(label="Home"), mo.ui.button(label="About")])
mo.sidebar(sidebar_content)

# 9. Stacks

# Horizontal Stack
hstack_layout = mo.hstack([mo.md("Left"), mo.ui.slider(0, 10), mo.md("Right")])
hstack_layout

# Vertical Stack
vstack_layout = mo.vstack([mo.md("Top"), mo.ui.slider(0, 10), mo.md("Bottom")])
vstack_layout

# 10. Tree
tree_data = ['Item 1', ['Subitem 1.1', 'Subitem 1.2'], {'Key': 'Value'}]
tree = mo.tree(tree_data)
tree

# Plotting

# Reactive charts with Altair
altair_chart = mo.ui.altair_chart(alt.Chart(data.cars()).mark_point().encode(x='Horsepower', y='Miles_per_Gallon', color='Origin'))
altair_chart

# Reactive plots with Plotly
plotly_chart = mo.ui.plotly(px.scatter(data.cars(), x="Horsepower", y="Miles_per_Gallon", color="Origin"))
plotly_chart

# Interactive matplotlib
plt.plot([1, 2, 3, 4])
interactive_mpl_chart = mo.mpl.interactive(plt.gcf())
interactive_mpl_chart

# Media

# 1. Image
image = mo.image("https://marimo.io/logo.png", width=100, alt="Marimo Logo")
image

# 2. Audio
audio = mo.audio("https://www.zedge.net/find/ringtones/ocean%20waves")
audio

# 3. Video
video = mo.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", controls=True)
video

# 4. PDF
pdf = mo.pdf("https://www.africau.edu/images/default/sample.pdf", width="50%")
pdf

# 5. Download Media
download_button = mo.download(data="This is the content of the file", filename="download.txt")
download_button

# 6. Plain text
plain_text = mo.plain_text("This is plain text")
plain_text

# Diagrams

# 1. Mermaid diagrams
mermaid_code = """
graph LR
    A[Square Rect] -- Link text --> B((Circle))
    A --> C(Round Rect)
    B --> D{Rhombus}
    C --> D
"""
mermaid_diagram = mo.mermaid(mermaid_code)
mermaid_diagram

# 2. Statistic cards
stat_card = mo.stat(value=100, label="Users", caption="Total users this month", direction="increase")
stat_card

# Status

# 1. Progress bar
for i in mo.status.progress_bar(range(10), title="Processing"):
    # Simulate some work
    pass

# 2. Spinner
with mo.status.spinner(title="Loading...", subtitle="Please wait"):
    # Simulate a long-running task
    pass

# Outputs

# 1. Replace output
mo.output.replace(mo.md("This is the new output"))

# 2. Append output
mo.output.append(mo.md("This is appended output"))

# 3. Clear output
mo.output.clear()

# 4. Replace output at index
mo.output.replace_at_index(mo.md("Replaced output"), 0)

# Display cell code
mo.show_code(mo.md("This output has code displayed"))

# Control Flow

# Stop execution
user_age = mo.ui.number(0, 100, label="Enter your age")
mo.stop(user_age.value < 18, mo.md("You must be 18 or older"))
mo.md(f"Your age is: {user_age.value}")

# HTML

# 1. Convert to HTML
html_object = mo.as_html(mo.md("This is markdown converted to HTML"))
html_object

# 2. Html object
custom_html = mo.Html("<p>This is custom HTML</p>")
custom_html

# Other API components

# Query Parameters
params = mo.query_params()
params['name'] = 'John'

# Command Line Arguments
args = mo.cli_args()

# State
get_count, set_count = mo.state(0)
mo.ui.button(on_click=lambda: set_count(get_count() + 1), label="Increment")
mo.md(f"Count: {get_count()}")

# App
# See documentation for embedding notebooks

# Cell
# See documentation for running cells from other notebooks

# Miscellaneous
is_running_in_notebook = mo.running_in_notebook()

--- Guides

## Marimo Guides: Concise Examples

Here are concise examples for each guide in the Marimo documentation:

### 1. Overview

```python
import marimo as mo

# Define a variable
x = 10

# Display markdown with variable interpolation
mo.md(f"The value of x is {x}")

# Create a slider and display its value reactively
slider = mo.ui.slider(0, 100, value=50)
mo.md(f"Slider value: {slider.value}")
```

### 2. Reactivity

```python
import marimo as mo

# Define a variable in one cell
data = [1, 2, 3, 4, 5]

# Use the variable in another cell - this cell will rerun when `data` changes
mo.md(f"The sum of the data is {sum(data)}")
```

### 3. Interactivity

```python
import marimo as mo

# Create a slider
slider = mo.ui.slider(0, 10, label="Select a value")

# Display the slider's value reactively
mo.md(f"You selected: {slider.value}")
```

### 4. SQL

```python
import marimo as mo

# Create a dataframe
df = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]})

# Query the dataframe using SQL
mo.sql("SELECT * FROM df WHERE age > 30")
```

### 5. Run as an app

```bash
# Run a notebook as an interactive web app
marimo run my_notebook.py 
```

### 6. Run as a script

```bash
# Execute a notebook as a Python script
python my_notebook.py
```

### 7. Outputs

```python
import marimo as mo

# Display markdown
mo.md("This is **markdown** output")

# Display a matplotlib plot
import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4, 5])
plt.show()
```

### 8. Dataframes

```python
import marimo as mo
import pandas as pd

# Create a Pandas dataframe
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})

# Display the dataframe in an interactive table
mo.ui.table(df)
```

### 9. Plotting

```python
import marimo as mo
import altair as alt
from vega_datasets import data

# Create a reactive Altair chart
chart = alt.Chart(data.cars()).mark_point().encode(x='Horsepower', y='Miles_per_Gallon')
chart = mo.ui.altair_chart(chart)

# Display the chart and selected data
mo.hstack([chart, chart.value])
```

### 10. Editor Features

- Explore variable values and their definitions in the **Variables Panel**.
- Visualize cell dependencies in the **Dependency Graph**.
- Use **Go-to-Definition** to jump to variable declarations.
- Enable **GitHub Copilot** for AI-powered code suggestions.
- Customize **Hotkeys** and **Theming** in the settings.

### 11. Theming

```python
# In your notebook.py file:

app = marimo.App(css_file="custom.css")
```

### 12. Best Practices

- Use global variables sparingly.
- Encapsulate logic in functions and modules.
- Minimize mutations.
- Write idempotent cells.
- Use caching for expensive computations.

### 13. Coming from other Tools

- Refer to guides for specific tools like Jupyter, Jupytext, Papermill, and Streamlit to understand the transition to Marimo.

### 14. Integrating with Marimo

```python
import marimo as mo

# Check if running in a Marimo notebook
if mo.running_in_notebook():
    # Execute Marimo-specific code
    pass
```

### 15. Reactive State

```python
import marimo as mo

# Create reactive state
get_count, set_count = mo.state(0)

# Increment the counter on button click
mo.ui.button(on_click=lambda: set_count(get_count() + 1), label="Increment")

# Display the counter value reactively
mo.md(f"Count: {get_count()}")
```

### 16. Online Playground

- Create and share Marimo notebooks online at [https://marimo.new](https://marimo.new).

### 17. Exporting

```bash
# Export to HTML
marimo export html my_notebook.py -o my_notebook.html

# Export to Python script
marimo export script my_notebook.py -o my_script.py
```

### 18. Configuration

- Customize user-wide settings in `~/.marimo.toml`.
- Configure notebook-specific settings in the `notebook.py` file.

### 19. Troubleshooting

- Use the **Variables Panel** and **Dependency Graph** to debug cell execution issues.
- Add `print` statements for debugging.
- Try the "Lazy" runtime configuration for identifying stale cells.

### 20. Deploying

```bash
# Deploy a Marimo notebook as an interactive web app
marimo run my_notebook.py
```

--- recipes

## Marimo Recipes: Concise Examples

Here are concise examples of common tasks and concepts from the Marimo Recipes section:

### Control Flow

#### 1. Show an output conditionally

```python
import marimo as mo

show_output = mo.ui.checkbox(label="Show output")
mo.md("This output is visible!") if show_output.value else None
```

#### 2. Run a cell on a timer

```python
import marimo as mo
import time

refresh = mo.ui.refresh(default_interval="1s")
refresh

# This cell will run every second
refresh
mo.md(f"Current time: {time.time()}")
```

#### 3. Require form submission before sending UI value

```python
import marimo as mo

form = mo.ui.text(label="Your name").form()
form

# This cell will only run after form submission
mo.stop(form.value is None, mo.md("Please submit the form."))
mo.md(f"Hello, {form.value}!")
```

#### 4. Stop execution of a cell and its descendants

```python
import marimo as mo

should_continue = mo.ui.checkbox(label="Continue?")

# Stop execution if the checkbox is not checked
mo.stop(not should_continue.value, mo.md("Execution stopped."))

# This code will only run if the checkbox is checked
mo.md("Continuing execution...")
```

### Grouping UI Elements Together

#### 1. Create an array of UI elements

```python
import marimo as mo

n_sliders = mo.ui.number(1, 5, value=3, label="Number of sliders")
sliders = mo.ui.array([mo.ui.slider(0, 100) for _ in range(n_sliders.value)])
mo.hstack(sliders)

# Access slider values
mo.md(f"Slider values: {sliders.value}")
```

#### 2. Create a dictionary of UI elements

```python
import marimo as mo

elements = mo.ui.dictionary({
    'name': mo.ui.text(label="Name"),****
    'age': mo.ui.number(0, 100, label="Age")
})

# Access element values
mo.md(f"Name: {elements['name'].value}, Age: {elements['age'].value}")
```

#### 3. Embed a dynamic number of UI elements in another output

```python
import marimo as mo

n_items = mo.ui.number(1, 5, value=3, label="Number of items")
items = mo.ui.array([mo.ui.text(placeholder=f"Item {i+1}") for i in range(n_items.value)])

mo.md(f"""
**My List:**

* {items[0]}
* {items[1]}
* {items[2]}
""")
```

#### 4. Create a `hstack` (or `vstack`) of UI elements with `on_change` handlers

```python
import marimo as mo

def handle_click(value, index):
    mo.md(f"Button {index} clicked!")

buttons = mo.ui.array(
    [mo.ui.button(label=f"Button {i}", on_change=lambda v, i=i: handle_click(v, i)) 
     for i in range(3)]
)
mo.hstack(buttons)
```

#### 5. Create a table column of buttons with `on_change` handlers

```python
import marimo as mo

def handle_click(value, row_index):
    mo.md(f"Button clicked for row {row_index}")

buttons = mo.ui.array(
    [mo.ui.button(label="Click me", on_change=lambda v, i=i: handle_click(v, i)) 
     for i in range(3)]
)

mo.ui.table({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Action': buttons
})
```

#### 6. Create a form with multiple UI elements

```python
import marimo as mo

form = mo.md(
    """
    **User Details**
    
    Name: {name}
    Age: {age}
    """
).batch(
    name=mo.ui.text(label="Name"),
    age=mo.ui.number(0, 100, label="Age")
).form()
form

# Access form values after submission
mo.md(f"Name: {form.value['name']}, Age: {form.value['age']}")
```

### Working with Buttons

#### 1. Create a button that triggers computation when clicked

```python
import marimo as mo
import random

run_button = mo.ui.run_button(label="Generate Random Number")
run_button

# This cell only runs when the button is clicked
mo.stop(not run_button.value, "Click 'Generate' to get a random number")
mo.md(f"Random number: {random.randint(0, 100)}")
```

#### 2. Create a counter button

```python
import marimo as mo

counter_button = mo.ui.button(value=0, on_click=lambda count: count + 1, label="Count")
counter_button

# Display the count
mo.md(f"Count: {counter_button.value}")
```

#### 3. Create a toggle button

```python
import marimo as mo

toggle_button = mo.ui.button(value=False, on_click=lambda state: not state, label="Toggle")
toggle_button

# Display the toggle state
mo.md(f"State: {'On' if toggle_button.value else 'Off'}")
```

#### 4. Re-run a cell when a button is pressed

```python
import marimo as mo
import random

refresh_button = mo.ui.button(label="Refresh")
refresh_button

# This cell reruns when the button is clicked
refresh_button
mo.md(f"Random number: {random.randint(0, 100)}")
```

#### 5. Run a cell when a button is pressed, but not before

```python
import marimo as mo

counter_button = mo.ui.button(value=0, on_click=lambda count: count + 1, label="Click to Continue")
counter_button

# Only run this cell after the button is clicked
mo.stop(counter_button.value == 0, "Click the button to continue.")
mo.md("You clicked the button!")
```

#### 6. Reveal an output when a button is pressed

```python
import marimo as mo

show_button = mo.ui.button(label="Show Output")
show_button

# Reveal output only after button click
mo.md("This is the hidden output!") if show_button.value else None
```

### Caching

#### 1. Cache expensive computations

```python
import marimo as mo
import functools
import time

@functools.cache
def expensive_function(x):
    time.sleep(2)  # Simulate a long computation
    return x * 2

# Call the function multiple times with the same argument
result1 = expensive_function(5)
result2 = expensive_function(5)  # This will be retrieved from the cache

mo.md(f"Result 1: {result1}, Result 2: {result2}")
```

These concise examples provide practical illustrations of various recipes, showcasing how Marimo can be used to create interactive, dynamic, and efficient notebooks.
