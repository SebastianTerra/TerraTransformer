import streamlit as st
import os
from openai import OpenAI

st.title('Terralabor File Transformer')

# Set OpenAI API key
openai_api_key = "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"

if openai_api_key is None:
    st.error("Please set the OPENAI_API_KEY environment variable.")
    st.stop()
client = OpenAI(api_key=openai_api_key)


# File uploader
uploaded_file = st.file_uploader("Please Select the File To Transform")

if uploaded_file is not None:
    # Display file name
    st.write("Uploaded File:", uploaded_file.name)

    # Create a vector store
    with st.spinner('Processing file...'):
        vector_store = client.beta.vector_stores.create(name="Uploaded File Vector Store")

        # Upload the file and add it to the vector store
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=[uploaded_file]
        )

    st.success('File processed successfully.')

    # Create an assistant with file_search enabled
    assistant = client.beta.assistants.create(
        name="File Query Assistant",
        instructions="You are a helpful assistant that can answer questions about the user's uploaded file.",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    # User input
    user_query = st.text_input("Enter your query about the file:")

    if user_query:
        # Create a thread
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": user_query,
                }
            ]
        )

        # Create a run
        with st.spinner('Getting response...'):
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id, assistant_id=assistant.id
            )

            # Get assistant's response
            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

            assistant_response = messages[0].content[0].text

        # Display assistant's response
        st.write("Assistant's response:")
        st.write(assistant_response)








