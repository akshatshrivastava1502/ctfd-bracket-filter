from flask import request, render_template
from CTFd.models import Challenges
from CTFd.plugins import (
    register_plugin_assets_directory,
    register_admin_plugin_menu_bar,
)
from CTFd.utils.user import get_current_user
from CTFd.utils.decorators import admins_only
from CTFd import utils
from CTFd.utils import set_config, get_config


def load(app):
    # Register assets (optional but good practice)
    register_plugin_assets_directory(app, base_path="/plugins/bracket_filter/static")

    # Add menu entry in admin panel
    register_admin_plugin_menu_bar(
        title="Bracket Filter",
        route="/admin/bracket_filter/settings",
    )

    # Admin settings page route
    @app.route("/admin/bracket_filter/settings", methods=["GET", "POST"])
    @admins_only
    def bracket_filter_settings():
        if request.method == "POST":
            enabled = request.form.get("enabled", "off")
            set_config("bracket_filter_enabled", "true" if enabled == "on" else "false")
        enabled = get_config("bracket_filter_enabled") == "true"
        return render_template("settings.html", enabled=enabled)

    @app.after_request
    def filter_challenges(response):
        try:
            # Check if plugin is enabled
            if get_config("bracket_filter_enabled") != "true":
                return response

            # Only filter for /api/v1/challenges
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
