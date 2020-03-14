def corsify_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def timetostr(time):
    try:
        return time.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return ""