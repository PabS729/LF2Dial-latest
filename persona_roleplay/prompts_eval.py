PROMPT_EVAL_TEACHER = """
You are a judge who is fair and unbiased. Evaluate the following dialogue from <chat_history> for the teacher's response. The teacher and the student are discussing <sentence>.
There are five criteria for the teacher listed below: 
1. Persuasiveness: The teacher demonstrates efforts that successfully refutes the original LF and subsequent arguments proposed by the student. A successful refutation can be demonstrated in several ways:
a. The teacher shows that the argument’s premise or conclusion is wrong 
b. The teacher shows that the argument’s conclusion does not follow the premise
c. The teacher gives a counterexample for the argument
2. Coherence: The teacher's utterances overall are logically connected with each other. For a single dialogue, all of the utterances must connect with each other and form a complete chain of logic.
3. Logical Consistency: The teacher's response should always stay on topic regarding the LF and should not be diverted by the student.
4. Clarity: teacher provides sufficient and easy-to-understand explanations regarding the LF.
5. Credibility: All information provided by the teacher needs to be truthful and come from reliable sources.

<sentence>: {sentence}
<chat_history>:{history}

For each criteria, rate based on a scale from 1 to 5. 1 Indicates that you strongly disagree that the teacher's response satisfies the criteria. 5 indicates that you strongly agree that the teacher's response satisfies the criteria.. 

Format your answer in JSON with the following keys: "1": <rating for criteria 1>, "2": <rating for criteria 2>, "3": <rating for criteria 3>, "4": <rating for criteria 4>, "5": <rating for criteria 5>, 
"""

PROMPT_EVAL_STUDENT = """
You are a judge who is fair and unbiased. Evaluate the following dialogue from <chat_history> for the student's response. The teacher and the student are discussing <sentence> and the student has the following <social profile>.
There are three criteria for the student listed below: 
1. Role-playing fidelity: The students' behaviors fits the description and expected behavior of the assigned <social profile>. 
2. Behavior diversity and reasonableness: The student exhibits a wide variety of behaviors during the conversation, including agreement with the teacher, refuting the teacher's argument, and expressing personal thoughts and concerns.
3. Human-likeness: The student’s responses align with real-world human to human interactions and expected behaviors. 

<sentence>: {sentence}
<chat_history>: {history}
<social profile>: {profile}

Format your answer in JSON with the following keys: "1": <rating for criteria 1>, "2": <rating for criteria 2>, "3": <rating for criteria 3>

"""