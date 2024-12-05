from ai_responses.openai_initialization import openaiClient


def ai_get_file_description(file_description):
    # Upload a file with an "assistants" purpose
    file = openaiClient.files.create(
        file=open(file_description, "rb"),
        purpose='assistants'
    )

    # Get the file description
    # Create an assistant using the file ID
    assistant = openaiClient.beta.assistants.create(
        instructions="You are a data scientist working with a dataset. Please provide a description of the dataset.",
        model="gpt-4o",
        tools=[{"type": "code_interpreter"}],
        tool_resources={
            "code_interpreter": {
                "file_ids": [file.id]
            }
        }
    )





