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

    selected_models_string = mo.ui.array(
        [mo.ui.text(value=m.model_id, disabled=True) for m in form.value["models"]]
    )
    selected_prompts_string = mo.ui.array(
        [mo.ui.text(value=p, disabled=True) for p in form.value["prompts"]]
    )

    mo.vstack(
        [
            mo.md("## Selected Models"),
            mo.hstack(selected_models_string, align="start", justify="start"),
            mo.md("## Selected Prompts"),
            mo.hstack(selected_prompts_string, align="start", justify="start"),
        ]
    ).style(prompt_style)
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
                prog_bar.update(
                    title=f"Prompting '{model_name}' with '{selected_prompt_name}'",
                    increment=1,
                )
                raw_prompt_response = llm_module.prompt_with_temp(
                    model, selected_prompt, form.value["temp"]
                )
                prompt_responses.append(
                    {
                        "model_id": model_name,
                        "model": model,
                        "output": raw_prompt_response,
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

            all_prompt_responses.append(
                {
                    "prompt_name": selected_prompt_name,
                    "prompt": selected_prompt,
                    "responses": prompt_responses,
                    "execution_filepath": execution_filepath,
                }
            )
    return (
        all_prompt_responses,
        execution_filepath,
        list_model_execution_dict,
        model,
        model_name,
        prog_bar,
        prompt_responses,
        raw_prompt_response,
        selected_prompt,
        selected_prompt_name,
        total_executions,
    )


@app.cell
def __(all_prompt_responses, mo, prompt_style, pyperclip):
    mo.stop(not all_prompt_responses, mo.md(""))

    def copy_to_clipboard(text):
        print("copying: ", text)
        pyperclip.copy(text)
        return 1

    all_prompt_elements = []

    for loop_prompt_data in all_prompt_responses:
        prompt_output_elements = [
            mo.vstack(
                [
                    mo.md(f"#### {response['model_id']}"),
                    mo.md(response["output"]),
                ]
            ).style(prompt_style)
            for response in loop_prompt_data["responses"]
        ]

        prompt_element = mo.vstack(
            [
                mo.md(f"### Prompt: {loop_prompt_data['prompt_name']}"),
                mo.hstack(prompt_output_elements),
            ]
        ).style(
            {
                "border-left": "4px solid #CCC",
                "padding": "2px 10px",
                "background": "#ffffee",
            }
        )

        all_prompt_elements.append(prompt_element)

    mo.vstack(all_prompt_elements)
    return (
        all_prompt_elements,
        copy_to_clipboard,
        loop_prompt_data,
        prompt_element,
        prompt_output_elements,
    )


@app.cell
def __(all_prompt_responses, copy_to_clipboard, mo):
    mo.stop(not all_prompt_responses, mo.md(""))


    # Prepare data for the table
    table_data = []
    for prompt_data in all_prompt_responses:
        for response in prompt_data["responses"]:
            table_data.append(
                {
                    "Prompt": prompt_data["prompt_name"],
                    "Model": response["model_id"],
                    "Output": response["output"],
                }
            )

    # Create the table
    results_table = mo.ui.table(
        data=table_data,
        pagination=True,
        selection="multi",
        page_size=10,
        label="Model Responses",
        format_mapping={
            "Output": lambda val: "(trimmed) " + val[:5],
        },
    )

    # Function to copy selected outputs to clipboard
    def copy_selected_outputs():
        selected_rows = results_table.value
        if selected_rows:
            outputs = [row["Output"] for row in selected_rows]
            combined_output = "\n\n".join(outputs)
            copy_to_clipboard(combined_output)
            return f"Copied {len(outputs)} response(s) to clipboard"
        return "No rows selected"

    # Create the run button
    run_button = mo.ui.run_button(label="Copy Selected Outputs")

    # Display the table and run button
    mo.vstack([results_table, run_button])
    return (
        copy_selected_outputs,
        prompt_data,
        response,
        results_table,
        run_button,
        table_data,
    )


@app.cell
def __(prompt_library_module):
    _rankings = prompt_library_module.pull_in_language_model_rankings()
    _rankings
    return


@app.cell
def __(form, mo, prompt_library_module):
    mo.stop(not form.value, mo.md(""))

    # Create an input field for new ranking name
    new_ranking_input = mo.ui.text(label="New ranking name")

    # Create buttons for creating and loading rankings
    create_ranking_button = mo.ui.run_button(label="Create Ranking")
    load_ranking_button = mo.ui.run_button(label="Load Ranking")

    # Load existing rankings
    get_rankings, set_rankings = mo.state(prompt_library_module.pull_in_language_model_rankings())

    # Create a dropdown for existing rankings
    ranking_dropdown = mo.ui.dropdown(
        options=list(get_rankings().keys()), label="Select existing ranking"
    )

    mo.hstack([new_ranking_input, create_ranking_button, ranking_dropdown, load_ranking_button])
    return (
        create_ranking_button,
        get_rankings,
        load_ranking_button,
        new_ranking_input,
        ranking_dropdown,
        set_rankings,
    )


@app.cell
def __(
    create_ranking_button,
    form,
    mo,
    new_ranking_input,
    prompt_library_module,
    set_rankings,
):
    mo.stop(not form.value, mo.md("no form values"))
    mo.stop(not create_ranking_button.value, mo.md("awaiting create click"))
    mo.stop(not new_ranking_input.value, mo.md("enter a name for the new ranking"))

    _current_ranking_name = new_ranking_input.value
    _current_ranking = prompt_library_module.new_rankings_file([model.model_id for model in form.value["models"]])
    prompt_library_module.upsert_rankings_file(_current_ranking_name, _current_ranking)

    set_rankings(lambda v: prompt_library_module.pull_in_language_model_rankings())

    mo.md(f"Created new ranking: '{_current_ranking_name}'")
    return


@app.cell
def __(
    form,
    load_ranking_button,
    mo,
    prompt_library_module,
    ranking_dropdown,
    rankings,
):
    mo.stop(not form.value, mo.md("no form values"))
    mo.stop(not load_ranking_button.value, mo.md("awaiting load click"))
    mo.stop(not ranking_dropdown.value, mo.md("select a ranking to load"))

    current_ranking_name = ranking_dropdown.value
    current_ranking = rankings[current_ranking_name]

    # Create UI elements for each model
    model_elements = []
    for model_ranking in current_ranking:
        llm_model_id = model_ranking["llm_model_id"]
        score = model_ranking["score"]

        stop_button = mo.ui.button(label=f"Stop {llm_model_id}")
        increment_button = mo.ui.button(label=f"Increment {llm_model_id}")
        score_display = mo.md(f"**Score:** {score}")

        model_elements.append(
            mo.hstack(
                [
                    mo.md(f"**{llm_model_id}**"),
                    score_display,
                    stop_button,
                    increment_button,
                ]
            )
        )

    # Function to handle increment button click
    def handle_increment(llm_model_id):
        for ranking in current_ranking:
            if ranking["llm_model_id"] == llm_model_id:
                ranking["score"] += 1
                break
        prompt_library_module.upsert_rankings_file(
            current_ranking_name, current_ranking
        )
        return current_ranking

    # Add event handlers to increment buttons
    for i, model_ranking in enumerate(current_ranking):
        model_elements[i].children[3].on_click(
            lambda _, i=i: handle_increment(current_ranking[i]["llm_model_id"])
        )

    mo.vstack(model_elements)
    return (
        current_ranking,
        current_ranking_name,
        handle_increment,
        i,
        increment_button,
        llm_model_id,
        model_elements,
        model_ranking,
        score,
        score_display,
        stop_button,
    )


@app.cell
def __(copy_to_clipboard, mo, results_table):
    mo.stop(not results_table.value, "No rows selected")

    selected_rows = results_table.value
    outputs = [row["Output"] for row in selected_rows]
    combined_output = "\n\n".join(outputs)
    copy_to_clipboard(combined_output)

    mo.md(f"Copied {len(outputs)} response(s) to clipboard")
    return combined_output, outputs, selected_rows


if __name__ == "__main__":
    app.run()
