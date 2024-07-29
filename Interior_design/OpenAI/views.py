#Libraries Required
import base64
import io
import json
import os
import sys
from io import StringIO
import pandas as pd
import razorpay
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from openai import OpenAI
from django.http import JsonResponse
from digiotai.digiotai_jazz import Agent, Task, OpenAIModel, SequentialFlow, InputType, OutputType
from .database import SQLiteDB
from .form import CreateUserForm
from django.core.mail import EmailMessage
from django.core.mail import send_mail

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Configure OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
expertise = "Interior Designer"
task = Task("Image Generation")
input_type = InputType("Text")
output_type = OutputType("Image")
agent = Agent(expertise, task, input_type, output_type)
api_key = OPENAI_API_KEY

db = SQLiteDB()

@csrf_exempt
def testing(request):
    return HttpResponse("Application is up")

@csrf_exempt
def api(request):
    return HttpResponse("Welcome to the otamat backend....")


# def get_csv_metadata(df):
#     metadata = {
#         "columns": df.columns.tolist(),
#         "data_types": df.dtypes.to_dict(),
#         "null_values": df.isnull().sum().to_dict(),
#         "example_data": df.head().to_dict()
#     }
#     return metadata

#Login Page Authentication(13)
@csrf_exempt
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_details = db.get_user_data(username)
            return HttpResponse(json.dumps({"status": "Success", "user_details": user_details}), content_type="application/json")
        else:
            return HttpResponse('User Name or Password is incorrect')
    return HttpResponse("Login failed")

# Forgot password missing
#Logout Page(8)
@csrf_exempt
def logoutpage(request):
    try:
        logout(request)
        request.session.clear()
        return redirect('demo:login')
    except Exception as e:
        return HttpResponse(str(e))

#Register Page(17)
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                db.add_user(user, email)
                user_details = db.get_user_data(user)
                return HttpResponse(json.dumps({"status": "Success", "user_details": user_details}), content_type="application/json")
            else:
                return HttpResponse(str(form.errors))
        except Exception as e:
            return HttpResponse(str(e))
    return HttpResponse("Registration Failed")

#Google Login(18)
@csrf_exempt
def googlelogin(request):
    username = request.POST.get("username")
    password = username + "@" + request.POST.get("id")
    email = request.POST.get("email")
    users = db.get_users()
    if username in users:
        user_details = db.get_user_data(username)
        return HttpResponse(json.dumps({"status": "Success", "user_details": user_details}), content_type="application/json")
    else:
        form = CreateUserForm({'username': username, 'email': email, 'password1': password, 'password2': password})
        if form.is_valid():
            form.save()
            db.add_user(username, email)
            user_details = db.get_user_data(username)
            return HttpResponse(json.dumps({"status": "Success", "user_details": user_details}), content_type="application/json")
        else:
            return HttpResponse(str(form.errors))





# @csrf_exempt
# def upload_data(request):
#     if request.method == "POST":
#         files = request.FILES['file']
#         if len(files) < 1:
#             return HttpResponse('No files uploaded')
#         else:
#             content = files.read().decode('utf-8')
#             csv_data = io.StringIO(content)
#             df = pd.read_csv(csv_data)
#             df.to_csv('data.csv', index=False)
#             username = request.POST.get("username")
#             result = genAIPrompt3(username)
#             return HttpResponse(json.dumps(result), content_type="application/json")
#     return HttpResponse("Failure")

# @csrf_exempt
# def genAIPrompt(request):
#     if request.method == "POST":
#         df = pd.read_csv("data.csv")
#         csv_metadata = get_csv_metadata(df)
#         metadata_str = ", ".join(csv_metadata["columns"])
#         query = request.POST["query"]
#         prompt_eng = (
#             f"You are graphbot. If the user asks to plot a graph, you only reply with the Python code of Matplotlib to plot the graph and save it as graph.png. "
#             f"The data is in data.csv and its attributes are: {metadata_str}. If the user does not ask for a graph, you only reply with the answer to the query. "
#             f"The user asks: {query}"
#         )

#         code = generate_code(prompt_eng)
#         if 'import matplotlib' in code:
#             try:
#                 exec(code)
#                 with open("graph.png", 'rb') as image_file:
#                     return HttpResponse(json.dumps({"graph": base64.b64encode(image_file.read()).decode('utf-8')}), content_type="application/json")
#             except Exception as e:
#                 prompt_eng = f"There has occurred an error while executing the code, please take a look at the error and strictly only reply with the full python code do not apologize or anything just give the code {str(e)}"
#                 code = generate_code(prompt_eng)
#                 try:
#                     exec(code)
#                     with open("graph.png", 'rb') as image_file:
#                         return HttpResponse(json.dumps({"graph": base64.b64encode(image_file.read()).decode('utf-8')}), content_type="application/json")
#                 except Exception as e:
#                     return HttpResponse("Failed to generate the chart. Please try again")
#         else:
#             return HttpResponse(code)



#Interior Design(23)-Text to Image
@csrf_exempt
def genAIPrompt2(request):
    if request.method == "POST":
        model = OpenAIModel(api_key=api_key, model="dall-e-2")
        sequential_flow = SequentialFlow(agent, model)
        selected_style = request.POST["selected_style"]
        selected_room_color = request.POST["selected_room_color"]
        selected_room_type = request.POST["selected_room_type"]
        number_of_room_designs = request.POST["number_of_room_designs"]
        additional_instructions = request.POST["additional_instructions"]
        user_name = request.POST["user_name"]
        stat, count, quota = checkQuota(user_name)
        if stat:
            prompt = f"Generate a Realistic looking Interior design with the following instructions style: {selected_style}, Room Color: {selected_room_color}, Room type: {selected_room_type}, Number of designs: {number_of_room_designs}, Instructions: {additional_instructions}"
            image_url = sequential_flow.execute(prompt)
            print(image_url)
            if quota == "FREE":
                db.update_count(user_name)
                count -= 1
            user_details = db.get_user_data(user_name)
            return HttpResponse(json.dumps({"image": image_url, "status": "Success", "count": count, "user_details": user_details}), content_type="application/json")
        else:
            user_details = db.get_user_data(user_name)
            return HttpResponse(json.dumps({"image": "NA", "status": "Quota limit exceeded", "count": count, "user_details": user_details}), content_type="application/json")




from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
import requests
from datetime import datetime
from .models import GeneratedImage
from django.core.files.base import ContentFile

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            selected_style = request.POST.get("selected_style")
            selected_room_color = request.POST.get("selected_room_color")
            selected_room_type = request.POST.get("selected_room_type")
            image_url = request.POST.get('image_url')

            if not all([email, selected_style, selected_room_color, selected_room_type, image_url]):
                messages.error(request, "All fields are required.")
                return HttpResponse("All fields are required.", status=400)

            # Get the current date
            current_date = datetime.now().strftime("%d/%m/%Y")
            subject = f'Interior design - {current_date}'
            message = (f'Please find the generated image attached.\n'
                       f'Count: 1\n'
                       f'Selected type: {selected_room_type}\n'
                       f'Selected style: {selected_style}\n'
                       f'Selected color: {selected_room_color}')

            # Download the image from the URL
            response = requests.get(image_url)
            response.raise_for_status()  # Ensure we catch any errors with the request
            image_data = response.content

            # Create and save the image in the database
            generated_image = GeneratedImage(
                email=email,
                selected_style=selected_style,
                selected_room_color=selected_room_color,
                selected_room_type=selected_room_type,
            )
            generated_image.image.save('generated_image.png', ContentFile(image_data))
            generated_image.save()

            # Create an EmailMessage object
            email_message = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            # Attach the image with explicit MIME type
            email_message.attach('generated_image.png', image_data, 'image/png')

            # Send the email
            email_message.send()

            messages.success(request, 'Email sent successfully. The image has been saved in the database.')
            return HttpResponse("Email sent successfully")
        except requests.exceptions.RequestException as req_e:
            messages.error(request, f"An error occurred while fetching the image: {str(req_e)}")
            return HttpResponse(f"An error occurred while fetching the image: {str(req_e)}", status=500)
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return HttpResponse("Only POST requests are allowed")



    

# def generate_code(prompt_eng):
#     response = client.chat.completions.create(
#         model="gpt-4-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt_eng}
#         ]
#     )
#     all_text = ""
#     for choice in response.choices:
#         message = choice.message
#         chunk_message = message.content if message else ''
#         all_text += chunk_message

#     code_start = all_text.find("```python") + 9
#     code_end = all_text.find("```", code_start)
#     code = all_text[code_start:code_end]
#     return code

# @csrf_exempt
# def genAIPrompt3(username):
#     df = pd.read_csv("data.csv")
#     prompt_eng = f"You are analytics_bot. Analyse the data: {df} and give description of the columns"
#     if checkQuota(username):
#         code = generate_code(prompt_eng)
#         prompt_eng1 = f"Generate 10 questions for the data: {df}"
#         prompt_eng_2 = f"Generate 10 simple possible plotting questions for the data: {df}"

#         code1 = generate_code(prompt_eng1)
#         code2 = generate_code(prompt_eng_2)
#         db.update_count(username)
#         return {"status": "Success", "col_desc": code, "sample data": df.head(10).to_json(), "text_questions": code1, "chart_questions": code2}
#     else:
#         return {"status": 'Quota limit exceeded'}
    

def checkQuota(user):
    user_details = db.get_user_data(user)
    quota = user_details[1]
    count = user_details[2]
    if quota != 'FREE':
        return True, count, quota
    else:
        if 0 < count <= 5:
            return True, count, quota
        else:
            return False, count, quota


# @csrf_exempt
# def regenerate_txt(request):
#     df = pd.read_csv("data.csv")
#     prompt_eng = (
#         f"Regenerate 10 questions for the data: {df}"
#     )
#     code = generate_code(prompt_eng)
#     return HttpResponse(json.dumps({"questions": code}),
#                         content_type="application/json")


# @csrf_exempt
# def regenerate_chart(request):
#     df = pd.read_csv("data.csv")
#     prompt_eng = (
#         f"Regenerate 10 simple possible plotting questions for the data: {df}. start the question using plot keyword"
#     )
#     code = generate_code(prompt_eng)
#     return HttpResponse(json.dumps({"questions": code}),
#                         content_type="application/json")


# @csrf_exempt
# def genresponse(request):
#     df = pd.read_csv("data.csv")
#     if request.method == "POST":
#         question = request.POST["query"]
#         graph = ''
#         if os.path.exists("graph.png"):
#             os.remove("graph.png")
#         prompt_eng = (
#             f"generate python code for the question {question} based on the data: {df} from data.csv file. "
#             f"If the question is related to plotting then save the plot as graph.csv"
#         )
#         code = generate_code(prompt_eng)
#         if "import" in code:
#             old_stdout = sys.stdout
#             redirected_output = sys.stdout = StringIO()
#             exec(code)
#             sys.stdout = old_stdout
#             print(redirected_output.getvalue())
#             if os.path.exists("graph.png"):
#                 with open("graph.png", 'rb') as image_file:
#                     graph = base64.b64encode(image_file.read()).decode('utf-8')

#             return HttpResponse(json.dumps({"answer": redirected_output.getvalue(), "graph": graph}),
#                                 content_type="application/json")
#         return HttpResponse(json.dumps({"answer": code}),
#                             content_type="application/json")

#Payment Gateway(23)
@csrf_exempt
def paymentinfo(request, ):
    if request.method == "POST":
        currency = 'INR'
        amount = request.POST['amount']  # Rs. 200
        request.session['amount'] = amount
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                           currency=currency,
                                                           payment_capture='0'))
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = 'http://3.132.248.171:4500/paymenthandler/'

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url

        return HttpResponse(json.dumps({"paymentinfo": context}),
                            content_type="application/json")


#Paymment Handler(35)
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        if "razorpay_signature" in request.POST:
            payment_verification = razorpay_client.utility.verify_payment_signature(request.POST)
            if payment_verification:
                return JsonResponse({"res": "success"})
                # Logic to perform is payment is successful
            else:
                return JsonResponse({"res": "failed"})
        else:
            return HttpResponse("Signature not available, payment failed")
    else:
        return HttpResponse("Get not valid")

@csrf_exempt
def get_user_details(request):
    if request.method == "POST":
        return HttpResponse(json.dumps({"paymentinfo": list(db.get_user_data(request.POST.get("user")))}),
                            content_type="application/json")

@csrf_exempt
def updateuserplan(request):
    if request.method == "POST":
        user = request.POST.get("user")
        plan = request.POST.get("plan")
        data = db.get_user_data(user)
        if plan.upper() == "BASIC":
            c = data[2] + 50
        elif plan.upper() == "PRO":
            c = data[2] + 200
        else:
            c = data[0]
        db.update_user(user, plan, c)
        return get_user_details(request)


# Generation of Image(25)-Image to Image
@csrf_exempt
def generateImage(request):
    if request.method == "POST":
        model= OpenAIModel(api_key=api_key, model="dall-e-2")
        sequential_flow = SequentialFlow(agent, model)
        selected_style = request.POST["selected_style"]
        selected_room_color = request.POST["selected_room_color"]
        selected_room_type = request.POST["selected_room_type"]
        number_of_room_designs = request.POST["number_of_room_designs"]
        additional_instructions = request.POST["additional_instructions"]
        user_name = request.POST["user_name"]
        stat, count, quota = checkQuota(user_name)
        if stat:
            prompt = f"Generate a Realistic looking Interior design with the following instructions style: {selected_style}, Room Color: {selected_room_color}, Room type: {selected_room_type}, Number of designs: {number_of_room_designs}, Instructions: {additional_instructions}"
            image_url = sequential_flow.execute(prompt)
            print(image_url)
            if quota == "FREE":
                db.update_count(user_name)
                count -= 1
            user_details = db.get_user_data(user_name)
            return HttpResponse(json.dumps({"image": image_url, "status": "Success", "count": count, "user_details": user_details}), content_type="application/json")
        else:
            user_details = db.get_user_data(user_name)
            return HttpResponse(json.dumps({"image": "NA", "status": "Quota limit exceeded", "count": count, "user_details": user_details}), content_type="application/json")


# @csrf_exempt
# def generatetestImage(request):
#     if request.method == "POST":
#         model = OpenAIModel(api_key=api_key, model="dall-e-2")
#         sequential_flow = SequentialFlow(agent, model)
#         prompt = request.POST.get("prompt")
#         prompt = f"Generate an image based on user prompt and save it as graph1.png. User prompt is {prompt}"
#         image_url = sequential_flow.execute(prompt)

#         return HttpResponse(json.dumps({"image": image_url, "status": "Success"}),
#                             content_type="application/json")
