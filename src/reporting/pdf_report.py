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
    """
    Adds a large, non-overlapping placeholder box for analysis that is
    roughly 1/3 of the page high.
    """
    pdf.ln(10)
    y_before = pdf.get_y()
    
    # Define a large, fixed height for the analysis box
    box_height = 80 # mm

    # If the box would run off the page, start a new one.
    if y_before + box_height > (pdf.h - pdf.b_margin):
        pdf.add_page()
        y_before = pdf.get_y()

    pdf.set_font('Arial', 'I', 10)
    # Draw the box and add placeholder text
    pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin, 5, "[Enter your summary and analysis here...]", 1, 'L')
    
    # After drawing, set the Y position to be exactly below where the box should end.
    # This prevents content from overlapping.
    pdf.set_y(y_before + box_height)
    pdf.set_font('Arial', '', 12)


def generate_pdf_report(all_results, summary_chart_path):
    """Generates a multi-page PDF report summarizing all simulation runs."""
    pdf = PDF()
    
    # --- Title Page (Combined Summary) ---
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 15, 'Simulation Summary Report', 0, 1, 'C')
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Scenario Performance Overview', 0, 1, 'L')
    pdf.set_font('Arial', 'B', 10)
    col_width = pdf.w / 5.5
    pdf.cell(col_width * 2, 10, 'Scenario Name', 1, 0, 'C')
    pdf.cell(col_width, 10, 'Meta Score', 1, 0, 'C')
    pdf.cell(col_width, 10, 'Functionality', 1, 0, 'C')
    pdf.cell(col_width, 10, 'Sustainability', 1, 1, 'C')
    
    pdf.set_font('Arial', '', 10)
    for res in all_results:
        pdf.cell(col_width * 2, 10, res['scenario_name'], 1, 0)
        pdf.cell(col_width, 10, f"{res['meta_score']:.3f}", 1, 0, 'C')
        pdf.cell(col_width, 10, f"{res['overall_scores']['Functionality']:.3f}", 1, 0, 'C')
        pdf.cell(col_width, 10, f"{res['overall_scores']['Sustainability']:.3f}", 1, 1, 'C')

    pdf.ln(5)
    pdf.image(summary_chart_path, x=10, w=pdf.w - 20)
    add_summary_placeholder(pdf)

    # --- Detailed Pages for Each Scenario ---
    for res in all_results:
        scenario_name = res['scenario_name']
        safe_name = scenario_name.replace(' ', '_').replace('/', '_')
        
        # --- Page 1: Design Image and Summary ---
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"Design Variation for: {scenario_name}", 0, 1, 'C')
        image_path = res['config'].get('image_path')
        if image_path and os.path.exists(image_path):
            pdf.image(image_path, x=10, y=30, w=pdf.w - 20)
            pdf.set_y(150) # Position cursor below the image
        else:
            pdf.set_font('Arial', 'I', 12)
            pdf.set_xy(10, 30)
            pdf.cell(pdf.w - 20, 20, f"[Image not found at path: {image_path}]", 1, 1, 'C')
            pdf.set_y(60)
        add_summary_placeholder(pdf)

        # --- Page 2: Domain Scores Chart ---
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"Detailed Domain Scores for: {scenario_name}", 0, 1, 'C')
        pdf.image(f"detailed_scores_{safe_name}.png", x=10, y=30, w=pdf.w - 20)
        
        # --- Page 3: Network Graph ---
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"Network Graph for: {scenario_name}", 0, 1, 'C')
        pdf.image(f"network_{safe_name}.png", x=10, y=30, w=pdf.w - 20)

        # --- Page 4: Input Attributes Table ---
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, f"Input Attributes for: {scenario_name}", 0, 1, 'C')
        pdf.ln(5)
        
        line_height = pdf.font_size * 2.5
        col_width_node = 60
        col_width_attr = pdf.w - pdf.l_margin - pdf.r_margin - col_width_node
        
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_width_node, line_height, 'Node ID', 1, 0, 'C')
        pdf.cell(col_width_attr, line_height, 'Attributes', 1, 1, 'C')
        pdf.set_font('Arial', '', 8)

        for node_id, state in sorted(res['node_states'].items()):
            if state['attributes']:
                y_start = pdf.get_y()
                pdf.multi_cell(col_width_node, line_height, node_id, 1, 'L')
                pdf.set_xy(pdf.l_margin + col_width_node, y_start)
                pdf.multi_cell(col_width_attr, line_height, str(state['attributes']), 1, 'L')
        
    filename = "Simulation_Report.pdf"
    pdf.output(filename)
    print(f"\nGenerated final PDF report: {filename}")
