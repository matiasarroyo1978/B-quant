import os
import joblib
import json
import fpdf

class PDFReport(fpdf.FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Investment Strategy Analysis Report', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_image(self, image_path):
        if os.path.exists(image_path):
            self.image(image_path, w=180)
        else:
            self.set_font('Arial', 'I', 12)
            self.cell(0, 10, 'Image not found: ' + image_path, 0, 1, 'C')
            self.ln(10)

def add_classification_report_table(pdf, report):
    pdf.set_font('Arial', 'B', 10)

    # Get all unique metric names (to handle missing metrics in some classes)
    all_metrics = set()
    for _, metrics in report.items():
        all_metrics.update(metrics.keys())

    # Header row
    for col in all_metrics:
        pdf.cell(40, 10, col, 1, 0, 'C')
    pdf.ln()

    # Data rows (handling missing metrics gracefully)
    for index, metrics in report.items():
        pdf.set_font('Arial', '', 10)
        pdf.cell(40, 10, index, 1, 0, 'C')
        for col in all_metrics:
            value = metrics.get(col, "N/A")  # Use "N/A" if metric is missing
            if isinstance(value, dict) and 'precision' in value:  # Handle nested dicts
                value = value['precision']  # Extract precision from support dict
            pdf.cell(40, 10, f"{value:.4f}", 1, 0, 'C')  # Format as float if possible
        pdf.ln()


def generate_report(results):
    pdf = PDFReport()
    pdf.add_page()

    pdf.chapter_title('1. Introduction')
    pdf.chapter_body('This report presents an analysis of investment strategies based on Value and Growth ETFs for the USA and Europe. The data was sourced from Yahoo Finance, and key indicators such as cumulative returns and RSI were calculated. Machine learning models were trained to predict future returns based on these indicators.')

    pdf.chapter_title('2. Data and Methods')
    pdf.chapter_body('Data was collected for the period from 2010 to 2024. The cumulative returns were calculated by compounding the daily returns, and the RSI was calculated using a 14-day window. Models used for prediction include RandomForest, LogisticRegression, and SVM.')

    pdf.chapter_title('3. Results')
    pdf.add_image('outputs/USA_analysis.png')
    pdf.chapter_body('Figure 1: Cumulative returns and RSI for the USA Value and Growth ETFs. The green line represents the combined strategy')
    pdf.add_image('outputs/EU_analysis.png')
    pdf.chapter_body('Figure 2: Cumulative returns and RSI for the European Value and Growth ETFs. Similar to the USA analysis, the combined strategy is represented by the green line.')

    pdf.chapter_title('4. Model Training and Prediction')
    pdf.add_image('results/model_performance.png')
    for result in results:
        model = result['model']
        accuracy = result['accuracy']
        report_dict = result['report']  # This is the JSON-like dict

        # Convert JSON-like dict back to nested dict (DataFrame is not needed here)
        report = {}
        for key, value in report_dict.items():
            report[key] = {k: v for k, v in value.items()} 

        pdf.chapter_body(f"{model} Model Accuracy: {accuracy * 100:.2f}%")
        pdf.chapter_body(f"Classification Report:")
        add_classification_report_table(pdf, report)

    pdf.chapter_title('5. Conclusion')
    pdf.chapter_body('The analysis shows that combining Value and Growth strategies can provide a diversified approach to investing. The use of technical indicators such as RSI, along with machine learning models, can enhance the decision-making process by providing predictive insights. Further research could involve testing additional models and expanding the feature set for improved accuracy.')

    pdf.chapter_title('6. Future Work')
    pdf.chapter_body('Future work could explore the use of more advanced machine learning models, such as ensemble methods or neural networks, to further improve prediction accuracy. Additionally, incorporating macroeconomic indicators and sentiment analysis from news data could provide a more holistic view of the market conditions.')

    # Save the PDF
    os.makedirs('reports', exist_ok=True)
    pdf.output('reports/investment_strategy_analysis_report.pdf')

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(current_dir, '../results/model_results.json')
    
    with open(results_path, 'r') as f:
        results = json.load(f)
    
    generate_report(results)

