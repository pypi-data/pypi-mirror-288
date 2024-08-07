from ai12z_api_sdk.Service import Ai12zService
from ai12z_api_sdk.Options import Ai12zOptions

import pprint

def main():
    healthckeck_ai_response = Ai12zService().health_check() 
    print("Ai12zHealthCheck Response: ") 
    pprint.pprint(healthckeck_ai_response)
   

    try:
        option = Ai12zOptions()
        option.api_key = "bb30bdb9ae661f8754cb780249f6c8f9b92f12ed9bcabdcaab5b3d4f1d704531"
        option.format = "html"
        ask_ai_response = Ai12zService().ask_ai("who is alpesh", option)
        print("Ai12zAskAi Response: ")
        pprint.pprint(ask_ai_response)
        
        

    except Exception as e:
        print(e)

    try:
 
        option.api_key = "bb30bdb9ae661f8754cb780249f6c8f9b92f12ed9bcabdcaab5b3d4f1d704531"
        option.num_docs = 5
        ask_ai_response = Ai12zService().search("who is alpesh", option)
        print("Ai12zSearch Response: ")
        pprint.pprint(ask_ai_response)
        
     

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
    

