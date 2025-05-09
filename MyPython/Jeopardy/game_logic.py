import json

def load_questions(filename):
    """
    Loads Jeopardy questions from a JSON file.

    Args:
        filename (str): The path to the JSON file.

    Returns:
        list: A list of categories, where each category is a dictionary
              containing the category name and a list of questions.
              Returns an empty list if the file is not found or there's an error.
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}'. Please ensure the file is correctly formatted.")
        return []

# Example of how to use the function:
if __name__ == "__main__":
    question_file = 'MyPython/Jeopardy/jeopardy_questions.json'  # Replace with your actual filename
    questions_data = load_questions(question_file)

    if questions_data:
        print("Questions loaded successfully:")
        for category in questions_data:
            print(f"Category: {category['name']}")
            for question in category['questions']:
                print(f"  Points: {question['points']}, Question: {question['question']}, Answer: {question['answer']}")
    else:
        print("No questions were loaded.")