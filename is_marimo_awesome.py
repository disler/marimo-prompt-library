import marimo

__generated_with = "0.8.17"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return mo,


@app.cell
def __(mo):
    mo.md(r"""Testing out markdown here""")
    return


if __name__ == "__main__":
    app.run()
