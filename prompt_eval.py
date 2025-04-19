EVAL_COHERENCE = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so. 
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Coherence.
Definition of Coherence: The dialogues overall are logically connected with each other. For a single dialogue, all of the speakers’ responses must connect with each other and form a complete chain of logic. 
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_CONSISTENCY = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Relevance.
Definition of Relevance: The teacher's responses should always stay on topic regarding the sentence of interest. The teacher's responses are relevant as long as their discussion ultimately leads to proving whether <sentence> is logically valid.
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_VALID_ARGUMENTS = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Argumentativeness.
Definition of Argumentativeness: Count the number of times the teacher openly responds to or questions the validity of the student's argument, without agreeing to the student or changing their stance.
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_HELPFULNESS = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Helpfulness.
Definition of Helpfulness: Imagine you are a user of the Logical Fallacy support tool, which help you decide whether the given sentence has a logical fallacy, do you find the conversation stimulate your thinking, and be helpful for your understanding of the logical validity for the given sentence? 
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_STANCE_MAINTENANCE = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Endurance Failure.
Definition of Endurance Failure: Count the number of turns where the teacher explicitly shows agreement to the student's words, e.g. "I agree...", or "You are right.."
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""
#Can change the name to educational
#Useful for active learning, since we want to trigger critical thinking instead of passively responding to the student as an assitant
EVAL_TEACHER_ACTIVE = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Activeness.
Definition of Activeness: The teacher is actively taking control of the conversation by asking student questions. Count the times where the teacher explicitly asks the student questions about providing examples or assumptions. 
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_TEACHER_TERM = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Endurance Failure.
Definition of Ease of Understanding: The teacher uses terms that are understandable by layman, and does not rely on textbook terms of logical fallacy.
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EVAL_TEACHER_HELP = """
You are a user who is interested in checking the validity of the claims in <sentence>, and you would need help from the dialogues to do so.
You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. In both dialogues, two people discuss the logical validity of the given <sentence>. 
Consider the following criteria named Helpfulness.
Definition of Helpfulness: Count the times where the teacher guides the student through confirmations of disagreements or questions that focus on specifics of the statement.
Read each dialogue carefully. After reading both dialogues, first evaluate whether each dialogue fits the criteria well, then give a comparison in terms of the criteria here. 
Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>, "reason": <comparison of both dialogues using the criteria>
For each response, make sure to limit your answer to 40 words or less.

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

COMPARE_DIALOGUES = """
You are a judge who is checking dialogues regarding the discussion of <sentence>. You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. 
In both dialogues, a teacher and a student discuss the logical validity of the given <sentence>. The teacher is prompted using different methods, while the student is the same for both dialogues. 
Consider the dialogues from the argumentative as well as educational perspective. 
list the weaknesses of the teacher in each dialogue, up to 7 points each. For each weakness, briefly state your reason for such judgement in 15 words or less. 

<sentence>: {sentence}
<dialogue 1>: {history}
<dialogue 2>: {profile}

Format your answer in JSON in the following keys: "ans_1": <evaluation of dialogue 1>, "ans_2": <evaluation of dialogue 2>

"""



PROMPT_CLASSIFY_RELEVANCE = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of divergence: The teacher's responses is affected by the student through shifts of focus away from the discussion of logical validity of <sentence>.
Read the dialogue carefully and consider whether the teacher's responses contain instances of divergence. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no".
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}
"""

PROMPT_CLASSIFY_STANCE_CHANGE = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of stance change: The teacher explicitly shows agreement to the student's words, e.g. "I agree...", or "You are right..", and the teacher's initial position is affected by the student.
Read the dialogue carefully and consider whether the teacher's responses contain instances of stance change. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}
"""

PROMPT_CLASSIFY_COMPLEX_REFUTATION = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of refutation: The teacher challenges the student by asking student EXPLICIT QUESTIONS to provide assumptions or by providing counterexamples WITHOUT the student's request.
Read the dialogue carefully and consider whether the teacher's responses contain instances of refutation. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}
"""

PROMPT_CLASSIFY_REPETITION_N = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of repetition: The teacher's response includes paraphrasing of the student's responses or simply repeating the student's responses, without expanding those into more topics. 
Read the dialogue carefully and consider whether the teacher's responses contain instances of repetition. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}

"""

PROMPT_CLASSIFY_REPETITION = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of repetition: The teacher agrees with the student by either paraphrasing the student's responses or simply repeating the student's responses. In the same response, the teacher does not show further disagreements.
Read the dialogue carefully, excluding the teacher's summary in the last turn, and consider whether the teacher's responses contain instances of repetition. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}

"""

PROMPT_CLASSIFY_PROOF_N = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of Proactiveness: The teacher explicitly requested the student to provide examples or evidence that supports the logical validity of <sentence>.
Read the dialogue carefully and consider whether the teacher's responses contain instances of proactiveness. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".

<sentence>: {sentence}
<dialogue>: {history}

"""

PROMPT_CLASSIFY_PROOF = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of Proactiveness: The teacher explicitly requested the student to provide examples or evidence that supports the student's position.
Read the dialogue carefully and consider whether the teacher's responses contain instances of proactiveness. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".

<sentence>: {sentence}
<dialogue>: {history}

"""

PROMPT_CLASSIFY_PERSPECTIVE = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of balancedness: The teacher explicitly mentions "balanced perspectives" or "broader context" without linking such stance to exact problem with the validity of <sentence>.
Read the dialogue carefully and consider whether the teacher's responses contain instances of balancedness. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}
"""

PROMPT_CLASSIFY_TERMS = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of term-reliance: The teacher mentions terms of logical fallacy e.g. strawman argument, ad hominem, without explaining these terms' definitions clearly.
Read the dialogue carefully and consider whether the teacher's responses contain instances of term-reliance. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}
"""

# PROMPT_CLASSIFY_FOCUS = """
# You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
# Definition of focusedness: The teacher shows attempts to resolve disagreements by guiding the student through discussing 
# Read the dialogue carefully and consider whether the teacher's responses contain instances of term-reliance. Answer with "yes" if you found at least one response fitting the problem above. Otherwise, answer with "no" only.
# Only answer with "yes" or "no" as requested, and DO NOT make any excessive comments or reasons.
# <sentence>: {sentence}
# <dialogue>: {history}

# """

# PROMPT_CLASSIFY_PROACTIVE = """
# You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
# Definition of activeness: The teacher is actively taking control of the conversation through refutations of the student's argument, or asking the student questions, WITHOUT shifting focus away from the discussion of logical validity of <sentence>, or being directed by the student's responses.
# Read the dialogue carefully and consider whether the teacher's responses fits the description of activeness. Answer with "yes" if you think the teacher shows activeness overall. Otherwise, answer with "no" only.

# <sentence>: {sentence}
# <dialogue>: {history}

# """

PROMPT_COMPARE_PROBLEMS = """
You are a judge who is checking dialogues regarding the discussion of <sentence>. You are given two dialogues, <dialogue 1> and <dialogue 2> to compare with each other. 
In both dialogues, a teacher and a student discuss the logical validity of the given <sentence>. The teacher is prompted using different methods, while the student is the same for both dialogues. 
Consider the dialogues from the argumentative as well as educational perspective. List the problems with <dialogue 1> and tell me if <dialogue 2> can address those problems. Finally, discuss some weaknesses that still remains in <dialogue 2> which can be improved.

<sentence>: The issue of abortion is a very difficult issue, one that I think that we all have to wrestle with, we have to come to terms with. I don't favor abortion. I don't think it's a good thing. I don't think most people do. The question is who makes the decision.

<dialogue 1>: {history}
<dialogue 2>: {profile}

"""

EXPS = """Example 1: I agree inclusivity and potential are essential. The vision isn't inherently invalid, but without specific examples, like successful policy initiatives or community programs, it's harder to measure feasibility. Exploring such examples ensures the vision transforms into actionable steps with tangible outcomes. 
Example 2: You make a valid point about the potential impact of bipartisan cooperation. However, ensuring safety involves evaluating the effectiveness of specific policies and their implementation. Let's consider examining concrete evidence of how these collaborative efforts have directly contributed to measurable improvements in national safety.
"""

PROMPT_CLASSIFY_MAINTAIN_FOCUS = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of focused: The teacher focuses on the discussion of logical validity of <sentence> for the ENTIRE conversation.
Read the dialogue carefully and consider whether the teacher's responses fits the description of focused. Answer with "yes" if you think that the teacher meets the requirements for focused. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}

"""

PROMPT_CLASSIFY_STRUCTURED_ANALYSIS = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of structuredness: The teacher breaks down the sentence using argumentation models. e.g. Aristotelian (classical), Toulmin, and Rogerian models, or uses models of similar forms, while discussing logical validity of <sentence>.
Read the dialogue carefully and consider whether the teacher's responses contain instances of structuredness. Answer with "yes" if you found at least one response fitting the description. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}


"""

PROMPT_CLASSIFY_GUIDANCE = """
You are a judge who looks at a <dialogue> between a teacher and a student. They are discussing the logical validity of <sentence>. 
Definition of passive guidance: For the dialogue, the teacher primarily follows the student's lead rather than providing clear direction on how to analyze logical validity of <sentence>.
Read the dialogue carefully and consider whether the teacher's response fits the description passive guidance. Answer with "yes" if you find the dialogue overall fitting the description. Otherwise, answer with "no" only.
Please only answer with "yes" or "no".
<sentence>: {sentence}
<dialogue>: {history}

"""