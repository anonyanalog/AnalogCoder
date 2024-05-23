import os
import subprocess
import pandas as pd
import math


data_path = 'problem_set.tsv'
df = pd.read_csv(data_path, delimiter='\t')

template = '''from PySpice.Unit import *
from PySpice.Spice.Netlist import SubCircuitFactory
'''


opmap_phase_template = '''output_voltage_phase = np.angle(output_voltage2, deg=True)
print(f"Phase of Vin at 100 Hz: {output_voltage_phase:.0f} degree.")
'''

amplifier_phase_template = '''output_voltage_phase = np.angle(output_voltage, deg=True)
print(f"Phase of Vin at 100 Hz: {output_voltage_phase:.0f} degree.")
'''


def write_phase_check(check_file_path, extra_check_file_path, task_type):
    check_file = open(check_file_path, "r")
    extra_check_code = ""
    for line in check_file.readlines():
        if line.startswith("import sys"):
            if task_type == "Amplifier":
                extra_check_code += amplifier_phase_template
            elif task_type == "Opamp":
                extra_check_code += opmap_phase_template
        extra_check_code += line
    with open(extra_check_file_path, "w") as f:
        f.write(extra_check_code)


def get_bias_voltage(code_path, node):
    print("code_path", code_path)
    print("node", node)
    op_file_path = code_path.replace("_success.py", "_op.txt")
    print("op_file_path", op_file_path)
    with open(op_file_path, "r") as f:
        for line in f.readlines():
            if line.lower().startswith(node):
                return float(line.split("\t")[1])

def generate_lib(code_path, task_id):
    code = template + "\n"
    submodule_name = df.loc[df['Id'] == task_id, 'Submodule Name'].values[0]
    code += f"class {submodule_name}(SubCircuitFactory):\n"
    inputs = df.loc[df['Id'] == task_id, 'Input'].values[0]
    outputs = df.loc[df['Id'] == task_id, 'Output'].values[0]
    code += f"\tNAME = ('" + submodule_name + "')\n"
    code += f"\tNODES = ("
    input_set = set()
    for input in inputs.split(","):
        input = input.strip()
        if "bias" not in input.lower():
            input_set.add(input.lower())
        if "in" not in input.lower() and "ref" not in input.lower():
            continue
        if code.endswith("("):
            code += f"'{input}'"
        else:
            code += f", '{input}'"
    print("input_set", input_set)
    for output in outputs.split(","):
        output = output.strip()
        if "out" not in output.lower() or "voutp" in output.lower():
            continue
        print("LAIYAO output", output)
        if code.endswith("("):
            code += f"'{output}'"
        else:
            code += f", '{output}'"
    code += ")\n"

    code+="\tdef __init__(self):\n"
    code+="\t\tsuper().__init__()\n"
    bias_voltage = 0
    with open(code_path, "r") as f:
        start = 0
        for line in f.readlines():
            if line.startswith("circuit = Circuit("):
                start = 1
                continue
            if start == 0:
                continue
            if line.startswith("circuit.V"):
                print(line)
                parts = line.split(",")
                print(parts)                
                if len(parts) > 2 and parts[1].strip()[1:-1].lower() in input_set:
                    bias_voltage = get_bias_voltage(code_path, parts[1].strip()[1:-1].lower())
                    continue
            if line.startswith("simulator = circuit.simulator()"):
                break
            if line.startswith("# Analysis Part"):
                break
            code += "\t\t" + line
    code = code.replace("circuit.", "self.")
    if not os.path.exists("subcircuit_lib"):
        os.mkdir("subcircuit_lib")
    output_file_path = f"subcircuit_lib/p{task_id}_lib.py"
    with open(output_file_path, "w") as f:
        f.write(code)
    return bias_voltage


def output_retrieval_prompt(output_df):
    retrieval_template = open("retrieval_prompt_template.md", "r").read()
    table_content = "| Id | Type | Circuit | Gain (dB) | Common Mode Gain (dB) | # of inputs | # of outputs | Input Phase |\n"
    table_content += "| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    for i, (index, row) in enumerate(output_df.iterrows()):
        input_string = df.loc[df['Id'] == i, 'Input'].item()
        output_string = df.loc[df['Id'] == i, 'Output'].item()
        circuit = df.loc[df['Id'] == i, 'Circuit'].item()
        if row['Type'] == "CurrentMirror":
            num_of_inputs = 1
            num_of_outputs = 1
        else:
            num_of_inputs = input_string.lower().count('vin')
            num_of_outputs = output_string.lower().count('vout')
        if row['Type'] == "Amplifier":
            vin_phase = row['Vin(n) Phase']
        elif row['Type'] == "Opamp":
            vin_phase = "non-inverting, inverting"
        else:
            vin_phase = "NA"
        if row['Av (dB)'] == 'NA':
            gain = 'NA'
        else:
            gain = f"{float(row['Av (dB)']):.2f}"
        if row['Com Av (dB)'] == 'NA':
            com_gain = 'NA'
        else:
            com_gain = f"{float(row['Com Av (dB)']):.2f}"
        table_content += f"| {row['Id']} | {row['Type']} | {circuit} | {gain} | {com_gain} | {num_of_inputs} | {num_of_outputs} | {vin_phase} |\n"

    retrieval_template = retrieval_template.replace("[TABLE]", table_content)
    with open("retrieval_prompt.md", "w") as f:
        f.write(retrieval_template)

def work():
    output_df = pd.DataFrame(columns=['Id', 'Type', 'Av (dB)', 'Com Av (dB)', 'Vin(n) Phase', 'Voltage Bias'])
    flog = open("write_all_lib_log.txt", "w")
    for task_id in range(1, 16):
        task_type = df.loc[df['Id'] == task_id, 'Type'].values[0]
        print("task_type", task_type)
        best_av = 0
        best_com_av = 0
        best_phase = None
        for model in ['gpt3p5', 'gpt4', 'gpt4o']:
            base_dir = f"{model}/p{task_id}"
            if not os.path.exists(base_dir):
                continue
            for it in os.listdir(base_dir):
                if not os.path.isdir(os.path.join(base_dir, it)):
                    continue
                for file in os.listdir(os.path.join(base_dir, it)):
                    if not file.endswith("_success.py"):
                        continue
                    print("file", file)
                    check_file_path = os.path.join(base_dir, it, file.replace("_success.py", "_check.py"))
                    if task_type == "Amplifier" or task_type == "Opamp":
                        extra_check_file_path = check_file_path.replace("_check.py", "_extra_check.py")
                        write_phase_check(check_file_path, extra_check_file_path, task_type)
                        result = subprocess.run(["python", "-u", extra_check_file_path], check=True, text=True, 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    else:
                        result = subprocess.run(["python", "-u", check_file_path], check=True, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    if task_type == "Amplifier":
                        for line in result.stdout.split("\n"):
                            if line.startswith("Voltage Gain"):
                                av = float(line.split(":")[-1].strip())
                            if line.startswith("Phase"):
                                phase = int(line.split(" ")[-2].strip())
                        if av > best_av and av <= 1e4:
                            best_av = av
                            best_code_path = check_file_path.replace("_check.py", "_success.py")
                            best_phase = phase
                        flog.write("{}\t{}\t{}\t{}\t{}\n".format(task_id, check_file_path, task_type, av, phase))
                    elif task_type == "Opamp":
                        for line in result.stdout.split("\n"):
                            if line.startswith("Common-Mode Gain"):
                                com_av = float(line.split(":")[-1].strip())
                            elif line.startswith("Differential-Mode Gain"):
                                av = float(line.split(":")[-1].strip())
                            elif line.startswith("Phase"):
                                phase = int(line.split(" ")[-2].strip())
                        if abs(phase) == 180:
                            phase = 0
                        elif phase == 0:
                            phase = 180
                        elif phase == 90 or phase == -90:
                            phase = -phase
                        if av > best_av:
                            best_av = av
                            best_com_av = com_av
                            best_code_path = check_file_path.replace("_check.py", "_success.py")
                            best_phase = phase
                        flog.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(task_id, check_file_path, task_type, av, com_av, phase))
                    else:
                        best_code_path = check_file_path.replace("_check.py", "_success.py")
        print("task_id", task_id)
        print("best_av", best_av)
        print("best_com_av", best_com_av)
        print("best_code_path", best_code_path)
        print("best_phase", best_phase)
        bias_voltage = generate_lib(best_code_path, task_id)
        assert isinstance(output_df, pd.DataFrame), "output_df is not a pandas DataFrame"
        
        if best_phase == 180 or best_phase == -180:
            phase_char = "inverting"
        elif best_phase == 0:
            phase_char = "non-inverting"
        elif best_phase == 90 or best_phase == -90:
            phase_char = f"{best_phase} degree"
        elif task_type == "Inverter":
            phase_char = "inverting"
        else:
            phase_char = "NA"
        av_db = "NA"
        if best_av != 0:
            av_db = 20*math.log10(best_av)
        com_av_db = "NA"
        if best_com_av != 0:
            com_av_db = 20*math.log10(best_com_av)
        new_row = {'Id': task_id, 'Type': task_type, 'Av (dB)': av_db, 'Com Av (dB)': com_av_db, 'Vin(n) Phase': phase_char, 'Voltage Bias': bias_voltage}
        output_df = pd.concat([output_df, pd.DataFrame([new_row])], ignore_index=True)
    output_df.to_csv("lib_info.tsv", sep='\t', index=False)
    output_retrieval_prompt(output_df)
    flog.close()

def main():
    work()


if __name__ == "__main__":
    work()
