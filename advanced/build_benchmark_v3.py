"""Generate fresh non-overlapping test_v3 (30 items) alongside dev (18 items)."""
from __future__ import annotations

import json
from typing import Any

from advanced.evaluate import BENCHMARK_PATH, validate_benchmark
from advanced.ingest import DATA_DIR

BENCHMARK_V3_PATH = DATA_DIR / "benchmark_v3.json"


def build_benchmark_v3() -> dict[str, list[dict[str, Any]]]:
    old_data = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))
    dev = old_data["dev"]

    test_v3: list[dict[str, Any]] = [
        # --- table (6): Table 16, Table 19, Table 23, Table 25, Table 48, Table 52 ---
        {
            "id": "v3_table_1",
            "category": "table",
            "question": "According to Table 16 on page 36, what are Gemini 1.5 Pro's Win %, Tie %, and Loss % when compared against baseline Gemini 1.0 Ultra?",
            "expected_answer": "Win %: 45.7%, Tie %: 16.7%, Loss %: 37.6%.",
            "evidence": "Table 16 (p.36), row (1.0 Ultra, Gemini 1.5 Pro): 45.7%, 16.7%, 37.6%.",
            "pages": [36],
        },
        {
            "id": "v3_table_2",
            "category": "table",
            "question": "In Table 19 on page 40 (Video understanding), which model achieves the highest score on OpenEQA (val), and what is Gemini 1.5 Pro's score on ActivityNet-QA (test)?",
            "expected_answer": "Gemini 1.5 Flash achieves the highest score on OpenEQA (val) at 63.1; Gemini 1.5 Pro achieves 57.5% on ActivityNet-QA (test).",
            "evidence": "Table 19 (p.40): OpenEQA 1.5 Flash = 63.1 (bold blue); ActivityNet-QA 1.5 Pro = 57.5% (bold blue).",
            "pages": [40],
        },
        {
            "id": "v3_table_3",
            "category": "table",
            "question": "According to Table 23 on page 52, what are Gemini 1.5 Pro's percentage reductions in violation rates for Text-to-Text English, Text-to-Text Multilingual, and Image-to-Text?",
            "expected_answer": "Text-to-Text English: -58%, Text-to-Text Multilingual: -44%, Image-to-Text: -62%.",
            "evidence": "Table 23 (p.52), row 'Gemini 1.5 Pro': -58%, -44%, -62%.",
            "pages": [52],
        },
        {
            "id": "v3_table_4",
            "category": "table",
            "question": "In Table 25 on page 54, what are the reductions in violation rate from Text-to-Text (T2T) for Gemini 1.5 Flash and Gemini 1.5 Pro?",
            "expected_answer": "Gemini 1.5 Flash: -4.5%; Gemini 1.5 Pro: -10.1%.",
            "evidence": "Table 25 (p.54): Gemini 1.5 Flash -4.5%, Gemini 1.5 Pro -10.1%.",
            "pages": [54],
        },
        {
            "id": "v3_table_5",
            "category": "table",
            "question": "According to Table 48 on page 112 (Intermediate Algebra Levels 4 & 5), what are the scores of GPT-4, GPT-4-turbo, and Gemini 1.5 Pro with the generic SymPy/SciPy prompt?",
            "expected_answer": "GPT-4: 12.5%, GPT-4-turbo: 20.6%, Gemini 1.5 Pro (generic SymPy/SciPy prompt): 25.8%.",
            "evidence": "Table 48 (p.112): GPT-4 12.5%, GPT-4-turbo 20.6%, Gemini 1.5 Pro (generic SymPy/SciPy) 25.8%.",
            "pages": [112],
        },
        {
            "id": "v3_table_6",
            "category": "table",
            "question": "In Table 52 on page 128 (Expertise QA), what are the average response lengths (Words) for Gemini 1.0 Pro, 1.0 Ultra, 1.5 Flash, and 1.5 Pro?",
            "expected_answer": "1.0 Pro: 270 +- 12, 1.0 Ultra: 314 +- 7, 1.5 Flash: 420 +- 7, 1.5 Pro: 390 +- 7 words.",
            "evidence": "Table 52 (p.128), row 'Words': 270+-12, 314+-7, 420+-7, 390+-7.",
            "pages": [128],
        },
        # --- image_diagram (5) ---
        {
            "id": "v3_img_1",
            "category": "image_diagram",
            "question": "In Figure 3 on page 8, what is the return statement inside the `backward_pass` function shown in the blue Model output box?",
            "expected_answer": "`return map(lambda v: Zero(v.aval), jaxpr.invars)`.",
            "evidence": "Figure 3 (p.8), right code box: `return map(lambda v: Zero(v.aval), jaxpr.invars)`.",
            "pages": [8],
        },
        {
            "id": "v3_img_2",
            "category": "image_diagram",
            "question": "In Figure 4 on page 8, what are the two types of reference materials illustrated with page icons on the left (above '250K tokens')?",
            "expected_answer": "Grammar book + Dictionary.",
            "evidence": "Figure 4 (p.8), left box: 'Grammar book + Dictionary' above '250K tokens'.",
            "pages": [8],
        },
        {
            "id": "v3_img_3",
            "category": "image_diagram",
            "question": "In Figure 5 on page 8, what does the user prompt ask above the stick-figure drawing?",
            "expected_answer": "'Look at the event in this drawing. What page is this on?'",
            "evidence": "Figure 5 (p.8), User prompt box: 'Look at the event in this drawing. What page is this on?'.",
            "pages": [8],
        },
        {
            "id": "v3_img_4",
            "category": "image_diagram",
            "question": "In Figure 28 on page 110 (AlphaGo documentary frame), what is the name of the event printed on the blue backdrop behind the players (above the date '8 - 15 March 2016')?",
            "expected_answer": "'Google DeepMind Challenge Match' (with 'KBA' logo to its left).",
            "evidence": "Figure 28 (p.110), backdrop text: 'Google DeepMind Challenge Match'.",
            "pages": [110],
        },
        {
            "id": "v3_img_5",
            "category": "image_diagram",
            "question": "In Figure 30 on page 139, what is the multiple-choice question text (and options a-d) under the middle 'Sub-Figure' panel for AzF?",
            "expected_answer": "'How many Nitrogen atoms are in chemical structure diagram AzF?' with options a) 2, b) 3, c) 4, d) 5.",
            "evidence": "Figure 30 (p.139), middle bottom box: 'How many Nitrogen atoms are in chemical structure diagram AzF? a) 2 b) 3 c) 4 d) 5'.",
            "pages": [139],
        },
        # --- chart (5) ---
        {
            "id": "v3_chart_1",
            "category": "chart",
            "question": "In Figure 2 on page 5, what was Gemini 1.5 Pro's score on Natural2Code in Feb 2024 vs. May 2024, and what was the delta?",
            "expected_answer": "Feb 2024: 77.7; May 2024: 82.6 (+4.9).",
            "evidence": "Figure 2 (p.5), Natural2Code bars: 77.7 and 82.6 (+4.9).",
            "pages": [5],
        },
        {
            "id": "v3_chart_2",
            "category": "chart",
            "question": "In Figure 8 (Text Haystack) on page 12, how many red cells appear for Gemini 1.5 Pro in the 'From 1k to 1M tokens' panel and in the 'Up to 10M tokens' panel?",
            "expected_answer": "3 red cells in 'From 1k to 1M tokens' and 2 red cells in 'Up to 10M tokens' (5 red cells total).",
            "evidence": "Figure 8 (p.12) heatmap: 3 red squares in 1k-1M panel, 2 red squares in 2M-10M panel.",
            "pages": [12],
        },
        {
            "id": "v3_chart_3",
            "category": "chart",
            "question": "In Figure 14 on page 22 (Bradley-Terry Strength scores), what are the Strength scores of '0k context Gemini 1.0 Pro', 'RAG 4k context Gemini 1.0 Pro', and 'RAG 4k context GPT-4 Turbo'?",
            "expected_answer": "0k context Gemini 1.0 Pro: 0.1041; RAG 4k context Gemini 1.0 Pro: 0.2971; RAG 4k context GPT-4 Turbo: 1.2994.",
            "evidence": "Figure 14 (p.22) bar labels: 0.1041, 0.2971, 1.2994.",
            "pages": [22],
        },
        {
            "id": "v3_chart_4",
            "category": "chart",
            "question": "In Figure 15 on page 24, what are Gemini 1.5 Pro's accuracies on 1H-VideoQA (40-105 minutes) across 'First frame', '16 frames', '150 frames', and 'All frames (1 fps)'?",
            "expected_answer": "First frame: 0.238*, 16 frames: 0.452, 150 frames: 0.563, All frames (1 fps): 0.722.",
            "evidence": "Figure 15 (p.24), 1H-VideoQA bars: 0.238*, 0.452, 0.563, 0.722.",
            "pages": [24],
        },
        {
            "id": "v3_chart_5",
            "category": "chart",
            "question": "In Figure 32 on page 154 (BetterChartQA by-capability performance), what is the overall micro average number of examples (in brackets), and which capability category has the fewest examples (17)?",
            "expected_answer": "Overall micro average has 374 examples; 'scatter_plot (17)' has the fewest examples (17).",
            "evidence": "Figure 32 (p.154) y-axis labels: 'overall (374; micro average)' and 'scatter_plot (17)'.",
            "pages": [154],
        },
        # --- multi_hop (4) ---
        {
            "id": "v3_multi_1",
            "category": "multi_hop",
            "question": "Compare Gemini 1.5 Pro's HumanEval (0-shot) score in Table 11 (p.30) with its Feb 2024 HumanEval score shown in Figure 2 (p.5): how many percentage points did it gain from Feb to May 2024?",
            "expected_answer": "Table 11 shows 84.1% (May 2024) vs. 71.9% (Feb 2024) in Figure 2, a gain of +12.2 percentage points.",
            "evidence": "Table 11 (p.30) 84.1% + Figure 2 (p.5) 71.9 -> 84.1 (+12.2).",
            "pages": [5, 30],
        },
        {
            "id": "v3_multi_2",
            "category": "multi_hop",
            "question": "Compare the English time per output character (ms) in Table 3 (p.6) between Gemini 1.5 Flash and Claude 3 Opus: how many times faster is Gemini 1.5 Flash?",
            "expected_answer": "Gemini 1.5 Flash is 1.5 ms vs. Claude 3 Opus 10.5 ms, which is exactly 7.0x faster (10.5 / 1.5 = 7).",
            "evidence": "Table 3 (p.6), row 'English': 1.5 ms vs 10.5 ms (10.5 / 1.5 = 7.0).",
            "pages": [6],
        },
        {
            "id": "v3_multi_3",
            "category": "multi_hop",
            "question": "Compare Gemini 1.5 Pro's WMT23 (All) BLEURT score in Table 46 (p.109) with its rounded WMT23 score in Table 11 (p.30).",
            "expected_answer": "Table 46 reports 75.25 BLEURT for WMT23 All, which rounds to 75.3 in Table 11.",
            "evidence": "Table 46 (p.109) WMT23 All = 75.25; Table 11 (p.30) WMT23 = 75.3.",
            "pages": [30, 109],
        },
        {
            "id": "v3_multi_4",
            "category": "multi_hop",
            "question": "From Figure 26 (p.65), compare Gemini 1.0 Ultra vs. Gemini 1.5 Flash on ambiguous 'Age' Bias score and Accuracy on BBQ (4-shot).",
            "expected_answer": "Gemini 1.0 Ultra has Bias 27.5 and Accuracy 0.7, whereas Gemini 1.5 Flash has Bias -0.05 and Accuracy 1.0.",
            "evidence": "Figure 26 (p.65), row Age ambiguous: 1.0 Ultra (Bias 27.5, Acc 0.7) vs 1.5 Flash (Bias -0.05, Acc 1.0).",
            "pages": [65],
        },
        # --- text (4) ---
        {
            "id": "v3_text_1",
            "category": "text",
            "question": "According to page 4, across the extensive battery of core evaluations, how many benchmarks out of 50 do Gemini 1.5 Pro and Gemini 1.5 Flash surpass Gemini 1.0 Pro on?",
            "expected_answer": "Gemini 1.5 Pro surpasses Gemini 1.0 Pro on 44/50 benchmarks, and Gemini 1.5 Flash on 41/50 benchmarks.",
            "evidence": "Page 4: '(44/50 for Gemini 1.5 Pro and 41/50 for Gemini 1.5 Flash)'.",
            "pages": [4],
        },
        {
            "id": "v3_text_2",
            "category": "text",
            "question": "According to Section 3.3 on page 6, which APIs were used to measure latency for Gemini 1.5 / Claude 3 vs. GPT-3.5 / GPT-4?",
            "expected_answer": "Vertex AI streaming API for Gemini 1.5 and Claude 3; OpenAI streaming API for GPT-3.5 and GPT-4.",
            "evidence": "Page 6, Section 3.3: Vertex AI streaming API (Gemini 1.5, Claude 3) and OpenAI streaming API (GPT-3.5, GPT-4).",
            "pages": [6],
        },
        {
            "id": "v3_text_3",
            "category": "text",
            "question": "According to Section 7 on page 43, how many times more problems from AIME does the math-specialized Gemini 1.5 Pro solve compared to the base model?",
            "expected_answer": "4x more problems from AIME (as also seen in Table 21: 8/30 vs 2/30).",
            "evidence": "Page 43, Section 7: 'solving 4x more problems from AIME'.",
            "pages": [43],
        },
        {
            "id": "v3_text_4",
            "category": "text",
            "question": "According to page 22 (Section 5.2.2.4), what statistical model is used to analyze the side-by-side answer quality rankings, and what two games is it best known for?",
            "expected_answer": "The Bradley-Terry model (1952), best known for rating player strength in Chess or Go.",
            "evidence": "Page 22-23: 'Bradley-Terry model (Bradley and Terry, 1952)... best known for their use in Chess or Go to rate player strength'.",
            "pages": [23],
        },
        # --- unanswerable (6): all verified 0 hits across all 154 pages ---
        {
            "id": "v3_unans_1",
            "category": "unanswerable",
            "question": "What Elo rating did Gemini 1.5 Pro achieve on the LMSYS Chatbot Arena leaderboard in this report?",
            "expected_answer": "Abstain: Chatbot Arena is not mentioned or reported in this paper.",
            "evidence": "Verified absent across all 154 pages ('Chatbot Arena' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v3_unans_2",
            "category": "unanswerable",
            "question": "What is Gemini 1.5 Pro's score on the MT-Bench benchmark in this technical report?",
            "expected_answer": "Abstain: MT-Bench is not evaluated or mentioned in this report.",
            "evidence": "Verified absent across all 154 pages ('MT-Bench' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v3_unans_3",
            "category": "unanswerable",
            "question": "What strict prompt-level accuracy does Gemini 1.5 Pro achieve on Google's IFEval benchmark in Table 13?",
            "expected_answer": "Abstain: IFEval is not mentioned in the report (Table 13 evaluates internal 1326/406 instruction-following sets).",
            "evidence": "Verified absent across all 154 pages ('IFEval' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v3_unans_4",
            "category": "unanswerable",
            "question": "What is Gemini 1.5 Pro's score on MMMU-Pro reported in Table 18?",
            "expected_answer": "Abstain: MMMU-Pro is not reported (Table 18 only reports MMMU val).",
            "evidence": "Verified absent across all 154 pages ('MMMU-Pro' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v3_unans_5",
            "category": "unanswerable",
            "question": "What accuracy does Gemini 1.5 Flash achieve on OpenAI's SimpleQA benchmark in this paper?",
            "expected_answer": "Abstain: SimpleQA is not evaluated or mentioned in this paper.",
            "evidence": "Verified absent across all 154 pages ('SimpleQA' = 0 hits).",
            "pages": [],
        },
        {
            "id": "v3_unans_6",
            "category": "unanswerable",
            "question": "What is Gemini 1.5 Pro's pass@1 score on BigCodeBench in Table 11?",
            "expected_answer": "Abstain: BigCodeBench is not reported in Table 11 or anywhere in the paper.",
            "evidence": "Verified absent across all 154 pages ('BigCodeBench' = 0 hits).",
            "pages": [],
        },
    ]

    data = {"dev": dev, "test": test_v3}
    BENCHMARK_V3_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data


if __name__ == "__main__":
    build_benchmark_v3()
    print(json.dumps(validate_benchmark(BENCHMARK_V3_PATH), indent=2))
