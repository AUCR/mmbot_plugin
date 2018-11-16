# coding=utf-8
"""Yara AUCR plugin default database tables."""
import udatetime as datetime
from aucr_app import db


class MmBotTable(db.Model):
    """MmBotTable data default table for aucr."""

    __searchable__ = ['id', 'processed_time_stamp', 'vba_lang_features', 'vba_avg_param_per_func',
                      'vba_cnt_comment_loc_ratio', 'vba_cnt_comments', 'vba_cnt_func_loc_ratio', 'vba_cnt_functions',
                      'vba_cnt_loc', 'vba_entropy_chars', 'vba_entropy_func_names', 'vba_entropy_words',
                      'vba_mean_loc_per_func', 'function_names', 'prediction', 'confidence', 'md5_hash']
    __tablename__ = 'mmbot_table'
    id = db.Column(db.Integer, primary_key=True)
    processed_time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    group_access = db.Column(db.Integer, db.ForeignKey('groups.id'))
    vba_lang_features = db.Column(db.String(120))
    vba_avg_param_per_func = db.Column(db.String(120))
    vba_cnt_comment_loc_ratio = db.Column(db.String(120))
    vba_cnt_comments = db.Column(db.String(120))
    vba_cnt_func_loc_ratio = db.Column(db.String(120))
    vba_cnt_functions = db.Column(db.String(120))
    vba_cnt_loc = db.Column(db.String(120))
    vba_entropy_chars = db.Column(db.String(120))
    vba_entropy_func_names = db.Column(db.String(120))
    vba_entropy_words = db.Column(db.String(120))
    vba_mean_loc_per_func = db.Column(db.String(120))
    function_names = db.Column(db.String(120))
    prediction = db.Column(db.String(32))
    confidence = db.Column(db.String(32))
    md5_hash = db.Column(db.String(128), db.ForeignKey('uploaded_file_table.md5_hash'))

    def __repr__(self):
        return '<MmBotTable {}>'.format(self.id)

    def to_dict(self):
        """Return dictionary object type for API calls."""
        data = {
            'id': self.id,
            'processed_time_stamp': self.processed_time_stamp.isoformat() + 'Z',
            'vba_lang_features': self.vba_lang_features,
            'vba_avg_param_per_func': self.vba_avg_param_per_func,
            'vba_cnt_comment_loc_ratio': self.vba_cnt_comment_loc_ratio,
            'vba_cnt_comments': self.vba_cnt_comments,
            'vba_cnt_func_loc_ratio': self.vba_cnt_func_loc_ratio,
            'vba_cnt_functions': self.vba_cnt_functions,
            'vba_cnt_loc': self.vba_cnt_loc,
            'vba_entropy_chars': self.vba_entropy_chars,
            'vba_entropy_func_names': self.vba_entropy_func_names,
            'vba_entropy_words': self.vba_entropy_words,
            'vba_mean_loc_per_func': self.vba_mean_loc_per_func,
            'function_names': self.function_names,
            'prediction': self.prediction,
            'confidence': self.confidence,
            'md5_hash': self.md5_hash
        }
        return data
