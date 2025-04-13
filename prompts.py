import json
from openai import OpenAI

with open("credentials.json", "r") as f:
    credentials = json.load(f)

openai_client = OpenAI(api_key=credentials["openai_api_key"])

##


def gen_stage0_template(review_text):
    out = [
        {
            "role": "system",
            "content": "You are an expert at providing constructive feedback.",
        },
        {
            "role": "user",
            "content": f"""
    The EMPATHY framework is a structured approach to crafting constructive peer reviews. It ensures that feedback is actionable, balanced, and professional while fostering growth and collaboration.

    You are tasked with analyzing a peer review to identify sentences that already align well with the EMPATHY framework. Identify constructive phrases that demonstrate strong adherence to EMPATHY principles.

    For each component, return only the sentences from the review that meet the criteria for constructive feedback.

    ### Criteria for Constructive Sentences:
    	1.	E (End Goal in Mind) - Sentences that align feedback with the journal's mission, expectations for rigor, and contribution. Feedback should encourage originality over replication and provide clear, actionable guidance tailored to the journal's audience.
        2.	M (Developmental Mindset) - Sentences that balance critique with constructive suggestions, focus on improvement rather than flaw-finding, and encourage learning and growth without demanding perfection.
        3.	P (Peruse the Paper Thoroughly) - Sentences that reflect deep engagement with the manuscript, connect different sections meaningfully, and provide a thorough, well-rounded evaluation rather than selective critique.
        4.	A (Allocate Critique Resources Wisely) - Sentences that prioritize major concerns over minor issues, offer efficient and actionable revision guidance, and balance depth with practicality to help the author focus effectively.
        5.	T (Tone: Avoid Toxicity, Be Professional) - Sentences that maintain a respectful, professional, and supportive tone, critique the work rather than the author, and avoid sarcasm, harshness, or unnecessary negativity.
        6.	H (Holistic and Balanced Feedback) - Sentences that acknowledge both strengths and weaknesses, assess the manuscript fairly rather than fixating on flaws, and weigh contributions against limitations constructively.
        7.	Y (Your Review as a Roadmap) - Sentences that provide structured, logically organized feedback with clear, actionable next steps, making it easy for the author to understand and implement revisions.

    ### Task:  
    Review the provided text and return only the sentences that demonstrate strong alignment with each EMPATHY component using the guidelines above.

    Review Text:  
    {review_text}

    Output:  
    - E: [List of constructive sentences]  
    - M: [List of constructive sentences]  
    - P: [List of constructive sentences]  
    - A: [List of constructive sentences]  
    - T: [List of constructive sentences]  
    - H: [List of constructive sentences]  
    - Y: [List of constructive sentences]  
    """,
        },
    ]
    return out


def gen_stage1_template(review_text):
    out = [
        {
            "role": "system",
            "content": "You are an expert at providing constructive feedback.",
        },
        {
            "role": "user",
            "content": f"""The EMPATHY framework is a structured approach to crafting constructive peer reviews. It focuses on offering actionable, balanced, and professional feedback to improve manuscripts while fostering growth and collaboration.

    You are tasked with identifying phrases in a peer review that align poorly with the EMPATHY framework. For each component, highlight phrases that exhibit the following opportunities for improvement:

    	1.	E (End Goal in Mind) - Identify sentences that fail to align feedback with the journal's mission, expectations for rigor, and emphasis on originality over replication. Look for instances where the review does not tailor feedback to the journal's standards, makes vague or unhelpful critiques, or does not clarify how the manuscript fits the journal's objectives.
        2.	M (Developmental Mindset) - Identify sentences that focus on criticism without offering constructive suggestions, fail to acknowledge the author's efforts, or reflect an overly perfectionistic, dismissive, or rigid tone. Look for areas where the review does not support the paper's development but instead fixates on flaws without guiding improvement.
        3.	P (Peruse the Paper Thoroughly) - Highlight sentences that indicate incomplete engagement with the manuscript, suggest the reviewer may not have read or understood the paper in its entirety, or overlook critical connections between sections. Look for instances where feedback is superficial, misinterprets the paper's core contribution, or critiques without considering the author's intended framework.
        4.	A (Allocate Critique Resources Wisely) - Pinpoint sentences that overemphasize minor issues while neglecting major concerns, fail to prioritize key areas for revision, or impose unnecessary burdens on the author. Identify cases where the reviewer demands unrealistic changes, provides vague critiques without evidence, or disregards the feasibility of revisions within the study's scope.
        5.	T (Tone: Avoid Toxicity, Be Professional) - Highlight sentences that are overly harsh, sarcastic, or unprofessional, and suggest where feedback could be reframed to focus on the research rather than making personal judgments about the authors. Look for instances where the tone discourages rather than supports the author's improvement.
        6.	H (Holistic and Balanced Feedback) - Identify sentences that focus solely on weaknesses without acknowledging the manuscript's strengths, present an unfairly negative assessment, or fail to offer a fair evaluation of the paper's contributions. Look for reviews that do not recognize the manuscript's potential or neglect to provide balanced, constructive guidance.
        7.	Y (Your Review as a Roadmap) - Highlight sentences where feedback lacks clear organization, actionable steps, or logical structure, making it difficult for authors to follow and implement suggestions. Look for reviews that present feedback in an unstructured, overwhelming, or incoherent manner rather than providing a clear path for revision.

    Task:
    Review the provided text and highlight sentences that align poorly with any of the components above. Return only the problematic phrases grouped by their respective components.

    Review Text:
    {review_text}

    Output:
    - E: [Highlighted sentences]
    - M: [Highlighted sentences]
    - P: [Highlighted sentences]
    - A: [Highlighted sentences]
    - T: [Highlighted sentences]
    - H: [Highlighted sentences]
    - Y: [Highlighted sentences]""",
        },
    ]
    return out


## Stage 2

cs_counts = {}
nis_counts = {}

# Calculate Constructiveness Score (CS%) for each component
constructiveness_scores = {}
for component in cs_counts.keys():
    total = cs_counts[component] + nis_counts[component]
    constructiveness_scores[component] = (
        (cs_counts[component] / total) * 100 if total > 0 else 0
    )

# Compute overall EMPATHY Score (average of all component scores)
empathy_score = sum(constructiveness_scores.values()) / len(constructiveness_scores)

# Convert to 0-10 scale
final_constructiveness_score = empathy_score / 10

## Stage 3


def gen_stage3a_template(text_areas):
    out = [
        {
            "role": "system",
            "content": "You are an expert at providing constructive feedback.",
        },
        {
            "role": "user",
            "content": f"""
    You are analyzing a peer review using the EMPATHY framework. I have identified areas in the text where improvements may be needed under the E, M, and P components. Your task is to classify these highlighted areas under the specific traits of each component.

    Below are the component-specific traits that guide your classification:

    1. E (End Goal in Mind)  
    - Appreciate the journal's mission - Sentences that would dismiss the relevance of the paper to the journal without offering any guidance on how it might be aligned with the journal's mission. For example, "The paper is interesting but doesn't fit JM."
    - Understand the review audience - Sentences that would provide vague or unhelpful feedback that does not consider the needs of the authors, editors, or other reviewers, making it unclear how the manuscript should be improved. For example, "This revision doesn't meet the bar."
    - Tailor the review to journal expectations - Sentences that would offer broad, generic critique without specifying how the paper can better align with the journal's standards. For example, "The analysis is okay, but more details are needed throughout."
    - Do not overindex on past papers - Sentences that would limit the author's creativity by insisting that they follow a previous approach rather than encouraging fresh contributions. For example, "This paper should follow the same approach as the one by [Author]."

    2. M (Developmental Mindset)  
    - Put yourself in the shoes of the author - Sentences that would dismiss the author's efforts without offering constructive guidance on how to improve clarity or argumentation. For example, "The argument is unclear."
    - Be comfortable with imperfection - Sentences that would demand perfection without acknowledging the practical constraints of the research process. For example, "The literature review is lacking."
    - Be specific and creative - Sentences that would provide vague criticism without suggesting concrete ways to refine the manuscript. For example, "The discussion is weak."
    - Work toward joint success - Sentences that would rigidly dismiss the author's approach rather than exploring potential improvements that align with their existing framework. For example, "This approach doesn't work."

    3. P (Peruse Thoroughly)  
    - Rearticulate the core contribution - Sentences that would critique the paper's positioning without demonstrating a clear understanding of its intended contribution. For example, "The paper is positioned like a marketing strategy paper, but it's not entirely clear."
    - Read before critiquing - Sentences that would offer surface-level feedback without engaging deeply with the manuscript's methodology or arguments. For example, "The methods section could use some work."
    - Engage in the world of the paper - Sentences that would dismiss the manuscript's theoretical foundation without providing thoughtful, context-driven insights. For example, "The theoretical arguments are not well-supported."
    - Cover the entire paper - Sentences that would focus only on select parts of the manuscript while neglecting to provide a holistic review. For example, "The discussion is too brief and vague."

    ### Task
    For each highlighted sentence under a component, classify it under one of the traits for that component. Return the output as follows:

    Input:
    {text_areas}

    Output:
    Component
    Trait: Sentence
    """,
        },
    ]
    return out


def gen_stage3b_template(text_areas):
    out = [
        {
            "role": "system",
            "content": "You are an expert at providing constructive feedback.",
        },
        {
            "role": "user",
            "content": f"""
    You are analyzing a peer review using the EMPATHY framework. I have identified areas in the text where improvements may be needed under the A, T, H, and Y components. Your task is to classify these highlighted areas under the specific traits of each component.

    Below are the component-specific traits that guide your classification:

    1. A (Allocate Critique Resources Wisely)  
    - Prioritize major and minor points - Sentences that would overwhelm the author with broad, unsorted criticism without distinguishing between critical and minor issues. For example, "Everything needs to be fixed."
    - Respect the author's paradigm - Sentences that would dismiss the author's chosen theoretical or methodological approach instead of suggesting refinements within their framework. For example, "The methodology is not suited to test this question."
    - Articulate flaws precisely and evidentially - Sentences that would make broad claims about issues in the manuscript without providing clear reasoning or supporting evidence. For example, "The theoretical foundation is fundamentally flawed."
    - Provide some stretch goals - Sentences that would reject the current approach without encouraging exploration of alternative perspectives. For example, "A different approach might work better."

    2. T (Tone: Avoid Toxicity, Be Professional)  
    - Direct feedback to the research, not the author - Sentences that would attack the author's competence instead of focusing on the paper's arguments and methodology. For example, "The author clearly doesn't understand the topic."
    - Be solution-oriented - Sentences that would highlight problems without offering constructive suggestions for improvement. For example, "The literature review is incomplete."
    - Declare conflicts of interest - Sentences that would acknowledge familiarity with the authors but fail to properly disclose potential bias. For example, "I know the authors and have read their previous work, which informs my critique here."
    - Avoid hatred and sarcasm - Sentences that would use dismissive or condescending language, making the feedback unnecessarily harsh. For example, "I can't believe the authors missed this—it's basically obvious."

    3. H (Holistic and Balanced Feedback)  
    - Be candid about the overall contribution - Sentences that would dismiss the paper's value without clearly articulating its contributions or potential improvements. For example, "The contribution seems limited."
    - Acknowledge both strengths and weaknesses - Sentences that would focus only on flaws without recognizing any positive aspects of the manuscript. For example, "The methodology is tragically flawed."
    - Remember that your feedback is one piece of input - Sentences that would make an absolute judgment on the manuscript rather than providing input for the editor's decision-making process. For example, "I would reject the paper."
    - Frame feedback encouragingly - Sentences that would be overly discouraging and fail to motivate the author to improve the manuscript. For example, "This paper is not worth publishing"

    4. Y (Your Review as a Roadmap)  
    - Use a logical structure - Sentences that would present feedback in a disorganized manner, making it difficult for the author to follow and implement. For example, "The manuscript has some issues in the methodology, theory, and presentation. These should be addressed in the revision."
    - Number your suggestions - Sentences that would list multiple critiques in a dense, unstructured way, making it harder for the author to track necessary changes. For example, "There are some issues you need to address in methods, data, and conclusions."
    - Create smooth flow between sections - Sentences that would provide fragmented feedback without connecting related points to help the author improve coherence. For example, "You need more literature, and the results need refining."
    - Optimize review length - Sentences that would overwhelm the author with excessive feedback or, conversely, provide vague and unhelpful brevity. For example, "The manuscript needs improvements in language and methodology."

    ### Task
    For each highlighted sentence under a component, classify it under one of the traits for that component. Return the output as follows:

    Input:
    {text_areas}

    Output
    Component
    Trait: Sentence
    """,
        },
    ]
    return out


### Stage 4


def gen_stage4a_template(needs_improvement):
    out = [
        {
            "role": "system",
            "content": "You are an expert at providing constructive feedback.",
        },
        {
            "role": "user",
            "content": f"""You are tasked with refining a peer review based on the EMPATHY framework. The previous step has identified phrases that align poorly with specific traits under the E, M and P components of the EMPATHY framework. Your job is to generate improvement suggestions for each identified phrase by applying the guidelies below. 

        1. E (End Goal in Mind):
            - Appreciate the Journal's Mission - Improve the sentence by explicitly connecting the manuscript to the journal's mission and scope. Instead of dismissing its fit, suggest ways to better align the research with the journal's objectives. For example, rather than saying, "The paper is interesting but doesn't fit JM," guide the author on how to highlight its relevance to the journal's readership and mission.
            - Understand the Review Audience - Improve the sentence by considering the needs of all stakeholders, including authors, editors, and other reviewers. Instead of vague or dismissive feedback like, "This revision doesn't meet the bar," clarify how the revision aligns with the associate editor's comments or previous reviews and suggest specific ways to refine the response.
            - Tailor the Review to Journal Expectations - Improve the sentence by aligning the critique with the journal's standards for rigor, contribution, and methodology. Instead of broadly stating, "The analysis is okay, but more details are needed throughout," provide journal-specific guidance, such as refining statistical analyses or improving theoretical positioning based on the journal's typical structure.
            - Do Not Overindex on Past Papers - Improve the sentence by encouraging originality rather than rigidly comparing the manuscript to past work. Instead of saying, "This paper should follow the same approach as the one by [Author]," acknowledge the paper's unique contribution and suggest ways to strengthen its novelty while situating it within the broader literature.

        2. M (Developmental Mindset):
            -	Put Yourself in the Shoes of the Author - Improve the sentence by framing feedback in a way that helps the author refine their argument rather than simply pointing out flaws. Instead of saying, "The argument is unclear," suggest a specific way to enhance clarity, such as, "Your argument could be clearer by explicitly stating [specific point]. Developing this idea further will help ensure your contribution is well understood."
            - 	Be Comfortable with Imperfection - Improve the sentence by focusing on feasible improvements rather than expecting a perfect paper. Instead of saying, "The literature review is lacking," acknowledge the existing effort and provide actionable ways to strengthen it, such as, "The literature review introduces key concepts but would benefit from engaging with recent studies on [specific topic] to further ground the argument."
            - 	Be Specific and Creative - Improve the sentence by avoiding vague criticism and instead offering concrete suggestions for improvement. Instead of saying, "The discussion is weak," provide a targeted recommendation like, "The discussion would be stronger by adding practical implications for [specific field]. For example, consider discussing how your findings influence [specific industry or practice]."
            - 	Work Toward Joint Success - Improve the sentence by adopting a collaborative mindset that recognizes the author's perspective. Instead of stating, "This approach doesn't work," offer a constructive alternative, such as, "While this approach has limitations, incorporating [alternative method] could help address some of these concerns and strengthen the overall contribution."

        3. P (Peruse the Paper Thoroughly)
            -	Rearticulate the Core Contribution - Improve the sentence by first summarizing the manuscript's main contribution before offering critique. Instead of saying, "The paper is positioned like a marketing strategy paper, but it's not entirely clear," clarify your understanding and guide the author, such as, "This paper aims to contribute to marketing strategy by introducing [specific theoretical contribution]. To make this clearer, I recommend elaborating on its significance in relation to [specific existing literature]."
            -	Read Before Critiquing - Improve the sentence by ensuring feedback is based on a thorough understanding of the manuscript rather than superficial critique. Instead of saying, "The methods section could use some work," provide a specific area of concern and suggest improvement, such as, "The methods section presents a novel approach, but additional detail on sample selection and variable justification would enhance clarity."
            -	Engage in the World of the Paper - Improve the sentence by demonstrating an understanding of the paper's theoretical and empirical context before offering critique. Instead of stating, "The theoretical arguments are not well-supported," acknowledge the core idea and provide targeted recommendations, such as, "The theoretical argument that [specific claim] is promising, but additional support from [specific citation or dataset] would help strengthen it."
            -	Cover the Entire Paper - Improve the sentence by ensuring feedback addresses all sections of the manuscript rather than focusing on only a few areas. Instead of saying, "The discussion is too brief and vague," suggest how to expand it meaningfully, such as, "The discussion introduces key points but would benefit from deeper engagement with the practical implications of H3. Additionally, linking these implications more closely to the introduction would improve the manuscript's cohesiveness."

    ### Task  
    For each highlighted phrase, provide an improved version that aligns with best practices using the above guidelines.  

    Input:  
    {needs_improvement} 

    Output:
    Component
    Trait: Sentence
    Trait: Suggested improvement  
    """,
        },
    ]

    return out


def gen_stage4b_template(needs_improvement):
    out = [
        {
            "role": "system",
            "content": "You are an expert at providing constructive feedback.",
        },
        {
            "role": "user",
            "content": f"""You are tasked with refining a peer review based on the EMPATHY framework. The previous step has identified phrases that align poorly with specific traits under the A, T, H and Y components of the EMPATHY framework. Your job is to generate improvement suggestions for each identified phrase by applying the guidelies below. 

        1. A (Allocate Critique Resources Wisely)
            -	Prioritize Major and Minor Points - Improve the sentence by distinguishing between critical and minor issues to help the author focus on the most impactful revisions. Instead of saying, "Everything needs to be fixed," provide a clear hierarchy of concerns, such as, "The key areas for improvement are [specific sections]. Addressing these will significantly enhance the manuscript, while other minor adjustments, such as [specific suggestion], can be made as time allows."
            -	Respect the Author's Paradigm - Improve the sentence by suggesting enhancements within the author's existing theoretical or methodological framework rather than demanding a complete overhaul. Instead of saying, "The methodology is not suited to test this question," offer an alternative approach that aligns with the current design, such as, "The methodology could be strengthened by incorporating additional robustness checks to confirm the validity of the findings."
            -	Articulate Flaws Precisely and Evidentially - Improve the sentence by providing clear explanations and evidence for any identified issues rather than making broad, unsupported critiques. Instead of stating, "The theoretical foundation is fundamentally flawed," clarify the concern and suggest a resolution, such as, "The theoretical foundation relies on [specific assumption], which may not hold in this context because [reason and evidence]. Incorporating [alternative theory or empirical support] would strengthen the argument."
            -	Provide Some Stretch Goals - Improve the sentence by offering aspirational yet feasible suggestions to enhance the manuscript's contribution without imposing unrealistic demands. Instead of saying, "A different approach might work better," propose a productive alternative, such as, "In addition to your current approach, consider incorporating insights from [specific theory] to provide a complementary perspective that enriches your findings."

        2. T (Tone: Avoid Toxicity, Be Professional)
            -	Direct Feedback to the Research, Not the Author - Improve the sentence by focusing on the manuscript's content rather than making personal judgments about the author's ability. Instead of saying, "The author clearly doesn't understand the topic," reframe the critique to be constructive, such as, "The argument in Section 3 would benefit from a clearer connection to [specific theory], as the linkage is currently underdeveloped. Strengthening this connection would enhance the contribution."
            -	Be Solution-Oriented - Improve the sentence by providing actionable suggestions instead of simply pointing out issues. Instead of stating, "The literature review is incomplete," offer a clear direction, such as, "To strengthen the literature review, I recommend incorporating recent studies on [specific topic]. This addition would better position the manuscript within the current research landscape."
            -	Declare Conflicts of Interest - Improve the sentence by ensuring transparency about any potential biases while maintaining professional integrity. Instead of saying, "I know the authors and have read their previous work, which informs my critique here," properly disclose potential conflicts in a neutral and professional manner, such as, "Private Comments to the Editor: I am familiar with the authors' prior work. Please let me know if you would like me to continue reviewing."
            -	Avoid Hatred and Sarcasm - Improve the sentence by maintaining a respectful tone and removing dismissive or condescending language. Instead of saying, "I can't believe the authors missed this—it's basically obvious," use a more constructive approach, such as, "Consider addressing [specific point], as it is a critical aspect that could significantly strengthen your argument."
                
        3. H (Holistic and Balanced Assessment)
            -	Be Candid About the Overall Contribution - Improve the sentence by clearly articulating both the manuscript's contributions and areas for improvement rather than vaguely dismissing its value. Instead of saying, "The contribution seems limited," provide a balanced critique such as, "The paper contributes to [specific area] by introducing [specific idea]. To enhance its impact, I recommend further elaborating on [key aspect]."
            -	Acknowledge Both Strengths and Weaknesses - Improve the sentence by ensuring that feedback highlights positive aspects along with areas that need refinement. Instead of stating, "The methodology is tragically flawed," provide a more balanced evaluation like, "The methodology provides a solid foundation, but there are areas, such as [specific aspect], that require refinement. Overall, the paper shows promise with some revisions."
            -	Remember That Your Feedback Is One Piece of Input - Improve the sentence by acknowledging that the reviewer's perspective is part of a broader evaluation process rather than making an absolute judgment. Instead of saying, "I would reject the paper," reframe it to, "While there are weaknesses in [specific areas], the paper has potential if revisions address [key issues]. These improvements could significantly enhance its contribution to [specific field]."
            -	Frame Feedback Encouragingly - Improve the sentence by ensuring critiques are phrased in a way that motivates the author to improve the work rather than discouraging them. Instead of saying, "I doubt this dog can hunt," offer a constructive perspective such as, "Although there are significant challenges, addressing them could result in a meaningful contribution to [specific area]. I encourage you to focus on refining [specific section] to strengthen the manuscript further."
                
        4. Y (Your Review as a Roadmap)
            -	Use a Logical Structure - Improve the sentence by organizing feedback in a clear, structured manner that guides the author through revisions. Instead of saying, "The manuscript has some issues in the methodology, theory, and presentation. These should be addressed in the revision," provide a structured roadmap like, "Summary: The manuscript addresses an important topic. Major concerns: 1) Methodology—clarify sample size justification, 2) Theory—strengthen the connection to [specific theory], 3) Presentation—restructure the discussion for clarity."
            -	Number Your Suggestions - Improve the sentence by breaking down feedback into numbered points to make it easier to follow. Instead of saying, "There are some issues you need to address in methods, data, and conclusions," reformat as, "1. Methods: Clarify the criteria for selecting participants. 2. Data: Recheck calculations involving outliers. 3. Conclusions: Align them more clearly with the research questions."
            -	Create Smooth Flow Between Sections - Improve the sentence by ensuring feedback transitions logically between different aspects of the manuscript. Instead of saying, "You need more literature, and the results need refining," provide a smoother transition like, "Literature: Start by adding sources to contextualize your framework. Results: Then use these sources to interpret your findings more thoroughly."
            -	Optimize Review Length - Improve the sentence by ensuring feedback is thorough but concise, avoiding excessive detail on minor points. Instead of saying, "The manuscript needs improvements in language and methodology," prioritize major concerns first, such as, "I recommend focusing on clarifying the theoretical framework in Section 3. Once this is strengthened, minor edits in language and methodology can follow."


    ### Task  
    For each highlighted phrase, provide an improved version that aligns with best practices using the above guidelines.  

    Input:  
    {needs_improvement} 

    Output:
    Component
    Trait: Sentence
    Trait: Suggested improvement  
    """,
        },
    ]

    return out
