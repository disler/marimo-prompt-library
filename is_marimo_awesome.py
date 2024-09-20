import marimo

__generated_with = "0.8.17"
app = marimo.App(width="medium")


@app.cell
def __():
    import random
    import marimo as mo
    return mo, random


@app.cell
def __(mo):
    mo.md("""# Is Marimo Awesome?""")
    return


@app.cell
def __(mo):
    answer = mo.ui.slider(1, 10, value=8, label="How awesome is Marimo?")

    answer
    return answer,


@app.cell
def __(answer, mo):
    if answer.value == 10:
        result = "Absolutely! Marimo is super awesome! 🎉"
    elif answer.value >= 7:
        result = "Yes, Marimo is pretty awesome! 😊"
    elif answer.value >= 4:
        result = "Marimo is cool, but there's room for improvement. 🤔"
    else:
        result = "Hmm, maybe you need to explore Marimo more? 🧐"

    mo.md(f"## Result\n\n{result}")
    return result,


@app.cell
def __(mo):

    fact = mo.ui.button(value=False, label="Click to generate a random fact about Marimo", on_click=lambda v: not v)

    mo.md(f"""### Fun fact
    {fact}
    """)

    return fact,


@app.cell
def __(fact, mo, random):
    facts = [
        "Marimo allows for interactive data exploration.",
        "You can create reactive web apps with pure Python in Marimo.",
        "Marimo supports various UI elements like sliders, buttons, and more.",
        "Marimo notebooks are version control friendly.",
        "You can easily share Marimo apps with others."
    ]

    random_fact = random.choice(facts) if fact.value else ""
    mo.md(f"Value: {fact.value}.\n\n random fact: {random_fact}")
    return facts, random_fact


if __name__ == "__main__":
    app.run()
