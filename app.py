
import contextlib
import gradio as gr
import spacy
import matplotlib.pyplot as plt
from collections import Counter

# Load NLP model
nlp = spacy.load("en_core_web_sm")


# Theme and styling
NEON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --page-bg: #090d19;
    --panel-bg: #121a2d;
    --inner-bg: #0c1325;
    --border: #293654;
    --violet: #8065ff;
    --cyan: #50dce5;
    --main-text: #f1f3ff;
    --muted: #a0accb;
}

html, body, body > div {
    background: var(--page-bg) !important;
}

.gradio-container {
    width: 100% !important;
    max-width: 100% !important;
    min-height: 100vh;
    box-sizing: border-box !important;
    padding: 22px clamp(12px, 2vw, 30px) !important;
    margin: 0 auto !important;
    background:
        radial-gradient(ellipse at 0% 0%, #242050 0%, transparent 32%),
        radial-gradient(ellipse at 100% 25%, #103543 0%, transparent 30%),
        var(--page-bg) !important;
    color: var(--main-text) !important;
    font-family: 'Manrope', 'Segoe UI', sans-serif !important;
}

.gradio-container * {
    font-family: 'Manrope', 'Segoe UI', sans-serif;
}

#app-header {
    padding: 18px 24px !important;
    margin-bottom: 20px !important;
    border: 1px solid #34365b;
    border-radius: 16px;
    background: linear-gradient(110deg, #191936, #101c30);
}

#eyebrow {
    color: var(--cyan);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

#app-header h1 {
    margin: 8px 0 !important;
    font-size: clamp(28px, 3vw, 40px) !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #ffffff, #c9baff, #65e8f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

#app-header p {
    color: var(--muted) !important;
}

#sidebar {
    background: rgba(18, 26, 45, .97) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    min-width: 0 !important;
    height: fit-content;
}

#sidebar h3 {
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 800 !important;
}

#sidebar button {
    text-align: left !important;
    justify-content: flex-start !important;
    min-height: 43px;
    border-radius: 9px !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    border: 1px solid transparent !important;
    transition: .2s ease;
}

#sidebar button:hover {
    background: #242344 !important;
    border-color: #5b4aab !important;
}

#home-page, #analysis-page, #stats-panel,
#input-panel, #results-panel, #cleaned-panel {
    min-width: 0 !important;
    box-sizing: border-box !important;
    background: rgba(18, 26, 45, .97) !important;
    border: 1px solid var(--border) !important;
    border-radius: 15px !important;
    padding: 20px !important;
}

#stats-panel {
    border-top: 2px solid var(--violet) !important;
}

#input-panel {
    border-top: 2px solid var(--cyan) !important;
}

#analysis-page {
    border-top: 2px solid var(--violet) !important;
}

#cleaned-panel {
    border-left: 3px solid var(--cyan) !important;
}

#home-page h1, #home-page h2, #home-page h3,
#analysis-page h1, #analysis-page h2, #analysis-page h3,
#stats-panel h1, #stats-panel h2, #stats-panel h3,
#input-panel h1, #input-panel h2, #input-panel h3,
#cleaned-panel h1, #cleaned-panel h2, #cleaned-panel h3 {
    color: #ffffff !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    letter-spacing: -.4px;
}

label {
    color: #e2e7ff !important;
    font-weight: 800 !important;
}

textarea, input {
    background: var(--inner-bg) !important;
    color: var(--main-text) !important;
    border: 1px solid #34415f !important;
    border-radius: 10px !important;
}

textarea:focus, input:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 2px rgba(128, 101, 255, .15) !important;
}

#input-text textarea {
    min-height: 200px !important;
    line-height: 1.8;
}

#analyze-button {
    width: 100%;
    min-height: 48px;
    border: none !important;
    border-radius: 10px !important;
    background: linear-gradient(100deg, #6746f5, #985bff) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    box-shadow: 0 5px 22px rgba(112, 77, 244, .25);
}

#analyze-button:hover {
    filter: brightness(1.12);
}

#stats-panel ul {
    list-style: none !important;
    padding: 0 !important;
    margin-top: 12px !important;
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
}

#stats-panel li {
    min-width: 0;
    overflow-wrap: anywhere;
    background: linear-gradient(145deg, #202644, #121a2e);
    border: 1px solid #303b5b;
    border-top: 2px solid #7059dc;
    border-radius: 11px;
    padding: 14px !important;
    color: var(--muted);
    font-weight: 600;
}

#stats-panel li strong {
    color: var(--cyan) !important;
    font-size: 16px;
    font-weight: 800 !important;
}

#analysis-results table {
    width: 100% !important;
    max-width: 100% !important;
    border-collapse: collapse;
    overflow-wrap: anywhere;
}

#analysis-results th {
    background: #29234c !important;
    color: #d9d0ff !important;
    font-weight: 800 !important;
    padding: 12px !important;
    border: 1px solid #39385e !important;
}

#analysis-results td {
    background: #10182b !important;
    color: #e4e9ff !important;
    padding: 10px 12px !important;
    border: 1px solid #2b3550 !important;
}

#analysis-results tr:hover td {
    background: #1b2540 !important;
}

#frequency-plot {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
    background: #0d1426 !important;
    border: 1px solid #303b5b !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

#frequency-plot > div {
    width: 100% !important;
    max-width: 100% !important;
}

footer {
    display: none !important;
}

@media (max-width: 850px) {
    .gradio-container {
        padding: 12px !important;
    }

    #stats-panel ul {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    #sidebar {
        padding: 10px !important;
    }

    #home-page, #analysis-page, #stats-panel,
    #input-panel, #results-panel, #cleaned-panel {
        padding: 14px !important;
    }
}
"""


# Helper functions
def escape_table_cell(text):
    text = str(text)
    text = text.replace("\\", "\\\\")
    text = text.replace("|", "\\|")
    text = text.replace("\n", " ").replace("\r", " ")
    return text


def create_tokens_table(doc):
    result = (
        "| Token | POS | Tag |\n"
        "|---|---|---|\n"
    )

    for token in doc:
        if not token.is_space:
            result += (
                f"| {escape_table_cell(token.text)} "
                f"| {escape_table_cell(token.pos_)} "
                f"| {escape_table_cell(token.tag_)} |\n"
            )

    return result


def create_stopwords_result(stopwords):
    if not stopwords:
        return "No stopwords found."

    words = ", ".join(
        f"`{word.replace('`', chr(92) + chr(96))}`"
        for word in stopwords
    )

    return (
        words
        + f"\n\n**Total stopwords:** {len(stopwords)}"
    )


def create_lemma_table(doc):
    result = (
        "| Original | Lemma | POS |\n"
        "|---|---|---|\n"
    )

    for token in doc:
        if not token.is_space and not token.is_punct:
            result += (
                f"| {escape_table_cell(token.text)} "
                f"| {escape_table_cell(token.lemma_)} "
                f"| {escape_table_cell(token.pos_)} |\n"
            )

    return result


def create_entities_result(entities):
    if not entities:
        return "No named entities detected."

    result = (
        "| Entity | Type |\n"
        "|---|---|\n"
    )

    for entity, label in entities:
        result += (
            f"| {escape_table_cell(entity)} "
            f"| {escape_table_cell(label)} |\n"
        )

    return result


def get_word_frequency(doc, top_n=10):
    words = [
        token.lemma_.lower()
        for token in doc
        if (
            not token.is_stop
            and not token.is_punct
            and not token.is_space
            and token.is_alpha
            and len(token.text) > 1
        )
    ]

    return Counter(words).most_common(top_n)


def create_frequency_result(word_frequency):
    if not word_frequency:
        return "No meaningful words found for frequency analysis."

    result = (
        "| Word | Frequency |\n"
        "|---|---:|\n"
    )

    for word, count in word_frequency:
        result += f"| {escape_table_cell(word)} | {count} |\n"

    return result


def create_frequency_chart(word_frequency):
    if not word_frequency:
        return None

    words = [item[0] for item in word_frequency]
    counts = [item[1] for item in word_frequency]

    fig, ax = plt.subplots(figsize=(9, 4.5))

    bars = ax.bar(
        words,
        counts,
        color="#8065ff",
        edgecolor="#50dce5",
        linewidth=0.7
    )

    ax.set_title(
        "Top 10 Most Frequent Words",
        color="#f1f3ff",
        fontsize=14,
        fontweight="bold",
        pad=14
    )

    ax.set_xlabel("Words", color="#a0accb")
    ax.set_ylabel("Frequency", color="#a0accb")
    ax.tick_params(axis="x", rotation=30, labelcolor="#cbd3ed")
    ax.tick_params(axis="y", labelcolor="#cbd3ed")
    ax.set_facecolor("#0d1426")
    fig.patch.set_facecolor("#0d1426")
    ax.grid(axis="y", alpha=0.15)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color("#303b5b")

    for bar, count in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(count),
            ha="center",
            va="bottom",
            color="#f1f3ff",
            fontsize=9
        )

    fig.tight_layout()
    return fig


# Process text
def process_text(text):
    if not text or not text.strip():
        return (
            "### Enter some text to begin your analysis.",
            None,
            "Please enter text before analyzing."
        )

    doc = nlp(text)

    tokens = [token.text for token in doc]
    stopwords = [token.text for token in doc if token.is_stop]
    punctuation = [token.text for token in doc if token.is_punct]

    unique_words = {
        token.text.lower()
        for token in doc
        if not token.is_punct and not token.is_space
    }

    entities = [(ent.text, ent.label_) for ent in doc.ents]

    cleaned_tokens = [
        token.lemma_.lower()
        for token in doc
        if (
            (not token.is_stop or token.lower_ == "not")
            and not token.is_punct
            and not token.is_space
        )
    ]

    cleaned_text = " ".join(cleaned_tokens)
    word_frequency = get_word_frequency(doc)

    stats = f"""
### Analysis Overview

- **Total Tokens:** {len(tokens)}
- **Unique Words:** {len(unique_words)}
- **Stopwords:** {len(stopwords)}
- **Punctuation Marks:** {len(punctuation)}
- **Named Entities:** {len(entities)}
- **Tokens After Cleaning:** {len(cleaned_tokens)}
"""

    results = {
        "Tokens and POS Tags": create_tokens_table(doc),
        "Stopwords": create_stopwords_result(stopwords),
        "Lemmatization": create_lemma_table(doc),
        "Named Entities": create_entities_result(entities),
        "Word Frequency": create_frequency_result(word_frequency),
        "Cleaned Text": cleaned_text,
        "Frequency Data": word_frequency
    }

    return stats, results, "Analysis completed successfully."


# Page navigation
def show_page(page, results):
    if page == "Dashboard":
        return (
            gr.update(visible=True),
            gr.update(visible=False),
            "Dashboard",
            "Select an analysis from the sidebar to explore your results.",
            gr.update(value=None, visible=False),
            "",
            "Dashboard"
        )

    if results is None:
        return (
            gr.update(visible=False),
            gr.update(visible=True),
            page,
            "Please return to the Dashboard, enter text, and click Analyze Text first.",
            gr.update(value=None, visible=False),
            "",
            "No analysis available yet"
        )

    if page == "Tokens and POS Tags":
        detail = results["Tokens and POS Tags"]
        chart_update = gr.update(value=None, visible=False)

    elif page == "Stopwords":
        detail = results["Stopwords"]
        chart_update = gr.update(value=None, visible=False)

    elif page == "Lemmatization":
        detail = results["Lemmatization"]
        chart_update = gr.update(value=None, visible=False)

    elif page == "Named Entities":
        detail = results["Named Entities"]
        chart_update = gr.update(value=None, visible=False)

    elif page == "Word Frequency":
        detail = results["Word Frequency"]
        chart = create_frequency_chart(results["Frequency Data"])
        chart_update = gr.update(value=chart, visible=True)

    else:
        detail = "Select an analysis from the sidebar."
        chart_update = gr.update(value=None, visible=False)

    return (
        gr.update(visible=False),
        gr.update(visible=True),
        page,
        detail,
        chart_update,
        results["Cleaned Text"],
        f"Viewing: {page}"
    )


# Application interface
with gr.Blocks(
    title="NLP Text Analyzer | Neural Studio",
    theme=gr.themes.Base(
        primary_hue="violet",
        secondary_hue="cyan",
        neutral_hue="slate"
    ),
    css=NEON_CSS
) as demo:

    gr.Markdown(
        """
        <div id="eyebrow">NEURAL STUDIO · TEXT INTELLIGENCE</div>

        # NLP Text Analyzer
        """,
        elem_id="app-header"
    )

    results_state = gr.State(None)

    with gr.Row(equal_height=False):

        # Sidebar
        with gr.Column(scale=1, min_width=190, elem_id="sidebar"):
            gr.Markdown("### Workspace")

            home_btn = gr.Button("⌂  Dashboard")
            tokens_btn = gr.Button("▤  Tokens and POS Tags")
            stopwords_btn = gr.Button("✂  Stopwords")
            lemma_btn = gr.Button("Aa  Lemmatization")
            entities_btn = gr.Button("◎  Named Entities")
            frequency_btn = gr.Button("▥  Word Frequency")


        # Main content
        with gr.Column(scale=5, min_width=320):

            with gr.Group(elem_id="home-page", visible=True) as home_page:
                gr.Markdown("### Your Workspace")
                gr.Markdown(
                    "Enter your text below, then explore its linguistic features."
                )

                text_input = gr.Textbox(
                    label="Input Text",
                    lines=9,
                    placeholder="Paste an article, paragraph, or sentence here...",
                    elem_id="input-text"
                )

                submit_btn = gr.Button(
                    "✦  Analyze Text",
                    variant="primary",
                    elem_id="analyze-button"
                )

                status_output = gr.Markdown("Ready for analysis.")

                with gr.Group(elem_id="stats-panel"):
                    gr.Markdown("### Analysis Overview")
                    stats_output = gr.Markdown(
                        "Your statistics will appear here after analysis."
                    )

            with gr.Group(
                elem_id="analysis-page",
                visible=False
            ) as analysis_page:

                page_title = gr.Markdown("### Analysis Results")

                detailed_output = gr.Markdown(
                    visible=True,
                    elem_id="analysis-results"
                )

                frequency_chart = gr.Plot(
                    label="Word Frequency Visualization",
                    visible=False,
                    elem_id="frequency-plot"
                )

                with gr.Group(elem_id="cleaned-panel"):
                    gr.Markdown("### Cleaned Text")

                    cleaned_output = gr.Textbox(
                        label="Processed Output",
                        lines=5,
                        interactive=False
                    )

    # Analyze button        
    def analyze_and_store(text):
        try:
            stats, results, status = process_text(text)
            return stats, results, status

        except Exception as e:
            print(f"Analysis error: {e}")
            return (
            "### Analysis could not be completed.",
            None,
            f"An error occurred during analysis: {e}"
        )
    submit_btn.click(
        fn=analyze_and_store,
        inputs=[text_input],
        outputs=[
            stats_output,
            results_state,
            status_output
        ]
    )

    # Navigation buttons
    page_outputs = [
        home_page,
        analysis_page,
        page_title,
        detailed_output,
        frequency_chart,
        cleaned_output,
        status_output
    ]

    home_btn.click(
        fn=lambda results: show_page("Dashboard", results),
        inputs=[results_state],
        outputs=page_outputs
    )

    tokens_btn.click(
        fn=lambda results: show_page("Tokens and POS Tags", results),
        inputs=[results_state],
        outputs=page_outputs
    )

    stopwords_btn.click(
        fn=lambda results: show_page("Stopwords", results),
        inputs=[results_state],
        outputs=page_outputs
    )

    lemma_btn.click(
        fn=lambda results: show_page("Lemmatization", results),
        inputs=[results_state],
        outputs=page_outputs
    )

    entities_btn.click(
        fn=lambda results: show_page("Named Entities", results),
        inputs=[results_state],
        outputs=page_outputs
    )

    frequency_btn.click(
        fn=lambda results: show_page("Word Frequency", results),
        inputs=[results_state],
        outputs=page_outputs
    )


# Launch application
if __name__ == "__main__":
    demo.launch(share=False)
