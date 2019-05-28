import os
import ujson
from mmbot import MaliciousMacroBot
from aucr_app import db, create_app
from aucr_app.plugins.mmbot_plugin.models import MmBotTable
from aucr_app.plugins.auth.models import Message, User
from aucr_app.plugins.unum.models import UNUM

mmb = MaliciousMacroBot()
mmb.mmb_init_model()


def call_back(ch, method, properties, md5_hash):
    """ Main function to process documents with mmbot."""
    # First make a log file to track any errors and all running info
    upload_path = os.environ.get('FILE_FOLDER')
    result = mmb.mmb_predict(str(upload_path + "/" + md5_hash.decode('utf-8')), datatype='filepath')
    json_result = mmb.mmb_prediction_to_json(result)
    if json_result:
        app = create_app()
        db.init_app(app)
        with app.app_context():
            new_mmbot = MmBotTable(vba_lang_features=str(json_result[0]["vba_lang_features"]), group_access=2,
                                   vba_avg_param_per_func=str(json_result[0]["vba_avg_param_per_func"]),
                                   vba_cnt_comment_loc_ratio=str(json_result[0]["vba_cnt_comment_loc_ratio"]),
                                   vba_cnt_comments=str(json_result[0]["vba_cnt_comments"]),
                                   vba_cnt_func_loc_ratio=str(json_result[0]["vba_cnt_func_loc_ratio"]),
                                   vba_cnt_functions=str(json_result[0]["vba_cnt_functions"]),
                                   vba_cnt_loc=str(json_result[0]["vba_cnt_loc"]),
                                   vba_entropy_chars=str(json_result[0]["vba_entropy_chars"]),
                                   vba_entropy_func_names=str(json_result[0]["vba_entropy_func_names"]),
                                   vba_entropy_words=str(json_result[0]["vba_entropy_words"]),
                                   vba_mean_loc_per_func=str(json_result[0]["vba_mean_loc_per_func"]),
                                   function_names=str(json_result[0]["function_names"]),
                                   prediction=str(json_result[0]["prediction"]),
                                   confidence=str(json_result[0]["confidence"]),
                                   md5_hash=md5_hash.decode('utf-8'))
            db.session.add(new_mmbot)
            db.session.commit()
            upload_file = UNUM.query.filter_by(md5_hash=md5_hash.decode('utf-8')).first()
            message_data = ujson.dumps(new_mmbot.to_dict(), indent=2, sort_keys=True)
            msg = Message(sender_id=1, recipient_id=upload_file.created_by, body=message_data)
            db.session.add(msg)
            db.session.commit()
            uploaded_user = User.query.filter_by(id=upload_file.created_by).first()
            uploaded_user.add_notification('unread_message_count', uploaded_user.new_messages())
            db.session.commit()
