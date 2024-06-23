import json
import uuid

from firebase_admin import firestore
from flask import Blueprint, Flask, current_app, jsonify, request
from flask_cors import CORS, cross_origin
from google.cloud.firestore import ArrayRemove, ArrayUnion
from google.cloud.firestore_v1.base_query import FieldFilter
from sentence_transformers import SentenceTransformer, util

db = firestore.client()
user_Ref = db.collection("user")
entpr_Ref = db.collection("entpr")
vc_Ref = db.collection("vc")
tag_Ref = db.collection("tag")
pitch_Ref = db.collection("pitch")
notification_Ref = db.collection("notification")

userAPI = Blueprint("userAPI", __name__)


# create entrepreneur
@userAPI.route("/user/add/entrepreneur", methods=["POST"])
@cross_origin()
def create_entrepreneur():
    try:
        json = request.json
        entpr_id = uuid.uuid4().hex
        user_id = json["user_id"]
        pitch_ids = []
        entpr_Ref.document(entpr_id).set(
            {"entpr_id": entpr_id, "user_id": user_id, "pitch_ids": pitch_ids}
        )
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# create vc
@userAPI.route("/user/add/vc", methods=["POST"])
@cross_origin()
def create_vc():
    try:
        json = request.json
        vc_id = uuid.uuid4().hex
        user_id = json["user_id"]
        pitch_ids = []
        tag_ids = []
        vc_Ref.document(vc_id).set(
            {
                "vc_id": vc_id,
                "user_id": user_id,
                "pitch_ids": pitch_ids,
                "tag_ids": tag_ids,
            }
        )
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# create user
@userAPI.route("/user/add", methods=["POST"])
@cross_origin()
def create_user():
    try:
        json = request.json
        user_id = json["user_id"]
        name = json["name"]
        role = json["role"]
        email = json["email"]
        photoUrl = json["photoUrl"]
        phoneNumber = json["phoneNumber"]
        address = json["address"]
        user_Ref.document(user_id).set(
            {
                "user_id": user_id,
                "name": name,
                "role": role,
                "email": email,
                "photoUrl": photoUrl,
                "phoneNumber": phoneNumber,
                "address": address,
            }
        )
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# get user by user_id
@userAPI.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        response_json = user_Ref.document(user_id).get()
        return response_json.to_dict(), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# Get users by role
@userAPI.route("/user", methods=["GET"])
def get_users_by_role():
    try:
        response = ""
        role = request.args.get("role")
        docs = user_Ref.where(filter=FieldFilter("role", "==", role)).stream()
        current_app.logger.info(docs)
        for doc in docs:
            # current_app.logger.info(doc)
            response = response + str(doc.to_dict()) + ","
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# get entrepreneur by user_id
@userAPI.route("/entrepreneur/<user_id>", methods=["GET"])
def get_entpr(user_id):
    try:
        response_json = entpr_Ref.where(
            filter=FieldFilter("user_id", "==", user_id)
        ).stream()
        for doc in response_json:
            return doc.to_dict(), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# get vc by user_id
@userAPI.route("/vc/<user_id>", methods=["GET"])
def get_vc(user_id):
    try:
        response_json = vc_Ref.where(
            filter=FieldFilter("user_id", "==", user_id)
        ).stream()
        for doc in response_json:
            return doc.to_dict(), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# create pitch
@userAPI.route("/pitch", methods=["POST"])
@cross_origin()
def create_pitch():
    try:
        json = request.json
        pitch_Ref.document(uuid.uuid4().hex).set(json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# get pitch by pitch_id
@userAPI.route("/pitch/<pitch_id>", methods=["GET"])
def get_pitch_by_id(pitch_id):
    try:
        response_json = pitch_Ref.document(pitch_id).get()
        return response_json.to_dict(), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# get all pitches
@userAPI.route("/pitch/all", methods=["GET"])
@cross_origin()
def get_all_pitches():
    try:
        response = []
        response_json = pitch_Ref.stream()
        for doc in response_json:
            response.append(doc.to_dict())
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# Get pitches by title
# @userAPI.route("/pitch", methods=["GET"])
# def get_pitches_by_title():
#     try:
#         title = request.args.get("title")
#         reg = r"\b\w*" + title + r"\w*\b"
#         docs = pitch_Ref.where(filter=FieldFilter("pitch_title", "==", reg)).stream()
#         response = ""
#         for doc in docs:
#             response = response + str(doc.to_dict()) + ","
#         return jsonify(response), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"


# Get pitches by tags
@userAPI.route("/pitch/tags", methods=["GET"])
def get_pitches_by_tags():
    try:
        tags = request.args.get("tags")
        tags = tags.split(",")
        response = ""
        pitch_ids = []
        for tag in tags:
            docs = pitch_Ref.where(
                filter=FieldFilter("tag_ids", "array_contains", tag)
            ).stream()
            for doc in docs:
                pitch_dict = doc.to_dict()
                if pitch_dict["pitch_id"] not in pitch_ids:
                    pitch_ids.append(pitch_dict["pitch_id"])
                    response = response + str(doc.to_dict()) + ","
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# create tag
@userAPI.route("/tag", methods=["POST"])
@cross_origin()
def create_tag():
    try:
        json = request.json
        tag_id = uuid.uuid4().hex
        tag_name = json["tag_name"]
        tag_Ref.document(tag_id).set({"tag_id": tag_id, "tag_name": tag_name})
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# @userAPI.route("/tag/<tag_id>", methods=["GET"])
# def get_tag(tag_id):
#     try:
#         response_json = tag_Ref.document(tag_id).get()
#         return response_json.to_dict(), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"


# get all tags
@userAPI.route("/tag/all", methods=["GET"])
@cross_origin()
def get_all_tags():
    try:
        response = []
        response_json = tag_Ref.stream()
        for doc in response_json:
            response.append(doc.to_dict())
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# create notification
@userAPI.route("/notifications", methods=["POST"])
def create_notification():
    try:
        json = request.json
        notification_id = uuid.uuid4().hex
        user_id = json["user_id"]
        to_user_id = json["to_user_id"]
        message = json["message"]
        notification_Ref.document(notification_id).set(
            {
                "notification_id": notification_id,
                "user_id": user_id,
                "to_user_id": to_user_id,
                "message": message,
            }
        )
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# @userAPI.route("/user/<notification_id>", methods=["GET"])
# def get_notification(notification_id):
#     try:
#         response_json = notification_Ref.document(notification_id).get()
#         return response_json.to_dict(), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"


# get all notifications for a user
@userAPI.route("/<user_id>/notifications", methods=["GET"])
def get_user_notifications(user_id):
    try:
        response = ""
        docs = notification_Ref.where(
            filter=FieldFilter("to_user_id", "==", user_id)
        ).stream()
        for doc in docs:
            response = response + str(doc.to_dict()) + ","
        return jsonify(response), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# add tags to pitches
@userAPI.route("/pitch/tags", methods=["POST"])
def add_tags_to_pitch():
    try:
        json = request.json
        pitch_id = json["pitch_id"]
        tags = json["tags"]
        pitch = pitch_Ref.document(pitch_id)
        for tag in tags:
            if tag not in pitch.get().to_dict()["tag_ids"]:
                # current_app.logger.info(pitch.get().to_dict()["tag_ids"])
                pitch.update({"tag_ids": ArrayUnion([tag])})
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# add tags to vc
@userAPI.route("/vc/tags", methods=["POST"])
def add_tags_to_vc():
    try:
        json = request.json
        user_id = json["user_id"]
        tags = json["tags"]
        vcs = vc_Ref.where(filter=FieldFilter("user_id", "==", user_id)).stream()
        for vc in vcs:
            vc_id = vc.to_dict()["vc_id"]
            vc_new = vc_Ref.document(vc_id)
            for tag in tags:
                if tag not in vc.to_dict()["tag_ids"]:
                    vc_new.update({"tag_ids": ArrayUnion([tag])})
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# add pitch to vc
@userAPI.route("/vc/pitches", methods=["POST"])
def add_pitch_to_vc():
    try:
        json = request.json
        user_id = json["user_id"]
        pitches = json["pitches"]
        vcs = vc_Ref.where(filter=FieldFilter("user_id", "==", user_id)).stream()
        for vc in vcs:
            vc_id = vc.to_dict()["vc_id"]
            vc_new = vc_Ref.document(vc_id)
            for pitch in pitches:
                if pitch not in vc.to_dict()["pitch_ids"]:
                    vc_new.update({"pitch_ids": ArrayUnion([pitch])})
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# add pitch to entrepreneur
@userAPI.route("/entrepreneur/pitches", methods=["POST"])
def add_pitch_to_entpr():
    try:
        json = request.json
        user_id = json["user_id"]
        pitches = json["pitches"]
        entprs = entpr_Ref.where(filter=FieldFilter("user_id", "==", user_id)).stream()
        for entpr in entprs:
            entpr_id = entpr.to_dict()["entpr_id"]
            entpr_new = entpr_Ref.document(entpr_id)
            for pitch in pitches:
                if pitch not in entpr.to_dict()["pitch_ids"]:
                    entpr_new.update({"pitch_ids": ArrayUnion([pitch])})
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


# generate tags
@userAPI.route("/get_tags", methods=["POST"])
@cross_origin()
def generate_tag():
    try:
        json = request.json
        # tag_id = uuid.uuid4().hex
        sentence = json["pitch"]
        model = SentenceTransformer("bert-base-nli-stsb-mean-tokens")

        tags = [
            "Insurance",
            "Real Estate",
            "Retail",
            "Agriculture",
            "Software Technology",
            "Education",
            "Health Hospitality",
            "Human Resource",
            "Marketing",
            "Media/Entertainment/Movie",
            "Green/CleanTech",
            "Electrical Vehicles",
            "Food and Beverage",
            "Manufacturing",
            "Travel",
            "Animal/Pets",
            "Fitness/Sports/Outdoors/Games",
            "Furnishing/Household",
            "Hardware",
            "Automotive",
            "Beauty/Fashion",
            "Electronics",
            "Uncertain/Other",
            "Finance",
        ]
        similarities = []
        predicted_tags = []

        for word in tags:
            word_embedding = model.encode(word, convert_to_tensor=True)
            sentence_embedding = model.encode(sentence, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(word_embedding, sentence_embedding)
            similarities.append(similarity)
        current_app.logger.info(similarities)
        top_indices = sorted(
            range(len(similarities)), key=lambda i: similarities[i], reverse=True
        )[:3]

        for idx in top_indices:
            predicted_tags.append(tags[idx])
        current_app.logger.info(predicted_tags)
        return jsonify({"tags": predicted_tags}), 200

    except Exception as e:
        return f"An Error Occured: {e}"
