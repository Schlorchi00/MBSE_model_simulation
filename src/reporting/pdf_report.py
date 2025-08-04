from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'MBSE Dynamic Network Simulation Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def add_summary_placeholder(pdf):
    pdf.ln(10)
    y_before = pdf.get_y()
    box_height = 80
    if y_before + box_height > (pdf.h - pdf.b_margin):
        pdf.add_page()
    pdf.set_font('Arial', 'I', 10)
    pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin, 5, "[Enter your summary and analysis here...]", 1, 'L')
    pdf.set_y(y_before + box_height)
    pdf.set_font('Arial', '', 12)

def generate_pdf_report(base_design_results, summary_chart_path, weighting_study_results, weighting_chart_path):
    """Generates a multi-page PDF report summarizing all simulation runs."""
    pdf = PDF()
    
    # --- Title Page with Base Design Comparison ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 15, 'Part 1: Base Design Concept Comparison', 0, 1, 'C')
    pdf.image(summary_chart_path, x=10, w=pdf.w - 20)
    add_summary_placeholder(pdf)
    
    # --- Detailed Pages for Each Base Design (Balanced Weights) ---
    for res in base_design_results:
        scenario_name = res['scenario_name']
        safe_name = scenario_name.replace(' ', '_').replace('/', '_')
        
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 15, f"Detailed Analysis for: {scenario_name}", 0, 1, 'C')
        
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"Design Variation for: {scenario_name}", 0, 1, 'C')
        image_path = res['config'].get('image_path')
        if image_path and os.path.exists(image_path):
            pdf.image(image_path, x=10, y=30, w=pdf.w - 20)
        else:
            pdf.set_font('Arial', 'I', 12)
            pdf.set_xy(10, 30)
            pdf.cell(pdf.w - 20, 20, f"[Image not found at path: {image_path}]", 1, 1, 'C')
            
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"Detailed Domain Scores for: {scenario_name}", 0, 1, 'C')
        pdf.image(f"detailed_scores_{safe_name}.png", x=10, y=30, w=pdf.w - 20)
        
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"Network Graph for: {scenario_name}", 0, 1, 'C')
        pdf.image(f"network_{safe_name}.png", x=10, y=30, w=pdf.w - 20)

    # --- New Section for Weighting Analysis ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 15, 'Part 2: Weighting Strategy Uncertainty Analysis', 0, 1, 'C')
    pdf.image(weighting_chart_path, x=10, w=pdf.w - 20)
    add_summary_placeholder(pdf)
        
    filename = "Simulation_Report.pdf"
    pdf.output(filename)
    print(f"\nGenerated final PDF report: {filename}")