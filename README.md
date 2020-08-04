# Full Stack Trivia API Backend

## Setting up

#### Download Python 3.7
#### Setup Virtual Enviornment (Virtualenv or pipenv)
#### PIP Dependencies

```bash
pip install -r requirements.txt
(or)
pipenv install -r requirements.txt  
```
##### Key Dependencies
#### Flask
#### SQLAlchemy
#### Flask-Cors


## Database Setup
### Please change database path in models.py(7th line ), test_flaskr.py(18th line)
Navigate to /backend
```bash
sudo -u postgres psql trivia < 'trivia.psql'
```

## Running the server

After Creating virtual environment Navigate /backend and
To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
 
## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

 

## Endpoints
#### GET '/categories'
Return all categories
- Sample:  `curl http://127.0.0.1:5000/categories`
```json
{
  "all_categories": 6, 
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
#### GET '/categories/<int:id>/questions'
Return questions based on category
- Sample:`curl http://127.0.0.1:5000/categories/1/questions -X GET`
```json
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Radesh", 
      "category": 1, 
      "difficulty": 1, 
      "id": 25, 
      "question": "WHo are you2"
    }, 
    {
      "answer": "3", 
      "category": 1, 
      "difficulty": 1, 
      "id": 26, 
      "question": "WHo are you3"
    }, 
    {
      "answer": "123", 
      "category": 1, 
      "difficulty": 1, 
      "id": 27, 
      "question": "hello"
    }, 
    {
      "answer": "123", 
      "category": 1, 
      "difficulty": 1, 
      "id": 38, 
      "question": "hello"
    }
  ], 
  "success": true, 
  "total_questions": 7
}

```
#### GET '/questions'
Returning Question with pagination=10
- Sample: `curl http://127.0.0.1:5000/questions`<br>
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
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
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "total_questions": 32
}
``` 
#### POST '/questions/add'
Adding new question
- Sample: `curl http://127.0.0.1:5000/questions/add -X POST -H "Content-Type: application/json" -d '{"question":"TestQuestion","answer":"TestAnswer","category":"5","difficulty":"5"}'`
```json
{
  "question_id": 39, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
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
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }
  ], 
  "success": true, 
  "total_questions": 31
}

```
### DELETE '/questions/<int:question_id>'
Deleting a question using id
- Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE` 
```json
{
  "deleted_id": 6, 
  "success": true
}

```
#### POST '/questions/search'
Searching Questions
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who are you"}'`
```json
{
  "current_category": "None", 
  "questions": [
    {
      "answer": "Radesh", 
      "category": 2, 
      "difficulty": 1, 
      "id": 24, 
      "question": "WHo are you"
    }, 
    {
      "answer": "Radesh", 
      "category": 1, 
      "difficulty": 1, 
      "id": 25, 
      "question": "WHo are you2"
    }, 
    {
      "answer": "3", 
      "category": 1, 
      "difficulty": 1, 
      "id": 26, 
      "question": "WHo are you3"
    }
  ], 
  "success": true, 
  "total_questions": 3
}

``` 
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```