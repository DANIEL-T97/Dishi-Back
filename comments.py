from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Comment,Recipe, User
from flask import Flask, make_response,jsonify, request, abort

import logging


def handle_error(e, status_code):
    logging.error(str(e))
    return jsonify({'error': str(e)}), status_code

comment_parser = reqparse.RequestParser()
comment_parser.add_argument('comment', type=str, help='Comment text', required=True)

# class CommentsResourceID(Resource):
#      def get(self, recipe_id):
#         try:
#             comments = Comment.query.filter_by(recipe_id=recipe_id).all()
#             serialized_comments = [{
#                 "id": comment.id,
#                 "comment": comment.comment,
#                 "user_id": comment.user_id,
#                 "recipe_id": comment.recipe_id
#             } for comment in comments]
#             return (serialized_comments), 200
#         except Exception as e:
#             return {"error": str(e)}, 500
class CommentsResourceID(Resource):
    def get(self, recipe_id):
        try:
            comments = Comment.query.filter_by(recipe_id=recipe_id).all()
            serialized_comments = []
            for comment in comments:
                user_name = "Unknown"  # Default value if user is not found
                if comment.user_id:
                    user = User.query.filter_by(id=comment.user_id).first()
                    if user:
                        user_name = user.name
                serialized_comments.append({
                    "id": comment.id,
                    "comment": comment.comment,
                    "user_id": comment.user_id,
                    "user_name": user_name,
                    "recipe_id": comment.recipe_id
                })
            return serialized_comments, 200
        except Exception as e:
            return {"error": str(e)}, 500

class CommentsResource(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user_email = get_jwt_identity()  # Retrieve current user's email for verification
            current_user = User.query.filter_by(email=current_user_email).first()
            
            if not current_user:
                return {"error": "User not found"}, 404

            data = request.get_json()
            comment_text = data.get('comment')
            recipe_id = data.get('recipe_id')

            new_comment = Comment(user_id=current_user.id, comment=comment_text, recipe_id=recipe_id)
            db.session.add(new_comment)
            db.session.commit()

            serialized_comment = {"id": new_comment.id, "comment": new_comment.comment, "user_id": new_comment.user_id, "recipe_id": new_comment.recipe_id}
            return {"comment": serialized_comment}, 201  

        except Exception as e:
            return {"error": str(e)}, 400  

class CommentByIDResource(Resource):
    # @jwt_required
    # def delete(self, id):
    #     comment = Comment.query.get(id)

    #     if not comment:
    #         return {"message": "Comment not found."}, 404

    #     db.session.delete(comment)
    #     db.session.commit()

    #     return {"message": "Comment deleted successfully."}, 204

    # @jwt_required
    # def patch(self, id):
    #     comment = Comment.query.get(id)

    #     if not comment:
    #         return {"message": "Comment not found."}, 404

    #     args = comment_parser.parse_args()
    #     comment.comment = args['comment']

    #     db.session.commit()

    #     return {"comment": {"id": comment.id, "comment": comment.comment}}
   
    
    @jwt_required()
    def delete(self, id):
        try:
            comment = Comment.query.get(id)
            current_user_email = get_jwt_identity()  # Retrieve current user's email for verification
            current_user = User.query.filter_by(email=current_user_email).first()

            if not comment:
                return {"message": "Comment not found."}, 404

            if comment.user_id != current_user.id:
                return {"message": "Unauthorized to delete this comment"}, 401

            db.session.delete(comment)
            db.session.commit()

            return {"message": "Comment with ID {} deleted successfully".format(id)}, 204  # Return success message with status code 204

        except Exception as e:
            return {"message": str(e)}, 500  # Return error message with status code 500 for server error

    @jwt_required()
    def patch(self, id):
        try:
            comment = Comment.query.get(id)
            current_user_email = get_jwt_identity()  # Retrieve current user's email for verification
            current_user = User.query.filter_by(email=current_user_email).first()

            if not comment:
                return {"message": "Comment not found."}, 404

            if comment.user_id != current_user.id:
                return {"message": "Unauthorized to update this comment"}, 401

            data = request.get_json()
            comment_text = data.get('comment')

            comment.comment = comment_text
            db.session.commit()

            serialized_comment = {"id": comment.id, "comment": comment.comment, "user_id": comment.user_id, "recipe_id": comment.recipe_id}
            return {"comment": serialized_comment}, 200  # Return updated comment with status code 200

        except Exception as e:
            return {"message": str(e)}, 500  # Return error message with status code 500 for server error
