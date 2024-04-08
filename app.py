import streamlit as st
import requests


def call(number, name, clinic_name):
    url = "https://api.vapi.ai/call/phone"

    print("Starting call")

    payload = {
        "assistant": {
            "model": {
                "messages": [
                    {
                        "content": "You are a portuguese receptionist in a dental clinic, calling the client that has an upcoming appointment in 48 hours.   You ask them to confirm it. If they confirm, end the call. If they want to reschedule, ask them what day and time and book with them the appointment. You don't need to ask for other information besides date and time.",
                        "role": "system"
                    }
                ],
                "model": "gpt-4-1106-preview",
                "provider": "openai",
                "temperature": 0.7,
            },
            "firstMessage": f"Olá {name}, fala a Eiva da clínica {clinic_name}. Estou a ligar para relembrar que tem uma consulta agendada para amanha às duas da tarde, confirma que vai estar presente?",
            # "endCallFunctionEnabled": True,
            # "endCallMessage": "Adeus",
            "forwardingPhoneNumber": "+351910229854",
            "name": "Carla",
            "transcriber":{
                "provider": "deepgram",
                "model": "nova-2",
                "language": "pt"
            },
            "voice": {
                "provider": "azure",
                "speed": 1,
                "voiceId": "pt-PT-FernandaNeural"
            },
            "voicemailMessage": f"Olá {name}, fala a Carla da Flora Dentista, marcou uma consulta para daqui a 2 dias às 14:00 e quero pedir-lhe que no caso de não poder comparecer, por favor ligue para a clínica para remarcarmos a sua consulta."
        },
        "customer": {
            "extension": "",
            "name": name,
            "number": number
        },
        "phoneNumberId": "e703e2d6-6b09-42a6-b7e4-8553e5f6d7f6",
        "type": "inboundPhoneCall"
    }
    headers = {
        "Authorization": "Bearer a5b355d4-8d79-4af0-bb9a-987a0ebaa8d5",
        "Content-Type": "application/json"
    }

    print("Starting request")

    response = requests.request("POST", url, json=payload, headers=headers)

    print("Starting request")
    response = requests.request("POST", url, json=payload, headers=headers)

    print("Request completed")
    if response.status_code == 200:
        try:
            response_json = response.json()
            print("Call initiated successfully")
            # Further processing with response_json here
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON from response. Raw response:", response.text)
    else:
        print(f"Error: {response.status_code}")
        print("Raw response content:", response.text)




def submit_action(telefonnummer, name, clinic_name):
    """
    Funktion, die ausgelöst wird, wenn der Submit-Button gedrückt wird.
    """
    call(telefonnummer, name, clinic_name)
    st.success(f"Number: {telefonnummer}, Name: {name}")

def main():
    st.title('RIP CALLS | 10k DAYS')
    
    # Erstellen der Input Felder
    clinic_name = st.text_input("Clinic name", placeholder="Flora Dentista")
    name = st.text_input("Name", placeholder="Client Name")
    number = st.text_input("Number", placeholder="Client Phone")
    
    # Submit Button
    submit_button = st.button('Submit')
    
    if submit_button:
        submit_action(number, name, clinic_name)

if __name__ == "__main__":
    main()