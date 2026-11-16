"""Generate fresh non-overlapping test_v2 (30 items) alongside dev (18 items)."""
from __future__ import annotations

import json
from typing import Any

from advanced.evaluate import BENCHMARK_PATH, validate_benchmark
from advanced.ingest import DATA_DIR

BENCHMARK_V2_PATH = DATA_DIR / "benchmark_v2.json"


def build_benchmark_v2() -> dict[str, list[dict[str, Any]]]:
    old_data = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
    dev = old_data["dev"]

    test_v2: list[dict[str, Any]] = [
        # --- table (6): Table 5, Table 6, Table 7, Table 11, Table 13, Table 14 ---
        {
            "id": "v2_table_1",
            "category": "table",
            "question": "According to Table 5 on page 18 (English->Kalamang translation on MTOB), what are Gemini 1.5 Pro's human evaluation score and chrF score in the 'full book' context setting?",
            "expected_answer": "Human evaluation score: 5.46; chrF score: 59.0.",
            "evidence": "Table 5 (p.18), row 'full book', column 'Gemini 1.5 Pro': 5.46 (59.0).",
            "pages": [18],
        },
        {
            "id": "v2_table_2",
            "category": "table",
            "question": "In Table 6 on page 19 (Gemini 1.5 Pro Kalamang ASR), what is the lowest Character Error Rate (CER) achieved and under which text and audio context combination?",
            "expected_answer": "22.9% CER, achieved with text context 'sentences' and audio context '800-audioshot'.",
            "evidence": "Table 6 (p.19): bold blue 22.9% at row 'sentences', column '800-audioshot'.",
            "pages": [19],
        },
        {
            "id": "v2_table_3",
            "category": "table",
            "question": "In Table 7 on page 20 (Gemini 1.5 Flash Kalamang ASR), what is the CER with 'none' text context and '0-audioshot', and what is the best (lowest) CER in the table?",
            "expected_answer": "73.3% at (none, 0-audioshot); lowest CER is 25.2% at (both, 800-audioshot).",
            "evidence": "Table 7 (p.20): 73.3% at none/0-audioshot; 25.2% (bold blue) at both/800-audioshot.",
            "pages": [20],
        },
        {
            "id": "v2_table_4",
            "category": "table",
            "question": "According to Table 11 on page 30, what are Gemini 1.5 Pro's scores on GSM8K (11-shot) and Hellaswag (10-shot)?",
            "expected_answer": "GSM8K (11-shot): 90.8%; Hellaswag (10-shot): 93.3%.",
            "evidence": "Table 11 (p.30), column '1.5 Pro': GSM8K 90.8%, Hellaswag 93.3%.",
            "pages": [30],
        },
        {
            "id": "v2_table_5",
            "category": "table",
            "question": "In Table 13 on page 34, what is Gemini 1.5 Pro's Per-instruction accuracy and Full-response accuracy on the 1326 long prompts set?",
            "expected_answer": "Per-instruction accuracy: 90.2 +/- 0.6; Full-response accuracy: 58.6 +/- 2.7.",
            "evidence": "Table 13 (p.34), section '1326 long prompts', column '1.5 Pro': 90.2+-0.6 and 58.6+-2.7.",
            "pages": [34],
        },
        {
            "id": "v2_table_6",
            "category": "table",
            "question": "According to Table 14 on page 36 (DOLOMITES benchmark LM-judge win rate), what are the scores of Gemini 1.0 Pro, 1.0 Ultra, 1.5 Flash, and 1.5 Pro?",
            "expected_answer": "1.0 Pro: 20.9%, 1.0 Ultra: 18.4%, 1.5 Flash: 34.5%, 1.5 Pro: 55.3%.",
            "evidence": "Table 14 (p.36): 20.9%, 18.4%, 34.5%, 55.3%.",
            "pages": [36],
        },
        # --- image_diagram (5): new non-overlapping visual details from Figure 3, 4, 5, 28, 30 ---
        {
            "id": "v2_img_1",
            "category": "image_diagram",
            "question": "In Figure 3 on page 8, what is the exact user question shown in the prompt box on the left, and what condition inside `if ...:` is shown in the `backward_pass` Python code?",
            "expected_answer": "User question: 'In what file is the backward pass for autodifferentiation implemented in JAX?'; condition: `if all(type(ct) is Zero for ct in cotangents_in) and not jaxpr.effects:`.",
            "evidence": "Figure 3 (p.8): left prompt box question and right code box `if all(type(ct) is Zero for ct in cotangents_in) and not jaxpr.effects:`.",
            "pages": [8],
        },
        {
            "id": "v2_img_2",
            "category": "image_diagram",
            "question": "In Figure 4 on page 8, what is the exact Kalamang translation output shown in the blue Model output box on the right?",
            "expected_answer": "'An padanual repte, irar paruotkin.'",
            "evidence": "Figure 4 (p.8), right Model output box: 'An padanual repte, irar paruotkin.'.",
            "pages": [8],
        },
        {
            "id": "v2_img_3",
            "category": "image_diagram",
            "question": "In Figure 5 on page 8, what PDF filename and total page/token count are shown in the Long context box on the left, and what spoken quote from the Bishop appears above the highlighted line in the Model output?",
            "expected_answer": "Filename: `les_miserables.pdf` (`1382 pages, 732162 tokens`); Bishop quote: '\"My friend,\" resumed the Bishop, \"before you go, here are your candlesticks. Take them.\"'",
            "evidence": "Figure 5 (p.8): `Parsed PDF les_miserables.pdf`, `1382 pages, 732162 tokens`, Bishop quote above highlighted text.",
            "pages": [8],
        },
        {
            "id": "v2_img_4",
            "category": "image_diagram",
            "question": "In Figure 28 on page 110 (AlphaGo documentary frame), what two country flags are shown in front of the players (under 'AlphaGo' and 'Lee Sedol'), and at what timestamp/frame is the needle embedded?",
            "expected_answer": "The UK (Union Jack) flag under AlphaGo and the South Korean flag under Lee Sedol; embedded at timestamp 52:31 (frame 3151).",
            "evidence": "Figure 28 (p.110): UK flag under AlphaGo, South Korean flag under Lee Sedol, caption 'timestamp 52:31, or frame 3151'.",
            "pages": [110],
        },
        {
            "id": "v2_img_5",
            "category": "image_diagram",
            "question": "In Figure 30 on page 139, what are the four multiple-choice chemical formula options (a-d) under the left 'Isolated Diagram', and what seven items appear in the color legend of the 'Full Figure' panel?",
            "expected_answer": "Options: a) C14H32N8O4, b) C16H28N8O4, c) C15H30N6O6, d) C15H30N8O4. Legend items: RRE, Substrate, P450, MNIO partner, MNIO, B12-rSAM, Methyl-transferase.",
            "evidence": "Figure 30 (p.139): left box options a-d; right box legend RRE, Substrate, P450, MNIO partner, MNIO, B12-rSAM, Methyl-transferase.",
            "pages": [139],
        },
        # --- chart (5): Figure 12, Figure 18, Figure 22, Figure 25, Figure 29 ---
        {
            "id": "v2_chart_1",
            "category": "chart",
            "question": "In Figure 12 (MRCR) on page 16, after what context length (in tokens) does Gemini 1.5 Pro outperform both Claude 3 Opus and GPT-4 Turbo (04-09-2024), and up to what maximum context length do Gemini 1.5 Pro and Flash extend on the x-axis?",
            "expected_answer": "After 32K tokens; Gemini 1.5 Pro and Flash extend up to 1M tokens (while competitors stop at 128K).",
            "evidence": "Figure 12 (p.16) plot + caption: after 32K tokens 1.5 Pro leads Opus and GPT-4 Turbo (04-09-2024); x-axis extends to 1M.",
            "pages": [16],
        },
        {
            "id": "v2_chart_2",
            "category": "chart",
            "question": "In Figure 18 on page 35 (Expertise QA), what are the exact 'Accurate' and 'Severely Inaccurate' percentages for Gemini 1.5 Flash and Gemini 1.5 Pro?",
            "expected_answer": "Accurate: Gemini 1.5 Flash 67.7%, Gemini 1.5 Pro 67.1%; Severely Inaccurate: Gemini 1.5 Flash 7.3%, Gemini 1.5 Pro 6.3%.",
            "evidence": "Figure 18 (p.35) bar labels: Accurate (1.5 Flash 67.7%, 1.5 Pro 67.1%); Severely Inaccurate (1.5 Flash 7.3%, 1.5 Pro 6.3%).",
            "pages": [35],
        },
        {
            "id": "v2_chart_3",
            "category": "chart",
            "question": "In Figure 22 on page 59 (Refusal rates relative to Gemini 1.0 Ultra), which direction is labeled 'Optimal this way', and which model has the highest relative Grounded Refusal Rate (~1.38)?",
            "expected_answer": "'Optimal this way' points to the right (higher ungrounded refusal rate, lower grounded refusal rate); Gemini 1.5 Flash has the highest relative Grounded Refusal Rate (~1.38).",
            "evidence": "Figure 22 (p.59): arrow pointing right labeled 'Optimal this way'; Gemini 1.5 Flash dot at (~0.33, ~1.38).",
            "pages": [59],
        },
        {
            "id": "v2_chart_4",
            "category": "chart",
            "question": "In Figure 25 on page 64 (Personal data memorization rates), which two models have % Memorized below 0.03% for both Personal='No' and Personal='Yes', and why is sensitive data omitted from the figure?",
            "expected_answer": "Gemini 1.5 Flash and Gemini 1.5 Pro; sensitive data is omitted because the authors did not find any memorized sensitive data.",
            "evidence": "Figure 25 (p.64) bars + caption: Gemini 1.5 Flash and Pro are below ~0.025%; caption states 'we did not find any memorized sensitive data, hence it is omitted from the figure.'",
            "pages": [64],
        },
        {
            "id": "v2_chart_5",
            "category": "chart",
            "question": "In Figure 29 on page 117 (individual attribute extraction plots), across all three panels (category, color, semantic attribute), which model stays highest across all batch sizes up to 512, and roughly what accuracy (%) does it achieve on 'category extraction'?",
            "expected_answer": "Gemini 1.5 Pro (blue line) stays highest across all batch sizes up to 512, achieving ~91% accuracy on category extraction.",
            "evidence": "Figure 29 (p.117): blue line (Gemini 1.5 Pro) is top line from batch size 8 to 512 in all 3 subplots, flat around ~91% in left subplot.",
            "pages": [117],
        },
        # --- multi_hop (4) ---
        {
            "id": "v2_multi_1",
            "category": "multi_hop",
            "question": "Compare Gemini 1.5 Pro's accuracy on BigBench-Hard (3-shot) and MMLU (5-shot) in Table 11 (p.30) with the improvement shown for those two benchmarks from Feb to May 2024 in Figure 2 (p.5).",
            "expected_answer": "In Table 11 (p.30), BigBench-Hard is 89.2% and MMLU is 85.9%; in Figure 2 (p.5), BigBench-Hard improved by +5.2 (84.0 -> 89.2) and MMLU improved by +4.0 (81.9 -> 85.9).",
            "evidence": "Table 11 (p.30) + Figure 2 (p.5).",
            "pages": [5, 30],
        },
        {
            "id": "v2_multi_2",
            "category": "multi_hop",
            "question": "Compare the lowest CER for Kalamang ASR achieved by Gemini 1.5 Pro in Table 6 (p.19) with the lowest CER achieved by Gemini 1.5 Flash in Table 7 (p.20): what is the difference in percentage points?",
            "expected_answer": "Gemini 1.5 Pro's lowest CER is 22.9% (Table 6, p.19) and Gemini 1.5 Flash's lowest CER is 25.2% (Table 7, p.20), a difference of 2.3 percentage points.",
            "evidence": "Table 6 (p.19) 22.9%; Table 7 (p.20) 25.2%; 25.2 - 22.9 = 2.3.",
            "pages": [19, 20],
        },
        {
            "id": "v2_multi_3",
            "category": "multi_hop",
            "question": "Compare Gemini 1.5 Pro's Physical_appearance Bias score in the disambiguous BBQ split (Figure 26a, p.65) with its Accuracy on that same disambiguous Physical_appearance cell (Figure 26b, p.65).",
            "expected_answer": "In the disambiguous Physical_appearance cell, Gemini 1.5 Pro has a Bias score of -5.1 (Figure 26a) and an Accuracy of 0.71 (Figure 26b).",
            "evidence": "Figure 26 (p.65), row Physical_appearance, disambiguous Gemini 1.5 Pro: Bias = -5.1, Accuracy = 0.71.",
            "pages": [65],
        },
        {
            "id": "v2_multi_4",
            "category": "multi_hop",
            "question": "From Table 28 on page 58, what is the average reduction in safety violation rates in long context relative to short context, and what is the strongest (most negative) reduction cell in the table (give depth and context length)?",
            "expected_answer": "Average reduction is -28.6%; the strongest reduction is -47.6% at 100% Document Depth and 256,768 Context Length.",
            "evidence": "Table 28 (p.58): 'On average: -28.6%'; row 100%, column 256,768 = -47.6%.",
            "pages": [58],
        },
        # --- text (4) ---
        {
            "id": "v2_text_1",
            "category": "text",
            "question": "According to page 4, how many native speakers does the Kalamang language have, and how many minutes of transcribed Kalamang speech recordings were added to demonstrate in-context ASR?",
            "expected_answer": "Fewer than 200 speakers, and 45 minutes of transcribed Kalamang speech recordings.",
            "evidence": "Page 4 top paragraph: 'fewer than 200 speakers' and '45 minutes of transcribed Kalamang speech recordings'.",
            "pages": [4],
        },
        {
            "id": "v2_text_2",
            "category": "text",
            "question": "According to page 23 (Section 5.2.2.5 Long-context Audio), why does Gemini 1.0 Pro have a 100% WER on 15-minute videos without segmentation, and what WER does it achieve when segmented every 30 seconds?",
            "expected_answer": "It has 100% WER without segmentation due to a mismatch between training and testing audio lengths; when segmented every 30 seconds, it achieves 7.8% WER.",
            "evidence": "Page 23 prose: 'WER of 100% due to a mismatch between training and testing audio lengths' and '7.8%' with 30s segmentation.",
            "pages": [23],
        },
        {
            "id": "v2_text_3",
            "category": "text",
            "question": "According to page 28 (Section 5.2.2.8), how many images are used in the image structuralization task, and why are mini-batches used for models with shorter context lengths?",
            "expected_answer": "1024 images are used; mini-batches are used when a model's context length does not permit processing all 1024 images at once (then concatenated).",
            "evidence": "Page 28 prose: 'set of 1024 images' and 'in case where context length of models does not permit processing of all the images at once, we use mini-batches'.",
            "pages": [28],
        },
        {
            "id": "v2_text_4",
            "category": "text",
            "question": "According to page 45 (Section 8), what does the report say about Gemini 1.5 Flash-8B's context window length and parameter scale?",
            "expected_answer": "It supports a context window exceeding 1 million tokens and belongs to the domain of single-digit billion parameter models.",
            "evidence": "Page 45, Section 8: 'context window exceeding 1 million tokens' and 'single-digit billion parameter models'.",
            "pages": [45],
        },
        # --- unanswerable (6): all verified 0 hits across all 154 pages ---
        {
            "id": "v2_unans_1",
            "category": "unanswerable",
            "question": "What score does Gemini 1.5 Pro achieve on the GPQA-Diamond benchmark in this report?",
            "expected_answer": "Abstain: GPQA-Diamond is not evaluated or mentioned in the report.",
            "evidence": "Verified absent across all 154 pages ('GPQA-Diamond' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v2_unans_2",
            "category": "unanswerable",
            "question": "What pass@1 score does Gemini 1.5 Pro achieve on LiveCodeBench in this technical report?",
            "expected_answer": "Abstain: LiveCodeBench is not evaluated or mentioned in the report.",
            "evidence": "Verified absent across all 154 pages ('LiveCodeBench' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v2_unans_3",
            "category": "unanswerable",
            "question": "What is Gemini 1.5 Pro's score on HumanEval+ (HumanEval Plus) reported in Table 11?",
            "expected_answer": "Abstain: HumanEval+ is not reported (Table 11 only reports standard HumanEval).",
            "evidence": "Verified absent across all 154 pages ('HumanEval+' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v2_unans_4",
            "category": "unanswerable",
            "question": "What score did Math-Specialized Gemini 1.5 Pro achieve on AIME 2025 in Table 21?",
            "expected_answer": "Abstain: AIME 2025 is not in the report (Table 21 only reports AIME 2024).",
            "evidence": "Verified absent across all 154 pages ('AIME 2025' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v2_unans_5",
            "category": "unanswerable",
            "question": "How many NVIDIA H100 GPUs were used in the training cluster for Gemini 1.5 Pro?",
            "expected_answer": "Abstain: NVIDIA H100 GPUs are not mentioned (the report states TPUv4 accelerators).",
            "evidence": "Verified absent across all 154 pages ('H100' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v2_unans_6",
            "category": "unanswerable",
            "question": "How does Gemini 1.5 Flash compare against DeepSeek-V3 and Qwen-2.5 in this technical report?",
            "expected_answer": "Abstain: neither DeepSeek nor Qwen appears anywhere in this technical report.",
            "evidence": "Verified absent across all 154 pages ('DeepSeek' = 0 hits, 'Qwen' = 0 hits).",
            "pages": [],
        },
    ]

    data = {"dev": dev, "test": test_v2}
    BENCHMARK_V2_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


if __name__ == "__main__":
    build_benchmark_v2()
    print(json.dumps(validate_benchmark(BENCHMARK_V2_PATH), indent=2))
