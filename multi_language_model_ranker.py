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
    # llm_sonnet = llm_module.build_sonnet_3_5()
    # gemini_1_5_pro, gemini_1_5_flash = llm_module.build_gemini_duo()
    # gemini_1_5_pro_2, gemini_1_5_flash_2 = llm_module.build_gemini_1_2_002()
    # llama3_2_model, llama3_2_1b_model = llm_module.build_ollama_models()
    # _, phi3_5_model, qwen2_5_model = llm_module.build_ollama_slm_models()

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
        # "phi3-5": phi3_5_model,
        # "qwen2-5": qwen2_5_model,
    }
    return (
        llm_gpt_4o_latest,
        llm_gpt_4o_mini,
        llm_o1_mini,
        llm_o1_preview,
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
        value=["gpt-4o-mini",],
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
def __(form, map_testable_prompts, mo, prompt_style):
    mo.stop(not form.value)

    selected_models_string = mo.ui.array(
        [mo.ui.text(value=m.model_id, disabled=True) for m in form.value["models"]]
    )

    selected_prompts_accordion = mo.accordion(
        {
            prompt: mo.md(f"```xml\n{map_testable_prompts[prompt]}\n```")
            for prompt in form.value["prompts"]
        }
    )

    mo.vstack(
        [
            mo.md("## Selected Models"),
            mo.hstack(selected_models_string, align="start", justify="start"),
            mo.md("## Selected Prompts"),
            selected_prompts_accordion,
        ]
    ).style(prompt_style)
    return selected_models_string, selected_prompts_accordion


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
def __(all_prompt_responses, mo, pyperclip):
    mo.stop(not all_prompt_responses, mo.md(""))

    def copy_to_clipboard(text):
        print("copying: ", text)
        pyperclip.copy(text)
        return 1

    all_prompt_elements = []

    output_prompt_style = {
        "background": "#eee",
        "padding": "10px",
        "border-radius": "10px",
        "margin-bottom": "20px",
        "min-width": "200px",
        "box-shadow": "2px 2px 2px #ccc",
    }

    for loop_prompt_data in all_prompt_responses:
        prompt_output_elements = [
            mo.vstack(
                [
                    mo.md(f"#### {response['model_id']}").style(
                        {"font-weight": "bold"}
                    ),
                    mo.md(response["output"]),
                ]
            ).style(output_prompt_style)
            for response in loop_prompt_data["responses"]
        ]

        prompt_element = mo.vstack(
            [
                mo.md(f"### Prompt: {loop_prompt_data['prompt_name']}"),
                mo.hstack(prompt_output_elements, wrap=True, justify="start"),
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
        output_prompt_style,
        prompt_element,
        prompt_output_elements,
    )


@app.cell
def __(all_prompt_responses, copy_to_clipboard, form, mo):
    mo.stop(not all_prompt_responses, mo.md(""))
    mo.stop(not form.value, mo.md(""))

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
        page_size=30,
        label="Model Responses",
        format_mapping={
            "Output": lambda val: "(trimmed) " + val[:15],
            # "Output": lambda val: val,
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

    # Create the run buttons
    copy_button = mo.ui.run_button(label="🔗 Copy Selected Outputs")
    score_button = mo.ui.run_button(label="👍 Vote Selected Outputs")

    # Display the table and run buttons
    mo.vstack(
        [
            results_table,
            mo.hstack(
                [
                    score_button,
                    copy_button,
                ],
                justify="start",
            ),
        ]
    )
    return (
        copy_button,
        copy_selected_outputs,
        prompt_data,
        response,
        results_table,
        score_button,
        table_data,
    )


@app.cell
def __(
    copy_to_clipboard,
    get_rankings,
    mo,
    prompt_library_module,
    results_table,
    score_button,
    set_rankings,
):
    mo.stop(not results_table.value, "")

    selected_rows = results_table.value
    outputs = [row["Output"] for row in selected_rows]
    combined_output = "\n\n".join(outputs)

    if score_button.value:
        # Increment scores for selected models
        current_rankings = get_rankings()
        for row in selected_rows:
            model_id = row["Model"]
            for ranking in current_rankings:
                if ranking.llm_model_id == model_id:
                    ranking.score += 1
                    break

        # Save updated rankings
        set_rankings(current_rankings)
        prompt_library_module.save_rankings(current_rankings)

        mo.md(f"Scored {len(selected_rows)} model(s)")
    else:
        copy_to_clipboard(combined_output)
        mo.md(f"Copied {len(outputs)} response(s) to clipboard")
    return (
        combined_output,
        current_rankings,
        model_id,
        outputs,
        ranking,
        row,
        selected_rows,
    )


@app.cell
def __(all_prompt_responses, form, mo, prompt_library_module):
    mo.stop(not form.value, mo.md(""))
    mo.stop(not all_prompt_responses, mo.md(""))

    # Create buttons for resetting and loading rankings
    reset_ranking_button = mo.ui.run_button(label="❌ Reset Rankings")
    load_ranking_button = mo.ui.run_button(label="🔐 Load Rankings")

    # Load existing rankings
    get_rankings, set_rankings = mo.state(prompt_library_module.get_rankings())

    mo.hstack(
        [
            load_ranking_button,
            reset_ranking_button,
        ],
        justify="start",
    )
    return (
        get_rankings,
        load_ranking_button,
        reset_ranking_button,
        set_rankings,
    )


@app.cell
def __():
    # get_rankings()
    return


@app.cell
def __(
    form,
    mo,
    prompt_library_module,
    reset_ranking_button,
    set_rankings,
):
    mo.stop(not form.value, mo.md(""))
    mo.stop(not reset_ranking_button.value, mo.md(""))

    set_rankings(
        prompt_library_module.reset_rankings(
            [model.model_id for model in form.value["models"]]
        )
    )

    # mo.md("Rankings reset successfully")
    return


@app.cell
def __(form, load_ranking_button, mo, prompt_library_module, set_rankings):
    mo.stop(not form.value, mo.md(""))
    mo.stop(not load_ranking_button.value, mo.md(""))

    set_rankings(prompt_library_module.get_rankings())
    return


@app.cell
def __(get_rankings, mo):
    # Create UI elements for each model
    model_elements = []

    model_score_style = {
        "background": "#eeF",
        "padding": "10px",
        "border-radius": "10px",
        "margin-bottom": "20px",
        "min-width": "150px",
        "box-shadow": "2px 2px 2px #ccc",
    }

    for model_ranking in get_rankings():
        llm_model_id = model_ranking.llm_model_id
        score = model_ranking.score
        model_elements.append(
            mo.vstack(
                [
                    mo.md(f"**{llm_model_id}**  "),
                    mo.hstack([mo.md(f""), mo.md(f"# {score}")]),
                ],
                justify="space-between",
                gap="2",
            ).style(model_score_style)
        )

    mo.hstack(model_elements, justify="start", wrap=True)
    return (
        llm_model_id,
        model_elements,
        model_ranking,
        model_score_style,
        score,
    )


if __name__ == "__main__":
    app.run()
