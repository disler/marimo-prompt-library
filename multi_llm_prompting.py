import marimo

__generated_with = "0.8.18"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    import src.marimo_notebook.modules.llm_module as llm_module
    import src.marimo_notebook.modules.prompt_library_module as prompt_library_module
    import json
    import pyperclip
    return json, llm_module, mo, prompt_library_module, pyperclip


@app.cell
def __(llm_module):
    llm_o1_mini, llm_o1_preview = llm_module.build_o1_series()
    llm_gpt_4o_latest, llm_gpt_4o_mini = llm_module.build_openai_latest_and_fastest()
    # llm_sonnet = llm_module.build_sonnet_3_5()
    # gemini_1_5_pro, gemini_1_5_flash = llm_module.build_gemini_duo()
    # gemini_1_5_pro_2, gemini_1_5_flash_2 = llm_module.build_gemini_1_2_002()
    # llama3_2_model, llama3_2_1b_model = llm_module.build_ollama_models()

    models = {
        "o1-mini": llm_o1_mini,
        "o1-preview": llm_o1_preview,
        "gpt-4o-latest": llm_gpt_4o_latest,
        "gpt-4o-mini": llm_gpt_4o_mini,
        # "sonnet-3.5": llm_sonnet,
        # "gemini-1-5-pro": gemini_1_5_pro,
        # "gemini-1-5-flash": gemini_1_5_flash,
        # "gemini-1-5-pro-002": gemini_1_5_pro_2,
        # "gemini-1-5-flash-002": gemini_1_5_flash_2,
        # "llama3-2": llama3_2_model,
        # "llama3-2-1b": llama3_2_1b_model,
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
    model_multiselect = mo.ui.multiselect(
        options=models.copy(),
        label="Models",
        value=["gpt-4o-mini"],
    )

    form = (
        mo.md(
            r"""
            # Multi-LLM Prompt
            {prompt}
            {temp}
            {models}
            """
        )
        .batch(
            prompt=prompt_text_area,
            temp=prompt_temp_slider,
            models=model_multiselect,
        )
        .form()
    )
    form
    return form, model_multiselect, prompt_temp_slider, prompt_text_area


@app.cell
def __(form, llm_module, mo, prompt_library_module):
    mo.stop(not form.value, "")

    prompt_responses = []

    with mo.status.progress_bar(
        title="Running prompts on selected models...",
        total=len(form.value["models"]),
        remove_on_exit=True,
    ) as prog_bar:
        # with mo.status.spinner(title="Running prompts on selected models...") as _spinner:
        for model in form.value["models"]:
            model_name = model.model_id
            prog_bar.update(title=f"Prompting '{model_name}'", increment=1)
            response = llm_module.prompt_with_temp(
                model, form.value["prompt"], form.value["temp"]
            )
            prompt_responses.append(
                {
                    "model_id": model_name,
                    "model": model,
                    "output": response,
                }
            )

    # Create a new list without the 'model' key for each response
    list_model_execution_dict = [
        {k: v for k, v in response.items() if k != "model"}
        for response in prompt_responses
    ]

    # Record the execution
    execution_filepath = prompt_library_module.record_llm_execution(
        prompt=form.value["prompt"],
        list_model_execution_dict=list_model_execution_dict,
        prompt_template=None,  # You can add a prompt template if you have one
    )
    print(f"Execution record saved to: {execution_filepath}")
    return (
        execution_filepath,
        list_model_execution_dict,
        model,
        model_name,
        prog_bar,
        prompt_responses,
        response,
    )


@app.cell
def __(mo, prompt_responses, pyperclip):
    def copy_to_clipboard(text):
        print("copying: ", text)
        pyperclip.copy(text)
        return mo.md("**Copied to clipboard!**").callout(kind="success")

    output_elements = [
        mo.vstack(
            [
                mo.md(f"# Prompt Output ({response['model_id']})"),
                mo.md(response["output"]),
            ]
        ).style(
            {
                "background": "#eee",
                "padding": "10px",
                "border-radius": "10px",
                "margin-bottom": "20px",
            }
        )
        for (idx, response) in enumerate(prompt_responses)
    ]

    mo.vstack(
        [
            mo.hstack(output_elements),
            # mo.hstack(output_elements, wrap=True),
            # mo.vstack(output_elements),
            # mo.carousel(output_elements),
            # mo.hstack(copy_buttons)
            # copy_buttons,
        ]
    )
    return copy_to_clipboard, output_elements


@app.cell
def __(copy_to_clipboard, mo, prompt_responses):
    copy_buttons = mo.ui.array(
        [
            mo.ui.button(
                label=f"Copy {response['model_id']} response",
                on_click=lambda v: copy_to_clipboard(prompt_responses[v]["output"]),
                value=idx,
            )
            for (idx, response) in enumerate(prompt_responses)
        ]
    )

    mo.vstack(copy_buttons, align="center")
    return (copy_buttons,)


if __name__ == "__main__":
    app.run()
