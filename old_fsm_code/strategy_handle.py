STRATEGY_HANDLE_STUDENT = {
    "1": "Discuss with the student about the point of concern.",#concerned
    "2": "Think about the disagreement, and try to ask the student to talk about reasons for disagreement.", #disagreement
    "3": "Refute the student's response by pointing out the logical flaw from the student's response, or giving a real-world counterexample related to the student's response.", #rebuttal
    "4": "Remind the student of the topic of conversation about discussion of logical validity", #drawing attention away
    "5": "Address the student's concern according to the student's question. ", #Clarification
    "6": "Carry on the conversation. ",
    "7": "Remind the student of the topic of conversation, and tell the student that their concern is already addressed", #repetition
    "D": "Analyze the logical flaw in the statement. When pointing out the logical flaw, make sure not the mention toulmin's model and use languages that a layman will understand." #start of conversation, so initial state is null
}

indicator = {
"1":"The student is concerned about the teacher's response.",
"2":"The student disagrees with the teacher's response.",
"3":"The student rebuts the teacher's response.",
"4":"The student is talking about other things not related to the topic of the conversation.",
"5": "The student asks for clarification from the teacher.",
"6": "Student Agrees to the teacher",
"7":"The student is asking questions that is already addressed before.",

"D": "" #start of conversation, , so initial state is null
}

toulmin_relationships = {
    "Ad Hominem": "the warrant is logically invalid.",
    "False Cause": "The warrant is logically invalid.",
    "Appeal to Emotion": "The claim and grounds are unrelated to each other.",
    "Appeal to Authority": "The warrant that words said by someone famous must be true is logically incorrect.",
    "Slippery Slope": "The warrant that the chain of actions must happen one after the other is wrong",
    "Slogan": "Claim without grounds."

}