# AnalogCoder: Analog Circuit Design via Training-Free Code Generation

Analog circuit design is a significant task in modern chip technology, focusing on selecting component types, connectivity, and parameters to ensure proper circuit functionality. Despite advances made by Large Language Models (LLMs) in digital circuit design, the complexity and scarcity of data in analog circuitry pose significant challenges. To mitigate these issues, we introduce AnalogCoder, the first training-free LLM agent for designing analog circuits that converts tasks into Python code generation. This approach has several advantages. Firstly, AnalogCoder features a feedback-enhanced flow with crafted domain-specific prompts, enabling effective and automated design of analog circuits with a high success rate. Secondly, it proposes a circuit skill library to archive successful designs as reusable modular sub-circuits, simplifying composite circuit creation. Thirdly, extensive testing on a custom-designed benchmark of 24 analog circuit design tasks of varying difficulty shows that AnalogCoder successfully designed 19 circuits, outperforming existing methods. We believe AnalogCoder can significantly improve the labor-intensive chip design process, enabling non-experts to efficiently design analog circuits.

In this repo, we provide AnalogCoder codes and benchmark.

# Installation
AnalogCoder requires Python ≥ 3.10, PySpice ≥ 1.5, and openai >= 1.16.1. 

## Python Install
```
git clone https://github.com/anonyanalog/AnalogCoder
conda env create -f environment.yml
conda activate analog
```



# Quick Start
You can directly run the following code for quick start.
```
python gpt_run.py --task_id=1 --api_key="[OPENAI_API]" --num_per_task=1
```
which will generate one circuit based on task 1.