import gradio as gr
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def process_text(text):                      #[FUNCTION RUNNS WHEN USER HITS analyze BUTTON]
    if not text.strip():
        return (
            "Please enter some text.",       #[IF EMPTY RETURNS THIS]
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            None
        )

    doc = nlp(text)

    # Calculate stats
    tokens = [token.text for token in doc]
    stopwords = [token.text for token in doc if token.is_stop]
    punctuation = [token.text for token in doc if token.is_punct]
    unique_words = set(token.text.lower() for token in doc if not token.is_punct and not token.is_space)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    cleaned_tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    cleaned_text = " ".join(cleaned_tokens)


    # Statistics
    stats = f"""
### 📊 Quick Statistics
- **Total Tokens**: {len(tokens)}
- **Stopwords**: {len(stopwords)}
- **Punctuation**: {len(punctuation)}
- **Unique Words**: {len(unique_words)}
- **Named Entities**: {len(entities)}
- **Clean Tokens**: {len(cleaned_tokens)}
"""

    # Store results
    results = {
        "Tokens (with POS tags)": create_tokens_table(doc),
        "Stopwords Removed": create_stopwords_result(stopwords),
        "Lemmatized Tokens": create_lemma_table(doc),
        "Named Entities": create_entities_result(entities),
        "Cleaned Text (no stopwords + lemmas)": cleaned_text
    }

    return (
        stats,
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(visible=True),
        gr.update(value="Tokens (with POS tags)"),
        results
    )


def create_tokens_table(doc):
    result = "### Tokens + POS Tags\n\n"
    result += "| Token | POS | Tag |\n|-------|-----|-----|\n"
    for token in doc:
        if not token.is_space:
            result += f"| {token.text} | {token.pos_} | {token.tag_} |\n"
    return result


def create_stopwords_result(stopwords):
    if stopwords:
        return "### Stopwords Found\n\n" + ", ".join([f"`{w}`" for w in stopwords]) + f"\n\n**Total**: {len(stopwords)}"
    return "No stopwords found."


def create_lemma_table(doc):
    result = "### Original → Lemma\n\n"
    result += "| Original | Lemma | POS |\n|----------|-------|-----|\n"
    for token in doc:
        if not token.is_space and not token.is_punct:
            result += f"| {token.text} | {token.lemma_} | {token.pos_} |\n"
    return result


def create_entities_result(entities):
    if entities:
        result = "### Named Entities\n\n"
        result += "| Entity | Type |\n|--------|------|\n"
        for ent, label in entities:
            result += f"| {ent} | {label} |\n"
        return result
    return "No named entities detected."


def show_selected_result(option, results):
    if results is None:
        return "Please submit text first.", ""

    detailed = results.get(option, "No data available.")
    cleaned = results.get("Cleaned Text (no stopwords + lemmas)", "")
    return detailed, cleaned


# ====================== INTERFACE ======================

with gr.Blocks(title="NLP Text Analyzer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧠 NLP Text Analyzer")
    gr.Markdown("### Step 1: Enter text and click Submit")

    results_state = gr.State(None)

    text_input = gr.Textbox(
        label="Enter your text here",
        lines=8,
        placeholder="Paste any paragraph, news article, or sentence..."
    )

    submit_btn = gr.Button("🚀 Submit & Analyze", variant="primary")

    stats_output = gr.Markdown()

    gr.Markdown("### Step 2: Select what you want to see")

    option_dropdown = gr.Dropdown(
        choices=[
            "Tokens (with POS tags)",
            "Stopwords Removed",
            "Lemmatized Tokens",
            "Named Entities",
            "Cleaned Text (no stopwords + lemmas)"
        ],
        label="Select Analysis Type",
        value="Named Entities",
        visible=False
    )

    detailed_output = gr.Markdown(visible=False)
    cleaned_output = gr.Textbox(label="Cleaned Text", lines=4, visible=False)

    # Submit button action
    submit_btn.click(
        fn=process_text,
        inputs=text_input,
        outputs=[
            stats_output,
            option_dropdown,
            detailed_output,
            cleaned_output,
            option_dropdown,
            results_state
        ]
    )

    # Dropdown change action
    option_dropdown.change(
           fn=show_selected_result,
          inputs=[option_dropdown, results_state],
          outputs=[detailed_output, cleaned_output]
)

    demo.launch(
    share=True,
    css="""
    footer {display: none !important;}
    .footer {display: none !important;}
    .gradio-container footer {display: none !important;}
    """
)
