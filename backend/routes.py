from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return list of picture URLs"""
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return picture with given id"""
    if data:
        for pic in data:
            if pic["id"] == id:
                return jsonify(pic)
        
        return {"message": f"Picture with id {id} not found"}, 404
    
    return {"message": "Internal server error"}, 500



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """ create new picture"""
    new_pic = request.json
    if not new_pic:
        return {"message": "Invalid input parameter"}, 422

    if data:
        for pic in data:
            if pic["id"] == new_pic["id"]:
                return {"Message": f"picture with id {new_pic['id']} already present"}, 302
        
        data.append(new_pic)
        return new_pic, 201

    return {"message": "Internal server error"}, 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """update picture with given id"""
    update_pic = request.json

    if data:
        for i in range(len(data)):
            if data[i]["id"] == update_pic["id"]:
                data[i] = update_pic
                return jsonify(data[i])
        
        return {"message": "picture not found"}, 404
        
    return {"message": "Internal server error"}, 500

    

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """delete picture by id"""
    if data:
        for pic in data:
            if pic["id"] == id:
                data.remove(pic)
                return {}, 204
        return {"message": "picture not found"}, 404

    return {"message": "Internal server error"}, 500
    


