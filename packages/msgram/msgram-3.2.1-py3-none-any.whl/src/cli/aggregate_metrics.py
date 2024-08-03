import os
import json

from src.cli.utils import print_error, print_info

metrics = {}
metrics["sonar"] = [
    "tests",
    "test_failures",
    "test_errors",
    "coverage",
    "test_execution_time",
    "functions",
    "complexity",
    "comment_lines_density",
    "duplicated_lines_density",
]

metrics["github"] = [
    "resolved_issues",
    "total_issues",
    "sum_ci_feedback_times",
    "total_builds",
]

measures = {}
measures["sonar"] = [
    "passed_tests",
    "test_builds",
    "test_errors",
    "test_coverage",
    "non_complex_file_density",
    "commented_file_density",
    "duplication_absense",
]

measures["github"] = ["team_throughput", "ci_feedback_time"]


def should_process_sonar_metrics(config):
    for characteristic in config.get("characteristics", []):
        for subcharacteristic in characteristic.get("subcharacteristics", []):
            for measure in subcharacteristic.get("measures", []):
                if measure.get("key") in measures["sonar"]:
                    return True
    return False


def should_process_github_metrics(config):
    for characteristic in config.get("characteristics", []):
        for subcharacteristic in characteristic.get("subcharacteristics", []):
            for measure in subcharacteristic.get("measures", []):
                if measure.get("key") in measures["github"]:
                    return True
    return False


def read_msgram(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except IsADirectoryError as e:
        print_error(f"> [red] Error: {e}")
        return False
    except FileNotFoundError as e:
        print_error(f"> [red] Error: {e}")
        return False


def list_msgram_files(folder_path):
    try:
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"{folder_path} is not a directory.")

        msgram_files = [
            file for file in os.listdir(folder_path) if file.endswith(".msgram")
        ]
        return msgram_files

    except NotADirectoryError as e:
        print_error(f"> [red] Error: {e}")
        return False


def save_metrics(file_name, metrics):
    directory = os.path.dirname(file_name)

    os.makedirs(directory, exist_ok=True)

    output_file_path = os.path.join(
        directory, os.path.basename(file_name).replace(".msgram", ".metrics")
    )
    with open(output_file_path, "w") as output_file:
        json.dump(metrics, output_file, indent=2)

    print_info(f"> [blue] Metrics saved to: {output_file_path}\n")


def process_sonar_metrics(folder_path, msgram_files, github_files):
    processed_files = []

    for file in msgram_files:
        if file not in github_files:
            print_info(f"> [blue] Processing {file}")
            sonar_metrics_dict = read_msgram(os.path.join(folder_path, file))

            if not sonar_metrics_dict:
                print_error(f"> [red] Error to read sonar metrics in: {folder_path}\n")
                return False

            processed_files.append((file, sonar_metrics_dict))

    return processed_files


def process_github_metrics(folder_path, github_files, metrics):
    if not github_files:
        print_error(f"> [red] GitHub files not found in the directory: {folder_path}\n")
        return False

    print_info(f"> [blue] GitHub metrics found in: {folder_path}\n")

    github_metrics_list = []

    for github_file_name in github_files:
        github_file_path = os.path.join(folder_path, github_file_name)
        github_file_content = read_msgram(github_file_path)

        if not github_file_content:
            print_error(
                f"> [red] Error to read github metrics in: {github_file_path}\n"
            )
            continue

        github_key = next(iter(github_file_content.keys() - metrics["sonar"]), "")

        github_metrics = [
            {
                "metric": metric,
                "value": next(
                    (
                        m["value"]
                        for m in github_file_content[github_key]
                        if m["metric"] == metric
                    ),
                    None,
                ),
            }
            for metric in metrics["github"]
        ]

        github_metrics_list.append((github_file_name, github_metrics))

    return github_metrics_list


def find_common_part(sonar_filename, github_result):
    sonar_filename_root, _ = os.path.splitext(sonar_filename)

    sonar_parts = sonar_filename_root.split("-")
    if len(sonar_parts) >= 7:
        sonar_key = "-".join(sonar_parts[:7])

        for github_filename, github_metrics in github_result:
            github_filename_root, _ = os.path.splitext(github_filename)

            if sonar_key in github_filename_root:
                return github_metrics

    return False


def aggregate_metrics(folder_path, config: json):
    msgram_files = list_msgram_files(folder_path)

    if not msgram_files:
        print_error("> [red]Error: Can not read msgram files in provided directory")
        return False

    github_files = [file for file in msgram_files if file.startswith("github_")]

    file_content = {}

    sonar_result = []
    github_result = []

    have_metrics = False

    config_has_github = should_process_github_metrics(config)

    if config_has_github:
        github_result = process_github_metrics(folder_path, github_files, metrics)

        if not github_result:
            print_error("> [red]Error: Unexpected result from process_github_metrics")
            return False

        have_metrics = True

    if should_process_sonar_metrics(config):
        sonar_result = process_sonar_metrics(folder_path, msgram_files, github_files)

        if not sonar_result:
            print_error("> [red]Error: Unexpected result from process_sonar_metrics")
            return False

        have_metrics = True

    if not have_metrics:
        print_error("> [red]Error: No metrics where found in the .msgram files")
        return False

    for sonar_filename, file_content in sonar_result:
        github_metrics = find_common_part(sonar_filename, github_result)

        if github_metrics:
            file_content["github_metrics"] = github_metrics
        elif config_has_github:
            print_error(
                f"> [red]Error: The configuration provided by the user requires github metrics\n"
                f"  but there was not found github metrics associated with the file:\n"
                f"  {sonar_filename}"
            )

            return False

        save_metrics(os.path.join(folder_path, sonar_filename), file_content)

    return True
