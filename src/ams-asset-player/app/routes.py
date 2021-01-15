from flask import render_template, request, session, redirect, url_for, jsonify
from app import app
from amshelper import AmsHelper
from datetime import datetime, timedelta
import pandas as pd
from dateutil.relativedelta import relativedelta
import json

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    try:
        model = session.pop('model')
    except KeyError:
        model = {
            'player_visibility': 'none',
            'error_message_visibility': 'none',
            'streaming_url': '',
            'asset_name': ''
        }

    return render_template('index.html', title='AMS Asset Player', model=model)


@app.route('/index', methods=['POST'])
def get_stream_for():
    asset = request.form.get('amsAssetName')
    streaming_url = AmsHelper().get_streaming_url(asset)
    model = {
        'player_visibility': 'display',
        'error_message_visibility': 'none',
        'streaming_url': streaming_url,
        'asset_name': asset
    }
    session['model'] = model

    return redirect(url_for('index'))


@app.route('/timeranges', methods=['GET'])
def get_time_ranges():
    asset = request.args.get('assetName')
    precision = request.args.get('precision')
    start_time = request.args.get('startTime')

    dt_start = datetime.now
    dt_end = datetime.now

    if precision == 'year':
        start_time = '2019'
        end_time = str(datetime.now().year)
    elif precision == 'month':
        year = int(start_time)
        dt_start = datetime(year, 1, 1, 0, 0, 0, 0)
        dt_end = datetime(year, 12, 1, 0, 0, 0, 0)
        start_time = dt_start.strftime('%Y-%m')
        end_time = dt_end.strftime('%Y-%m')
    elif precision == 'day':
        dt_start = pd.to_datetime(start_time)
        dt_end = dt_start + relativedelta(months=1) - relativedelta(days=1)
        start_time = dt_start.strftime('%Y-%m-%d')
        end_time = dt_end.strftime('%Y-%m-%d')
    elif precision == 'full':
        dt_start = pd.to_datetime(start_time)
        dt_end = dt_start + relativedelta(days=1)
        start_time = dt_start.strftime("%Y-%m-%dT00:00:00")
        end_time = dt_start.strftime("%Y-%m-%dT23:59:59")

    available_time_ranges = AmsHelper().get_available_media_timeranges(
        asset,
        precision,
        start_time,
        end_time
    )
    result_string = AmsHelper.get_available_mediatime(available_time_ranges, precision)
    return jsonify(result_string)


@app.route('/streamingurl', methods=['GET'])
def get_streaming_url():
    asset = request.args.get('assetName')
    precision = request.args.get('precision')
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')

    streaming_url = AmsHelper().get_streaming_url(asset)

    if precision == 'full':
        dt_start = datetime.now()
        dt_start = pd.to_datetime(start_time)

        streaming_url += '(format=mpd-time-csf,startTime=' + dt_start.strftime('%Y-%m-%dT%H:%M:%S') + ')'
    elif precision == 'range':
        if start_time is None:
            streaming_url += '(format=mpd-time-csf)'
        elif end_time is None or end_time == '':
            streaming_url += '(format=mpd-time-csf,startTime=' + start_time + ')'
        else:
            streaming_url += '(format=mpd-time-csf,startTime=' + start_time + ',endTime=' + end_time + ')'

    result = {'url': streaming_url}
    return jsonify(json.dumps(result))
