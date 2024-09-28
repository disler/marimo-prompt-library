Explain what the PYTHON_CODE does in 100 words or less.

PYTHON_CODE
def get_first_keyword_in_prompt(prompt: str):
    map_keywords_to_agents = {
        "bash,browser": run_bash_command_workflow, 
        "question": question_answer_workflow, 
        "hello,hey,hi": soft_talk_workflow, 
        "exit": end_conversation_workflow,
    }
    for keyword_group, agent in map_keywords_to_agents.items():
        keywords = keyword_group.split(",")
        for keyword in keywords:
            if keyword in prompt.lower():
                return agent, keyword
    return None, None