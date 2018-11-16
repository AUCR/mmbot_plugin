"""YARA plugin api functionality."""
# coding=utf-8
from flask import jsonify, g, request
from aucr_app.plugins.mmbot_plugin.models import MmBotTable
from aucr_app.plugins.api.auth import token_auth
from aucr_app.plugins.api.routes import api_page as mmbot_api_page
from aucr_app.plugins.auth.models import Group


@mmbot_api_page.route('/mmbot_plugin/reports/<string:md5_hash>', methods=['GET'])
@token_auth.login_required
def mmbot_plugin_report(md5_hash):
    """Return mmbot report API call."""
    if request.method == "GET" and len(md5_hash) == 32:
        mmbot_object = MmBotTable.query.filter_by(md5_hash=md5_hash).first()
        api_current_user = g.current_user
        group_access_value = Group.query.filter_by(username_id=api_current_user.id,
                                                   groups_id=mmbot_object.group_access).first()
        if group_access_value:
            return jsonify(MmBotTable.query.get_or_404(mmbot_object.id).to_dict())
        else:
            error_data = {"error": "Not authorized to view this Data.", "error_code": 403}
            return jsonify(error_data)
