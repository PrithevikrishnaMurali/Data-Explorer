Design Patterns Usage:

a. Singleton Pattern:

Used in: Logger class (logger.py)
How it's implemented:

The Logger class has a private class variable _instance.
The get_instance() method checks if _instance exists. If not, it creates a new instance.


Where it's called:

In main.py: logger = Logger.get_instance()


Purpose: Ensures only one Logger instance exists throughout the application.

b. Factory Pattern:

Used in: DataLoaderFactory class (loader.py)
How it's implemented:

The create_loader() method creates and returns the appropriate DataLoader based on the file type.


Where it's called:

In main.py: loader = data_loader_factory.create_loader(file_type)


Purpose: Centralizes the creation of DataLoader objects, making it easy to add new loaders.

c. Adapter Pattern:

Used in:

ConsoleLogAdapter and FileLogAdapter classes (adapter.py)
XMLLoaderAdapter and PDFLoaderAdapter classes (loader.py)


How it's implemented:

Log adapters implement the LoggerOutputAdapter interface.
XML and PDF adapters inherit from DataLoader and adapt the loading process for these file types.


Where it's called:

In main.py:

logger.set_adapter(ConsoleLogAdapter())
logger.set_adapter(FileLogAdapter("/home/krish/patterns/log.txt"))


In main.py:

loader = XMLLoaderAdapter(logger, subject)
loader = PDFLoaderAdapter(logger, subject)




Purpose: Allows different implementations for logging output and file loading without changing the core classes.

d. Observer Pattern:

Used in: Subject class (observer.py), Observer interface, and concrete observers (ErrorObserver, WarningObserver in logger.py, GeneralObserver in observer.py)
How it's implemented:

Subject maintains a list of observers and notifies them of events.
Observers implement the update method to react to notifications.


Where it's called:

In main.py:

subject = Subject()
observer = GeneralObserver()
subject.attach(observer)
Throughout the code: subject.notify("info", "Some message")


In logger.py:

self.notify_observers(message, level)




Purpose: Allows loose coupling between components that need to be informed of events.

e. Strategy Pattern:

Used in: DataLoader abstract class and its concrete implementations (CSVLoader, JSONLoader, etc. in loader.py)
How it's implemented:

DataLoader defines the interface with the load() method.
Concrete classes implement load() for specific file types.


Where it's called:

In main.py: data = loader.load(uploaded_file)


Purpose: Allows interchangeable algorithms for loading different file types.


Code Flow from Data Upload:

Let's walk through the code flow when a user uploads a file:
a. File Upload:

In main.py, Streamlit's st.file_uploader() is used to allow file upload.
When a file is uploaded, the code checks if a logging method has been selected.

b. Loader Creation:

The file type is determined from the file extension.
For PDF and XML files, specific adapters are created.
For other file types, the DataLoaderFactory creates the appropriate loader.

c. Data Loading:

The load() method of the created loader is called with the uploaded file.
The loader reads the file and returns the data (usually as a pandas DataFrame).
Any errors during loading are caught and logged.

d. Data Display:

The loaded data is displayed using Streamlit's st.dataframe().
The data is also stored in the Streamlit session state for later use.

e. Data Modification:

The display_and_modify_data() function is called, which sets up UI elements for data modification.
Three expandable sections are created for adding, editing, and deleting data.

f. Adding New Data:

In the "Add New Data" expander, input fields are created for each column.
When the "Add Data" button is clicked, add_new_data() is called.
This function creates a new row from the input, checks for duplicates, and adds it to the DataFrame if valid.

g. Editing Data:

In the "Edit Data" expander, the user selects a row to edit and modifies the values.
When "Save Edits" is clicked, edit_data() is called.
This function updates the selected row with the new values, checking for duplicates.

h. Deleting Data:

In the "Delete Data" expander, the user selects a row to delete.
When "Delete Row" is clicked, delete_data() is called.
This function removes the selected row from the DataFrame.

i. Saving Updated Data:

After modifications, the updated data is displayed.
The save_updated_file() function is called to save the modified data back to a file.
The file is saved in the same format as the input file (CSV, JSON, etc.).

Throughout this process, logging and notifications are used:

The Logger instance logs important events (info, warnings, errors).
The Subject notifies observers of these events.
Streamlit is used to display informational messages, warnings, and errors to the user.