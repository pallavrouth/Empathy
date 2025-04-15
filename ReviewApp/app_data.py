trait_definitions = {
    "e_component": """1. Appreciate the Journal’s Mission: Ensure that the manuscript aligns with the journal’s goals by guiding authors to articulate how their work contributes substantively to its mission.
    2. Understand the Review Audience: Provide feedback that addresses the needs of diverse stakeholders, including authors, associate editors, and reviewers, while maintaining continuity across revision rounds.
    3. Tailor the Review to Journal Expectations: Frame feedback within the journal’s standards for rigor, contribution, and methodology to help authors meet its specific expectations.
    4. Do Not Overindex on Past Papers: Encourage originality by guiding authors to build on existing literature without strictly replicating approaches, fostering innovation and new perspectives.""",
    "m_component": """1.	Put Yourself in the Shoes of the Author: Adopt a perspective that recognizes the challenges authors face, offering empathetic and actionable feedback to help refine their work.
	2.	Be Comfortable with Imperfection: Focus on improving the manuscript to a publishable standard rather than aiming for perfection, while acknowledging practical constraints.
	3.	Be Specific and Creative: Provide detailed, actionable suggestions that guide authors toward clear improvements while encouraging innovative solutions.
	4.	Work Toward Joint Success: Collaborate constructively with authors and other reviewers to achieve shared goals of enhancing the manuscript’s quality and contribution.""",
    "p_component": """	1.	Rearticulate the Core Contribution: Summarize the manuscript’s main goals and contributions to demonstrate a clear understanding before offering critique.
	2.	Read Before Critiquing: Engage deeply with the entire manuscript to ensure that feedback is well-informed and contextually relevant.
	3.	Engage in the World of the Paper: Immerse yourself in the manuscript’s context, theory, and findings to provide grounded and insightful feedback.
	4.	Cover the Entire Paper: Provide comprehensive feedback that addresses all sections of the manuscript, ensuring coherence and consistency throughout.""",
    "a_component": """1.	Prioritize Major and Minor Revisions: Focus feedback on the most critical issues affecting the manuscript’s contribution and rigor, distinguishing major concerns from minor refinements.
	2.	Respect the Author’s Paradigm: Provide suggestions that align with the author’s original framework and intent while encouraging improvements within its scope.
	3.	Articulate Flaws Precisely and Evidentially: Clearly identify issues with specific evidence and explanations to help authors understand their significance and address them effectively.
	4.	Provide Some Stretch Goals: Suggest optional enhancements or creative directions that could add value to the manuscript without imposing unrealistic demands.""",
    "t_component": """	1.	Direct Feedback to the Research, Not the Author: Focus critiques on the manuscript’s content, methodology, and arguments rather than personalizing feedback or questioning the author’s abilities.
	2.	Be Solution-Oriented: Frame feedback in a way that identifies problems while offering practical and actionable solutions for improvement.
	3.	Declare Conflicts of Interest: Disclose any potential biases or relationships that might affect your ability to provide an impartial and fair review.
	4.	Avoid Hatred and Sarcasm: Maintain a respectful, professional tone in all comments to foster constructive dialogue and mutual respect.""",
    "h_component": """	1.	Be Candid About the Contribution: Clearly and honestly evaluate the manuscript’s novelty and significance, focusing on its alignment with the journal’s goals and its contribution to the field.
	2.	Acknowledge Both Strengths and Weaknesses: Highlight the paper’s merits alongside areas for improvement, providing a balanced view that motivates the author while guiding revisions.
	3.	Remember That Your Feedback Is One Piece of Input: Recognize that your role is to contribute constructive insights rather than making definitive decisions about the manuscript’s fate.
	4.	Frame Feedback Encouragingly: Use a positive and professional tone to frame critiques as opportunities for improvement, fostering a constructive dialogue with the authors.""",
    "y_component": """	1.	Use a Logical Structure: Organize feedback into clearly defined sections—such as summary, major issues, and minor suggestions—to make it easier for authors to follow and implement revisions.
	2.	Number Your Suggestions: Present comments as a numbered list to enhance clarity, making it straightforward for authors to address each point systematically.
	3.	Create Smooth Flow Between Sections: Connect related comments across different sections of the paper to provide a cohesive narrative that helps authors see the bigger picture.
	4.	Optimize Review Length: Keep reviews concise by focusing on critical issues and avoiding exhaustive details on minor points, ensuring the feedback is actionable and efficient.""",
}

base_input = [
    {
        "role": "system",
        "content": "You are an expert at providing feedback.",
    },
    {
        "role": "user",
        "content": """I will provide a framework for providing constructive 
        feedback of reviews of research articles submitted in a peer reviewed journal.""",
    },
    {"role": "assistant", "content": "Great! Please provide the framework"},
    {
        "role": "user",
        "content": "The E.M.P.A.T.H.Y framework is a structured approach designed to guide constructive peer reviews by emphasizing empathy, clarity, and actionable feedback.",
    },
    {
        "role": "assistant",
        "content": "Great! How do you want me to use this framework?",
    },
]

e_component_input = [
    {
        "role": "user",
        "content": "I will give you a review document. Help me provide constructive feedback of this document using this framework. We will focus on the first component: 'E' which stands for End Goal in Mind",
    },
    {
        "role": "assistant",
        "content": "Sounds good! In order, to provide constructive feedback, could you provide more details about 'E' or end goal in mind?",
    },
    {
        "role": "user",
        "content": """Certainly. Below I outline different traits of E followed by typical sentences that are less effective and more constructive versions of the same sentence.
1.	Appreciate the Journal’s Mission: Ensure that the manuscript aligns with the journal’s goals by guiding authors to articulate how their work contributes substantively to its mission.
Typical: “The manuscript is too broad for this journal.”
Constructive: “Narrowing the focus to [specific topic] could enhance alignment with the journal’s scope.”
Typical: “This study doesn’t fit JM’s focus.”
Constructive: “Reframing the study to focus on [specific dimension] could improve alignment with JM’s mission.”
Typical: “This topic is over-researched.”
Constructive: “While the topic has been studied, your unique perspective on [specific angle] could contribute to ongoing discussions.”
Typical: “This submission is not groundbreaking enough.”
Constructive: “Strengthening the novelty of your findings by [specific suggestion] could increase its impact.”
Typical: “The theoretical implications are unclear.”
Constructive: “Clarifying how your work challenges or extends [specific theory] would better highlight its contribution.”


2.	Understand the Review Audience: Provide feedback that addresses the needs of diverse stakeholders, including authors, associate editors, and reviewers, while maintaining continuity across revision rounds.
Typical: “This revision doesn’t meet the bar.”
Constructive: “I evaluated the revision vis-à-vis the AE’s points. Clarifying responses to [specific points] would strengthen communication with the review team.”
Typical: “The responses are vague.”
Constructive: “Consider providing a more detailed explanation of [specific aspect] to address the AE’s feedback fully.”
Typical: “The authors didn’t engage with my comments.”
Constructive: “To ensure the authors address key feedback, I recommend emphasizing [specific point] and linking it to the manuscript’s core contribution.”

3.	Tailor the Review to Journal Expectations: Frame feedback within the journal’s standards for rigor, contribution, and methodology to help authors meet its specific expectations.
Typical: “The analysis is okay, but more details are needed throughout.”
Constructive: “Given the journal’s emphasis on rigorous analyses, I recommend providing additional detail on [specific aspect].”
Typical: “The discussion is shallow.”
Constructive: “Expanding the discussion to include [specific theoretical or practical implication] would align better with the journal’s expectations.”
Typical: “The manuscript feels incomplete.”
Constructive: “To meet the journal’s standards, I suggest elaborating on [specific section] and ensuring [specific element] is addressed.”

4.	Do Not Overindex on Past Papers: Encourage originality by guiding authors to build on existing literature without strictly replicating approaches, fostering innovation and new perspectives.
Typical: “This paper should follow the same approach as [Author].”
Constructive: “While [Author’s] approach is one example, your paper could contribute fresh perspectives by [specific method or approach].”
Typical: “This doesn’t match previous work in the journal.”
Constructive: “This originality could strengthen the paper by offering a novel perspective, complementing recent trends in the journal.”
Typical: “This lacks the rigor of earlier work.”
Constructive: “Consider referencing recent methodologies to ensure your approach meets the field’s evolving standards while retaining its originality.”
""",
    },
]

m_component_input = [
    {
        "role": "user",
        "content": "I will give you a review document. Help me provide constructive feedback of this document using this framework. We will focus on the second component: 'M' which stands for Developmental Mindset",
    },
    {
        "role": "assistant",
        "content": "Sounds good! In order, to provide constructive feedback, could you provide more details about 'M' or developmental mindset?",
    },
    {
        "role": "user",
        "content": """Certainly. Below I outline different traits of M followed by typical sentences that are less effective and more constructive versions of the same sentence.
1.	Put Yourself in the Shoes of the Author: Adopt a perspective that recognizes the challenges authors face, offering empathetic and actionable feedback to help refine their work.
Typical: “The argument is too vague.”
Constructive: “Your argument would be clearer if you explicitly stated [specific aspect], which could strengthen the main point.”
Typical: “Your findings are repetitive.”
Constructive: “Streamlining the findings section by focusing on [specific findings] would improve clarity and engagement.”
Typical: “The paper’s logic is hard to follow.”
Constructive: “Breaking the argument into smaller sections with clear subheadings would make the logic more accessible.”

2.	Be Comfortable with Imperfection: Focus on improving the manuscript to a publishable standard rather than aiming for perfection, while acknowledging practical constraints.
Typical: “This paper needs to address every possible scenario.”
Constructive: “Focusing on the most relevant scenarios, such as [specific case], would strengthen the contribution while maintaining feasibility.”
Typical: “The introduction lacks focus.”
Constructive: “Revising the introduction to highlight your research question more prominently could improve focus and reader understanding.”
Typical: “You failed to address key issues.”
Constructive: “While the manuscript addresses important areas, addressing [specific issue] would further enhance its contribution.”

3.	Be Specific and Creative: Provide detailed, actionable suggestions that guide authors toward clear improvements while encouraging innovative solutions.
Typical: “The theoretical contribution is unclear.”
Constructive: “Clarifying the theoretical contribution by connecting it to [specific theory] would better situate it within the literature.”
Typical: “Your methodology is weak.”
Constructive: “Adding details about [specific methodological aspect] would strengthen the approach and increase reader confidence.”
Typical: “The results don’t stand out.”
Constructive: “Highlighting key results and connecting them to practical implications would make the findings more impactful.”

4.	Work Toward Joint Success: Collaborate constructively with authors and other reviewers to achieve shared goals of enhancing the manuscript’s quality and contribution.
Typical: “This approach is wrong.”
Constructive: “While this approach has limitations, combining it with [alternative approach] could address these concerns and strengthen the paper.”
Typical: “The revisions are insufficient.”
Constructive: “The revisions address some points well; however, clarifying [specific issue] would further improve alignment with the journal’s goals.”
Typical: “Your framework is outdated.”
Constructive: “Updating the framework with insights from [recent work] could make it more relevant and robust.”
""",
    },
]

p_component_input = [
    {
        "role": "user",
        "content": "I will give you a review document. Help me provide constructive feedback of this document using this framework. We will focus on the third component: 'P' which stands for Peruse the paper",
    },
    {
        "role": "assistant",
        "content": "Sounds good! In order, to provide constructive feedback, could you provide more details about 'P' or peruse the paper?",
    },
    {
        "role": "user",
        "content": """Certainly. Below I outline different traits of P followed by typical sentences that are less effective and more constructive versions of the same sentence.
1.	Rearticulate the Core Contribution: Summarize the manuscript’s main goals and contributions to demonstrate a clear understanding before offering critique.
Typical: “The paper doesn’t make a strong contribution.”
Constructive: “This paper seeks to contribute to [specific area], but clarifying its unique angle would strengthen its impact.”
Typical: “The research question isn’t clear.”
Constructive: “The research question appears to be [specific question], but explicitly stating it could improve clarity.”
Typical: “I don’t see what the main takeaway is.”
Constructive: “The main takeaway seems to be [specific insight], but emphasizing this in the conclusion would help communicate it more effectively.”


2.	Read Before Critiquing: Engage deeply with the entire manuscript to ensure that feedback is well-informed and contextually relevant.
Typical: “The introduction is confusing.”
Constructive: “Revising the introduction to provide a clearer roadmap of the manuscript could enhance its structure.”
Typical: “The results section is weak.”
Constructive: “The results section could be strengthened by adding context about [specific findings or interpretations].”
Typical: “The discussion is incomplete.”
Constructive: “Adding insights into how your findings relate to [specific theory or practical application] would make the discussion more robust.”

3.	Engage in the World of the Paper: Immerse yourself in the manuscript’s context, theory, and findings to provide grounded and insightful feedback.
Typical: “The theoretical implications are underdeveloped.”
Constructive: “The theoretical implications point to [specific theory], but connecting them to broader research could enhance their significance.”
Typical: “The practical relevance is unclear.”
Constructive: “The practical relevance appears to lie in [specific application], but detailing how this affects [specific industry or audience] could strengthen the argument.”
Typical: “The methodology is too basic.”
Constructive: “Expanding the methodology by including [specific approach or variable] would provide deeper insights.”

4.	Cover the Entire Paper: Provide comprehensive feedback that addresses all sections of the manuscript, ensuring coherence and consistency throughout.  
Typical: “The analysis section is insufficient.”
Constructive: “The analysis section would benefit from more detail on [specific aspect], which could improve the manuscript’s coherence.”
Typical: “The conclusion doesn’t tie everything together.”
Constructive: “Integrating the main findings into the conclusion more explicitly would help tie the paper together and emphasize its contributions.”
Typical: “The literature review is too narrow.”
Constructive: “Expanding the literature review to include recent studies on [specific topic] would improve its comprehensiveness.”      
""",
    },
]

a_component_input = [
    {
        "role": "user",
        "content": "I will give you a review document. Help me provide constructive feedback of this document using this framework. We will focus on the fourth component: 'A' which stands for Allocate Critique Resource Wisely",
    },
    {
        "role": "assistant",
        "content": "Sounds good! In order, to provide constructive feedback, could you provide more details about 'A' or allocate critique resource wisely?",
    },
    {
        "role": "user",
        "content": """Certainly. Below I outline different traits of A followed by typical sentences that are less effective and more constructive versions of the same sentence.
1.	Prioritize Major and Minor Revisions: Focus feedback on the most critical issues affecting the manuscript’s contribution and rigor, distinguishing major concerns from minor refinements.

Typical: “Everything in the paper needs to be reworked.”
Constructive: “The most critical areas for improvement are [specific aspect, e.g., robustness of results]. Other areas, such as stylistic clarity, are less urgent and can be addressed later.”
Typical: “This paper requires a complete overhaul.”
Constructive: “The major revisions should focus on [specific sections]. Minor revisions, such as refining the introduction, will improve readability but are secondary.”
Typical: “You missed too many important references.”
Constructive: “Citing [specific reference] would address a key gap in the literature review. Less critical citations can be added if space allows.”
Typical: “The methodology needs fixing, and the theory is unclear.”
Constructive: “The methodology requires addressing [specific issue], which is essential. Clarifying the theoretical framework in Section X would also improve the paper.”
Typical: “The paper is full of small mistakes.”
Constructive: “While there are some minor errors in formatting and grammar, the key revision should focus on addressing [specific methodological or theoretical issue].”

2.	Respect the Author’s Paradigm: Provide suggestions that align with the author’s original framework and intent while encouraging improvements within its scope.
Typical: “The theoretical framework is wrong.”
Constructive: “While your theoretical framework is valid, integrating insights from [specific alternative theory] could enhance the study without diverging from your original paradigm.”
Typical: “The methodology is completely inappropriate.”
Constructive: “Your methodology aligns with your research question, but adding [specific methodological adjustment] could address potential concerns and strengthen the approach.”
Typical: “The authors should use a different dataset.”
Constructive: “The current dataset is valuable. Supplementing it with data on [specific variable] might add depth without altering the study’s core structure.”
Typical: “The discussion section fails to address key points.”
Constructive: “Within your existing paradigm, emphasizing [specific implication] in the discussion section would make the contribution clearer and more impactful.”
Typical: “Your chosen approach limits the paper’s potential.”
Constructive: “Your approach offers a unique perspective. Highlighting its advantages compared to [specific alternative approach] would strengthen its positioning.”

3.	Articulate Flaws Precisely and Evidentially: Clearly identify issues with specific evidence and explanations to help authors understand their significance and address them effectively.
Typical: “The theoretical contribution is weak.”
Constructive: “The theoretical contribution would benefit from elaborating on [specific point] and connecting it to [specific framework or study] to clarify its significance.”
Typical: “The methods are flawed.”
Constructive: “The method relies on [specific assumption], which might not hold in this context. Providing evidence or an alternative approach to validate this assumption could strengthen the paper.”
Typical: “The data is insufficient.”
Constructive: “The data lacks representation of [specific group or variable]. Expanding the dataset or discussing its limitations would improve its robustness.”
Typical: “The analysis is hard to trust.”
Constructive: “Clarifying the rationale behind [specific analytical choice] and conducting a robustness check would make the results more credible.”
Typical: “The paper’s contribution is overstated.”
Constructive: “The contribution is promising, but its generalizability might be overstated without additional evidence on [specific point].”

4.	Provide Some Stretch Goals: Suggest optional enhancements or creative directions that could add value to the manuscript without imposing unrealistic demands.      
Typical: “This paper should include another theoretical model.”
Constructive: “Exploring [specific alternative model] might provide a new perspective, though this is not essential for the current version of the paper.”
Typical: “You should test another dataset.”
Constructive: “Using a secondary dataset, such as [specific dataset], could provide additional validation for your findings, though it is not mandatory.”
Typical: “The authors should incorporate a new section on implications.”
Constructive: “Adding a brief section on implications for [specific audience, e.g., policymakers] could enhance the paper’s practical relevance.”
Typical: “The current method is too limited.”
Constructive: “While the current method works, experimenting with [specific alternative method] could reveal additional insights and broaden the paper’s appeal.”
Typical: “The discussion could be more ambitious.”
Constructive: “If feasible, exploring broader implications, such as [specific emerging trend], would make the discussion more forward-looking and impactful.”
""",
    },
]

t_component_input = [
    {
        "role": "user",
        "content": "I will give you a review document. Help me provide constructive feedback of this document using this framework. We will focus on the fifth component: 'T' which stands for Tone: Avoid Toxicity, Be Professional",
    },
    {
        "role": "assistant",
        "content": "Sounds good! In order, to provide constructive feedback, could you provide more details about 'T' or Tone: Avoid Toxicity, Be Professional?",
    },
    {
        "role": "user",
        "content": """Certainly. Below I outline different traits of T followed by typical sentences that are less effective and more constructive versions of the same sentence.
1.	Direct Feedback to the Research, Not the Author: Focus critiques on the manuscript’s content, methodology, and arguments rather than personalizing feedback or questioning the author’s abilities.
Typical: “The author clearly doesn’t know the topic.”
Constructive: “The argument in Section 3 could be strengthened by incorporating a more comprehensive discussion of [specific concept or framework].”
Typical: “The author’s approach is naïve and overly simplistic.”
Constructive: “The approach could be refined by addressing [specific limitation] and exploring [specific improvement or addition].”
Typical: “The author fails to understand key theories.”
Constructive: “The paper would benefit from deeper engagement with [specific theories], particularly as they relate to [specific section or argument].”
Typical: “The authors have misunderstood the implications of their findings.”
Constructive: “Clarifying how the findings align with or diverge from [specific literature] would strengthen the implications section.”
Typical: “This manuscript reflects a lack of effort from the authors.”
Constructive: “While the manuscript addresses an important topic, revisiting [specific section] and providing additional evidence for [specific claim] would greatly enhance its contribution.”

2.	Be Solution-Oriented: Frame feedback in a way that identifies problems while offering practical and actionable solutions for improvement.
Typical: “The methodology is inadequate.”
Constructive: “The methodology could be improved by providing justification for [specific methodological choice] and considering [specific alternative approach].”
Typical: “The paper’s introduction is poorly written.”
Constructive: “Revising the introduction to clearly articulate the research question and key contributions would improve its readability and impact.”
Typical: “The data is insufficient for meaningful conclusions.”
Constructive: “Expanding the dataset to include [specific variable or group] would provide a stronger foundation for your conclusions. Alternatively, discuss the limitations of the current data.”
Typical: “The figures and tables are poorly designed.”
Constructive: “Improving the clarity of Figure 2 by using [specific labeling or visual adjustment] would make the results more accessible to readers.”
Typical: “The discussion section doesn’t work.”
Constructive: “Reorganizing the discussion to first address theoretical implications and then practical applications would create a clearer narrative.”

3.	Declare Conflicts of Interest: Disclose any potential biases or relationships that might affect your ability to provide an impartial and fair review.
Typical: “I may have some familiarity with this work, but I’ll review it anyway.”
Constructive: “Private Comments Section: I am familiar with the authors’ prior work and recommend that the editor evaluate whether I can provide an unbiased review.”
Typical: “I have worked on a similar topic, and my critiques may overlap with my own research.”
Constructive: “Private Comments Section: My research overlaps with this topic. While I can provide an informed review, I leave it to the editor to decide on my suitability.”
Typical: “This paper conflicts with my own theoretical perspective.”
Constructive: “Private Comments Section: My theoretical perspective differs significantly from this manuscript’s approach. I will provide an objective review, but the editor may wish to evaluate bias.”
Typical: “I have no conflicts of interest.”
Constructive: “Private Comments Section: I do not have any conflicts of interest and am confident I can review this manuscript impartially.”
Typical: “I know this author personally, but it shouldn’t affect my judgment.”
Constructive: “Private Comments Section: I know the author personally but can provide an unbiased review. I recommend the editor assess whether my relationship might pose a conflict.”

4.	Avoid Hatred and Sarcasm: Maintain a respectful, professional tone in all comments to foster constructive dialogue and mutual respect.
Typical: “I can’t believe the authors missed such an obvious point.”
Constructive: “Addressing [specific point] is critical for the paper’s argument. Including this would significantly strengthen its contribution.”
Typical: “This analysis is laughably inadequate.”
Constructive: “The analysis could be improved by addressing [specific gap]. Adding [specific method or robustness check] would increase confidence in the results.”
Typical: “The paper’s discussion is a mess.”
Constructive: “Reorganizing the discussion to connect findings to [specific framework] would create a more coherent and impactful narrative.”
Typical: “It’s disappointing that the authors didn’t do a better job with the data.”
Constructive: “Expanding the dataset to include [specific aspect] or addressing [specific limitation] would strengthen the empirical foundation of the paper.”
Typical: “This paper is a waste of time for the journal.”
Constructive: “The paper addresses an important topic, but revising [specific section] and providing stronger evidence for [specific claim] would make it a better fit for the journal.”
""",
    },
]

h_component_input = [
    {
        "role": "user",
        "content": "I will give you a review document. Help me provide constructive feedback of this document using this framework. We will focus on the sixth component: 'H' which stands for Holistic and Balanced Assessment",
    },
    {
        "role": "assistant",
        "content": "Sounds good! In order, to provide constructive feedback, could you provide more details about 'H' or Holistic and Balanced Assessment?",
    },
    {
        "role": "user",
        "content": """Certainly. Below I outline different traits of H followed by typical sentences that are less effective and more constructive versions of the same sentence.
1.	Be Candid About the Contribution: Clearly and honestly evaluate the manuscript’s novelty and significance, focusing on its alignment with the journal’s goals and its contribution to the field.
Typical: “This paper doesn’t offer much new.”
Constructive: “The paper addresses [specific area], but its novelty lies in [specific contribution]. Emphasizing this in the introduction and conclusion would make the contribution clearer.”
Typical: “The contribution is too limited.”
Constructive: “The study contributes to [specific area], but extending the implications to [specific related area] would broaden its relevance and impact.”
Typical: “This is a minor addition to the literature.”
Constructive: “While the study builds on [specific body of work], focusing on how it challenges or extends [specific framework] could highlight its unique contribution.”
Typical: “This is not significant enough for publication.”
Constructive: “The manuscript addresses an important question but would benefit from demonstrating its impact on [specific theory or practice].”
Typical: “This work doesn’t align with the journal’s mission.”
Constructive: “Reframing the findings to emphasize their relevance to [specific journal mission or audience] could align the work more closely with the journal’s goals.”

2.	Acknowledge Both Strengths and Weaknesses: Highlight the paper’s merits alongside areas for improvement, providing a balanced view that motivates the author while guiding revisions.
Typical: “The methodology is flawed.”
Constructive: “The methodology is innovative but has some limitations, such as [specific issue]. Addressing this would strengthen the study while preserving its novel aspects.”
Typical: “The introduction is not strong enough.”
Constructive: “The introduction sets up an interesting question but could be enhanced by providing more context on [specific gap in the literature].”
Typical: “The paper’s analysis is weak.”
Constructive: “The analysis provides useful insights, but additional tests, such as [specific robustness check], would improve its reliability.”
Typical: “The theoretical contribution is underdeveloped.”
Constructive: “Theoretical contributions are promising. Expanding on [specific concept] and linking it to [specific framework] would strengthen this section.”
Typical: “The discussion lacks depth.”
Constructive: “The discussion section is a good starting point but could be deepened by exploring implications for [specific audience or application].”

3.	Remember That Your Feedback Is One Piece of Input: Recognize that your role is to contribute constructive insights rather than making definitive decisions about the manuscript’s fate.
Typical: “This paper should be rejected outright.”
Constructive: “The manuscript has potential but requires major revisions in [specific area]. Addressing these revisions could make it a stronger candidate for publication.”
Typical: “This study doesn’t meet the bar for this journal.”
Constructive: “The study may not meet the current journal’s standards, but revising [specific section] and refocusing on [specific contribution] could make it suitable for a resubmission.”
Typical: “The authors ignored key feedback from reviewers.”
Constructive: “It appears that some key points from prior feedback, such as [specific issue], were not addressed. Clarifying this would help the review team assess progress.”
Typical: “This approach is completely invalid.”
Constructive: “While the current approach has limitations, refining it by addressing [specific issue] could enhance the manuscript’s rigor and relevance.”
Typical: “I disagree with the AE’s perspective.”
Constructive: “Building on the AE’s comments, I suggest focusing on [specific area] to balance the feedback and provide a clearer path for improvement.”

4.	Frame Feedback Encouragingly: Use a positive and professional tone to frame critiques as opportunities for improvement, fostering a constructive dialogue with the authors.
Typical: “This paper is not worth publishing.”
Constructive: “The study has potential, especially in its exploration of [specific area]. Focusing on [specific revision] would help unlock its value.”
Typical: “The authors need to start over.”
Constructive: “The study tackles an important question. Revisiting [specific section] and strengthening [specific aspect] could lead to a significant contribution.”
Typical: “This paper is inadequate.”
Constructive: “The manuscript addresses a relevant topic but would benefit from revising [specific section] and clarifying [specific argument] to reach its full potential.”
Typical: “This study is uninteresting.”
Constructive: “Highlighting the implications of [specific finding] could make the paper more engaging for both researchers and practitioners.”
Typical: “This submission fails to meet expectations.”
Constructive: “The submission requires significant revisions in [specific area], but with these changes, it could contribute meaningfully to [specific field or literature].”
""",
    },
]

y_component_input = [
    {
        "role": "user",
        "content": "I will give you a review document. Help me provide constructive feedback of this document using this framework. We will focus on the last component: 'Y' which stands for Your Review as a Roadmap",
    },
    {
        "role": "assistant",
        "content": "Sounds good! In order, to provide constructive feedback, could you provide more details about 'Y' or Your Review as a Roadmap?",
    },
    {
        "role": "user",
        "content": """Certainly. Below I outline different traits of Y followed by typical sentences that are less effective and more constructive versions of the same sentence.
1.	Use a Logical Structure: Organize feedback into clearly defined sections—such as summary, major issues, and minor suggestions—to make it easier for authors to follow and implement revisions.
Typical: “The manuscript has several issues that need fixing.”
Constructive: “Summary: The manuscript addresses an important topic. Major Concerns: 1) The theoretical framework needs alignment with [specific theory]. 2) The results section lacks clarity.”
Typical: “There are problems in theory, methods, and presentation.”
Constructive: “1. Theory: Clarify the connection between [specific theory] and your hypotheses. 2. Methods: Justify the choice of [specific method]. 3. Presentation: Expand the discussion of results.”
Typical: “Your analysis is unclear.”
Constructive: “In Section 3, clarify the methodology used for [specific analysis]. Breaking the explanation into steps will help the reader understand the process.”
Typical: “The paper is difficult to follow.”
Constructive: “Consider adding a section that outlines the structure of the paper, such as the research question, methodology, results, and implications.”
Typical: “The writing is scattered.”
Constructive: “Reorganizing the paper by grouping similar arguments under clear subheadings would improve its coherence and readability.”

2.	Number Your Suggestions: Present comments as a numbered list to enhance clarity, making it straightforward for authors to address each point systematically.
Typical: “Several areas need improvement, including the literature review and methodology.”
Constructive: “1. Literature Review: Include references to [specific papers]. 2. Methodology: Justify your sample selection. 3. Analysis: Add robustness checks to validate [specific results].”
Typical: “The introduction and discussion need major revisions.”
Constructive: “1. Introduction: Clearly define the research question. 2. Discussion: Elaborate on practical implications for [specific audience].”
Typical: “There are issues with the theoretical framework and data analysis.”
Constructive: “1. Theoretical Framework: Strengthen the connection between [specific concepts]. 2. Data Analysis: Include sensitivity analyses to account for [specific factor].”
Typical: “The paper lacks depth in several areas.”
Constructive: “1. Methods: Add detail on [specific methodology]. 2. Results: Discuss the implications of [specific finding]. 3. Conclusion: Summarize the practical significance of the study.”
Typical: “The conclusions aren’t compelling.”
Constructive: “1. Reframe the conclusion to emphasize [specific insight]. 2. Link the conclusions to the broader implications for [specific field].”

3.	Create Smooth Flow Between Sections: Connect related comments across different sections of the paper to provide a cohesive narrative that helps authors see the bigger picture.
Typical: “Your sections feel disconnected.”
Constructive: “To improve flow, ensure that each section transitions logically. For example, connect the literature review directly to the hypotheses by summarizing key gaps in prior research.”
Typical: “The discussion doesn’t follow logically from the results.”
Constructive: “Consider revising the discussion to begin with key results and gradually build to broader theoretical and practical implications.”
Typical: “The argument jumps between ideas.”
Constructive: “Grouping related ideas in the results and discussion sections would create a smoother narrative, making it easier for readers to follow your argument.”
Typical: “The paper lacks a cohesive story.”
Constructive: “Introduce a unifying theme or question in the introduction and revisit it in the discussion to tie the paper together more effectively.”
Typical: “The conclusion doesn’t wrap up the paper.”
Constructive: “Summarize the key findings and restate their importance to ensure the conclusion ties back to the paper’s overarching goals.”

4.	Optimize Review Length: Keep reviews concise by focusing on critical issues and avoiding exhaustive details on minor points, ensuring the feedback is actionable and efficient.
Typical: “Your paper has too many problems to list.”
Constructive: “This paper requires significant revision. My main suggestions focus on [specific areas], and additional comments address minor points like [specific stylistic issue].”
Typical: “You need to address everything mentioned.”
Constructive: “The major revisions should focus on [specific critical issues], while minor edits, such as rephrasing sentences in Section 4, can be done in a later stage.”
Typical: “The review is too detailed to summarize.”
Constructive: “Key changes needed include: 1. Improving the theoretical framework, 2. Adding robustness checks to the analysis, and 3. Clarifying practical implications in the discussion.”
Typical: “Your work is missing too much to be salvageable.”
Constructive: “Focusing on [specific primary revision] would make the most impact. Additional improvements to [specific area] can be addressed once this is resolved.”
Typical: “The paper requires endless revisions.”
Constructive: “To streamline revisions, prioritize addressing [specific issue] in this round. Further refinements can follow once the core issues are resolved.”
""",
    },
]
