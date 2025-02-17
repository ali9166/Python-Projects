from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en")  # Default to English

# HTML code for speech recognition
HtmlCode = HtmlCode = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {{
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {{
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            }};

            recognition.onend = function() {{
                recognition.start();
            }};
            recognition.start();
        }}

        function stopRecognition() {{
            recognition.stop();
            output.innerHTML = "";
        }}
    </script>
</body>
</html>'''


# Save HTML file
os.makedirs("Data", exist_ok=True)
with open(r"Data/Voice.html", "w") as f:
    f.write(HtmlCode)

# Define Chrome driver options
Chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
Chrome_options.add_argument(f'user-agent={user_agent}')
Chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Allow microphone access
Chrome_options.add_argument("--use-fake-device-for-media-stream")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=Chrome_options)

def QueryModifier(Query):
    Query = Query.strip().capitalize()
    if Query[-1] not in ['.', '?', '!']:
        Query += '.'
    return Query

def UniversalTranslator(Text):
    return mt.translate(Text, "en", "auto").capitalize()

def SpeechRecognition():
    driver.get("file://" + os.path.abspath("Data/Voice.html"))
    driver.find_element(By.ID, "start").click()
    
    while True:
        try:
            Text = driver.find_element(By.ID, "output").text.strip()
            if Text:
                driver.find_element(By.ID, "end").click()
                return QueryModifier(Text if InputLanguage == "en" else UniversalTranslator(Text))
        except Exception:
            pass

if __name__ == "__main__":
    while True:
        print(SpeechRecognition())
