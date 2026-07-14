import os
import pandas as pd

def generate_excel_workbook():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    output_path = os.path.join(script_dir, "Quicksort_Benchmark_Data.xlsx")
    
    # Load raw CSV files
    csv_files = {
        "Random Distribution": "random_results.csv",
        "Ascending Distribution": "ascending_results.csv",
        "Descending Distribution": "descending_results.csv"
    }
    
    # Write to Excel using xlsxwriter for formatting
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats for headers and data
        header_format = workbook.add_format({
            'bold': True,
            'font_name': 'Segoe UI',
            'font_size': 11,
            'font_color': 'white',
            'bg_color': '#1F4E79',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        
        number_format = workbook.add_format({
            'font_name': 'Segoe UI',
            'font_size': 10,
            'num_format': '#,##0.0',
            'align': 'right'
        })
        
        size_format = workbook.add_format({
            'font_name': 'Segoe UI',
            'font_size': 10,
            'align': 'center'
        })
        
        for sheet_name, filename in csv_files.items():
            csv_path = os.path.join(data_dir, filename)
            df = pd.read_csv(csv_path)
            
            # Write data to sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0)
            
            worksheet = writer.sheets[sheet_name]
            
            # Show gridlines explicitly
            worksheet.hide_gridlines(2)
            
            # Freeze the top row so headers stick when scrolling
            worksheet.freeze_panes(1, 0)
            
            # Format the header row
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                
            # Set columns widths and alignment
            worksheet.set_column('A:A', 15, size_format)  # Size column
            worksheet.set_column('B:E', 15, number_format) # Time columns (First, Last, Middle, Random)
            
            # Set row heights
            worksheet.set_row(0, 24) # Header row height
            
    print(f"Successfully generated formatted Excel workbook: {output_path}")

if __name__ == "__main__":
    generate_excel_workbook()
