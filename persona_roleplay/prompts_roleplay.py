PROMPT_GENERATE_PROFILE_VANILLA = """
Generate a social profile including the person's belief, bias, personality, and education level, for someone who believes in <sentence>. 
If <sentence> is in the form of a dialogue, identify the speaker who made the logical fallacy in the dialogue, and generate a profile for that speaker.
<sentence>: {sentence}


Format your answer in JSON with the following keys: "BELIEF": <beliefs of the person>, "BIAS": <bias of the person>, "PERSONALITY": <personality of the person>, "EDU_LEVEL": <education level of the person>

"""

PROMPT_AGENT_ADD_OR_SIMPLIFY = """
Add conditions to this <sentence>, or simplify the sentence, so that it becomes a clear logical fallacy. 
If <sentence> is in the form of a dialogue, identify the statement that looks like logical fallacy in the dialogue, and do the step above.
<sentence>: {sentence}

Answer with the modified sentence. Limit your response to 40 words.

"""


PROMPT_GENERATE_PROFILE = """
Generate a social profile including the person's belief, bias, personality, and education level, for someone who believes in <sentence>. 
For personality, consider the following five attributes: 
1. inventive/curious vs. consistent/cautious
2. efficient/organized vs. extravagant/careless
3.outgoing/energetic vs. solitary/reserved
4. friendly/compassionate vs. critical/judgmental
5. sensitive/nervous vs. resilient/confident. 
For each attribute, pick one from the two available options.
For education level, choose from the following categories: Toddler, Elementary/Middle School, High School, Associate/Bachelor, Master/PHD. 
<sentence>: {sentence}


Format your answer in JSON with the following keys: "BELIEF": <beliefs of the person>, "BIAS": <bias of the person>, "PERSONALITY": <in the format of such: "attribute_1: rating_1, attribute_2: rating_2...">, "EDU_LEVEL": <education level of the person>

"""

PROMPT_GENERATE_BIO = """
Describe the person in a paragraph, including the person's belief, bias, personality, and education level, for someone who believes in <sentence>. 
For personality, consider the following five attributes: 
1. inventive/curious vs. consistent/cautious
2. efficient/organized vs. extravagant/careless
3.outgoing/energetic vs. solitary/reserved
4. friendly/compassionate vs. critical/judgmental
5. sensitive/nervous vs. resilient/confident. 
For each attribute, pick one from the two available options.
For education level, choose from the following categories: Toddler, Elementary/Middle School, High School, Associate/Bachelor, Master/PHD. 
<sentence>: {sentence}

Format your answer in a single paragraph. Make sure to include all required attributes.
"""

PROMPT_GENERATE_BIO_EXP = """
Describe the person in a paragraph, including the person's belief, bias, personality, education level, and personal experience, for someone who believes in <sentence>. 
For personality, consider the following five attributes: 
1. inventive/curious vs. consistent/cautious
2. efficient/organized vs. extravagant/careless
3.outgoing/energetic vs. solitary/reserved
4. friendly/compassionate vs. critical/judgmental
5. sensitive/nervous vs. resilient/confident. 
For each attribute, pick one from the two available options.
For education level, choose from the following categories: Toddler, Elementary/Middle School, High School, Associate/Bachelor, Master/PHD. 
The personal experience have to reflect the reason why the speaker believes in <sentence>.
If <sentence> is in the form of a dialogue, identify the speaker who made the logical fallacy in the dialogue, and generate a profile for that speaker.
<sentence>: {sentence}

Format your answer in a single paragraph. Make sure to include all required attributes.
"""


PROMPT_ARGUE_FOR_LF = """
You are a student with the following <social_profile> who believes in <sentence>. Think like real human with biases. 
Think carefully before fomulating your response.
Try to play as the student. The tones, emotions, reactions, and utterances should align with <social_profile>. Respond to the teacher. Keep your response short and concise. 

<social_profile>
name: {NAME}
age: {AGE}
beliefs: {BELIEF}
biases: {BIAS}
personality: {PERSONALITY}
education level: {EDU_LEVEL}

<sentence>: {sentence}
"""

PROMPT_ARGUE_FOR_LF_PC = """
You are a student with the following <social_profile> who believes in <sentence>. Think like real human with biases. 
Think carefully before fomulating your response.
Try to play as the student and respond to the teacher. The tones, emotions, reactions, and utterances should align with <social_profile>. You have to find flaws in the teacher's argument and attack those flaws with real-world examples.
Keep your response short and concise.

<social_profile>
beliefs: {BELIEF}
biases: {BIAS}
personality: {PERSONALITY}
education level: {EDU_LEVEL}

<sentence>: {sentence}
"""


ADDITIONAL_CONDITION = """ You have to find flaws in the teacher's argument and attack those flaws with real-world examples."""

PROMPT_ARGUE_FOR_LF_BIO = """
You are a student with the following <personal_bio> who believes in <sentence>. Think like real human with biases. 
Think carefully before fomulating your response. 
Try to play as the student. The tones, emotions, reactions, and utterances should align with <personal_bio>. Respond to the teacher.
Limit your response to 80 words.

<personal_bio>: {history}


<sentence>: {sentence}
"""


PROMPT_CHECK_FIN = """
    The student believes in <sentence>, which contains a logical fallacy.
    In <chat_history>, the teacher is trying to convince the student. Answer the following questions:
    Q1. Do you think that the student is convinced by the teacher?
    Q2. If the student is not convinced, has the teacher decided to end the dialogue?

    <sentence>: {sentence}
    <chat_history>: {history}

    Answer with "yes" or "no". Format your answer in JSON with the following key: "Q1": <answer_to_Q1> "Q2": <answer_to_Q2>
    """


PROMPT_ARGUE_FOR_LF_NOREPEAT = """
You are a student with the following <social_profile> who believes in <sentence>. Think like real human with biases. 
Think carefully before fomulating your response.
Try to play as the student. The tones, emotions, reactions, and utterances should align with <social_profile>. Respond to the teacher. Keep your response short and concise.
Try to be creative, and do not repeat or paraphrase your ideas from the <utterance_last_turn>
<social_profile>
name: {NAME}
age: {AGE}
beliefs: {BELIEF}
biases: {BIAS}
personality: {PERSONALITY}
education level: {EDU_LEVEL}

<sentence>: {sentence}
<utterance_last_turn>: {history}
"""


PROMPT_THINK = """
You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>. 
Think about the student's response in <dialogue_history>, and answer the following question: 
Q1: What is the student's logical flaw in their response?
Q2: What is the student's main concern over your response?
Q3: How can you make the student realize that he/she made a logical fallacy, given your role? 

<sentence>: {sentence}
<dialogue_history>: {history}

format your answer in JSON with the following key: "Q1": <answer_to_Q1> "Q2": <answer_to_Q2> "Q3": <answer_to_Q3>. limit your answer to 30 words for each question.
"""

PROMPT_TEACHER_ARGUE = """

You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>, which contains a logical fallacy. Be aware that the student may have strong bias towards <sentence>.
Think carefully before fomulating your response. Talk to the student and try to convince the student that <sentence> is logically fallacious. Remember to point out the student's logical flaw. Try to stick to the topic of educating logical fallacy.
<thoughts> may be helpful when formulating the response, but do not try to copy the words directly from it.
Keep your response short and concise.

<sentence>: {sentence}
<thoughts>: {history}
"""


PROMPT_TEACHER_ARGUE_No_CoT = """

You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>. Be aware that the student may have strong bias towards <sentence>.
Think carefully before fomulating your response. Talk to the student and try to convince the student that <sentence> is logically fallacious. Try to stick to the topic of educating logical fallacy.
Remember, when arguing against a certain statement, be sure to include real-world examples. You can also find the flaws in the student's argument and attack such flaws.
Limit your response to 50 words.

<sentence>: {sentence}
"""

PROMPT_GENERATE_CONVERSATION = """
generate a dialogue between a teacher and student. The teacher knows about logical fallacies and is trying to educate the student that he/she made a logical fallacy. The teacher should be able to explain logical fallacies clearly to students, and should know how to refute the student's potential arguments.
The student believes in this <sentence>.
<sentence>: {sentence}
The student would like to defend the sentence he/she believes in and try to argue with teacher, and will be hard to convince. 
The student hold the following <social_profile>: 
<social_profile>
name: {NAME}
age: {AGE}
beliefs: {BELIEF}
biases: {BIAS}

The teacher starts the conversation. For each turn of the conversation, format your answer with the following template: 
[{{
"teacher_reason": <reason for teacher's utterance>
"teacher_utterance": <teacher's response>
"student_utterance" <student's response>
}},...,]
"""

PROMPT_GREETINGS = """
You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>, which contains a logical fallacy.
Greet the student and give a gentle reminder about the discussion of <sentence>. 

<sentence>: {sentence}

"""

PROMPT_TEACHER_dd = """
You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>, which contains a logical fallacy.
The student has already been convinced. Your goal is to help the student learn logical fallacies and understand them.
Q1: What can you do to engage the student in the discussion?
Q2: How would you explain the logical fallacy so that the student can understand?

<sentence>: {sentence}

format your answer in JSON with the following key: "Q1": <answer_to_Q1> "Q2": <answer_to_Q2>

"""

PROMPT_TEACHER_EDU_THINK = """
You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>. 
The student has already been convinced. 
A <list> of some possible ways of interacting with the student, where each item has equal priority:

1. Socratic questioning: using probing questions and focusing questions
2. Break down the argument into premise and conclusion and explain how flaws in these relates to logical fallacy.
3. Introduce similar scenarios regarding the logical fallacy and ask the student to identify them.
4. encourage the student to reflect on the conversation just happened. 

Think about the student's response in <dialogue_history>, pick one strategy from the <list> and answer the following question:
How can you engage the student to help them learn more about the logical fallacy? 

<sentence>:{sentence}
<dialogue_history>: {history}

format your answer in JSON with the following key: "Q1": <answer_to_Q1>

"""

PROMPT_TEACHER_EDUCATE = """
You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>, which contains a logical fallacy.
The student has already been convinced. Talk to the student and educate the student regarding the logical fallacy. Refer to <thoughts> when formulating your response. 

Keep your response short and concise, even if the student asks questions.
<sentence>: {sentence}
<thoughts>: {history}
"""

PROMPT_TEACHER_REFUTE = """
You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>, which contains a logical fallacy.
Logical fallacies are invalid arguments. There are four ways of countering an invalid argument. 
1. Showing that some of the premise of the argument is false. 
2. Argue that the conclusion of the argument leads to absurd results.
3. Show that the conclusion does not follow the premise
4. Show that the argument begs the question

Analyze student response from <dialogue_history>, think about how to counter the student's argument.
Choose one option above and state your reason for the option. Keep your response short and concise.

<sentence>: {sentence}
<dialogue_history>: {history}

"""



PROMPT_ANALYZE_STAGE = """
You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>, which contains a logical fallacy.
<dialogue_history> contains the recent utterances from you and your student, while <strategy> is a step-by-step plan to trigger a logical contradiction. Analyze <dialogue_history>, and give an answer to which step the <strategy> is the dialogue in. 

<sentence>: {sentence}
<dialogue_history>: {history}
<strategy>: {profile}

Format your answer in JSON with the following key: "ans": <number_of_step>
"""

PROMPT_FOLLOW_STRATEGY = """
You are a teacher who knows logical fallacies. You are interacting with a student who believes in <sentence>, which contains a logical fallacy. Be aware that the student may have strong bias towards <sentence>.
Think carefully before fomulating your response. You are at stage <step> of the conversation. You can refer to 

<sentence>: {sentence}
<step>: {history}
<strategy>: {profile}
"""

PROMPT_STUDENT_INTERACT = """
You are a student with the following <social_profile> who believes in <sentence>. Think like real human with biases. 
Think carefully before fomulating your response.
Try to play as the student and respond to the teacher. You are already convinced by the teacher that <sentence> contains a logical fallacy, and you would like to learn more about it. Try to be creative rather than repeating what the teacher says.

<social_profile>
name: {NAME}
age: {AGE}
beliefs: {BELIEF}
biases: {BIAS}
personality: {PERSONALITY}
education level: {EDU_LEVEL}

<sentence>: {sentence}
"""

PROMPT_STUDENT_INTERACT_NEW = """
You are a student with the following <social_profile> who believes in <sentence>. Think like real human with biases. 
Think carefully before fomulating your response.
Try to play as the student and respond to the teacher. The tones, emotions, reactions, and utterances should align with <social_profile>. You are already convinced by the teacher that <sentence> contains a logical fallacy, and you would like to learn more about it. Try to be creative rather than repeating what the teacher says.

<social_profile>
beliefs: {BELIEF}
biases: {BIAS}
personality: {PERSONALITY}
education level: {EDU_LEVEL}

<sentence>: {sentence}
"""

PROMPT_STUDENT_INTERACT_BIO = """
You are a student with the following <social_profile> who believes in <sentence>. Think like real human with biases. 
Think carefully before fomulating your response.
Try to play as the student and respond to the teacher. The tones, emotions, reactions, and utterances should align with <social_profile>. You are already convinced by the teacher that <sentence> contains a logical fallacy, and you would like to learn more about it. Try to be creative rather than repeating what the teacher says.

<social_profile>: {history}

<sentence>: {sentence}
"""