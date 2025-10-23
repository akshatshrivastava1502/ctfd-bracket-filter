from flask import request
from CTFd.models import Challenges, Brackets
from CTFd.plugins import register_plugin_assets_directory
from CTFd.utils.user import get_current_user
from CTFd.utils.decorators import authed_only
from CTFd.api.v1.challenges import ChallengesListAPI
from CTFd import utils

def load(app):
    register_plugin_assets_directory(app, base_path="/plugins/bracket_filter/assets")

    @app.after_request
    def filter_challenges(response):
        try:
            # Only modify challenge list API responses
            if request.path.startswith("/api/v1/challenges") and response.is_json:
                data = response.get_json()
                if not data or "data" not in data:
                    return response

                user = get_current_user()
                if not user:
                    return response

                user_bracket = user.bracket.name if user.bracket else None
                if not user_bracket:
                    return response

                filtered = []
                for challenge in data["data"]:
                    name = challenge.get("name", "")
                    if user_bracket.lower() == "basic" and name.startswith("B - "):
                        filtered.append(challenge)
                    elif user_bracket.lower() == "advanced" and name.startswith("A - "):
                        filtered.append(challenge)

                data["data"] = filtered
                response.set_data(utils.serializers.json.dumps(data))
        except Exception as e:
            app.logger.error(f"Bracket filter error: {e}")
        return response
