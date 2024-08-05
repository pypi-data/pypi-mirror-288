import requests
from typing import Any
import multiprocessing as mp
import time
import json
import os
from openai import OpenAI
from .llm_judge import JUDGE_PROMPT

def call_rag(endpoint, query):
    response = requests.post(endpoint, json={"query": query})
    try:
        output = response.json()
        return output["output"] 
    except:
        return "Error in response"
    
def evaluate_rag_result(
    client: OpenAI,
    question: str, 
    answer: str,
    model_output: str
) -> dict[str, Any]:
    exact_match = model_output == answer
    llm_judge_result = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        max_tokens=1,
        messages=[
            {"role": "system", "content": JUDGE_PROMPT}, 
            {"role": "user", "content": f"[User Question] {question} \n [Reference Answer] {answer} \n [Assistant Answer] {model_output} \n"}
            ],
    )
    return {"question": question, "answer": answer, "model_output": model_output, "exact_match": exact_match, "llm_judge_result": llm_judge_result}

def write_result_to_file(
    result: dict[str, Any], 
    write_file_name: str,
    file_write_lock: mp.Lock,
) -> None:
    with file_write_lock:
        with open(write_file_name, "a+") as outfile:
            json.dump(result, outfile)
            outfile.write("\n")


def main(args):
    client = OpenAI()
    endpoint = args.host
    question_file = args.question_file
    storage_file =  args.storage_file
    if os.path.isfile(storage_file):
        os.remove(storage_file)

    num_workers = 20
    file_write_lock = mp.Lock()
    inputs = []
    with open(args.question_file, 'r') as f:
        for line in f:
            inputs.append(json.loads(line))

    print('number of inputs: ', len(inputs))
    print("Start generating answers for evaluation dataset")
    start_time = time.time()
    with mp.Pool(num_workers) as pool:
        intermediate_results = []
        for idx, input in enumerate(inputs):
            result = pool.apply_async(
                call_rag,
                args=(endpoint,input["question"]),
                callback=lambda result: write_result_to_file(result, storage_file, file_write_lock),
            )
            input["model_output"] = result
            intermediate_results.append(input)
        pool.close()
        pool.join()
    end_time = time.time()
    print("total time used for inferencing evaluation dataset: ", end_time - start_time)

    evaluation_result_file = storage_file.replace(".jsonl", "_evaluation.jsonl")
    print("Start evaluating the generated answers")
    with mp.Pool(num_workers) as pool:
        results = []
        for idx, input in enumerate(intermediate_results):
            result = pool.apply_async(
                evaluate_rag_result,
                args=(client, input["question"], input["cot_answer"], input["model_output"]),
                callback=lambda result: write_result_to_file(result, evaluation_result_file),
            )
            input["model_output"] = result
            results.append(input)
        pool.close()
        pool.join()