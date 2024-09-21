# Marimo Cheat Sheet 0.2.5

## Install and Import

### Install
```bash
pip install marimo
```
```bash
marimo (open Marimo app) 
```
Open Safari 
```bash
http://localhost:8888
```
### Open Tutorials
```bash
marimo tutorial DITTS
```
### View Server Info
```bash
marimo tutorial --help
```
```bash
Create new notebook
```
```bash
> create notebook
```
```bash
ls lists directories
```
```bash
marimo export my_notebook.py
```
### Serve notebook as script
```bash
marimo serve my_notebook.py
```
### Serve notebook as app
```bash
marimo export my_notebook.json > your_notebook.py
```
```bash
Run jupyter server
```
```bash
jupyter notebook
```
```bash
marimo export my_notebook.json > your_notebook.py
```
### CLI Commands (MARIMO CLI)
```bash
marimo -p {PORT} NAME  
```
```bash
--p  {PORT}  SERVER to attach to.
```
```bash
--h --show home screen in the app.
```
```bash
--h  displays   Home screen in app.
```
```bash
marimo export my_notebook.json > your_notebook.py
```
**Server Port Tips**:
```bash
If a port is busy use --port option. Server should start with /, /app subfolder. Use CLI or URL to access.
```
### Run server and exit. 
[GitHub](https://github.com/tithyhs/marimo-cheat-sheet)  
[Docs](http://docs.marimo.io)

## Inputs
```python
# Array of ID elements
ctlA.get_value(df.id),  ctlC.set()  

# Add new elements with sample label labels[]
new_labels.add('example_label'),['label'],['tag',C.init()])

# Buttons with optional on-click
m.ui_buttons(labels=[‘Ok’, 9], Labeled=‘Click Me’, m.ui_onclick('on_click'))

# Basic checkbox layout
ctl_inputs.add(['label':('Check me')])

# Combo box code
def_code_box[selector='dropdown',['shown']])

# Dataframe code: column_names df.columns.labels df.cf.head()]
df_render_data(df,'render_data','visualizations']

# Dictionary
m.ui_dictionary([‘text’:‘No.1 Column’, ‘data’: m.ui.set(df)])
```
#### Set Dropdown

```python
# Slider
m.ui_checkbox(['id_range=[‘1’,‘Choice 2’]', ‘Choice 2'])
```
#### Multi Dropdown

```python
m.ui_multiselect(options=['Basic',3,'Row 5'])
```
### Table output

```python
table().rows=['Header',['Example 1'5,‘Item 2’])
```
#### Expand
```python
rows(), show_folded_value()
```
## MarkDown
```markdown
## Music markdown

- # 'Markdown Text' 
- ## Integrative Playlist - Start
```
```bash
 m.link('https://spotify' }])
```
**Text Positioning**  
```python
m.md_text('Hello world') ])
```
```python
m.md_link('Playlist URL  ')
```
Zoom in  
```python
m_md_zoom ]
```
```python
m.md_add_input_code(`music-rocker`)`
```
```markdown
- **Use Syntax:**
'|data_content',['m.md_render('Tooltip-Hello')])
```
```markdown
Code Syntax:
‘’`
```
## Outputs
```python
# Replace cell's output  
m.output_replace(‘cell_output2’)

# Append data cell
m_output(append_cell('cell-output3’)
```
## Plotting
```python
# Create Axis chart
chart.plot(df_chart_data()).axis(['figure_color='],‘Width_px,G.title['Origin'])

# Add chart (after show function)
 m.axis_chart([],function_completed)

# Chart as Plotly interactive
axis_chart_loader['function_return_chart'])
```
```python
m.set.axis.plot(figure_data['canvas']).plot.chart.[sizes=s,parameter=plots])

m.plot_data(plt.D3,[],[interactive() ])
```
### Plot

```python
plt.axis(['Start Plot'])
``` 
## Media
### Render an image

```python
m.md_image({‘File.jpg’})
‘Image description’=[m.md_title_image-].add-Image id:to_800)
```
Add Markdown Media:
```python
m.media_add(video‘video_display  ]])
m_media.stream({'Source_load-[‘MP4')})
```
```python
img_embed=[m.youtube_link].render.{MP4’],embed[call]).allow('toggle_toolbar()’))
```
Embed Audio
```python
md.audio(‘audio_name', 'path.mp3')

m.md_figure.img_reference.link'
```
## Diagrams
### Define Diagram
```python
m_diag_define(m.diagram_structure].create()
 
# Label
diagram_diagram('Line path',['Node Arrow'])
``` 
### Showing simple path
```python
simple_showchart='Example Path', ‘label','Diagonal_top'])
``` 
```python
path_node]-(vertical_direction)]
``` 
## Status
```python
# Progress bars
 progress_text(‘task-subtitle-updating.progress’)  

[Fetching Data]
[please_processing_title_loadtext_spinner.png]
```
#### Time Display Progress  
```python
time.sleep(['progress_loader'])
```
## Control Flow
```python
# If/Else Looping State Variables
# Call cell_state.log (['iteration_num=0)
```
```python
# Ends current loop iteration/executes cell 
```  
```python
def.goto(‘state=cell_suspended’)
ctl_current({state}).wait()  
```
## State
### State Management Code

```python
ctl_set.state=[]['C.State']
 ctl_render_type(['current_frame_reset()])
# toggle state
ctl_state]
```
## HTML  
### Convert Python to HTML
```python
html_cell.add(html.tags()```
html_justified
```
```python
 m.html_create_wrapper
def(fixalignment_item])

# Apply single batch to cell
html.md_wrap.applyAlign(color)
```
### Set Justify  
 ```python 
html_tag.set='center]
```
## Debug
### Debugging cell output:
```python
ctl_debug().output
m.debug.retrieve_debug().info
```
### Inspect Execution Code
```python
 ctl_last.debug()
``` 
[GitHub](https://github.com/tithyhs/marimo-cheat-sheet)  
[Docs](http://docs.marimo.io)