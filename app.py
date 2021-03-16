from chalice import Chalice
import openai
import boto3

app = Chalice(app_name='convoapp')


@app.route('/')
def index():
    return {'convo': 'start'}

@app.route('/convo', methods=['GET'], cors=True)
def convo():
    ssm = boto3.client("ssm") 
    api_key = ssm.get_parameter(Name="openai_api_key", WithDecryption=True)['Parameter']['Value']
    openai.api_key = api_key

    with open("chalicelib/training_text.txt", "r") as infile:
        training_text = infile.read()

    request = app.current_request
    prompt = request.query_params['prompt']
    training_text = f"{training_text}\nUser:{prompt}"
    print(prompt)
    print(training_text)
    response = openai.Completion.create(
        engine="davinci",
        prompt=training_text,
        temperature=0.7,
        max_tokens=150, # max length of the reply, training_text+prompt+response ≤ 2048
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=['.']
    )

    return {"api": response}

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

# Rate limiting
# Error handling
# disable send until bot responds
# prevent empty message
# fix the preset side buttons