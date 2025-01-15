import marimo

__generated_with = "0.8.18"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    from src.marimo_notebook.modules import prompt_library_module, llm_module
    import re  # For regex to extract placeholders
    return llm_module, mo, prompt_library_module, re


@app.cell
def __(prompt_library_module):
    map_prompt_library: dict = prompt_library_module.pull_in_prompt_library()
    return (map_prompt_library,)


@app.cell
def __(llm_module):
    llm_o1_mini, llm_o1_preview = llm_module.build_o1_series()
    llm_gpt_4o_latest, llm_gpt_4o_mini = llm_module.build_openai_latest_and_fastest()
    mistral_model, phi4_14b_model, llama3_2_model = llm_module.build_ollama_models()
    llama_3_3_70b_versatile_model = llm_module.build_groq_models()

    models = {
        "o1-mini": llm_o1_mini,
        "o1-preview": llm_o1_preview,
        "gpt-4o-latest": llm_gpt_4o_latest,
        "gpt-4o-mini": llm_gpt_4o_mini,
        "phi4": phi4_14b_model,
        "mistral": mistral_model,
        "llama3.2": llama3_2_model,
        "groq:llama-3.3-70b-versatile": llama_3_3_70b_versatile_model,
    }
    return (
        llama3_2_model,
        llama_3_3_70b_versatile_model,
        llm_gpt_4o_latest,
        llm_gpt_4o_mini,
        llm_o1_mini,
        llm_o1_preview,
        mistral_model,
        models,
        phi4_14b_model,
    )


@app.cell
def __():
    prompt_styles = {"background": "#eee", "padding": "10px", "border-radius": "10px"}
    return (prompt_styles,)


@app.cell
def __(map_prompt_library, mo, models):
    prompt_keys = list(map_prompt_library.keys())
    prompt_dropdown = mo.ui.dropdown(
        options=prompt_keys,
        label="Select a Prompt",
    )
    model_dropdown = mo.ui.dropdown(
        options=models,
        label="Select an LLM Model",
        value="gpt-4o-mini",
    )
    form = (
        mo.md(
            r"""
            # Prompt Library
            {prompt_dropdown}
            {model_dropdown}
            """
        )
        .batch(
            prompt_dropdown=prompt_dropdown,
            model_dropdown=model_dropdown,
        )
        .form()
    )
    form
    return form, model_dropdown, prompt_dropdown, prompt_keys


@app.cell
def __(form, map_prompt_library, mo, prompt_styles):
    selected_prompt_name = None
    selected_prompt = None

    mo.stop(not form.value or not len(form.value), "")
    selected_prompt_name = form.value["prompt_dropdown"]
    selected_prompt = map_prompt_library[selected_prompt_name]
    mo.vstack(
        [
            mo.md("# Selected Prompt"),
            mo.accordion(
                {
                    "### Click to show": mo.md(f"```xml\n{selected_prompt}\n```").style(
                        prompt_styles
                    )
                }
            ),
        ]
    )
    return selected_prompt, selected_prompt_name


@app.cell
def __(mo, re, selected_prompt, selected_prompt_name):
    mo.stop(not selected_prompt_name or not selected_prompt, "")

    # Extract placeholders from the prompt
    placeholders = re.findall(r"\{\{(.*?)\}\}", selected_prompt)
    placeholders = list(set(placeholders))  # Remove duplicates

    # Create text areas for placeholders, using the placeholder text as the label
    placeholder_inputs = [
        mo.ui.text_area(label=ph, placeholder=f"Enter {ph}", full_width=True)
        for ph in placeholders
    ]

    # Create an array of placeholder inputs
    placeholder_array = mo.ui.array(
        placeholder_inputs,
        label="Fill in the Placeholders",
    )

    # Create a 'Proceed' button
    proceed_button = mo.ui.run_button(label="Prompt")

    # Display the placeholders and the 'Proceed' button in a vertical stack
    vstack = mo.vstack([mo.md("# Prompt Variables"), placeholder_array, proceed_button])
    vstack
    return (
        placeholder_array,
        placeholder_inputs,
        placeholders,
        proceed_button,
        vstack,
    )


@app.cell
def __(mo, placeholder_array, placeholders, proceed_button):
    mo.stop(not placeholder_array.value or not len(placeholder_array.value), "")

    # Check if any values are missing
    if any(not value.strip() for value in placeholder_array.value):
        mo.stop(True, mo.md("**Please fill in all placeholders.**"))

    # Ensure the 'Proceed' button has been pressed
    mo.stop(
        not proceed_button.value,
        mo.md("**Please press the 'Proceed' button to continue.**"),
    )

    # Map the placeholder names to the values
    filled_values = dict(zip(placeholders, placeholder_array.value))
    return (filled_values,)


@app.cell
def __(filled_values, selected_prompt):
    # Replace placeholders in the prompt
    final_prompt = selected_prompt
    for key, value in filled_values.items():
        final_prompt = final_prompt.replace(f"{{{{{key}}}}}", value)

    # Create context_filled_prompt
    context_filled_prompt = final_prompt
    return context_filled_prompt, final_prompt, key, value


@app.cell
def __(context_filled_prompt, mo, prompt_styles):
    mo.vstack(
        [
            mo.md("# Context Filled Prompt"),
            mo.accordion(
                {
                    "### Click to Show Context Filled Prompt": mo.md(
                        f"```xml\n{context_filled_prompt}\n```"
                    ).style(prompt_styles)
                }
            ),
        ]
    )
    return


@app.cell
def __(context_filled_prompt, form, llm_module, mo):
    # Get the selected model
    model = form.value["model_dropdown"]
    # Run the prompt through the model using context_filled_prompt
    with mo.status.spinner(title="Running prompt..."):
        prompt_response = llm_module.prompt(model, context_filled_prompt)

    mo.md(f"# Prompt Output\n\n{prompt_response}").style(
        {"background": "#eee", "padding": "10px", "border-radius": "10px"}
    )
    return model, prompt_response


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
