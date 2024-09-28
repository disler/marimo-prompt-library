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
def __(prompt_library_module):
    map_testable_prompts: dict = prompt_library_module.pull_in_testable_prompts()
    return (map_testable_prompts,)


@app.cell
def __(llm_module):
    llm_o1_mini, llm_o1_preview = llm_module.build_o1_series()
    llm_gpt_4o_latest, llm_gpt_4o_mini = llm_module.build_openai_latest_and_fastest()
    llm_sonnet = llm_module.build_sonnet_3_5()
    gemini_1_5_pro, gemini_1_5_flash = llm_module.build_gemini_duo()
    gemini_1_5_pro_2, gemini_1_5_flash_2 = llm_module.build_gemini_1_2_002()
    llama3_2_model, llama3_2_1b_model = llm_module.build_ollama_models()

    models = {
        "o1-mini": llm_o1_mini,
        "o1-preview": llm_o1_preview,
        "gpt-4o-latest": llm_gpt_4o_latest,
        "gpt-4o-mini": llm_gpt_4o_mini,
        "sonnet-3.5": llm_sonnet,
        "gemini-1-5-pro": gemini_1_5_pro,
        "gemini-1-5-flash": gemini_1_5_flash,
        "gemini-1-5-pro-002": gemini_1_5_pro_2,
        "gemini-1-5-flash-002": gemini_1_5_flash_2,
        "llama3-2": llama3_2_model,
        "llama3-2-1b": llama3_2_1b_model,
    }
    return (
        gemini_1_5_flash,
        gemini_1_5_flash_2,
        gemini_1_5_pro,
        gemini_1_5_pro_2,
        llama3_2_1b_model,
        llama3_2_model,
        llm_gpt_4o_latest,
        llm_gpt_4o_mini,
        llm_o1_mini,
        llm_o1_preview,
        llm_sonnet,
        models,
    )


@app.cell
def __(map_testable_prompts, mo, models):
    prompt_multiselect = mo.ui.multiselect(
        options=list(map_testable_prompts.keys()),
        label="Select Prompts",
    )
    prompt_temp_slider = mo.ui.slider(
        start=0, stop=1, value=0.5, step=0.05, label="Temp"
    )
    model_multiselect = mo.ui.multiselect(
        options=models.copy(),
        label="Models",
        value=["gpt-4o-mini", "llama3-2", "gemini-1-5-flash-002"],
    )
    return model_multiselect, prompt_multiselect, prompt_temp_slider


@app.cell
def __():
    prompt_style = {
        "background": "#eee",
        "padding": "10px",
        "border-radius": "10px",
        "margin-bottom": "20px",
    }
    return (prompt_style,)


@app.cell
def __(mo, model_multiselect, prompt_multiselect, prompt_temp_slider):
    form = (
        mo.md(
            r"""
            # Multi Language Model Ranker 📊
            {prompts}
            {temp}
            {models}
            """
        )
        .batch(
            prompts=prompt_multiselect,
            temp=prompt_temp_slider,
            models=model_multiselect,
        )
        .form()
    )
    form
    return (form,)


@app.cell
def __(form, mo, prompt_style):
    mo.stop(not form.value)

    selected_models_string = mo.ui.array([mo.ui.text(value=m.model_id, disabled=True) for m in form.value['models']])
    selected_prompts_string = mo.ui.array([mo.ui.text(value=p, disabled=True) for p in form.value['prompts']])

    mo.vstack([
        mo.md("## Selected Models"),
        mo.hstack(selected_models_string, align="start", justify="start"),
        mo.md("## Selected Prompts"),
        mo.hstack(selected_prompts_string, align="start", justify="start")
    ]).style(prompt_style)
    return selected_models_string, selected_prompts_string


@app.cell
def __(form, llm_module, map_testable_prompts, mo, prompt_library_module):
    mo.stop(not form.value, "")

    all_prompt_responses = []

    total_executions = len(form.value["prompts"]) * len(form.value["models"])

    with mo.status.progress_bar(
        title="Running prompts on selected models...",
        total=total_executions,
        remove_on_exit=True,
    ) as prog_bar:
        for selected_prompt_name in form.value["prompts"]:
            selected_prompt = map_testable_prompts[selected_prompt_name]
            prompt_responses = []

            for model in form.value["models"]:
                model_name = model.model_id
                prog_bar.update(title=f"Prompting '{model_name}' with '{selected_prompt_name}'", increment=1)
                response = llm_module.prompt_with_temp(
                    model, selected_prompt, form.value["temp"]
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
                prompt=selected_prompt,
                list_model_execution_dict=list_model_execution_dict,
                prompt_template=selected_prompt_name,
            )
            print(f"Execution record saved to: {execution_filepath}")

            all_prompt_responses.append({
                "prompt_name": selected_prompt_name,
                "prompt": selected_prompt,
                "responses": prompt_responses,
                "execution_filepath": execution_filepath,
            })
    return (
        all_prompt_responses,
        execution_filepath,
        list_model_execution_dict,
        model,
        model_name,
        prog_bar,
        prompt_responses,
        response,
        selected_prompt,
        selected_prompt_name,
        total_executions,
    )


@app.cell
def __(all_prompt_responses, mo, prompt_style, pyperclip):
    def copy_to_clipboard(text):
        print("copying: ", text)
        pyperclip.copy(text)
        return 1

    all_prompt_elements = []

    for prompt_data in all_prompt_responses:
        prompt_output_elements = [
            mo.vstack(
                [
                    mo.md(f"## {response['model_id']}"),
                    mo.md(response["output"]),
                ]
            ).style(prompt_style)
            for response in prompt_data['responses']
        ]


        prompt_element = mo.vstack([
            mo.md(f"# Prompt: {prompt_data['prompt_name']}"),
            mo.hstack(prompt_output_elements),
        ])

        all_prompt_elements.append(prompt_element)

    mo.vstack(all_prompt_elements)
    return (
        all_prompt_elements,
        copy_to_clipboard,
        prompt_data,
        prompt_element,
        prompt_output_elements,
    )


@app.cell
def __():
    # all_prompt_responses
    return


@app.cell
def __(all_prompt_responses, copy_to_clipboard, mo):
    prompt_copy_buttons = []
    for i, _prompt_data in enumerate(all_prompt_responses):
        prompt_buttons = mo.ui.array([
            mo.ui.button(
                label=f"Copy {response['model_id']} response",
                on_click=lambda v, i=i, j=j: copy_to_clipboard(all_prompt_responses[i]['responses'][j]['output']),
                value=(i, j)
            )
            for j, response in enumerate(_prompt_data['responses'])
        ])
        prompt_copy_buttons.append(mo.vstack([
            mo.md(f"### {_prompt_data['prompt_name']}"),
            mo.hstack(prompt_buttons)
        ]))

    mo.vstack(prompt_copy_buttons)
    return i, prompt_buttons, prompt_copy_buttons


if __name__ == "__main__":
    app.run()
