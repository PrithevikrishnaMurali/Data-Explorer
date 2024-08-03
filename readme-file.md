# Data Explorer Application

## Project Description

This Data Loader Application is a flexible and extensible system for loading, displaying, and modifying data from various file formats. It features a user-friendly Streamlit interface and implements several design patterns to ensure modularity and maintainability.

## Input and Output

### Input:
- CSV, JSON, HTML, XML, or PDF files containing structured data
- User interactions through the Streamlit UI for data manipulation

### Output:
- Displayed data in the Streamlit UI
- Modified data saved back to files
- Logs (console or file-based, depending on user selection)

## Design Patterns Used

1. **Singleton Pattern**
   - **Where**: `Logger` class in `logger.py`
   - **How**: Ensures only one instance of the logger exists
   - **Why**: Provides a global point of access to the logging functionality

2. **Adapter Pattern**
   - **Where**: `ConsoleLogAdapter` and `FileLogAdapter` classes in `adapter.py`
   - **How**: Adapts different logging outputs to a common interface
   - **Why**: Allows for flexible switching between logging to console or file

3. **Observer Pattern**
   - **Where**: `Subject`, `Observer`, and various concrete observer classes in `logger.py` and `observer.py`
   - **How**: Implements a publish-subscribe model for logging events
   - **Why**: Enables flexible notification of logging events to different components without tight coupling

4. **Factory Pattern**
   - **Where**: `DataLoaderFactory` class in `loader.py`
   - **How**: Creates appropriate data loader objects based on file type
   - **Why**: Centralizes object creation and makes it easy to add new file types

5. **Strategy Pattern**
   - **Where**: Different data loader classes in `loader.py`
   - **How**: Implements different algorithms for loading various file types
   - **Why**: Allows for interchangeable data loading strategies without altering client code

## How to Run

1. Ensure you have Python and Streamlit installed
2. Clone the repository
3. Navigate to the project directory
4. Run `streamlit run main.py`
5. Use the Streamlit UI to upload files, modify data, and save changes

## Future Enhancements

- Add support for more file formats
- Implement more advanced data manipulation features
- Enhance error handling and user feedback

