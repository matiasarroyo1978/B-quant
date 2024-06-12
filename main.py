import subprocess
import os

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(current_dir, 'scripts')

    subprocess.run(['python', os.path.join(scripts_dir, 'download_data.py')])
    subprocess.run(['python', os.path.join(scripts_dir, 'train_model.py')])
    subprocess.run(['python', os.path.join(scripts_dir, 'analyze_and_plot.py')])
    subprocess.run(['python', os.path.join(scripts_dir, 'generate_report.py')])

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f'python {os.path.join(current_dir, "scripts/download_data.py")}')
    os.system(f'python {os.path.join(current_dir, "scripts/train_model.py")}')
    os.system(f'python {os.path.join(current_dir, "scripts/analyze_and_plot.py")}')
    os.system(f'python {os.path.join(current_dir, "scripts/generate_report.py")}')