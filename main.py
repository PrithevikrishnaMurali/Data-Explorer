import streamlit as st
import pandas as pd
from logger import Logger, ConsoleLogAdapter, FileLogAdapter, ErrorObserver, WarningObserver, UIObserver
from observer import Subject, GeneralObserver
from loader import DataLoaderFactory, PDFLoaderAdapter, XMLLoaderAdapter

def main():
    st.set_page_config(page_title="Data Loader", layout="wide")
    set_custom_css()
    st.title("Data Loader")

    # Initialize logger
    logger = Logger.get_instance()

    # Add observers to the logger
    error_observer = ErrorObserver()
    warning_observer = WarningObserver()
    ui_observer = UIObserver()
    logger.add_observer(error_observer)
    logger.add_observer(warning_observer)
    logger.add_observer(ui_observer)

    # Initialize subject and observer
    subject = Subject()
    observer = GeneralObserver()
    subject.attach(observer)

    # Initialize data loader factory
    data_loader_factory = DataLoaderFactory(logger, subject)

    # Log level selection
    log_level = st.sidebar.selectbox("Select Log Level:", ("Info", "Update", "Warning", "Error", "All"))

    # Logging method selection
    log_method = st.sidebar.radio("Select Logging Method:", ("None", "Console", "File"))

    if st.sidebar.button("Start Program"):
        if log_method == "Console":
            logger.set_handler(ConsoleLogAdapter())
        elif log_method == "File":
            logger.set_handler(FileLogAdapter("/home/krish/patterns/log.txt"))
        elif log_method == "None":
            st.warning("Please select a logging method before starting the program.")
            return
        
        # Set the log level and mark the log method as selected
        logger.set_log_level(log_level.lower())
        logger.info("Program started")
        subject.notify("info", "Program started")
        st.session_state.log_method_selected = True

    # File upload
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'json', 'html', 'xml', 'pdf'])

    if uploaded_file is not None:
        if not getattr(st.session_state, 'log_method_selected', False):
            st.warning("Please select a log method and click 'Start Program' before uploading a file.")
            return
        
        file_type = uploaded_file.name.split('.')[-1]
        if file_type == 'pdf':
            loader = PDFLoaderAdapter(logger, subject)
        elif file_type == 'xml':
            loader = XMLLoaderAdapter(logger, subject)
        else:
            loader = data_loader_factory.create_loader(file_type)
        
        try:
            data = loader.load(uploaded_file)
            logger.info(f"{file_type.upper()} file loaded: {uploaded_file.name}")
            subject.notify("info", f"{file_type.upper()} file loaded: {uploaded_file.name}")

            if isinstance(data, pd.DataFrame):
                # Reset index to start from 1
                data.index = range(1, len(data) + 1)

                # Store the data in session state
                st.session_state.data = data

                display_and_modify_data(data, logger, subject, file_type)

            elif isinstance(data, str):  # For HTML content
                st.write("HTML Content:")
                st.code(data, language='html')
            
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            subject.notify("error", f"Error processing file: {str(e)}")

def display_and_modify_data(data, logger, subject, file_type):
    st.write("Data Preview:")
    st.dataframe(data)

    # Ensure all columns are of type string to avoid dtype incompatibility
    data = data.astype(str)

    # Add new data
    with st.expander("Add New Data"):
        new_data = {}
        cols = st.columns(len(data.columns))
        for i, col in enumerate(data.columns):
            new_data[col] = cols[i].text_input(f"Enter {col}")
        
        if st.button("Add Data"):
            data = add_new_data(data, new_data, logger, subject)

    # Edit data
    with st.expander("Edit Data"):
        row_to_edit = st.selectbox("Select row to edit", options=data.index)
        edited_data = {}
        cols = st.columns(len(data.columns))
        for i, col in enumerate(data.columns):
            edited_data[col] = cols[i].text_input(f"Edit {col}", value=data.loc[row_to_edit, col])
        
        if st.button("Save Edits"):
            data = edit_data(data, row_to_edit, edited_data, logger, subject)

    # Delete data
    with st.expander("Delete Data"):
        row_to_delete = st.selectbox("Select row to delete", options=data.index)
        if st.button("Delete Row"):
            data = delete_data(data, row_to_delete, logger, subject)

    st.write("Updated Data:")
    st.dataframe(data)

    # Update session state
    st.session_state.data = data

    # Save updated file
    save_updated_file(data, logger, subject, file_type)

def add_new_data(data, new_data, logger, subject):
    if any(new_data.values()):
        new_row = pd.DataFrame([new_data])
        temp_data = pd.concat([data, new_row], ignore_index=True)
        temp_data.index = range(1, len(temp_data) + 1)  # Reset index to start from 1
        
        if not data.duplicated().any() and not temp_data.duplicated().any():
            data = temp_data
            logger.update("New data added")
            subject.notify("update", "New data added")
            st.info("New data added")  # Corrected the usage of st.info

        else:
            logger.warning("Attempt to add duplicate data")
            logger.error("Cannot add duplicates in singleton")
            subject.notify("warning", "Attempt to add duplicate data")
            st.error("Cannot add duplicates in singleton")  # Corrected the usage of st.error
    return data

def edit_data(data, row_to_edit, edited_data, logger, subject):
    if any(edited_data.values()):
        for col, value in edited_data.items():
            data.loc[row_to_edit, col] = value
        if not data.duplicated().any():
            logger.update(f"Row {row_to_edit} edited")
            subject.notify("update", f"Row {row_to_edit} edited")
            st.info("Data edited")  # Corrected the usage of st.info
        else:
            logger.warning(f"Attempt to edit row {row_to_edit} to duplicate data")
            subject.notify("warning", f"Attempt to edit row {row_to_edit} to duplicate data")
            st.error("Cannot edit data to add duplicates in singleton")  # Corrected the usage of st.error
    return data

def delete_data(data, row_to_delete, logger, subject):
    data = data.drop(index=row_to_delete)
    logger.warning(f"Row {row_to_delete} deleted")
    subject.notify("warning", f"Row {row_to_delete} deleted")
    st.warning("Data deleted")  # Corrected the usage of st.warning
    return data

def save_updated_file(data, logger, subject, file_type):
    try:
        if file_type == 'csv':
            data.to_csv("/home/krish/patterns/updated_data.csv", index=False)

        elif file_type == 'json':
            data.to_json("/home/krish/patterns/updated_data.json", orient='records')

        elif file_type == 'html':
            data.to_html("/home/krish/patterns/updated_data.html", index=False)

        elif file_type == 'xml':
            data.to_xml("/home/krish/patterns/updated_data.xml", index=False)

        logger.info(f"Data saved to updated_data.{file_type}")
        subject.notify("info", f"Data saved to updated_data.{file_type}")
        st.info(f"Data saved to updated_data.{file_type}")  # Corrected the usage of st.info

    except Exception as e:
        logger.error(f"Error saving updated data: {str(e)}")
        subject.notify("error", f"Error saving updated data: {str(e)}")
        st.error(f"Error saving updated data: {str(e)}")  # Corrected the usage of st.error

def set_custom_css():
    st.markdown(
        """
        <style>
        body {
            color: #f0f0f0;
            background-color: #1e1e1e;
            font-family: 'Roboto', sans-serif;
        }
        .stButton button {
            color: #ffffff;
            background-color: #4a4a4a;
            border: 1px solid #ffffff;
        }
        .stButton button:hover {
            color: #ffffff;
            background-color: #6a6a6a;
        }
        .stFileUploader label, .stRadio label, .stSelectbox label {
            color: #ffffff;
        }
        .stExpander .stExpanderHeader {
            color: #ffffff;
            background-color: #4a4a4a;
        }
        .stExpander .stExpanderContent {
            color: #ffffff;
            background-color: #2a2a2a;
        }
        .stWarning {
            color: red;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
