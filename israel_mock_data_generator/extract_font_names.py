import subprocess


def main(pdf_file_path):
    command = ['dumppdf.py', '-a', '-t', pdf_file_path]
    output = subprocess.check_output(command, text=True)
    last_line = None
    for line in output.splitlines():
        if last_line and 'FontName' in last_line:
            print(line)
        last_line = line
