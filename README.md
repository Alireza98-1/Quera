# Form Builder Project

This project is a Django-based API for creating and managing forms with various question types.

## Setup and Installation

1. Clone the repository:
2. Create a virtual environment and activate it:

3. Install the required packages:

4. Apply migrations:

5. Run the development server:

The API should now be accessible at `http://localhost:8000/`.

## Running Tests

To run the tests, use the following command:

This will run all the tests in the project, including the API tests for the FormViewSet.

## API Endpoints

- `GET /api/forms/`: List all forms
- `POST /api/forms/`: Create a new form
- `GET /api/forms/{id}/`: Retrieve a specific form
- `PUT /api/forms/{id}/`: Update a specific form
- `DELETE /api/forms/{id}/`: Delete a specific form
- `GET /api/forms/{id}/questions/`: List all questions for a specific form
- `POST /api/forms/{id}/add_question/`: Add a new question to a specific form
- `PUT /api/forms/{id}/update_question/`: Update a question in a specific form
- `DELETE /api/forms/{id}/delete_question/`: Delete a question from a specific form

For more detailed API documentation, please refer to the API documentation or contact the development team.
