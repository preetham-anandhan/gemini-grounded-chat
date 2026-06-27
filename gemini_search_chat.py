import sys
from google import genai
from google.genai import types

# =====================================================================
# CONFIGURATION: HARDCODED CREDENTIALS
# =====================================================================
# Your Gemini API Key from Google AI Studio
MY_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

def run_grounded_chat():
    # 1. Initialize the official Google GenAI Client with the hardcoded key
    print("🔑 Authenticating API Key...")
    client = genai.Client(api_key=MY_API_KEY)
    
    # 2. Configure Google Search as a live Tool for Grounding
    search_tool = types.Tool(google_search=types.GoogleSearch())
    
    config = types.GenerateContentConfig(
        tools=[search_tool],
        system_instruction="You are a helpful assistant with access to real-time Google Search information. Be concise and accurate."
    )
    
    # 3. Create a stateful multi-turn chat session using gemini-2.5-flash
    model_id = "gemini-2.5-flash"
    
    print(f"🚀 Initializing Chat Session with [{model_id}] + Google Search...")
    chat = client.chats.create(model=model_id, config=config)
    print("✨ System online. Type 'exit' or 'quit' to close the program.\n")
    
    # 4. Interactive Conversation Loop
    while True:
        try:
            user_input = input("👤 You: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("👋 Goodbye!")
                break
                
            # Send message through the stateful chat stream
            response = chat.send_message(user_input)
            print(f"🤖 Gemini: {response.text}")
            
            # 5. Extract and print Grounding/Search Metadata (Optional inspection)
            candidates = response.candidates
            if candidates and candidates[0].grounding_metadata:
                metadata = candidates[0].grounding_metadata
                if metadata.web_search_queries:
                    print(f"   [🔍 Search Queries Executed: {', '.join(metadata.web_search_queries)}]")
                    
            print("-" * 50)
            
        except Exception as e:
            print(f"⚠️ An error occurred: {e}")

# =====================================================================
# EXECUTION ENTRY POINT (Crucial: This tells Python to execute the function!)
# =====================================================================
if __name__ == "__main__":
    run_grounded_chat()