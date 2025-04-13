# Empathy

Use Gen AI to provide constructive feedback of reviews of articles submitted to peer review journals. 
Constructive feedback based on EMPATHY framework created by Srihari Sridhar - https://journals.sagepub.com/doi/full/10.1177/00222429241312127

## Flow (Given a review document how should gen AI proceed)

## Flow (Given a review document how should LLM proceed)

- **Stage 0:** Identify sentences that already align with each component of the EMPATHY framework  
  - Input: Review document  
  - Output: List of sentences for each component of EMPATHY that are already constructive

- **Stage 1:** Identify sentences that needs improvement under each component of the empathy framework  
  - Input: Review document  
  - Output: List of sentences for each component of EMPATHY that potentially needs improvement

- **Stage 2:** Compute score  
  - Input: Outputs from stage 0 + 1  
  - Output: constructive score  
    Constructive score (CS%) = (# stage 0 / (# stage 0 + # stage 1)) * 100  
    Above score for each component: E,…,Y (CS_E%,….., CS_Y%)  
    Aggregate empathy score = (CS_E% + … + CS_Y%) / 7 {alternatively a weighted score here}  
    Convert to a 10 point scale = Aggregate empathy score / 10  

**Interpret score:**  
- 9–10 Highly Constructive – The review is well-structured, follows the EMPATHY framework effectively, and requires minimal improvement.  
- 7–8 Mostly Constructive – The review is strong but has areas that could be improved for better clarity, tone, or structure.  
- 5–6 Moderately Constructive – Some aspects align well with EMPATHY, but there are several areas needing refinement.  
- 3–4 Somewhat Constructive – The review lacks balance, depth, or professionalism in multiple areas. Needs significant improvement.  
- 1–2 Not Very Constructive – The review has little structure, lacks clarity, and does not align well with EMPATHY. Major revisions are required.  
- 0 Completely Unconstructive – The review does not follow constructive feedback principles at all. It may be vague, harsh, or unhelpful.

- **Stage 3:** Assign the sentences that need improvement under each component to each trait of the EMPATHY framework  
  - Divided into 2 sub prompts: one for (E,M,P) and the other for (A,T,H,Y)  
  - Input: Output from stage 1  
  - Output: Each sentence that needs improvement classified under each subcomponent of EMPATHY

- **Stage 4:** Generate suggestions for improvement for each sentence classified into each trait of the empathy framework  
  - Divided into 2 sub prompts: one for (E,M,P) and the other for (A,T,H,Y)  
  - Input: Output from stage 3  
  - Output: Constructive versions of sentences identified for improvement under each subcomponent of EMPATHY

