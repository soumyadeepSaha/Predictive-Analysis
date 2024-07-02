from flask import Flask, request, jsonify, send_file
import redis
import datetime
import threading
import time
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy import func
import json
import matplotlib.pyplot as plt  #for plotting the graph
import seaborn as sns    #for plotting->
import io
import matplotlib

matplotlib.use('Agg')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Soum2106@localhost/UpdateNic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking modifications

db = SQLAlchemy(app)

forecast_steps = 12

redis_client = redis.StrictRedis(host='localhost', port=6379)


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


with app.app_context():
    db.create_all()


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


def save_forecast_to_db(forecast, key, series):
    with app.app_context(): #run according to the context of app (it lets this call run inside the thread)
        try:

            forecast_dict = {str(i + 1): float(f) for i, f in enumerate(forecast)} #forecasted data from arima model is converted to dictionary(same as key value pair)-> then this is easy to convert to json inorder to store in db
            series_dict = {str(k): v for k, v in series.to_dict().items()} #kind of array having index as data and value as the demand(input)-for graph

            new_result = PredictiveAnalysisResult( #object inorder to save in db(dict-json)
                request_key=key,
                result_set=forecast_dict,
                series_data=series_dict,
                last_accessed_on=datetime.datetime.now(),
            )
            db.session.add(new_result)
            db.session.commit()
            print("saved in db")
        except Exception as e:
            print(f"Error saving to database: {e}")


@app.route('/plot/<key>') # when we hit the route via the req key for user ->we start he process for plotting the graph
def get_forecast_data(key): 
    result = fetch_result_from_db(key)#here we get the data from postgress
    if result is not None:
        forecast_data = result['result_set'] #result-set-column(output) in db we store both input and output
        # print(key)
        series_data = result['series_data'] #series_data-column(input)
        try:
            series = pd.Series(series_data)  #series kindof formatting
            forecast = pd.Series(forecast_data)

            sns.set(style="whitegrid")
            plt.figure(figsize=(14, 7))
            plt.plot(pd.to_datetime(series.index), series.values, label='Demand Qty', color='blue',
                     linestyle='-', linewidth=2)
            plt.plot(pd.date_range(start=pd.to_datetime(series.index).max(), periods=len(forecast), freq='M'),
                     forecast, label='Forecasted Qty', color='red', linestyle='--', linewidth=2)
            plt.title('Demand Quantity and Forecast', fontsize=16)
            plt.xlabel('Date', fontsize=14)
            plt.ylabel('Demand Qty', fontsize=14)
            plt.legend(fontsize=12)
            plt.tight_layout()
#creating an image from the above data(for graph)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()
            return send_file(buf, mimetype='image/png') #send to frontend to the url()
        
        except Exception as e:
            print(e)
            return jsonify({'message': 'Data Not formatted correctly'}), 400

    else:
        return jsonify({'message': 'result not found'}), 404


def process_data_from_redis():
    while True:
        keys = redis_client.keys('*')
        for key in keys:
            rawdata = redis_client.get(key) # taken raw data from key
            request_key = key.decode('utf-8')  #everything in reddis is in byte so we converted both the req key and its value to string
            rawdata_str = rawdata.decode('utf-8') 

            data = json.loads(rawdata_str)# cob=nvert string to json

            proper_data = {
                'demandDate': data["demandDate"],
                'demandQty': data['demandQty'],
            }

            df = pd.DataFrame(proper_data) #this ARIMA model works on dataframe # so (bytecode(reddis)->string->json->dataframe) #pd(pandas function to convert in dataframe)#pandas->(data analysis)
            df['demandDate'] = pd.to_datetime(df['demandDate'], format='%d-%m-%Y')
            df.set_index('demandDate', inplace=True)
            df.sort_index(inplace=True)
            df['demandQty'] = df['demandQty'].astype(float)#string->float (while pushing in db)
            series = df['demandQty'] #quantity array(dataframe)
            model = ARIMA(df['demandQty'], order=(5, 1, 0)) #ARIMA->we push the damandqty with scales for scalling(x,y,z) #
            model_fit = model.fit() # we get the processeddata
            forecast = model_fit.forecast(steps=12) #forecast the processed data

            # store in postgres
            save_forecast_to_db(forecast, request_key, series) # (springboot we generate a key for user withrespect to the key we push in the reddis and that key is the identifier passed to the func left)
            # clear redis record
            redis_client.delete(key)
        else:
            print("No key")
            time.sleep(1)


if __name__ == '__main__':
    threading.Thread(target=process_data_from_redis, daemon=True).start()
    app.run(port=8000)