import marimo

__generated_with = "0.8.18"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    from src.marimo_notebook.modules import llm_module
    import json
    return json, llm_module, mo


@app.cell
def __(llm_module):
    llm_o1_mini, llm_o1_preview = llm_module.build_o1_series()
    llm_gpt_4o_latest, llm_gpt_4o_mini = llm_module.build_openai_latest_and_fastest()
    # llm_sonnet = llm_module.build_sonnet_3_5()
    # gemini_1_5_pro, gemini_1_5_flash = llm_module.build_gemini_duo()

    models = {
        "o1-mini": llm_o1_mini,
        "o1-preview": llm_o1_preview,
        "gpt-4o-latest": llm_gpt_4o_latest,
        "gpt-4o-mini": llm_gpt_4o_mini,
        # "sonnet-3.5": llm_sonnet,
        # "gemini-1-5-pro": gemini_1_5_pro,
        # "gemini-1-5-flash": gemini_1_5_flash,
    }
    return (
        llm_gpt_4o_latest,
        llm_gpt_4o_mini,
        llm_o1_mini,
        llm_o1_preview,
        models,
    )


@app.cell
def __(mo, models):
    prompt_text_area = mo.ui.text_area(label="Prompt", full_width=True)
    prompt_temp_slider = mo.ui.slider(
        start=0, stop=1, value=0.5, step=0.05, label="Temp"
    )
    model_dropdown = mo.ui.dropdown(
        options=models.copy(),
        label="Model",
        value="gpt-4o-mini",
    )
    multi_model_checkbox = mo.ui.checkbox(label="Run on All Models", value=False)

    form = (
        mo.md(
            r"""
            # Ad-hoc Prompt
            {prompt}
            {temp}
            {model}
            {multi_model}
            """
        )
        .batch(
            prompt=prompt_text_area,
            temp=prompt_temp_slider,
            model=model_dropdown,
            multi_model=multi_model_checkbox,
        )
        .form()
    )
    form
    return (
        form,
        model_dropdown,
        multi_model_checkbox,
        prompt_temp_slider,
        prompt_text_area,
    )


@app.cell
def __(form, mo):
    mo.stop(not form.value or not len(form.value), "")

    # Format the form data for the table
    formatted_data = {}
    for key, value in form.value.items():
        if key == "model":
            formatted_data[key] = value.model_id
        elif key == "multi_model":
            formatted_data[key] = value
        else:
            formatted_data[key] = value

    # Create and display the table
    table = mo.ui.table(
        [formatted_data],  # Wrap in a list to create a single-row table
        label="",
        selection=None,
    )

    mo.md(f"# Form Values\n\n{table}")
    return formatted_data, key, table, value


@app.cell
def __(form, llm_module, mo):
    mo.stop(not form.value or form.value["multi_model"], "")

    prompt_response = None

    with mo.status.spinner(title="Loading..."):
        prompt_response = llm_module.prompt_with_temp(
            form.value["model"], form.value["prompt"], form.value["temp"]
        )

    mo.md(f"# Prompt Output\n\n{prompt_response}").style(
        {"background": "#eee", "padding": "10px", "border-radius": "10px"}
    )
    return (prompt_response,)


@app.cell
def __(form, llm_module, mo, models):
    prompt_responses = []

    mo.stop(not form.value or not form.value["multi_model"], "")

    with mo.status.spinner(title="Running prompts on all models..."):
        for model_name, model in models.items():
            response = llm_module.prompt_with_temp(
                model, form.value["prompt"], form.value["temp"]
            )
            prompt_responses.append(
                {
                    "model_id": model_name,
                    "output": response,
                }
            )
    return model, model_name, prompt_responses, response


@app.cell
def __(mo, prompt_responses):
    mo.stop(not len(prompt_responses), "")

    # Create a table using mo.ui.table
    multi_model_table = mo.ui.table(
        prompt_responses, label="Multi-Model Prompt Outputs", selection=None
    )

    mo.vstack(
        [
            mo.md("# Multi-Model Prompt Outputs"),
            mo.ui.table(prompt_responses, selection=None),
        ]
    )
    return (multi_model_table,)


if __name__ == "__main__":
    app.run()
