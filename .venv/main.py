from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from browser_use import Agent, Browser, BrowserConfig
import asyncio
import re
import json

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    )
)

api_key = os.getenv("GEMINI_API_KEY")
llm = ChatGoogleGenerativeAI(model='gemini-2.5-pro-exp-03-25', api_key=api_key)

url = "https://www.nike.com/in/"

async def main():
    agent = Agent(
        # task="analyse this website https://www.nike.com/in/ and give me what kind of product they are selling, the theme of the company, and the target audience. Provide details in JSON format.",
        # task=f"analyse this website {urls} and give me what kind of product they are selling, the theme of the company, and the target audience. Provide details in JSON format.",
        task=f"Analyse this website {url} and give me:\n"
                     f"- What kind of products they are selling\n"
                     f"- The theme of the company\n"
                     f"- The target audience\n"
                     f"Return everything in proper JSON format.",
        llm=llm,
        browser=browser,
    )
    result = await agent.run()
    final_output = str(result[-1])
    
    match = re.search(r'```json(.*?)```', final_output, re.DOTALL)
    if match:
        raw_json = match.group(1).strip().strip("`")
        
        try:
            json_obj = json.loads(raw_json)
            formatted_json = json.dumps(json_obj, indent=2)
            print("Formatted JSON:\n", formatted_json)

            domain = url.split("//")[1].split("/")[0].replace(".", "_")
            with open(f"{domain}.json", "w", encoding="utf-8") as f:
                f.write(formatted_json)
                print(f"💾 Saved to {domain}.json")

        except json.JSONDecodeError as e:
            print("❌ Error decoding JSON:", e)
            print("⚠️ Raw output (for debug):\n", raw_json)
    else:
        print("🚫 No JSON block found in the result.")
        
    await browser.close()

asyncio.run(main())
