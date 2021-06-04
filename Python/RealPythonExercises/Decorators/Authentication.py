import functools


def is_valid_token(token):
    return token == '999'


def authenticate_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = args[0]
        response = {}
        if is_valid_token(token):
            response['code'] = '200'
            response['payload'] = func(*args, **kwargs)
        else:
            response['code'] = '400'
            response['payload'] = ''
        return response
    return wrapper


@authenticate_token
def simulate_rest_api(token, a, b):
    return a + b


@authenticate_token
def simulate_rest_api_2(token, a, b):
    """
    :type a: fist input
    :type b: second input
    :type token: string simulating an authentication token
    """
    return a * b


print(simulate_rest_api('999', 6, 7))
print(simulate_rest_api_2('098', 7, 8))
