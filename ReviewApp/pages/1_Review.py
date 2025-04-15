import streamlit as st
from io import BytesIO, StringIO
from helper import (
    process_docx_file,
    dict_to_df,
    match_sentences_with_similarity,
    add_context,
    highlight_sentences,
    highlight_suggestions,
    replace_multiple_dots,
    apply_accepted_changes,
    annotate_changes,
)
from response_gen import ResponseGenerator
from app_data import (
    trait_definitions,
    base_input,
    e_component_input,
    m_component_input,
    p_component_input,
    a_component_input,
    t_component_input,
    h_component_input,
    y_component_input,
)

#####################
##### App Info ######
#####################

st.sidebar.title("Get Constructive Feedback")
st.sidebar.markdown(
    """
This application is designed to help you refine your review through constructive feedback. The process begins with uploading your current review text, after which you will be guided through seven stages based on the EMPATHY framework for constructive reviewing. 

At each stage, a language model (LLM) will evaluate your text against specific traits relevant to that stage, offering suggestions for improvement. You can choose to accept or reject these suggestions. Once all suggested improvements have been reviewed, an “Update” button will appear, allowing you to apply the accepted changes to your document seamlessly.
"""
)

with open("secretkey.txt", "r") as file:
    secrets = dict(line.strip().split("=") for line in file if line.strip())

api_key = secrets.get("API_KEY")

###############################
##### Session state vars ######
###############################

if "diagnostics" not in st.session_state:
    st.session_state["diagnostics"] = {}
if "rtext" not in st.session_state:
    st.session_state["rtext"] = ""
if "llm" not in st.session_state:
    st.session_state["llm"] = ResponseGenerator(api_key=api_key)
if "updated_text" not in st.session_state:
    st.session_state["updated_text"] = {}
if "updated_text_clean" not in st.session_state:
    st.session_state["updated_text_clean"] = {}
if "annotated_text" not in st.session_state:
    st.session_state["annotated_text"] = {}
if "decisions" not in st.session_state:
    st.session_state["decisions"] = []

###############################
### Repeated Tab components ###
###############################

run_options = ["Run this stage", "Skip this stage"]


def analyze_stage(
    llm, review_text, component_input, base_input, trait_definitions, component_name
):
    """
    The purpose of this function is to take the text, and use the
    LLM to generate diagnostics (sentences that need to be improved,
    improved sentences, comments)

    Args:
        llm (ResponseGenerator): The language model instance.
        review_text (str): The text to be analyzed.
        component_input (dict): The component input specific to the stage. (each tab is specific to a component)
        base_input (dict): The base input for the LLM (see response_gen)
        ##--##
        Sometimes sentences are assigned to two traits - conflict is resolved using LLM2
        ##--##
        trait_definitions (dict): Trait definitions for conflict resolution.
        component_name (str): The component name (e.g., "e_component").

    Returns:
        DataFrame: Diagnostics data as a DataFrame.
    """
    diagnostics = llm.generate_response(
        review_text=review_text,
        component_input=component_input,
        base_input=base_input,
    )
    diagnostics_df = dict_to_df(data_dict=diagnostics)
    # check if there are duplicates of sentences identified -- these duplicates need to be resolved
    duplicated_sentences = sum(diagnostics_df.duplicated(subset="sentences"))
    # run resolve diagnostics
    if duplicated_sentences > 0:
        resolved_diagnostics = llm.resolve_conflicts(
            gpt_response=diagnostics,
            trait_definitions=trait_definitions,
            component=component_name,
        )
        diagnostics_df = dict_to_df(data_dict=resolved_diagnostics)
    # the LLM does not always return the exact sentence (partial matches returned) -- function that
    # finds out the sentence from the text
    xdf = match_sentences_with_similarity(
        dataset=diagnostics_df,
        rtext=review_text,
    )
    # for safety purposes resolve conflicts again -- naively (keep last)
    ydf = xdf.drop_duplicates(
        subset=["corrected_sentences", "suggestions"], keep="last"
    ).assign(
        # in later stages, some sentences are tagged with "<<>>" -- need to be cleaned
        suggestions_clean=lambda d: d.suggestions.apply(
            lambda x: x.replace("<<", "").replace(">>", "")
        ),
        sent_clean=lambda d: d.corrected_sentences.apply(
            lambda x: x.replace("<<", "").replace(">>", "")
        ),
    )
    return {
        "traits_list": ydf.trait.to_list(),
        "comments_list": ydf.comment.to_list(),
        "suggestions_list": ydf.suggestions_clean.to_list(),
        "sent_list": ydf.sent_clean.to_list(),
    }


# once we get the traits (sub component of each component), comments, suggestions
# and sentences, we need to display them
def diagnostics_decisions(diagnostic_components, text, stage):
    # all of the below are of equal length
    traits = diagnostic_components["traits_list"]
    comments = diagnostic_components["comments_list"]
    suggestions = diagnostic_components["suggestions_list"]
    sentences = diagnostic_components["sent_list"]
    # a counter to check whether all sentences have been reviewed in the sentence list
    # only them show "updated text" option
    counter = 0

    # for each item in the above list we want to show the trait,
    # then show the comment, then show the highlighted sentence,
    # highlight the suggested improvement and then an accept or reject button
    for trait, comment, suggestion, sentence in zip(
        traits, comments, suggestions, sentences
    ):
        counter += 1
        st.markdown(f"**Trait:** {trait}")
        st.markdown(f"**Comment:** {comment}")
        # 2 columns - one for sentence to be changed and the other for suggested improvement
        with st.container(height=250, border=False):
            col1, col2 = st.columns(2)
            focal_text = add_context(text=text, sentence=sentence)
            with col1:
                st.markdown("**Original Text**")
                # show sentence to be improved
                highlighted_text = highlight_sentences(
                    text=focal_text,
                    sentence=sentence,
                )
                st.markdown(highlighted_text, unsafe_allow_html=True)
            with col2:
                st.markdown("**Suggestions**")
                # show highlighted suggestion
                suggested_text = highlight_suggestions(
                    text=focal_text,
                    sentence=sentence,
                    suggestion=suggestion,
                )
                st.markdown(suggested_text, unsafe_allow_html=True)
        # then show the accept and reject button
        with st.container(border=False):
            col3, col4, col5, col6 = st.columns([0.25, 0.25, 0.25, 0.25])
            with col6:
                decision_opts = st.pills(
                    label="lab",
                    label_visibility="hidden",
                    key=f"dec_{stage}_{counter}",
                    options=["Accept", "Reject"],
                    default=None,
                )
                if decision_opts == "Accept":
                    st.session_state["decisions"].append(
                        {
                            "decision": "accept",
                            "sentence": sentence,
                            "suggestion": suggestion,
                        }
                    )
                elif decision_opts == "Reject":
                    st.session_state["decisions"].append(
                        {
                            "decision": "reject",
                            "sentence": sentence,
                            "suggestion": suggestion,
                        }
                    )
            st.markdown("---------------")


##############
### App UI ###
##############

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
    [
        "Upload document",
        "Stage 1",
        "Stage 2",
        "Stage 3",
        "Stage 4",
        "Stage 5",
        "Stage 6",
        "Stage 7",
        "Download document",
    ]
)

# tab1 will upload the file
with tab1:
    uploaded_file = st.file_uploader("Choose a DOCX file", accept_multiple_files=False)

    if uploaded_file:
        file = BytesIO(uploaded_file.read())
        text = process_docx_file(file)
        st.markdown("### Document")
        st.markdown(text)
        st.session_state["rtext"] = text
        st.markdown("--------------")
        st.success("File uploaded successfully! Go to next tab to begin analysis.")

# tab2 - tab8 each component or stage of EMPATHY (for example tab 2 is E component/stage)
with tab2:
    st.markdown(f"**E**.M.P.A.T.H.Y. dimension: **E**nd Goal in Mind")
    st.markdown(
        f"Reviewers should evaluate manuscripts by understanding the journal’s scope and mission, ensuring the research aligns with advancing the field and meeting practical and scholarly expectations while offering constructive feedback on methodology, analysis, and contribution to the journal’s goals."
    )
    # run this stage or skip it
    if st.session_state["rtext"]:
        run_stage1 = st.pills(
            label="lab",
            label_visibility="hidden",
            options=run_options,
            key="stage1_pill",
        )
        # if run this step generate diagnostics
        if run_stage1 == "Run this stage":
            if "stage1" not in st.session_state["diagnostics"]:
                with st.spinner("Analyzing..."):
                    llm = st.session_state["llm"]
                    diagnostics = analyze_stage(
                        llm=llm,
                        review_text=st.session_state["rtext"],
                        component_input=e_component_input,
                        base_input=base_input,
                        trait_definitions=trait_definitions,
                        component_name="e_component",
                    )
                    st.session_state["diagnostics"]["stage1"] = diagnostics
            else:
                pass
        # if skip this stage take the input text and pass on to M stage
        elif run_stage1 == "Skip this stage":
            st.markdown("Please click on stage 2 to continue.")
            st.session_state["updated_text"]["stage1"] = st.session_state["rtext"]
            st.session_state["annotated_text"]["stage1"] = st.session_state["rtext"]

    else:
        st.markdown("No document available. Please upload a document first.")

    if "stage1" in st.session_state["diagnostics"]:
        diagnostics_decisions(
            diagnostic_components=st.session_state["diagnostics"]["stage1"],
            text=st.session_state["rtext"],
            stage="stage1",
        )

        st.session_state["decisions"] = list(
            {
                frozenset(item.items()): item for item in st.session_state["decisions"]
            }.values()
        )
        len_sents = len(st.session_state["diagnostics"]["stage1"]["sent_list"])
        len_decisions = len(st.session_state["decisions"])
        if len_sents == len_decisions:
            show_updated_text = st.button("Show updated text", key="update_stage1")
            if show_updated_text:
                st.markdown(
                    """All suggestions from stage 1 have been reviewed! 
                    Here is the updated review document."""
                )
                st.markdown("---------------")
                st.markdown("### Updated Document")
                updated_text = apply_accepted_changes(
                    st.session_state["rtext"],
                    st.session_state["decisions"],
                )
                ut_clean = replace_multiple_dots(text=updated_text)
                # keep a log of all texts being updated at each stage
                st.session_state["updated_text_clean"]["stage1"] = ut_clean
                st.markdown(st.session_state["updated_text_clean"]["stage1"])
                st.session_state["updated_text"]["stage1"] = ut_clean

                annotated_text = annotate_changes(
                    st.session_state["rtext"],
                    st.session_state["decisions"],
                )
                # separately keep log of annotated text at each stage
                st.session_state["annotated_text"]["stage1"] = annotated_text

                st.markdown("----------")
                st.markdown("Click on next tab to review next stage")
        # before exiting a stage
        st.session_state["decisions"] = []

with tab3:
    st.markdown(f"E.**M**.P.A.T.H.Y. dimension:** Developmental **M**indset")
    st.markdown(
        f"A developmental mindset transforms the reviewer’s role into that of a mentor, emphasizing growth and refinement through constructive feedback that builds on a manuscript’s strengths, identifies actionable improvements, and fosters a culture of academic support and advancement."
    )
    if "stage1" in st.session_state["updated_text"]:
        if st.session_state["rtext"]:
            run_stage2 = st.pills(  # change
                label="lab",
                label_visibility="hidden",
                options=run_options,
                key="stage2_pill",  # change
            )
            if run_stage2 == "Run this stage":  # change
                if "stage2" not in st.session_state["diagnostics"]:  # chnage
                    with st.spinner("Analyzing..."):
                        llm = st.session_state["llm"]
                        diagnostics = analyze_stage(
                            llm=llm,
                            review_text=st.session_state["annotated_text"]["stage1"],
                            component_input=m_component_input,  # change
                            base_input=base_input,
                            trait_definitions=trait_definitions,
                            component_name="m_component",  # change
                        )
                        st.session_state["diagnostics"][
                            "stage2"
                        ] = diagnostics  # change
                else:
                    pass
            elif run_stage2 == "Skip this stage":  # chnage
                st.markdown("Please click on stage 3 to continue.")  # change
                st.session_state["updated_text"]["stage2"] = st.session_state[
                    "updated_text"
                ]["stage1"]
                st.session_state["annotated_text"]["stage2"] = st.session_state[
                    "annotated_text"
                ]["stage1"]

        else:
            st.markdown("No document available. Please upload a document first.")

        if "stage2" in st.session_state["diagnostics"]:  # change
            diagnostics_decisions(
                diagnostic_components=st.session_state["diagnostics"][
                    "stage2"
                ],  # change
                text=st.session_state["updated_text"]["stage1"],
                stage="stage2",  # change
            )

            st.session_state["decisions"] = list(
                {
                    frozenset(item.items()): item
                    for item in st.session_state["decisions"]
                }.values()
            )
            len_sents = len(
                st.session_state["diagnostics"]["stage2"]["sent_list"]
            )  # change
            len_decisions = len(st.session_state["decisions"])
            if len_sents == len_decisions:
                show_updated_text = st.button("Show updated text", "update_stage2")
                if show_updated_text:  # change
                    st.markdown(
                        """All suggestions from stage 2 have been reviewed! 
                        Here is the updated review document."""
                    )
                    st.markdown("---------------")
                    st.markdown("### Updated Document")
                    updated_text = apply_accepted_changes(
                        st.session_state["updated_text"]["stage1"],
                        st.session_state["decisions"],
                    )
                    ut_clean = replace_multiple_dots(text=updated_text)
                    st.session_state["updated_text_clean"]["stage2"] = ut_clean
                    st.markdown(st.session_state["updated_text_clean"]["stage2"])
                    st.session_state["updated_text"]["stage2"] = ut_clean

                    annotated_text = annotate_changes(
                        st.session_state["updated_text"]["stage1"],
                        st.session_state["decisions"],
                    )
                    st.session_state["annotated_text"]["stage2"] = annotated_text

                    st.markdown("----------")
                    st.markdown("Click on next tab to review next stage")
            st.session_state["decisions"] = []
    else:
        st.markdown("Please make a decision on stage 1 before progressing to stage 2.")

with tab4:
    st.markdown(f"E.M.**P**.A.T.H.Y. dimension: **P**eruse Paper Thoroughly")
    st.markdown(
        f"Reviewers should deeply engage with the entirety of a manuscript to understand its core problem, theoretical contributions, and intended impact, ensuring that feedback is empathetic, constructive, and collaborative while rearticulating the paper’s goals to build credibility and provide well-grounded insights."
    )
    if "stage2" in st.session_state["updated_text"]:
        if st.session_state["rtext"]:
            run_stage3 = st.pills(  # change
                label="lab",
                label_visibility="hidden",
                options=run_options,
                key="stage3_pill",  # change
            )
            if run_stage3 == "Run this stage":  # change
                if "stage3" not in st.session_state["diagnostics"]:  # chnage
                    with st.spinner("Analyzing..."):
                        llm = st.session_state["llm"]
                        diagnostics = analyze_stage(
                            llm=llm,
                            review_text=st.session_state["annotated_text"]["stage2"],
                            component_input=p_component_input,  # change
                            base_input=base_input,
                            trait_definitions=trait_definitions,
                            component_name="p_component",  # change
                        )
                        st.session_state["diagnostics"][
                            "stage3"
                        ] = diagnostics  # change
                else:
                    pass
            elif run_stage3 == "Skip this stage":  # chnage
                st.markdown("Please click on stage 4 to continue.")  # change
                st.session_state["updated_text"]["stage3"] = st.session_state[
                    "updated_text"
                ]["stage2"]
                st.session_state["annotated_text"]["stage3"] = st.session_state[
                    "annotated_text"
                ]["stage2"]

        else:
            st.markdown("No document available. Please upload a document first.")

        if "stage3" in st.session_state["diagnostics"]:  # change
            diagnostics_decisions(
                diagnostic_components=st.session_state["diagnostics"][
                    "stage3"
                ],  # change
                text=st.session_state["updated_text"]["stage2"],
                stage="stage3",  # change
            )

            st.session_state["decisions"] = list(
                {
                    frozenset(item.items()): item
                    for item in st.session_state["decisions"]
                }.values()
            )
            len_sents = len(
                st.session_state["diagnostics"]["stage3"]["sent_list"]
            )  # change
            len_decisions = len(st.session_state["decisions"])
            if len_sents == len_decisions:
                show_updated_text = st.button("Show updated text", "update_stage3")
                if show_updated_text:  # change
                    st.markdown(
                        """All suggestions from stage 3 have been reviewed! 
                        Here is the updated review document."""
                    )
                    st.markdown("---------------")
                    st.markdown("### Updated Document")
                    updated_text = apply_accepted_changes(
                        st.session_state["updated_text"]["stage2"],
                        st.session_state["decisions"],
                    )
                    ut_clean = replace_multiple_dots(text=updated_text)
                    st.session_state["updated_text_clean"]["stage3"] = ut_clean
                    st.markdown(st.session_state["updated_text_clean"]["stage3"])
                    st.session_state["updated_text"]["stage3"] = ut_clean

                    annotated_text = annotate_changes(
                        st.session_state["updated_text"]["stage2"],
                        st.session_state["decisions"],
                    )
                    st.session_state["annotated_text"]["stage3"] = annotated_text

                    st.markdown("----------")
                    st.markdown("Click on next tab to review next stage")
            st.session_state["decisions"] = []
    else:
        st.markdown("Please make a decision on stage 2 before progressing to stage 3.")

with tab5:
    st.markdown(f"E.M.P.**A**.T.H.Y. dimension: **A**llocate Critique Resources Wisely")
    st.markdown(
        f"Reviewers, entrusted with guiding manuscripts through their scholarly trajectory, should focus on impactful, constructive feedback by prioritizing critical theoretical, methodological, or empirical issues over minor refinements, thereby ensuring their time is used effectively to advance the manuscript while fostering a balance between rigor and innovation."
    )
    if "stage3" in st.session_state["updated_text"]:
        if st.session_state["rtext"]:
            run_stage4 = st.pills(  # change
                label="lab",
                label_visibility="hidden",
                options=run_options,
                key="stage4_pill",  # change
            )
            if run_stage4 == "Run this stage":  # change
                if "stage4" not in st.session_state["diagnostics"]:  # chnage
                    with st.spinner("Analyzing..."):
                        llm = st.session_state["llm"]
                        diagnostics = analyze_stage(
                            llm=llm,
                            review_text=st.session_state["annotated_text"]["stage3"],
                            component_input=a_component_input,  # change
                            base_input=base_input,
                            trait_definitions=trait_definitions,
                            component_name="a_component",  # change
                        )
                        st.session_state["diagnostics"][
                            "stage4"
                        ] = diagnostics  # change
                else:
                    pass
            elif run_stage4 == "Skip this stage":  # chnage
                st.markdown("Please click on stage 5 to continue.")  # change
                st.session_state["updated_text"]["stage4"] = st.session_state[
                    "updated_text"
                ]["stage3"]
                st.session_state["annotated_text"]["stage4"] = st.session_state[
                    "annotated_text"
                ]["stage3"]

        else:
            st.markdown("No document available. Please upload a document first.")

        if "stage4" in st.session_state["diagnostics"]:  # change
            diagnostics_decisions(
                diagnostic_components=st.session_state["diagnostics"][
                    "stage4"
                ],  # change
                text=st.session_state["updated_text"]["stage3"],
                stage="stage4",  # change
            )

            st.session_state["decisions"] = list(
                {
                    frozenset(item.items()): item
                    for item in st.session_state["decisions"]
                }.values()
            )
            len_sents = len(
                st.session_state["diagnostics"]["stage4"]["sent_list"]
            )  # change
            len_decisions = len(st.session_state["decisions"])
            if len_sents == len_decisions:
                show_updated_text = st.button("Show updated text", "update_stage4")
                if show_updated_text:  # change
                    st.markdown(
                        """All suggestions from stage 4 have been reviewed! 
                        Here is the updated review document."""
                    )
                    st.markdown("---------------")
                    st.markdown("### Updated Document")
                    updated_text = apply_accepted_changes(
                        st.session_state["updated_text"]["stage3"],
                        st.session_state["decisions"],
                    )
                    ut_clean = replace_multiple_dots(text=updated_text)
                    st.session_state["updated_text_clean"]["stage4"] = ut_clean
                    st.markdown(st.session_state["updated_text_clean"]["stage4"])
                    st.session_state["updated_text"]["stage4"] = ut_clean

                    annotated_text = annotate_changes(
                        st.session_state["updated_text"]["stage3"],
                        st.session_state["decisions"],
                    )
                    st.session_state["annotated_text"]["stage4"] = annotated_text

                    st.markdown("----------")
                    st.markdown("Click on next tab to review next stage")
            st.session_state["decisions"] = []
    else:
        st.markdown("Please make a decision on stage 3 before progressing to stage 4.")

with tab6:
    st.markdown(
        f"E.M.P.A.**T**.H.Y. dimension: **T**one: Avoid Toxicity, Be Professional"
    )
    st.markdown(
        f"Professionalism in peer review fosters trust, transparency, and respect by ensuring feedback is constructive, respectful, and focused on the research rather than personal critiques, while adhering to ethical principles such as avoiding conflicts of interest, maintaining confidentiality, and providing timely and honest reviews."
    )
    if "stage4" in st.session_state["updated_text"]:
        if st.session_state["rtext"]:
            run_stage5 = st.pills(  # change
                label="lab",
                label_visibility="hidden",
                options=run_options,
                key="stage5_pill",  # change
            )
            if run_stage5 == "Run this stage":  # change
                if "stage5" not in st.session_state["diagnostics"]:  # chnage
                    with st.spinner("Analyzing..."):
                        llm = st.session_state["llm"]
                        diagnostics = analyze_stage(
                            llm=llm,
                            review_text=st.session_state["annotated_text"]["stage4"],
                            component_input=t_component_input,  # change
                            base_input=base_input,
                            trait_definitions=trait_definitions,
                            component_name="t_component",  # change
                        )
                        st.session_state["diagnostics"][
                            "stage5"
                        ] = diagnostics  # change
                else:
                    pass
            elif run_stage5 == "Skip this stage":  # chnage
                st.markdown("Please click on stage 6 to continue.")  # change
                st.session_state["updated_text"]["stage5"] = st.session_state[
                    "updated_text"
                ]["stage4"]
                st.session_state["annotated_text"]["stage5"] = st.session_state[
                    "annotated_text"
                ]["stage4"]

        else:
            st.markdown("No document available. Please upload a document first.")

        if "stage5" in st.session_state["diagnostics"]:  # change
            diagnostics_decisions(
                diagnostic_components=st.session_state["diagnostics"][
                    "stage5"
                ],  # change
                text=st.session_state["updated_text"]["stage4"],
                stage="stage5",  # change
            )

            st.session_state["decisions"] = list(
                {
                    frozenset(item.items()): item
                    for item in st.session_state["decisions"]
                }.values()
            )
            len_sents = len(
                st.session_state["diagnostics"]["stage5"]["sent_list"]
            )  # change
            len_decisions = len(st.session_state["decisions"])
            if len_sents == len_decisions:
                show_updated_text = st.button("Show updated text", "update_stage5")
                if show_updated_text:  # change
                    st.markdown(
                        """All suggestions from stage 5 have been reviewed! 
                        Here is the updated review document."""
                    )
                    st.markdown("---------------")
                    st.markdown("### Updated Document")
                    updated_text = apply_accepted_changes(
                        st.session_state["updated_text"]["stage4"],
                        st.session_state["decisions"],
                    )
                    ut_clean = replace_multiple_dots(text=updated_text)
                    st.session_state["updated_text_clean"]["stage5"] = ut_clean
                    st.markdown(st.session_state["updated_text_clean"]["stage5"])
                    st.session_state["updated_text"]["stage5"] = ut_clean

                    annotated_text = annotate_changes(
                        st.session_state["updated_text"]["stage4"],
                        st.session_state["decisions"],
                    )
                    st.session_state["annotated_text"]["stage5"] = annotated_text

                    st.markdown("----------")
                    st.markdown("Click on next tab to review next stage")
            st.session_state["decisions"] = []
    else:
        st.markdown("Please make a decision on stage 4 before progressing to stage 5.")

with tab7:
    st.markdown(f"E.M.P.A.T.**H**.Y. dimension: **H**olistic and Balanced Feedback")
    st.markdown(
        f"A balanced and authentic review provides a comprehensive assessment of a manuscript by acknowledging its strengths and limitations, offering actionable suggestions for improvement, and maintaining transparent, unbiased feedback that is constructive, fair, and focused on the manuscript’s overall contribution and potential for development."
    )
    if "stage5" in st.session_state["updated_text"]:
        if st.session_state["rtext"]:
            run_stage6 = st.pills(  # change
                label="lab",
                label_visibility="hidden",
                options=run_options,
                key="stage6_pill",  # change
            )
            if run_stage6 == "Run this stage":  # change
                if "stage6" not in st.session_state["diagnostics"]:  # chnage
                    with st.spinner("Analyzing..."):
                        llm = st.session_state["llm"]
                        diagnostics = analyze_stage(
                            llm=llm,
                            review_text=st.session_state["annotated_text"]["stage5"],
                            component_input=h_component_input,  # change
                            base_input=base_input,
                            trait_definitions=trait_definitions,
                            component_name="h_component",  # change
                        )
                        st.session_state["diagnostics"][
                            "stage6"
                        ] = diagnostics  # change
                else:
                    pass
            elif run_stage6 == "Skip this stage":  # chnage
                st.markdown("Please click on stage 7 to continue.")  # change
                st.session_state["updated_text"]["stage6"] = st.session_state[
                    "updated_text"
                ]["stage5"]
                st.session_state["annotated_text"]["stage6"] = st.session_state[
                    "annotated_text"
                ]["stage5"]

        else:
            st.markdown("No document available. Please upload a document first.")

        if "stage6" in st.session_state["diagnostics"]:  # change
            diagnostics_decisions(
                diagnostic_components=st.session_state["diagnostics"][
                    "stage6"
                ],  # change
                text=st.session_state["updated_text"]["stage5"],
                stage="stage6",  # change
            )

            st.session_state["decisions"] = list(
                {
                    frozenset(item.items()): item
                    for item in st.session_state["decisions"]
                }.values()
            )
            len_sents = len(
                st.session_state["diagnostics"]["stage6"]["sent_list"]
            )  # change
            len_decisions = len(st.session_state["decisions"])
            if len_sents == len_decisions:
                show_updated_text = st.button("Show updated text", "update_stage6")
                if show_updated_text:  # change
                    st.markdown(
                        """All suggestions from stage 6 have been reviewed! 
                        Here is the updated review document."""
                    )
                    st.markdown("---------------")
                    st.markdown("### Updated Document")
                    updated_text = apply_accepted_changes(
                        st.session_state["updated_text"]["stage5"],
                        st.session_state["decisions"],
                    )
                    ut_clean = replace_multiple_dots(text=updated_text)
                    st.session_state["updated_text_clean"]["stage6"] = ut_clean
                    st.markdown(st.session_state["updated_text_clean"]["stage6"])
                    st.session_state["updated_text"]["stage6"] = ut_clean

                    annotated_text = annotate_changes(
                        st.session_state["updated_text"]["stage5"],
                        st.session_state["decisions"],
                    )
                    st.session_state["annotated_text"]["stage6"] = annotated_text

                    st.markdown("----------")
                    st.markdown("Click on next tab to review next stage")
            st.session_state["decisions"] = []
    else:
        st.markdown("Please make a decision on stage 5 before progressing to stage 6.")

with tab8:
    st.markdown(f"E.M.P.A.T.H.**Y**. dimension: **Y**our Review as Roadmap")
    st.markdown(
        f"Impactful reviews guide authors by offering precise, practical, and inspiring feedback that identifies opportunities for improvement, organizes comments logically by themes or sections, and provides a clear roadmap of actionable solutions to foster constructive and productive revisions."
    )
    if "stage6" in st.session_state["updated_text"]:
        if st.session_state["rtext"]:
            run_stage7 = st.pills(  # change
                label="lab",
                label_visibility="hidden",
                options=run_options,
                key="stage7_pill",  # change
            )
            if run_stage7 == "Run this stage":  # change
                if "stage7" not in st.session_state["diagnostics"]:  # chnage
                    with st.spinner("Analyzing..."):
                        llm = st.session_state["llm"]
                        diagnostics = analyze_stage(
                            llm=llm,
                            review_text=st.session_state["annotated_text"]["stage6"],
                            component_input=y_component_input,  # change
                            base_input=base_input,
                            trait_definitions=trait_definitions,
                            component_name="y_component",  # change
                        )
                        st.session_state["diagnostics"][
                            "stage7"
                        ] = diagnostics  # change
                else:
                    pass
            elif run_stage7 == "Skip this stage":  # chnage
                st.markdown(
                    "Please click on next tab to download the updated review."
                )  # change
                st.session_state["updated_text"]["stage7"] = st.session_state[
                    "updated_text"
                ]["stage6"]
                st.session_state["annotated_text"]["stage7"] = st.session_state[
                    "annotated_text"
                ]["stage6"]

        else:
            st.markdown("No document available. Please upload a document first.")

        if "stage7" in st.session_state["diagnostics"]:  # change
            diagnostics_decisions(
                diagnostic_components=st.session_state["diagnostics"][
                    "stage7"
                ],  # change
                text=st.session_state["updated_text"]["stage6"],
                stage="stage7",  # change
            )

            st.session_state["decisions"] = list(
                {
                    frozenset(item.items()): item
                    for item in st.session_state["decisions"]
                }.values()
            )
            len_sents = len(
                st.session_state["diagnostics"]["stage7"]["sent_list"]
            )  # change
            len_decisions = len(st.session_state["decisions"])
            if len_sents == len_decisions:
                show_updated_text = st.button("Show updated text", "update_stage7")
                if show_updated_text:  # change
                    st.markdown(
                        """All suggestions from stage 7 have been reviewed! 
                        Here is the updated review document."""
                    )
                    st.markdown("---------------")
                    st.markdown("### Updated Document")
                    updated_text = apply_accepted_changes(
                        st.session_state["updated_text"]["stage6"],
                        st.session_state["decisions"],
                    )
                    ut_clean = replace_multiple_dots(text=updated_text)
                    st.session_state["updated_text_clean"]["stage7"] = ut_clean
                    st.markdown(st.session_state["updated_text_clean"]["stage7"])
                    st.session_state["updated_text"]["stage7"] = ut_clean

                    annotated_text = annotate_changes(
                        st.session_state["updated_text"]["stage6"],
                        st.session_state["decisions"],
                    )
                    st.session_state["annotated_text"]["stage7"] = annotated_text

                    st.markdown("----------")
                    st.markdown("Click on next tab to review next stage")
            st.session_state["decisions"] = []
    else:
        st.markdown("Please make a decision on stage 6 before progressing to stage 7.")

# download updated text
with tab9:
    st.markdown("**Download Updated Document**")
    if "stage7" in st.session_state["updated_text"]:
        download_file = StringIO(st.session_state["updated_text"]["stage7"])
        st.download_button(
            label="Download Document",
            data=download_file.getvalue(),
            file_name="updated_document.txt",
            mime="text/plain",
        )
