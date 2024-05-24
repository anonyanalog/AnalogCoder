# AnalogCoder: Analog Circuit Design via Training-Free Code Generation

<p align="center">
  <img src="AnalogCoder.png" alt="alt text"width="200">
</p>

Analog circuit design is a significant task in modern chip technology, focusing on selecting component types, connectivity, and parameters to ensure proper circuit functionality. Despite advances made by Large Language Models (LLMs) in digital circuit design, the complexity and scarcity of data in analog circuitry pose significant challenges. To mitigate these issues, we introduce AnalogCoder, the first training-free LLM agent for designing analog circuits that converts tasks into Python code generation. This approach has several advantages. Firstly, AnalogCoder features a feedback-enhanced flow with crafted domain-specific prompts, enabling effective and automated design of analog circuits with a high success rate. Secondly, it proposes a circuit skill library to archive successful designs as reusable modular sub-circuits, simplifying composite circuit creation. Thirdly, extensive testing on a custom-designed benchmark of 24 analog circuit design tasks of varying difficulty shows that AnalogCoder successfully designed 20 circuits, outperforming existing methods. We believe AnalogCoder can significantly improve the labor-intensive chip design process, enabling non-experts to efficiently design analog circuits.

In this repo, we provide AnalogCoder codes and benchmark.

# Installation
AnalogCoder requires Python ≥ 3.10, PySpice ≥ 1.5, and openai >= 1.16.1. 

## Python Install
```
git clone https://github.com/anonyanalog/AnalogCoder
conda env create -f environment.yml
conda activate analog
```

## Environment Check
To ensure the current environment is functional, the following tests can be performed:

```
cd sample_design
python test_all_sample_design.py
```

When the program finishes running, if `All tasks passed` is displayed, it indicates that the environment is normal.

Otherwise, it will display `Please check your environment and try again`. It means you should check the configuration of the current Python environment, especially the settings related to PySpice.





# Quick Start
You can directly run the following code for quick start.
```
python gpt_run.py --task_id=1 --api_key="[OPENAI_API]" --num_per_task=1
```
which will generate one circuit based on task 1.

# Full Tutorial
1. Design basic circuits. 

For circuits 1-15 are basic circuits which can be designed by AnalogCoder directly.

```
for task_id in {1..15}
do
   python run_gpt.py --task_id=$task_id --api_key="[OPENAI_API]" --num_per_task=15 --model=gpt-4o
done
```

All the generated circuits are saved in directory ```gpt4o/```.

2. Build circuit tool library. (Optional)

We already provided a circuit tool library in directory ```subcircuit_lib```.
You can also build a new library based on the generated basic circuits.
```
python write_all_library.py
```

3. Design composite circuits.
For circuits 16-24, they are composite circuits. They can be more easily designed with the circuit tool library.
```
for task_id in {16..24}
do
   python run_gpt.py --task_id=$task_id --api_key="[OPENAI_API]" --num_per_task=15 --model=gpt-4o --skill --retrieval
done
```
The argument *skill* means using the circuit tool library.

The argument *retrieval* means using LLM to retrieve tools from the library first.

# Benchmark
- Task descriptions are in `problem_set.tsv`.
- Sample circuits are in directory `sample_design`.
- Test-benches are in directory `problem_check`.