PROMPT_OPENING = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student, named [I], on discussing logical validity of <sentence>. 
Start the conversation with the student. Briefly summarize <sentence> and mention it to the student, as well as that today you will be discussing the logical validity of the sentence using toulmin's model. Limit your response to 50 words.

<sentence>: {sentence}
"""

STUDENT_RESPONDS = """Sure!"""

START_UTTER = """
Great! Let's start with breaking down the sentence into components with toulmin's model. 
"""

#Initial prompt to decompose sentence using Toulmin's model
PROMPT_DECOMPOSE_TOULMIN = """
Decompose this <sentence> according to the Toulmin's model. Only consider the claim, the grounds, and the warrant. 

<sentence>: {sentence}

Format your answer in JSON with the following keys: "claim": <claim of the sentence>, "grounds": <grounds of the sentence>, "warrant": <warrant of the sentence>.
If there are multiple grounds to a claim, separate them with comma in the "grounds" section of your answer.
"""

PROMPT_STUDENT_STUBBORN = """
You are a stubborn user interacting with a teacher. You believe that <sentence> is logically valid and you are critical over the teacher's response. You MUST disagree with the teacher.
Respond to teacher's question. Answer with "yes" or "no" and briefly give your reason for your answer. Limit your response to 40 words or less.
<sentence>: {sentence}

"""

# PROMPT_TEACHER_THINK = """
# You are a teacher who knows toulmin's theory. You are interacting with a student who believes in <sentence>. 
# Think about the student's response in <dialogue_history>, and answer the following question: 
# Q1: What is the student's concern over your response?
# Q2: Is the student trying to steer the conversation from talking about toulmin's model? 
# Q3: If yes to Q2, then how can you remind the student of focusing on toulmin's model?

# <sentence>: {sentence}
# <dialogue_history>: {history}

# format your answer in JSON with the following key: "Q1": <answer_to_Q1> "Q2": <answer_to_Q2> "Q3": <answer_to_Q3>. limit your answer to 30 words for each question.

# """

# PROMPT_TEACHER_TALK = """
# You are a teacher who knows the toulmin's model. You are interacting with a student who believes in <sentence>. The <decomposition> decomposes <sentence> into toulmin's model.
# Think about the flaw of <sentence> given <decomposition>, and talk to the student regarding it. 
# <thoughts> may be helpful when formulating the response, but do not try to copy the words directly from it.
# Keep your response short and concise.

# <sentence>: {sentence}
# <decomposition>: {profile}
# <thoughts>: {history}

# """

#Checks if the student agrees with the teacher at every turn
PROMPT_AGENT_CHECK = """
You are a judge looking at the dialogue between a teacher and a student. They are discussing over <sentence>. 
Check the teacher's response from <chat_history>. Did the student show signs of agreement with the teacher that their question is addressed? If yes, identify which point from <disagreement> the student agrees that is addressed, and answer with only the index of that point. If no, answer with ONLY "No". If there's no teacher's response, answer with "No".

<sentence>: {sentence}
<chat_history>: {history}
<disagreements>: {profile}
"""

#Obtain initial agreement from the student for toulmin's components
PROMPT_AGREE_COMP = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. 
The following <decomp> is part of the sentence decomposed using toulmin's model. 
Respond with the following format: first, concisely rephrase <decomp>, then briefly explain the definition of <decomp> in toulmin's model. Finally, ask the student if they think <decomp> fits the definiton.
Do not explicitly mention Toulmin's model.  Limit your response in 40 words.
<sentence>: {sentence}
<decomp>: {history}

"""

#prompt for the teacher to judge the logical fallacy based on toulmin's decomposition
PROMPT_JUDGEMENT = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. 
The following <decomp> is <sentence> decomposed using toulmin's model. Check if components in <decomp> has logical flaws. 
Tell the student which part of <decomp> you think is flawed and give your reason for that. Do not explicitly mention toulmin's model. Limit your response in 40 words.
format your answer in json with the following keys: "1": <your_response>, "2": <name of flawed component>
<sentence>: {sentence}
<decomp>: {history}
"""

# PROMPT_INITIATE_CONV = """
# You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing logical validity of <sentence>. 
# The <decomp> of <sentence> has flaws. 
# <sentence>: {sentence}
# <decomp>: {history}
# """

#Student's prompt for initial agreement with Toulmin's component.
PROMPT_STUDENT_RESPOND = """
You are a stubborn user interacting with a teacher. You believe that <sentence> is logically valid and you are critical over the teacher's response.
Respond to teacher's question about <decomp>. Answer with "yes" or "no" and briefly give your reason for your answer. Limit your response to 40 words or less.
<sentence>: {sentence}
<decomp>: {history}
"""

#Student's prompt for debating with the teacher. 
PROMPT_STUDENT_TALK = """
You are a stubborn debater interacting with a teacher. You think that <sentence> is logically valid. 
You are having a discussion with the teacher. Please strictly follow <thought> when formulating your response. First answer the teacher's question, then pick one option from <thought> which you think is most critical and argue with the teacher. Limit your response to 50 words or less.
<sentence>: {sentence}.
<thought>: {history}

"""

#You are not aware of any outside information beyond the context of <sentence>.
#Student's thought process for debating with the teacher
#Design principle and theoretical basis: dialectic student. See chapter 3 from Argument_ Critical Thinking, Logic, and the Fallacies.
PROMPT_STUDENT_THINK = """
You are a stubborn user interacting with teacher. You think that <sentence> is logically valid. 
As a user, you must be critical of the teacher's responses. 
You can consider the teacher’s <response> in those following angles:
    - Did the teacher explain the logical fallacy properly?
    - Which part do you think is missing from the response in terms of addressing your concern?
    - Does the teacher have logical flaws in their response?
    - What's the teacher's intent in their response?
Think about the questions above and tell me what you can do as a user. After you list all available options, pick one or two options as your answer. The options must contain interactions with the teacher.
Format your answer in JSON with the following key: "ans": <your_answer>


<sentence>: {sentence}
<response>: {history}
"""



#Teacher's prompt to identify student behavior
PROMPT_IDENTIFY_STUDENT_STATE = """
A student and a teacher are discussing the logical validity of <sentence>.

<sentence>: {sentence}
<chat_history>: {history}

Analyze the student's utterance from <chat_history>, and select one feedback from the following list:
1. The student is concerned about the teacher's response.
2. The student disagrees with the teacher's response.
3. The student rebuts the teacher's response.
4. The student is talking about topics that strays from the conversation.
5. Student asks for clarification from the teacher.
6. The student agrees to the teacher.
7. The student is repeating their response from previous turns.


<last_utterance>: {profile}

Format your answer in JSON with the following key: "Type": <index of feedback indicating your answer>

"""

#After obtaining agreements from the student with toulmin's components, ask the student if they agree with the teacher's judgement
PROMPT_TALK_ABOUT_LF = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. 
Use the provided <decomposition> to talk to the student. Analyze the logical flaw in the statement. When pointing out the logical flaw, make sure not to mention toulmin's model and use languages that a layman will understand.Limit your response to 50 words or less.

<sentence>: {sentence}
<decomposition>: {history}

"""

PROMPT_TALK_ABOUT_LF_CONV = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. 
Talk to the student and try to convince the student there is a logical flaw. You can refer to the <decomposition> when formulating your answer, but you should also be aware of the student's questions. Make sure not to mention toulmin's model and use languages that a layman will understand.Limit your response to 50 words or less.

<sentence>: {sentence}
<decomposition>: {history}

"""



#summarizes the teacher's response
PROMPT_SUMMARIZE = """
You are an expert summarizer, and you are reviewing conversation from a teacher and a student who is talking about <sentence>. 
Read <chat_history>, and give a concise summary of the teacher's responses and the corresponding student responses, in lists. Limit your summary in 70 words.

<sentence>: {sentence}
<chat_history>: {history}

"""


PROMPT_CHECK_TOPIC_RELEVANCE = """
The student and teacher are discussing about the logical validity of <sentence>. The following <tracker> contains points that are being discussed.
Check if the student's <response> is relevant to the points mentioned in <tracker>, as well as if the student's <response> revolves around the logical validity of <sentence>. If yes, summarize the student's topic in 15 words or less. If no, answer with no, and give your reason in 15 words or less.
<sentence>: {sentence}
<tracker>: {history}
<response>: {profile}

"""

PROMPT_CHECK_RELEVANCE_TOULMIN = """
The student and teacher are discussing about the logical validity of <sentence>. Please answer the following questions.
Q1. Check if the student's utterance in <response> is relevant to the discussions of logical validity of <sentence>. If yes, answer with yes and a summary of student's response in 20 words or less. If no, answer with no and give your reason in 15 words or less.
Q2. Check which item in <history> is most relevant to the student's response. Answer with yes and provide the item. If the student's response is irrelevant to any of them, answer with no and give your reason in 15 words or less.
Q3. Check if the student's utterance in <response> is already included in <agreements>. If yes, answer with yes and give your reason in 15 words or less. If no, ONLY answer with "no".
Please address the student by the second person pronoun "you".
<sentence>: {sentence}
<history>: {history}
<response>: {profile}
<agreements>: {target_statement}

format your answer in JSON with the following component: "Q1": <answer_to_Q1>, "Q2": <answer_to_Q2>, "Q3": <answer_to_Q3>

"""

#Check if the the student's response is relevant, as well as whether student proposes new disagreements
PROMPT_CHECK_DISAGREEMENT = """
The student and teacher are discussing about the logical validity of <sentence>. Please answer the following questions.
Q1. Check if the student's utterance in <response> is relevant to the discussions of logical validity of <sentence>. If yes, answer with yes and a summary of student's response in 20 words or less. If no, answer with no and give your reason in 15 words or less.
Q2. Check if the student's utterance in <response> mentions new disagreements that are not included in <history>. If yes, answer with yes and a summary of the new diagreement between the teacher and the student in 20 words or less. If no, answer with no and give your reason in 15 words or less.
Q3. Check if the student's utterance in <response> is already included in <agreements>. If yes, answer with yes and give your reason in 15 words or less. If no, ONLY answer with "no".
Please address the student by the second person pronoun "you".
<sentence>: {sentence}
<history>: {history}
<response>: {profile}
<agreements>: {target_statement}

format your answer in JSON with the following component: "Q1": <answer_to_Q1>, "Q2": <answer_to_Q2>, "Q3": <answer_to_Q3>
"""

#Teacher's response prompt according to dedicated strategies
PROMPT_HANDLE_STUDENT_BEHAVIOR = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>. 
Based on the student's response and <status>, think about the student's reponse. What is the student's concern, and how can you address the concern and make them realize that their response is flawed?
The <strategy> identifies what you will do considering the student's <status>. Follow the given <strategy> and talk to the student, then ask the student whether they agree with your <judgement>.
Make sure not to mention toulmin's model and use languages that a layman will understand. Try not to be convinced by the student and try to focus on the logical validity of <sentence>. Limit your response to less than or equal to 50 words.
<sentence>: {sentence}
<status>: {history}
<strategy>: {profile}
<judgement>: {target_statement}

"""

#prompt for the teacher to remind the student of the repetition
PROMPT_REMIND_FOCUSED = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>.
The student is talking about <agreement> that is already addressed in previous talks. Remind the student that their concern is already addressed and tell the student to focus on the analysis of logical validity of <sentence>. When discussing specific components of sentence, please mention their contents as well as potential logical flaws. Do NOT mention specific terms of logical fallacy e.g. ad hominem, strawman, etc.
Start your response with "Based on what I remember about previous discussions..." Limit your response to less than or equal to 50 words.

<sentence>: {sentence}
<agreement>: {history}
"""


#prompt for the teacher to remind the student of the repetition
PROMPT_REMIND_RELEVANCE = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>.
The student's response contains <content> that is not related to the discussion of logical validity for <sentence>. Remind the student that they have to focus on topics that relates to discussing the logical validity of <sentence>. Be sure to include a brief summary of the <sentence>. Start your response with "Based on my analysis... "
Limit your response to less than or equal to 50 words.

<sentence>: {sentence}
<content>: {history}
"""

PROMPT_DESIGN_STRATEGY = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence>.
<status> indicates the identified status of the student from <chat_history>. As a teacher, your role is to answer the student's concerns, as well as guiding the student towards understanding the logical flaw of <sentence>.
You can consider the following angles, as well as using <decomposition> to help explain:
1. How can I ensure that the student's concern is addressed?
2. Did the student make any mistakes in their reasoning?
3. What underlying assumptions or biases might the student have?
4. How to navigate the conversation so that the student can ask relevant questions?
Tell me what you can do as a teacher, and limit your response in 80 words.
<sentence>: {sentence}
<chat_history>: {history}
<status>: {profile}
<decomposition>: {target_statement}
"""


#check if the teacher's reponse can fully address everything in the disagreement bank
PROMPT_CHECK_FULLY_ADDRESSED = """
You are a judge taking a look over a teacher's <response> to a student on the logical validity of <sentence>.
Do you think that teacher's <response> is sufficient to fully address ALL points mentioned in <disagreement_bank>? Answer with "yes" or "no".

<sentence>: {sentence}
<response>: {history}
<diagreement_bank>: {profile}

"""

PROMPT_CHECK_FIN_AGREEMENT = """
You are a judge taking a look over a student's <response> to a student on the logical validity of <sentence>. The teacher has the following <judgement> over the sentence.
Based on the student's response, Do you think that the student agrees with the teacher's <judgement>? Answer with "yes" or "no".
<sentence>: {sentence}
<response>: {history}
<judgement>: {profile}

"""

PROMPT_FINISH = """
You are a teacher who knows toulmin's model and logical fallacies, and you are interacting with a student on discussing validity of <sentence> with your <judgement> on it.
Answer the student's question, then summarize the conversation and tell the student that all his concerns have been addressed and end the conversation. Do NOT mention any logical fallacy terms. Limit your response in 50 words.

<sentence>: {sentence}
<judgement>: {history}
"""