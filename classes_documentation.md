# Classes Documentation

## Overview
This document provides detailed information about the classes implemented in `main.py`. The application is a GUI-based system for managing student records and academic information.

## Class: Student
The `Student` class represents a student entity in the system.

### Attributes
- `id` (int): Unique identifier for the student
- `name` (str): Student's full name
- `age` (int): Student's age
- `grade` (str): Student's current grade level
- `major` (str): Student's field of study
- `gpa` (float): Student's Grade Point Average

### Methods
- `__init__(self, id, name, age, grade, major, gpa)`: Constructor that initializes a new student object
- `to_dict(self)`: Converts student object to a dictionary format
- `from_dict(cls, data)`: Class method to create a student object from a dictionary

## Class: StudentManagementSystem
The `StudentManagementSystem` class manages the core functionality for handling student records.

### Attributes
- `students` (list): List of Student objects
- `db_file` (str): Path to the database file

### Methods
- `__init__(self, db_file)`: Constructor that initializes the system and loads existing data
- `load_data(self)`: Loads student data from the database file
- `save_data(self)`: Saves current student data to the database file
- `add_student(self, student)`: Adds a new student to the system
- `update_student(self, student_id, updated_data)`: Updates an existing student's information
- `delete_student(self, student_id)`: Removes a student from the system
- `get_student(self, student_id)`: Retrieves a specific student's information
- `get_all_students(self)`: Returns a list of all students

## Class: StudentManagementApp
The `StudentManagementApp` class implements the graphical user interface for the student management system.

### Attributes
- `root` (tk.Tk): Main application window
- `system` (StudentManagementSystem): Instance of the management system
- `current_student` (Student): Currently selected student
- `student_list` (tk.Listbox): UI element displaying list of students
- `name_var`, `age_var`, `grade_var`, `major_var`, `gpa_var` (tk.StringVar): Variables for student information fields

### Methods
- `__init__(self, root)`: Constructor that sets up the main application window and UI components
- `setup_ui(self)`: Initializes and arranges all UI elements
- `load_students(self)`: Populates the student list with current data
- `select_student(self, event)`: Handles student selection from the list
- `add_student(self)`: Creates a new student record
- `update_student(self)`: Updates the selected student's information
- `delete_student(self)`: Removes the selected student
- `clear_fields(self)`: Resets all input fields
- `validate_inputs(self)`: Validates user input before processing
- `show_error(self, message)`: Displays error messages to the user
- `show_success(self, message)`: Displays success messages to the user

## Class: CustomEntry
The `CustomEntry` class is a custom widget that extends the basic entry widget with additional styling.

### Attributes
- Inherits from `tk.Entry`

### Methods
- `__init__(self, master, **kwargs)`: Constructor that initializes the custom entry widget with specific styling

## Class: CustomButton
The `CustomButton` class is a custom widget that extends the basic button widget with additional styling.

### Attributes
- Inherits from `tk.Button`

### Methods
- `__init__(self, master, **kwargs)`: Constructor that initializes the custom button widget with specific styling

## Class: CustomLabel
The `CustomLabel` class is a custom widget that extends the basic label widget with additional styling.

### Attributes
- Inherits from `tk.Label`

### Methods
- `__init__(self, master, **kwargs)`: Constructor that initializes the custom label widget with specific styling

## Class: CustomListbox
The `CustomListbox` class is a custom widget that extends the basic listbox widget with additional styling.

### Attributes
- Inherits from `tk.Listbox`

### Methods
- `__init__(self, master, **kwargs)`: Constructor that initializes the custom listbox widget with specific styling

## Class: CustomFrame
The `CustomFrame` class is a custom widget that extends the basic frame widget with additional styling.

### Attributes
- Inherits from `tk.Frame`

### Methods
- `__init__(self, master, **kwargs)`: Constructor that initializes the custom frame widget with specific styling 