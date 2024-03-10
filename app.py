from flask import Flask, render_template, request,jsonify
import speech_recognition as sr
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient

app = Flask(__name__)


API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {'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'}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    if request.method == 'POST':
       
       
       # Email credentials
        sender_email = "nikhiljain876900@gmail.com"
        sender_password = "qndm lcva ajeu ytfi"
        receiver_emails = ["swn.himanshu@gmail.com","cisjoksa@gmail.com","12115028@nitkkr.ac.in"]#add furthur mails here


        #--------------------------------------------------------------------------------------------------------
        #TASK >>>>mongo se data fetch karna hai 

        # client = MongoClient("mongodb+srv://swnhimanshu:MdMU3vyQG79T9kUd@cluster0.iumnaqh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        # db = client["my-magic-database"]
        # collection = db["my-magic-collection"]




        # # Apply summarization to each document
        # for document in data:
        #     text_generated = document["value"]  # Assuming your text data is stored in a field named "text"


        #>>>>>DATA FETCHING OVER NOW STORED IN text_generated
        #--------------------------------------------------------------------------------------------------------------
 
        with open('meeting_transcript.txt', 'r') as file:
            text_generated = file.read()



        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_emails)  
        message["Subject"] = "MEET_SUMMARY"# yaha par meeting id add karni hai bs + karke string of id likhna hai
                                  #collection ka use karke
        
        output = query({"inputs": text_generated})

        # Add body to email
        body = output[0]["summary_text"]
        message.attach(MIMEText(body, "plain"))#yaha attechement like pdf vgerah kar skate h if needed

        # Connect to the SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_emails, text)


        return "summary of this conversation is sent to your mail""please check your mail"""




@app.route('/save_audio', methods=['POST'])
def save_audio():
    try:
        audio_file = request.files['audio']
        audio_file.save('meeting_audio.wav')

        recognizer = sr.Recognizer()
        with sr.AudioFile('meeting_audio.wav') as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        with open("meeting_transcript.txt", "a") as file:
            file.write(text + "\n")

        return jsonify({'message': 'Audio saved and transcript generated successfully.'})
    except Exception as e:
        return jsonify({'error': str(e)})
    


if __name__ == '__main__':
    app.run(debug=True)
