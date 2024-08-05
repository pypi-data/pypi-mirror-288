import inspect
JUDGE_PROMPT = inspect.cleandoc("""
Please act as an impartial judge and evaluate the accuracy of the responses provided by an
AI assistant to the user question displayed below given the referebce answer to the question. 
Your evaluation should consider factual existence and correctness. You will be given a reference answer, 
assistant A’s answer,. Your job is to output a binary score of your judgement.
Begin your evaluation by comparing the assistants’ answer with the reference answer.
Identify and correct any mistakes. Avoid any position biases and ensure that the order in
which the responses were presented does not influence your decision. Do not allow the
length of the responses to influence your evaluation. Do not favor certain names of the
assistants. Be as objective as possible.After providing your explanation, output your
final verdict by strictly following this format : 1 if the assistant’s answer is correct, 0 if it is incorrect.
You should only output 1 or 0. No other output is allowed.                                
                                """)