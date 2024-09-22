import marimo

__generated_with = "0.8.18"
app = marimo.App(width="full")


@app.cell
def __():
    import random
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    from vega_datasets import data
    import io
    import altair as alt
    return alt, data, io, mo, pd, plt, random


@app.cell
def __(mo):
    mo.md(
        """
        # Marimo Awesome Examples

        This notebook demonstrates various features and capabilities of Marimo. Explore the different sections to see how Marimo can be used for interactive data analysis, visualization, and more!

        ---
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 1. Basic UI Elements

        ---
        """
    )
    return


@app.cell
def __(mo):
    slider = mo.ui.slider(1, 10, value=5, label="Slider Example")
    checkbox = mo.ui.checkbox(label="Checkbox Example")
    text_input = mo.ui.text(placeholder="Enter text here", label="Text Input Example")

    mo.vstack([slider, checkbox, text_input])
    return checkbox, slider, text_input


@app.cell
def __(checkbox, mo, slider, text_input):
    mo.md(
        f"""
    Slider value: {slider.value}
    Checkbox state: {checkbox.value}
    Text input: {text_input.value}
    Slider * Text input: {slider.value * "⭐️"}
    """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## 2. Reactive Data Visualization
        ---
        """
    )
    return


@app.cell
def __(mo, pd):
    # Create a sample dataset
    sample_df = pd.DataFrame(
        {"x": range(1, 11), "y": [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]}
    )

    plot_type = mo.ui.dropdown(
        options=["scatter", "line", "bar"], value="scatter", label="Select Plot Type"
    )

    mo.vstack(
        [
            plot_type,
            # mo.ui.table(sample_df, selection=None)
        ]
    )
    return plot_type, sample_df


@app.cell
def __(mo, plot_type, plt, sample_df):
    plt.figure(figsize=(10, 6))

    if plot_type.value == "scatter":
        plt.scatter(sample_df["x"], sample_df["y"])
    elif plot_type.value == "line":
        plt.plot(sample_df["x"], sample_df["y"])
    else:
        plt.bar(sample_df["x"], sample_df["y"])

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"{plot_type.value.capitalize()} Plot")
    mo.mpl.interactive(plt.gcf())
    return


@app.cell
def __(mo):
    mo.md("""## 3. Conditional Output and Control Flow""")
    return


@app.cell
def __(mo):
    show_secret = mo.ui.checkbox(label="Show Secret Message")
    show_secret
    return (show_secret,)


@app.cell
def __(mo, show_secret):
    mo.stop(not show_secret.value, mo.md("Check the box to reveal the secret message!"))
    mo.md(
        "🎉 Congratulations! You've unlocked the secret message: Marimo is awesome! 🎉"
    )
    return


@app.cell
def __(mo):
    mo.md("""## 4. File Handling and Data Processing""")
    return


@app.cell
def __(mo):
    file_upload = mo.ui.file(label="Upload a CSV file")
    file_upload
    return (file_upload,)


@app.cell
def __(file_upload, io, mo, pd):
    mo.stop(
        not file_upload.value, mo.md("Please upload a CSV file to see the preview.")
    )

    uploaded_df = pd.read_csv(io.BytesIO(file_upload.value[0].contents))
    mo.md(f"### Uploaded File Preview")
    mo.ui.table(uploaded_df)
    return (uploaded_df,)


@app.cell
def __(mo):
    mo.md("""## 5. Advanced UI Components""")
    return


@app.cell
def __(mo, pd):
    accordion = mo.accordion(
        {
            "Section 1": mo.md("This is the content of section 1."),
            "Section 2": mo.ui.slider(0, 100, value=50, label="Nested Slider"),
            "Section 3": mo.ui.table(pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})),
        }
    )
    accordion
    return (accordion,)


@app.cell
def __(mo):
    tabs = mo.ui.tabs(
        {
            "Tab 1": mo.md("Content of Tab 1"),
            "Tab 2": mo.ui.button(label="Click me!"),
            "Tab 3": mo.mermaid(
                """
        graph TD
        A[Start] --> B{Decision}
        B -->|Yes| C[Do Something]
        B -->|No| D[Do Nothing]
        C --> E[End]
        D --> E
        """
            ),
        }
    )
    tabs
    return (tabs,)


@app.cell
def __(mo):
    mo.md("""## 6. Batch Operations and Forms""")
    return


@app.cell
def __(mo):
    user_form = (
        mo.md(
            """
    ### User Information Form

    First Name: {first_name}
    Last Name: {last_name}
    Age: {age}
    Email: {email}
    """
        )
        .batch(
            first_name=mo.ui.text(label="First Name"),
            last_name=mo.ui.text(label="Last Name"),
            age=mo.ui.number(start=0, stop=120, label="Age"),
            email=mo.ui.text(label="Email"),
        )
        .form()
    )

    user_form
    return (user_form,)


@app.cell
def __(mo, user_form):
    mo.stop(
        not user_form.value.get("first_name"),
        mo.md("Please submit the form to see the results."),
    )

    mo.md(
        f"""
    ### Submitted Information

    - **First Name:** {user_form.value['first_name']}
    - **Last Name:** {user_form.value['last_name']}
    - **Age:** {user_form.value['age']}
    - **Email:** {user_form.value['email']}
    """
    )
    return


@app.cell
def __(mo):
    mo.md("""## 7. Embedding External Content""")
    return


@app.cell
def __(mo):
    mo.image("https://marimo.io/logo.png", width=200, alt="Marimo Logo")
    return


@app.cell
def __(mo):
    mo.video(
        "https://v3.cdnpk.net/videvo_files/video/free/2013-08/large_watermarked/hd0992_preview.mp4",
        width=560,
        height=315,
    )
    return


@app.cell
def __(mo):
    mo.md("""## 8. Custom Styling and Layouts""")
    return


@app.cell
def __(mo):
    styled_text = mo.md(
        """
    # Custom Styled Header

    This text has custom styling applied.
    """
    ).style(
        {
            "font-style": "italic",
            "background-color": "#aaa",
            "padding": "10px",
            "border-radius": "5px",
        },
    )

    styled_text
    return (styled_text,)


@app.cell
def __(mo):
    layout = mo.vstack(
        [
            mo.hstack(
                [
                    mo.md("Left Column").style(
                        {
                            "background-color": "#e0e0e0",
                            "padding": "10px",
                        }
                    ),
                    mo.md("Right Column").style(
                        {
                            "background-color": "#d0d0d0",
                            "padding": "10px",
                        }
                    ),
                ]
            ),
            mo.md("Bottom Row").style(
                {"background-color": "#c0c0c0", "padding": "10px"}
            ),
        ]
    )

    layout
    return (layout,)


@app.cell
def __(mo):
    mo.md(
        """
        ## 9. Interactive Data Exploration
        ---
        """
    )
    return


@app.cell
def __(data, mo):
    cars = data.cars()
    mo.ui.data_explorer(cars)
    return (cars,)


@app.cell
def __(alt, data, mo):
    chart = (
        alt.Chart(data.cars())
        .mark_circle()
        .encode(
            x="Horsepower",
            y="Miles_per_Gallon",
            color="Origin",
            tooltip=["Name", "Origin", "Horsepower", "Miles_per_Gallon"],
        )
        .interactive()
    )

    mo.ui.altair_chart(chart)
    return (chart,)


@app.cell
def __(mo):
    mo.md(
        """
        ## Conclusion

        This notebook has demonstrated various features and capabilities of Marimo. From basic UI elements to advanced data visualization and interactive components, Marimo provides a powerful toolkit for creating dynamic and engaging notebooks.

        Explore the code in each cell to learn more about how these examples were created!
        """
    )
    return


if __name__ == "__main__":
    app.run()
