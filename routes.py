import udatetime
from aucr_app import db
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, g
from flask_login import login_required, current_user
#from aucr_app.plugins.mmbot_plugin.forms import EditUploadFile, Unum
from aucr_app.plugins.mmbot_plugin.models import MmBotTable

mmbot_page = Blueprint('mmbot', __name__, template_folder='templates')


@mmbot_page.route('/dashboard', methods=['GET'])
@login_required
def mmbot_plugin_dashboard():
    """Mmbot default dashboard view."""
    page = request.args.get('page', 1, type=int) or 1
    count = page * 10
    mmbot_results_dict = {}
    total = 0
    while total < 10:
        total += 1
        id_item = count - 10 + total
        try:
            item = MmBotTable.query.filter_by(id=id_item).first().to_dict()
        except AttributeError:
            item = None
        if item:
            upload_dict = {"id": item["id"],
                           "md5": item["md5_hash"],
                           "prediction": item["prediction"],
                           "confidence": item["confidence"],
                           "time": item["processed_time_stamp"]}
            mmbot_results_dict[str(item["id"])] = upload_dict
    prev_url = '?page=' + str(page - 1)
    next_url = '?page=' + str(page + 1)
    return render_template('mmbot.html', title='MMBOT Search', page=page, table_dict=mmbot_results_dict,
                           next_url=next_url, prev_url=prev_url)


@mmbot_page.route('/report', methods=['GET'])
@login_required
def mmbot_plugin_report():
    """Mmbot report page view."""
    file_hash = request.args.get("md5_hash")
    item = MmBotTable.query.filter_by(md5_hash=file_hash).first().to_dict()
    return render_template('mmbot_report.html', title='MMBOT Search', file_hash=file_hash, table_dict=item)
