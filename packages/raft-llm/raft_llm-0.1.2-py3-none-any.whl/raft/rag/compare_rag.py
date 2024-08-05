import time
from openai import OpenAI
import openai
import threading
import curses
from queue import Queue
import requests
import logging
# Function to handle model response fetching
def fetch_model_response(client, model, context, query, output_queue):
    try:
        # Create a generator to handle streaming
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": str([doc["page_content"] for doc in context])},
                {"role": "user", "content": query},
            ],
            stream=True
        )
        current_word = ""
        for chunk in response:
            chunk_text = chunk.choices[0].delta.content
            if chunk_text is not None:
                chunk_text = chunk_text
                # Handle partial words
                if " " in chunk_text:
                    parts = chunk_text.split(" ")
                    if current_word:
                        parts[0] = current_word + parts[0]
                    current_word = parts[-1]
                    for part in parts[:-1]:
                        output_queue.put(part + " ")
                else:
                    current_word += chunk_text
            else:
                chunk_text = ""
        if current_word:
            output_queue.put(current_word)
    except Exception as e:
        output_queue.put(f"Error: {e}")

def compare(modelA: str, modelB: str, query: str, retrieval_endpoint: str):
    # Set the logging level to WARNING to ignore INFO logs
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)
    # Retrieve context
    retrieve_content = requests.post(retrieval_endpoint, json={"query": query}).json()["output"]
    
    # Queues to hold model responses
    queueA = Queue()
    queueB = Queue()
    client = OpenAI()
    
    # Create threads for model responses
    threadA = threading.Thread(target=fetch_model_response, args=(client, modelA, retrieve_content, query, queueA))
    threadB = threading.Thread(target=fetch_model_response, args=(client, modelB, retrieve_content, query, queueB))
    
    # Start threads
    threadA.start()
    threadB.start()
    
    # Buffers to hold output for printing later
    bufferA = []
    bufferB = []
    outputBufferA = []
    outputBufferB = []
    # Initialize curses for terminal display
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    
    try:
        # Get the size of the terminal
        max_y, max_x = stdscr.getmaxyx()
        split_x = max_x // 2
        
        stdscr.clear()
        stdscr.addstr(0, 0, "Model A Response")
        stdscr.addstr(0, split_x, "Model B Response")
        
        lineA = 1
        lineB = 1
        
        while threadA.is_alive() or threadB.is_alive() or not queueA.empty() or not queueB.empty():
            if not queueA.empty():
                responseA = queueA.get()
                if type(responseA) is not None:
                    outputBufferA.append(responseA)
                    responseA = str(responseA).replace('\n', ' ')
                    words = responseA.split()
                    for word in words:
                        if len(" ".join(bufferA)) + len(word) + 5 > split_x:
                            stdscr.addstr(lineA, 0, " ".join(bufferA))
                            bufferA = [word]
                            lineA += 1
                        else:
                            bufferA.append(word)
                    stdscr.addstr(lineA, 0, " ".join(bufferA))
            if not queueB.empty():
                responseB = queueB.get()
                if type(responseB) is not None:
                    outputBufferB.append(responseB)
                    responseB = str(responseB).replace('\n', ' ')
                    words = responseB.split()
                    for word in words:
                        if len(" ".join(bufferB)) + len(word) + 5 > split_x:
                            stdscr.addstr(lineB, split_x, " ".join(bufferB))
                            bufferB = [word]
                            lineB += 1
                        else:
                            bufferB.append(word)
                    stdscr.addstr(lineB, split_x, " ".join(bufferB))
            
            stdscr.refresh()
            curses.napms(100)
        
    finally:
        time.sleep(10)
        # End curses
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(False)
        curses.endwin()
    
    # Wait for threads to complete
    threadA.join()
    threadB.join()
    # Print the buffered output after exiting curses mode
    print("Model A Response:")
    for line in outputBufferA:
        print(line, end="")
    
    print("\nModel B Response:")
    for line in outputBufferB:
        print(line,end="")
    print("\n")
