import streamlit as st
import time
import streamlit.components.v1 as components  # For rendering raw HTML

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File {filename} not found."

def main():
    st.set_page_config(layout="wide")
    
    if 'submit_clicked' not in st.session_state:
        st.session_state.submit_clicked = False

    if 'task_status' not in st.session_state:
        st.session_state.task_status = []

    col1, col2 = st.columns([1, 2])
    
    with col1:
        assistant_options = {
            "Streamlit Devrel": 1,
            "Vercel Devrel": 1,
            "MongoDB Devrel": 1
        }
        
        # Add a default option as the first item
        options = ["Select a Writer"] + list(assistant_options.keys())
        
        selected_assistant = st.selectbox(
            "Select a Writer",
            options=options,
            key="assistant_select"
        )
        
        if selected_assistant != "Select a Writer":
            selected_value = assistant_options[selected_assistant]
            
            description = read_file(f"desc_{selected_value}.txt")
            st.text_area("Describe the article", value=description, height=200, key="description")  # Increased the height to 200px
            
            if st.button("Write Article"):
                st.session_state.submit_clicked = True
                tasks = read_file(f"tasks_{selected_value}.txt").splitlines()
                
                # Reset task status
                st.session_state.task_status = [""] * len(tasks)
                
                # Add header for task list
                st.markdown("<b>Executing steps for the article</b>", unsafe_allow_html=True)

                # Create a placeholder for task updates
                task_placeholder = st.empty()
                
                # Dynamically render tasks during execution
                for i, task in enumerate(tasks):
                    # Parse the task for duration and task description
                    try:
                        duration, task_description = task.split(": ", 1)
                        duration = int(duration)
                    except ValueError:
                        duration, task_description = 3, task  # Default sleep time if parsing fails
                    
                    # Update task status as it's being processed
                    st.session_state.task_status[i] = f"<p style='color: blue;'>🔄 {task_description}</p>"
                    task_placeholder.markdown("".join(st.session_state.task_status), unsafe_allow_html=True)
                    
                    # Sleep for the duration specified by the task
                    time.sleep(duration)
                    
                    # Mark task as completed
                    st.session_state.task_status[i] = f"<p style='color: green;'>✅ {task_description}</p>"
                    task_placeholder.markdown("".join(st.session_state.task_status), unsafe_allow_html=True)
    
    with col2:
        if st.session_state.submit_clicked:
            # Read HTML content from the selected file and render it
            html_content = read_file(f"content_{selected_value}.txt")
            # Use st.components.v1.html to render the HTML content properly
            components.html(html_content, height=600, scrolling=True)

if __name__ == "__main__":
    main()
