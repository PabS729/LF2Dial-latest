#Definitions of fallacies and strategies. Used for prior attempts of finding contradictions.
fallacy_dc = {
"faulty generalization": "an argument applies a belief to a large population without having a large enough sample to do so",
"false causality": "an argument assumes that since two events are correlated, they must also have a cause and effect relationship",
"circular reasoning": "an argument uses the claim it is trying to prove as proof that the claim is true.",
"ad populum": "an argument is based on affirming that something is true because a statistical majority believes so.",
"ad hominem": "a speaker trying to argue the opposing view on a topic makes claims against the other speaker instead of the position they are maintaining.",
"fallacy of logic": "there is a logical flaw in the reasoning behind the argument, such as a propositional logic flaw",
"appeal to emotion": "emotion is used to support an argument, such as pity, fear, anger, etc.",
"false dilemma": "incorrect limitations are made on the possible options in a scenario when there could be other options",
"equivocation": "ambiguous or evasive language is used to avoid committing oneself to a position, or the same is word is used in an argument but with different meanings.",
"fallacy of extension":"Also known as straw man, this is when an argument appears to be refuted by being replaced with an argument with a similar but weaker argument.",
"fallacy of relevance":"the speaker attempts to divert attention from the primary argument by offering a point that does not suffice as counterpoint/supporting evidence (even if it is true)",
"fallacy of credibility":"an appeal is made to some form of ethics, authority, or credibility.",
}

strategy_dc = {
"faulty generalization": "If the argument is a slippery slope, find a counterexample with the first sub-claim's premise and a conclusion that is contrary to the last sub-claim's conclusion. Otherwise, find a real-world example that is contrary to the conclusion.",
"false causality": "find a real-world example with the same premise, but leads to an opposite conclusion",
"circular reasoning": "Talk about what should hold true for the premise to be true, and talk about what should hold true for the conclusion to be true.",
"ad populum": "find a real-world example with a similar premise to the original argument, but the conclusion is clearly false",
"ad hominem": "find a real-world example where another person has the same attribute as the person being attacked, but exhibits traits that are opposite to the conclusion of the argument",
"fallacy of logic": "there is a logical flaw in the reasoning behind the argument, such as a propositional logic flaw",
"appeal to emotion": "Find a real-world example with a similar premise, but leads to a false conclusion.",
"false dilemma": "Take note of the two positions to choose from the sentence. Find a real-world example in the same premise, but can lead to a third conclusion different from the positions mentioned.",
"equivocation": " Identify the key word which is spoken with two different meanings. Find an example where the key word is used with its original meaning. ",
"fallacy of extension":"Understand the original position of the proponent and the interpretations made to this position. Find a real-world example that represents the original position, but leads to conclusions opposite from the interpretation.",
"fallacy of relevance": "Find a real-world example with a similar premise to the original argument, but leads to a false conclusion",
"fallacy of credibility":"find a real-world example where someone famous said something in the same topic, and what he or she said was proven clearly wrong",
"intentional":"an appeal is made to some form of ethics, authority, or credibility.",
"false analogy": "Regarding the two subjects of comparison, find one attribute from one of the subjects that leads to opposite conclusions from the argument."

}

option_refute = {
"1. Showing that some of the premise of the argument is false." ,
"2. Argue that the conclusion of the argument leads to absurd results.",
"3. Show that the conclusion does not follow the premise",
"4. Show that the argument begs the question"

}


strategy_dc_commonsense = {
"faulty generalization": "Find an example with a similar premise but the conclusion is the opposite from the original argument.",
"slippery slope": "Find a counterexample with the first sub-claim's premise and a conclusion that is contrary to the last sub-claim's conclusion. ",
"false causality": "find an example with the same premise, but leads to an opposite conclusion",
"circular reasoning": "Talk about what should hold true for the premise to be true, and talk about what should hold true for the conclusion to be true.",
"ad populum": "find a real-world example with a similar premise to the original argument, but the conclusion is clearly false",
"ad hominem": "find an example where another person has the same attribute as the person being attacked, but exhibits traits that are opposite to the conclusion of the argument",
# "fallacy of logic": "there is a logical flaw in the reasoning behind the argument, such as a propositional logic flaw",
"appeal to emotion": "Find an example with a similar premise, but leads to a false conclusion.",
"false dilemma": "Take note of the two positions to choose from the sentence. Find an example in the same premise, but can lead to a third conclusion different from the positions mentioned.",
"equivocation": " Identify the key word which is spoken with two different meanings. Find an example where the key word is used with its original meaning. ",
"fallacy of extension":"Understand the original position of the proponent and the interpretations made to this position. Find an example that represents the original position, but leads to conclusions opposite from the interpretation.",
"fallacy of relevance": "Analyze the premise and conclusion of the argument. Find an example with a similar premise, but leads to the opposite conclusion",
"fallacy of credibility":"find an example where someone famous said something in the same topic, and what he or she said was proven clearly wrong",
#"intentional":"an appeal is made to some form of ethics, authority, or credibility.",
"false analogy": "Regarding the two subjects of comparison, find one attribute from one of the subjects that leads to opposite conclusions from the argument."

}

V1_adp = "find a situation with a similar premise to the original argument, but the conclusion is clearly false"
emo_alt = "Find a situation with a similar premise and conclusion, but it is clearly absurd should the conclusion and premise both holds. "
straw_orig = "Understand the original position of the proponent. Make a real-world counterexample that represents the original position, but leads to conclusions opposite from the refutation made"
herring_orig = "Find a real-world example with similar premise to the original argument, but leads to the opposite conclusion"