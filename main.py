import subprocess
import os

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(current_dir, 'scripts')

    # Descargar datos
    subprocess.run(['python', os.path.join(scripts_dir, 'download_data.py')])

    # Entrenar el modelo
    subprocess.run(['python', os.path.join(scripts_dir, 'train_model.py')])

    # Analizar datos y generar gráficos
    subprocess.run(['python', os.path.join(scripts_dir, 'analyze_and_plot.py')])

    # Generar informe PDF
    subprocess.run(['python', os.path.join(scripts_dir, 'generate_report.py')])

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Ejecutar el script para descargar datos
    os.system(f'python {os.path.join(current_dir, "scripts/download_data.py")}')

    # Ejecutar el script para entrenar el modelo
    os.system(f'python {os.path.join(current_dir, "scripts/train_model.py")}')
    # Ejecutar el script para analizar y graficar los datos de USA
    os.system(f'python {os.path.join(current_dir, "scripts/analyze_and_plot.py")}')

    # Ejecutar el script para generar el informe
    os.system(f'python {os.path.join(current_dir, "scripts/generate_report.py")}')