from flask import Blueprint, request, jsonify
from some_social_media_library import SocialMediaAPI

social_media = Blueprint('social_media', __name__)

api = SocialMediaAPI('api_key')

@social_media.route('/upload', methods=['POST'])
def upload_content():
    content = request.json.get('content')
    response = api.upload_content(content)
    return jsonify(response)