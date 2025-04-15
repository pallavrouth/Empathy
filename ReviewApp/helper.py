import re
import docx2txt
from io import BytesIO
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
from rapidfuzz import fuzz, process


# function to make sure there anre't too many newlines
def strip_consecutive_newlines(text):
    return "\n\n".join(line for line in text.splitlines() if line.strip())


# function to make sure ... -> .
def replace_multiple_dots(text):
    return re.sub(r"\.{2,}", ".", text)


# text cleaner - the app has trouble identifying sentences with formatting
# all space formatting is stripped. And text is reconstructed
def decompose_join(text):
    sentences = sent_tokenize(text)
    cleaned_sentences = [
        re.sub(r"\s+", " ", sent.strip()) for sent in sentences if len(sent.strip()) > 1
    ]
    joined_text = ". ".join(cleaned_sentences)
    cleaned_text = replace_multiple_dots(joined_text)
    return cleaned_text


# function to process the input file with the above function
def process_docx_file(file: BytesIO) -> str:
    text = docx2txt.process(file)
    cleaned_text = decompose_join(text)
    return cleaned_text.strip()


# def match_sentences_with_similarity(dataset, rtext):
#     text_sentences = [sent.strip() for sent in rtext.split(".") if sent.strip()]
#     vectorizer = TfidfVectorizer().fit(text_sentences + dataset["sentences"].tolist())
#     text_vectors = vectorizer.transform(text_sentences)
#     df_vectors = vectorizer.transform(dataset["sentences"].tolist())

#     corrected_sentences = []
#     for _, sentence_vec in enumerate(df_vectors):
#         similarities = cosine_similarity(sentence_vec, text_vectors).flatten()
#         best_match_index = similarities.argmax()
#         corrected_sentences.append(text_sentences[best_match_index])
#     dataset["corrected_sentences"] = corrected_sentences
#     return dataset


# LLM returns partial matches. Function to find which sentence the partial
# matches belong to. Useful for highlighting purposes.
def match_sentences_with_similarity(dataset, rtext):
    rtext = rtext.replace("<<", "").replace(">>", "")
    text_sentences = sent_tokenize(rtext)
    corrected_sentences = []
    for sent in dataset["sentences"].tolist():
        best_sent, _, _ = process.extractOne(
            sent, text_sentences, scorer=fuzz.partial_ratio
        )
        # if score > 99:
        corrected_sentences.append(best_sent)
    dataset["corrected_sentences"] = corrected_sentences
    return dataset


# don't display the whole text rather some portion of it
def add_context(text, sentence):
    match = re.search(re.escape(sentence), text)
    if match:
        start_idx = match.start()
        end_idx = match.end()
        before = text[max(0, start_idx - 100) : start_idx]
        after = text[end_idx : min(len(text), end_idx + 200)]
        context = f"....{before}{text[start_idx:end_idx]}{after}..."
        return context
    else:
        return text


# highlight the sentences that needs improvement
def highlight_sentences(text, sentence, color="rgba(128, 0, 0, 0.2)"):
    updated_text = text
    updated_text = updated_text.replace(
        sentence,
        f"<span style='background-color: {color}; "
        f"border-radius: 3px; display: inline; border-left: 3.5px solid darkred; "
        f"margin: 0; padding: 0;'>{sentence}</span>",
    )
    return updated_text


# highlight the suggested replacement in place of the sentence
def highlight_suggestions(text, sentence, suggestion, color="rgba(0, 128, 0, 0.2)"):
    updated_text = text
    suggestion = suggestion.rstrip(".")
    updated_text = updated_text.replace(
        sentence,
        f"<span style='background-color: {color}; "
        f"border-radius: 3px; display: inline; border-left: 3.5px solid darkgreen; "
        f"margin: 0; padding: 0;'>{suggestion}.</span>",
    )
    return updated_text


# once a change is accepted -- annotate it using "<<>>" because we want to tell LLM to
# process these carefully
def annotate_changes(original_text, decisions):
    for decision in decisions:
        original_text = original_text.replace(
            decision["sentence"], f"""<<{decision["suggestion"]}>>"""
        )
    return original_text


# if accepted then apply changes
def apply_accepted_changes(original_text, decisions):
    for decision in decisions:
        if decision["decision"] == "accept":
            original_text = original_text.replace(
                decision["sentence"], decision["suggestion"]
            )
    return original_text


def dict_to_df(data_dict):
    data_list = []
    for item in data_dict:
        for sentence, suggestion in zip(
            item["sentences_needing_improvement"], item["suggested_improvement"]
        ):
            data_list.append(
                {
                    "trait": item["trait"],
                    "comment": item["comment"],
                    "sentences": sentence,
                    "suggestions": suggestion,
                }
            )
    return pd.DataFrame(data_list)


# def progress_history(decision_history):
#     progress = "Decision history:<br>"
#     for i, decision in enumerate(decision_history):
#         if decision["decision"] == "accept":
#             progress += f"Area {i+1}: ✅<br>"
#         elif decision["decision"] == "reject":
#             progress += f"Area {i+1}: ❌<br>"
#     return progress
