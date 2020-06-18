import os
import re
import requests
import json
import azure.cognitiveservices.speech as speechsdk

"""
Update Microsoft Azure voice list
"""

AZURE_SERVICES_KEY_ENVVAR_NAME = 'AZURE_SERVICES_KEY'

LOCALE_TO_LANGUAGE = {
    'ar-EG':'Arabic (Egypt)',
    'ar-SA':'Arabic (Saudi Arabia)',
    'bg-BG':'Bulgarian',
    'ca-ES':'Catalan',
    'cs-CZ':'Czech',
    'da-DK':'Danish',
    'de-AT':'German (Austria)',
    'de-CH':'German (Switzerland)',
    'de-DE':'German (Germany)',
    'el-GR':'Greek',
    'en-AU':'English (Australia)',
    'en-CA':'English (Canada)',
    'en-GB':'English (UK)',
    'en-IE':'English (Ireland)',
    'en-IN':'English (India)',
    'en-US':'English (US)',
    'es-ES':'Spanish (Spain)',
    'es-MX':'Spanish (Mexico)',
    'fi-FI':'Finnish',
    'fr-CA':'French (Canada)',
    'fr-CH':'French (Switzerland)',
    'fr-FR':'French (France)',
    'he-IL':'Hebrew (Israel)',
    'hi-IN':'Hindi (India)',
    'hr-HR':'Croatian',
    'hu-HU':'Hungarian',
    'id-ID':'Indonesian',
    'it-IT':'Italian',
    'ja-JP':'Japanese',
    'ko-KR':'Korean',
    'ms-MY':'Malay',
    'nb-NO':'Norwegian',
    'nl-NL':'Dutch',
    'pl-PL':'Polish',
    'pt-BR':'Portuguese (Brazil)',
    'pt-PT':'Portuguese (Portugal)',
    'ro-RO':'Romanian',
    'ru-RU':'Russian',
    'sk-SK':'Slovak',
    'sl-SI':'Slovenian',
    'sv-SE':'Swedish',
    'ta-IN':'Tamil (India)',
    'te-IN':'Telugu (India)',
    'th-TH':'Thai',
    'tr-TR':'Turkish (Turkey)',
    'vi-VN':'Vietnamese',
    'zh-CN':'Chinese (Mandarin, simplified)',
    'zh-HK':'Chinese (Cantonese, Traditional)',
    'zh-TW':'Chinese (Taiwanese Mandarin)'
}

def get_token(subscription_key):
    fetch_token_url = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    access_token = str(response.text)
    return access_token


def get_voice_short_name(voice_name):
    short_name = re.match('.*(\(.*\))', voice_name).group(1)
    short_name = short_name.replace('(', '').replace(')', '')
    components = short_name.split(',')
    final = ', '.join(components[1:])
    return final.strip()

def get_voices(access_token):
    base_url = 'https://eastus.tts.speech.microsoft.com/'
    path = 'cognitiveservices/voices/list'
    constructed_url = base_url + path
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }        
    response = requests.get(constructed_url, headers=headers)
    if response.status_code == 200:
        voice_data = json.loads(response.content)
        #print(voice_data)
        sorted_voice_data = sorted(voice_data, key=lambda x: x['Name'])
        for voice in sorted_voice_data:
            #print(voice)
            language = LOCALE_TO_LANGUAGE[voice['Locale']]
            voice['Language'] = language
            voice['ShortNameFriendly'] = get_voice_short_name(voice['Name'])
            print(str(voice) + ',')
            #output = "'" + voice['Name'] + "': ('" + voice['Locale'] + "', '" + voice['Gender'] + "'),"
            #print(output)
            #print(f"'{voice['Name']}': ('{voice['Locale]}', '{voice['Gender']}')")

def print_voice_list():

    service_region = "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    #speech_config.

if __name__ == '__main__':
    assert AZURE_SERVICES_KEY_ENVVAR_NAME in os.environ
    subscription_key = os.environ[AZURE_SERVICES_KEY_ENVVAR_NAME]
    token = get_token(subscription_key)
    get_voices(token)
