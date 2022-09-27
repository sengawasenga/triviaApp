# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.


## Getting started

### Backend instructions

#### Step 1: Install required software

- Python 3.7 - Follow instructions to install the latest version of python for your platform in the python docs
- Virtual Environment - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the python docs
- Postgres

#### Step 2: Set up and Populate the Database

1. With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

2. Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

#### Step 3: Install dependencies

Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Step 4: Start the server

Start the Server

In the `backend` directory, start the Flask server by running:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

#### Setting up testing

Since you are working in a local environment, you'll need to manually set up and populate the testing database:

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```

### Frontend instructions

The frontend app was built using create-react-app and uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository.

1. Install Node and NPM This project requires on Nodejs and Node Package Manager (NPM). If you haven't already installed Node on your local machine, see the instructions here: Before continuing, you must download and install Node (the download includes NPM) from Nodejs.com.

2. Install project dependencies After confirming you have NPM installed, navigate to the `frontend` directory of the project and run:

```bash
npm install
```

3. To start the app in development mode, run:

```bash
npm start
```

4. Open http://localhost:3000 to view it in the browser.

## API documentation

### Getting started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling

Errors are returned as JSON objects in the following format:

```json
{
    "success": false, 
    "error": 404,
    "message": "Resource not found"
}
```
The API will return three error types when requests fail:

- 404: Resource Not Found
- 422: Unprocessable 
- 405: Method not allowed

### Endpoints

#### GET /categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An JSON object with a single key, categories, that contains an object of id: category_string key: value pairs.

`curl http://127.0.0.1:5000/categories`

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sport"
    }
}
```

#### GET /categories/{id}

- Fetches a dictionary of category in which the key is the id and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An JSON object with a single key, category, that contains an object of id: category_string key: value pairs.

`curl http://127.0.0.1:5000/categories/2`

```json
{
    "category": {
        "id": 2,
        "type": "Art"
    },
    "success": true
}
```

#### POST /categories

- Creates a brand new category
- Request Arguments: The only one argument required is the `type`
- Returns: An JSON object with two keys, `success` which is either true or false and `created` which is the id the newly created category.

`curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"type":"Entertainment"}'`

```json
{
    "created": 1,
    "success": true
}
```

#### GET /questions

- Get a list of paginated questions
- Returns a list of question objects, success value total number of questions, a dictionary of categories and the current category.
- Request Arguments: None

`curl http://127.0.0.1:5000/questions`

```json
{
    "categories": {
        "1": "Environment",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sport"
    },
    "currentCategory": "All",
    "questions": [
        {
            "answer": "Francis Ngannou",
            "category": 6,
            "difficulty": 4,
            "id": 1,
            "question": "Who is the most powerful fighter of UFC ?"
        },
        {
            "answer": "Albert Einstein",
            "category": 1,
            "difficulty": 4,
            "id": 3,
            "question": "Who invented the quantic mechanic ?"
        },
        {
            "answer": "Aime Cesaire",
            "category": 4,
            "difficulty": 5,
            "id": 4,
            "question": "Who was the first black writer talking about negritude ?"
        },
        {
            "answer": "Egypt",
            "category": 4,
            "difficulty": 2,
            "id": 7,
            "question": "From which ancient Kingdom the Washington DC were inspired of ?"
        },
        {
            "answer": "fleshOwl",
            "category": 1,
            "difficulty": 2,
            "id": 8,
            "question": "What username Marcel Senga uses in his dailybases ?"
        },
        {
            "answer": "Alexander Usyk",
            "category": 6,
            "difficulty": 3,
            "id": 9,
            "question": "Who is current heavyweight WBC champion"
        },
        {
            "answer": null,
            "category": null,
            "difficulty": null,
            "id": 10,
            "question": null
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 18
}
```

#### GET /questions/{id}

- Get a specific question based on his id
- Returns a single question and a success value
- Request Arguments: None

`curl http://127.0.0.1:5000/questions/3`

```json
{
    "question": {
        "answer": "Albert Einstein",
        "category": 1,
        "difficulty": 4,
        "id": 3,
        "question": "Who invented the quantic mechanic ?"
    },
    "success": true
}
```

#### POST /questions

- Create a brand new question
- Request Arguments: Required arguments are: question, answer, difficulty and category.
- Returns a success message

`curl http://127.0.0.1:5000/categories -X POST -H "Content-Type: application/json" -d '{"question":"Who is the most powerful fighter of UFC ?", "answer":"Francis Ngannou", "difficulty":4, "category":6}'`

```json
{
    "success": true
}
```

#### DELETE /questions/{id}

- Deletes a specific question based on his id
- Request arguments: None
- Returns a success message and the id of the deleted question

`curl -X DELETE http://127.0.0.1:5000/questions/3`

```json
{
    "success": true,
    "deleted": 3
}
```

#### GET /questions

- Get a list of paginated questions of a specific category
- Returns a list of paginated question objects, success value, total number of questions and the current category.
- Request Arguments: None

`curl http://127.0.0.1:5000/categories/3/questions`

```json
{
    "currentCategory": "Geography",
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```

#### POST search/questions

- Search for questions based on a search term
- Returns a list of paginated question objects, success value, total number of questions and the current category.
- Request arguments: the only one required argument is the `searchTerm`

`curl http://127.0.0.1:5000/search/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"lake"}'`

```json
{
    "currentCategory": "All",
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

#### POST /quizzes

- Get the next question for the trivia game based on a list of previous questions and the quiz category
- Returns a single question
- Request arguments: the required arguments are `previous_questions` and `quiz_category`
The previous question is a list of integers.
The quiz category is a dictionary of `id` and `type` key values pairs.

`curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[13,15], "quiz_category":{"id":3, "type":"Geography"}}'`

```json
{
    "question": {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
    }
}
```
