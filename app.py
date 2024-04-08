import streamlit as st
import requests


def call(number, name, clinic_name):
    url = "https://api.vapi.ai/call/phone"

    print("Starting call")


    prompt_1 = """You are a portuguese receptionist in a dental clinic, calling the client that has an upcoming appointment in 48 hours.   
                        You ask them to confirm it. If they confirm, end the call. If they want to reschedule, ask them what day and time and book with them the appointment. 
                        You don't need to ask for other information besides date and time."""

    prompt_2 = """
    Your only job is to understand if the user confirms or not.
    If they confirm, "confirmo" (agree), say "sim" (yes), say "thank you" and end the call.

    If they say no, "agora" or intent to reschedule, forward the call.

    You do not reschedule, you only forward the call.
    """

    assistant_prompt = """ Your job is to understand if the user confirms or not.
    If they confirm, say "thank you" and end the call.
    If they say no or intent to reschedule, forward the call. """
    
    # prompt_2 = """Tu és uma recepcionista que trabalha para clínicas dentárias. Vais ligar aos clientes para lhes dizer que eles tem consulta agendada.
    #                 Se os clientes confirmarem que vão comparecer, agredeces a confirmaÇão e terminas a chamada. Se eles desconfirmarem, ou seja disserem que não podem comparecer,
    #                 dizes que vais reencaminhar a chamada para as recepcionistas da clínica para eles reagendarem a consulta. Logo a seguir reencaminhas a chamada.
    #                     """

    payload = {
        "assistant": {
            "model": {
                "messages": [
                    {
                        "content": prompt_2,
                        "role": "assistant"
                    },
                    # {
                    #     "content": assistant_prompt,
                    #     "role": "assistant"
                    # }
                ],
                "model": "gpt-4-1106-preview",
                "provider": "openai",
                "temperature": 0.7,
            },
            "firstMessage": f"Olá {name}, eu sou o assistente virtual da clínica {clinic_name}, estou a ligar para confirmar que tem uma consulta agendada para amanhã às catorze horas. Diga sim para confirmar a sua presença.",
            # "endCallFunctionEnabled": True,
            # "endCallPhrases": [
            #     "Sim",
            #     "Confirmo",
            #     "Sim, confirmo"
            # ],
            # "endCallMessage": "Obrigado pelo seu tempo. Tenha um bom dia.",
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

# """
# Olá [name], eu sou o assistente virtual da clínica [clinic name], estou a ligar para confirmar que tem uma consulta agendada para [day and time]. Diga sim para confirmar a sua presença. No caso de não poder será reecaminhado para as nossas recepcionistas.

# Olá [name], eu sou o assistente virtual da clínica [clinic name], estou a ligar para confirmar que tem uma consulta agendada para amanhã às catorze horas. Diga sim para confirmar a sua presença. No caso de não poder será reecaminhado para as nossas recepcionistas.

# """


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