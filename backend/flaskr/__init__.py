import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from random import randrange

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# this function is for paginating
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


# this function is used to get a well formatted dictionary
# this link helped me a lot to figure out how to update a value in a dictionary
# https://www.w3schools.com/python/python_dictionaries_add.asp
def dictionary_format(selection):
    selection_dictionary = {}

    for item in selection:
        selection_dictionary.update({item.id: item.type})
    
    return selection_dictionary


# this function get a specific category by his name then return his id
def get_category_by_name(category_name):
    category = Category.query.filter(Category.type == category_name).one_or_none()
    if category is None:
        abort(404)
    
    return category.id



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # """
    # @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    # """
    CORS(app)

    # """
    # @TODO: Use the after_request decorator to set Access-Control-Allow
    # """

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE"
        )
        return response

    
    # this endpoint retrieves every categories
    @app.route('/categories', methods=['GET'])
    def retrieve_categories():

        # getting every categories then format them
        categories = Category.query.order_by(Category.id).all()
        categories_dictionary = dictionary_format(categories)

        if len(categories) == 0:
            abort(404)

        # returns a formated json response
        return jsonify({
            "categories": categories_dictionary
        })

    
    # this endpoint get a specific catgory based on his id
    @app.route('/categories/<int:category_id>', methods=['GET'])
    def get_category_by_id(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()

        if category is None:
            abort(404)

        return jsonify({
            'success': True,
            'category': category.format()
        })


    # this endpoint retrieves every questions paginated by 10 questions each page
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        # getting every questions ordered by id then paginate them
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        # getting every categories then format them
        categories = Category.query.order_by(Category.id).all()
        categories_dictionary = dictionary_format(categories)

        if len(current_questions) == 0:
            abort(404)

        # returns a formatted json response
        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(Question.query.all()),
                "categories": categories_dictionary,
                "currentCategory": "null"
            }
        )

    

    # this endpoint deletes a specific question
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                # unable to find resource
                abort(404)

            question.delete()
            
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                }
            )

        except:
            # unprocessable query
            abort(422)

    

    # this endpoint creates a new question
    @app.route('/questions', methods=['POST'])
    def create_new_question():
        body = request.get_json()

        question_input = body.get("question", None)
        answer_input = body.get("answer", None)
        category_input = body.get("category", None)
        difficulty_input = body.get("difficulty", None)

        try:
            question = Question(
                question=question_input,
                answer=answer_input,
                category=category_input,
                difficulty=difficulty_input)

            question.insert()


            return jsonify(
                {
                    "success": True,
                }
            )

        except:
            abort(422)

    

    # this endpoint retrieves questions by search terms...
    # the user is actually looking for a specific question, by typing the search term
    @app.route('/search/questions', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            search_term = body.get("searchTerm", None)

            selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            if len(selection) == 0:
                abort(404)

            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(selection),
                "currentCategory": "null"
            })
        
        except:
            abort(422)

    

    # this endpoint retrieves questions based on their category
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        # getting questions of a specific related category
        selection = Question.query.filter(Question.category == category_id).all()

        if len(selection) == 0:
            abort(404)

        current_questions = paginate_questions(request, selection)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "currentCategory": "null"
        })


    # this endpoint is for getting the next question in the TRIVIA app game
    @app.route('/quizzes', methods=['POST'])
    def next_question():
        
        # from the body, we get previous questions which is nothing but a list of questions id
        # and the quiz category
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        quiz_category_id = int(quiz_category['id'])


        # we can now use the quiz category to get all current questions
        
        current_questions_query = Question.query.all()

        if quiz_category_id > 0:
            category_id = quiz_category_id
            current_questions_query = Question.query.filter(Question.category == category_id)

        current_questions = [question.format() for question in current_questions_query]

        # since we have the current questions, we can now have available questions
        # these links helped me a lot to achieve what I wanted
        # https://www.w3schools.com/python/gloss_python_array_remove.asp
        value_to_remove = []
        
        if len(previous_questions) > 0:
            for question_id in previous_questions:
                for question in current_questions:
                    if question['id'] == question_id:
                        value_to_remove.append(question)
                
        
            for value in value_to_remove:
                current_questions.remove(value)


        # from above, it's now clear that the current_questions is actually the available questions
        # we did great, we can now randomly choose the question to send back
        # to do so, this article helped to figure out 
        # https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9
        
        if len(current_questions) > 0:
            next_question_index = randrange(len(current_questions))

            nextQuestion = current_questions[next_question_index]
        else :
            nextQuestion = {}
        

        return jsonify({
            'question': nextQuestion
        })
        




    # this is just for error handlers for all expected errors

    # the resource not found error handler
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "Resource not found"}),
            404,
        )

    # the unprocessable error handler
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "Unprocessable"}),
            422,
        )

    # the bad request error handler
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    # the method not allowed error handler
    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "Method not allowed"}),
            405,
        )

    return app
