from flask import Flask, request, jsonify, send_file
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import func
import matplotlib.pyplot as plt
import seaborn as sns
import io

import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/nic_predictive_analysis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications

db = SQLAlchemy(app)


class PredictiveAnalysisResult(db.Model):
    __tablename__ = 'predictive_analysis_result'

    sl_no = db.Column(db.Integer, primary_key=True)
    request_key = db.Column(db.String(255), nullable=False)
    result_set = db.Column(JSONB)
    series_data = db.Column(JSONB)
    no_of_time_accessed = db.Column(db.Integer, nullable=False, default=0)
    last_accessed_on = db.Column(db.TIMESTAMP, server_default=func.now())
    last_accessed_from = db.Column(db.String(20))
    is_block = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<PredictiveAnalysisResult sl_no={self.sl_no} request_key={self.request_key}>'


def fetch_result_from_db(request_key):
    result = PredictiveAnalysisResult.query.filter_by(request_key=request_key).first()
    if result:
        result.no_of_time_accessed += 1
        result.last_accessed_on = func.now()
        result.last_accessed_from = request.remote_addr
        db.session.commit()

        return {
            'sl_no': result.sl_no,
            'request_key': result.request_key,
            'result_set': result.result_set,
            'series_data': result.series_data,
            'no_of_time_accessed': result.no_of_time_accessed,
            'last_accessed_on': result.last_accessed_on,
            'last_accessed_from': result.last_accessed_from,
            'is_block': result.is_block
        }
    else:
        return None


@app.route('/plot/<key>')
def get_forecast_data(key):
    result = fetch_result_from_db(key)
    if result is not None:
        forecast_data = result['result_set']
        series_data = result['series_data']

        try:
            series = pd.Series(series_data)
            forecast = pd.Series(forecast_data)

            sns.set(style="whitegrid")
            plt.figure(figsize=(14, 7))
            plt.plot(pd.to_datetime(series.index), series.values, label='Demand Qty', color='blue',
                     linestyle='-', linewidth=2)
            plt.plot(pd.date_range(start=pd.to_datetime(series.index).max(), periods=len(forecast), freq='ME'),
                     forecast, label='Forecasted Qty', color='red', linestyle='--', linewidth=2)
            plt.title('Demand Quantity and Forecast', fontsize=16)
            plt.xlabel('Date', fontsize=14)
            plt.ylabel('Demand Qty', fontsize=14)
            plt.legend(fontsize=12)
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()
            return send_file(buf, mimetype='image/png')

        except Exception as e:
            return jsonify({'message': 'Data Not formatted correctly'}), 400

    else:
        return jsonify({'message': 'result not found'}), 404


if __name__ == '__main__':
    app.run(debug=False)
