import os
import argparse
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_functions import available_functions, call_function


def main():
    print("Hello from aibootbot!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("api key not found")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(
        role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    if response.usage_metadata is None:
        raise RuntimeError(
            "Response metadata unavailable; possible request failure")
    if args.verbose:
        print(f"User prompt:{args.user_prompt}")
        print(f"Prompt tokens:{response.usage_metadata.prompt_token_count}")
        print(
            f"Response tokens:{response.usage_metadata.candidates_token_count}")

    if response.function_calls is not None:
        result_list = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if len(function_call_result.parts) == 0:
                raise Exception("No results from function call?")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Nothing in results.parts[0]")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Nothing in results.parts[0].response")
            result_list.append(function_call_result.parts[0])
            if args.verbose:
                print(
                    f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(f"Response:{response.text}")


if __name__ == "__main__":
    main()
