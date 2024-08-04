import requests

url = 'http://stone-in-waiting.sbs/api'

# 参数查询
def API_query_parameter(graph_data, qc_depth):
    data_dict = {'api_name': 'query_parameter', 'graph_data':graph_data, 'qc_depth':qc_depth}
    response = requests.post(url, json=data_dict).json()
    return response['status'], response['parameter']

# 参数提交
def API_submit_parameter(graph_data, user_parameter, qc_depth):
    data_dict = {'api_name': 'submit_parameter', 'graph_data':graph_data, 'user_parameter':user_parameter,'qc_depth':qc_depth}
    response = requests.post(url, json=data_dict).json()
    return response['status'], response['score_dict']

# 参数对比
def API_compare_parameter(graph_data, user_parameter, qc_depth):
    data_dict = {'api_name': 'compare_parameter', 'graph_data':graph_data, 'user_parameter':user_parameter,'qc_depth':qc_depth}
    response = requests.post(url, json=data_dict).json()
    return response['status'], response['score_dict']
