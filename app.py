import streamlit as st
import requests


def call(number, name):
    url = "https://api.vapi.ai/call/phone"

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
            "firstMessage": f"Olá {name}, fala a Carla da Flora Dentista, marcou uma consulta para daqui a 2 dias às catorze e quero pedir-lhe que a confirme.",
            "endCallFunctionEnabled": True,
            "endCallMessage": "Adeus",
            "endCallPhrases": ["Obrigado pelo seu tempo. Continuação de um bom dia.", "Obrigado pela sua atenção. Desejo-lhe um bom dia."],
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

    response = requests.request("POST", url, json=payload, headers=headers)
    # response = requests.request("POST", url, json=payload, headers=headers, hooks={'response': get_response})

    print(response.json)



def submit_action(telefonnummer, name):
    """
    Funktion, die ausgelöst wird, wenn der Submit-Button gedrückt wird.
    """
    # Hier können weitere Aktionen durchgeführt werden, wie z.B. die Daten speichern oder verarbeiten
    st.success(f"Number: {telefonnummer}, Name: {name}")

def main():
    st.title('RIP CALLS')
    st.subheader('10k days lets go')
    
    # Erstellen der Input Felder
    name = st.text_input("Name", placeholder="Client Name")
    telefonnummer = st.text_input("Number", placeholder="Client Phone")
    
    # Submit Button
    submit_button = st.button('Submit')
    
    if submit_button:
        call(telefonnummer, name)

if __name__ == "__main__":
    main()