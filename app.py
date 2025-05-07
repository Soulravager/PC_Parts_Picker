import os
import google.generativeai as genai
import streamlit as st


genai.configure(api_key=os.environ.get("AIzaSyBS6zUQANjgspTU1DT4C1PHdfJrmDngOA4","AIzaSyBS6zUQANjgspTU1DT4C1PHdfJrmDngOA4"))

#Gemini model with the custom configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=(
        "Only answer computer-related topics. This chat is for a PC builder chatbot.\n"
        "If the user asks something unrelated, either ask for clarification or reply with:\n"
        "'I can only answer that Related to PC Building.'\n"
        "Focus on PC-building or computer hardware/software issues."
    ),
)

def generate_response(prompt):
    """Generates a response from the Gemini API based on the given prompt."""
    try:
        # new chat session
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "Only answer computer-related topics. This chat is for a PC builder chatbot.\n"
                        "If the user asks something unrelated, either ask for clarification or reply with:\n"
                        "'I can only answer that in PC Builder.'\n"
                        "Focus on PC-building or computer hardware/software issues."
                    ],
                },
            ]
        )

        # Send the user's prompt
        response = chat_session.send_message(prompt)

        # Return the response text
        return response.text.strip() if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"An error occurred: {e}"


def main():
    st.title("PC Builder AI Assistant Chatbot")
    st.write("Welcome to the PC Parts Picker AI Chat Support! Type your message below and press Enter to chat.")

    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # User input
    user_input = st.text_input("User:", "")

    if user_input:
        # Generate response from Gemini
        ai_response = generate_response(user_input)

        # Append user input and AI response to chat history
        st.session_state.chat_history.append(f"User: {user_input}")
        st.session_state.chat_history.append(f"PC PICKER: {ai_response}")

        # Display chat history
        st.write("Chat History:")
        for message in st.session_state.chat_history:
            st.write(message)

# Run the Streamlit app
if __name__ == "__main__":
    main()
