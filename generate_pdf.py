import os
import csv
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setStrokeColor(colors.gray)
        self.setLineWidth(0.5)
        
        # We do not draw running headers on page 1 (cover / title page)
        if self._pageNumber > 1:
            # Running Header
            self.drawString(54, 755, "MD Mominul Islam — Quicksort Pivot Selection Analysis")
            self.line(54, 747, 612-54, 747)
            
            # Running Footer Line
            self.line(54, 45, 612-54, 45)
            
            # Running Footer Text
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(612 - 54, 32, page_text)
            self.drawString(54, 32, "Shahjalal University of Science and Technology — Department of CSE")
        else:
            # First page footer (no lines, just page number)
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(612 - 54, 32, page_text)
            self.drawString(54, 32, "Department of Computer Science and Engineering, SUST")
            
        self.restoreState()


def load_summarized_data(csv_path):
    """Loads CSV results and returns a summarized list of rows for the PDF table."""
    df = pd.read_csv(csv_path)
    # Select rows at sizes: 10, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000
    target_sizes = [10, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    sub_df = df[df['Size'].isin(target_sizes)].copy()
    
    # Format times: round to 2 decimal places and show in microseconds
    headers = ["Size (N)", "First (μs)", "Last (μs)", "Middle (μs)", "Random (μs)"]
    data = [headers]
    for _, row in sub_df.iterrows():
        data.append([
            f"{int(row['Size'])}",
            f"{row['First']:.1f}",
            f"{row['Last']:.1f}",
            f"{row['Middle']:.1f}",
            f"{row['Random']:.1f}"
        ])
    return data


def build_pdf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    plot_dir = os.path.join(script_dir, "plot")
    code_dir = os.path.join(script_dir, "code")
    
    pdf_filename = os.path.join(script_dir, "Quicksort_Assignment_Solutions.pdf")
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,  # 0.75 in
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom academic styles (using Times Roman)
    title_style = ParagraphStyle(
        'AcademicTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'AcademicSubtitle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=15
    )
    
    author_style = ParagraphStyle(
        'AcademicAuthor',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        spaceAfter=25
    )
    
    abstract_heading = ParagraphStyle(
        'AbstractHeading',
        parent=styles['Normal'],
        fontName='Times-BoldItalic',
        fontSize=10,
        leading=12,
        alignment=TA_JUSTIFY,
        spaceAfter=4,
        leftIndent=36,
        rightIndent=36
    )
    
    abstract_text = ParagraphStyle(
        'AbstractText',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9.5,
        leading=13,
        alignment=TA_JUSTIFY,
        spaceAfter=30,
        leftIndent=36,
        rightIndent=36
    )
    
    h1_style = ParagraphStyle(
        'AcademicH1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'AcademicH2',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        alignment=TA_LEFT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        firstLineIndent=18,
        spaceAfter=6
    )

    body_no_indent = ParagraphStyle(
        'AcademicBodyNoIndent',
        parent=body_style,
        firstLineIndent=0,
        spaceAfter=6
    )
    
    caption_style = ParagraphStyle(
        'FigureCaption',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=15,
        keepWithNext=True
    )
    
    code_style = ParagraphStyle(
        'CodeMonospace',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        alignment=TA_LEFT,
        spaceAfter=10
    )

    ref_style = ParagraphStyle(
        'AcademicReference',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=12,
        leftIndent=24,
        firstLineIndent=-24,
        spaceAfter=4
    )

    # Styles for tables
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=11,
        alignment=TA_CENTER
    )
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9,
        leading=11,
        alignment=TA_CENTER
    )
    
    # Booktabs table styling
    booktabs_style = TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.black),  # Top thick line
        ('LINEBELOW', (0, 0), (-1, 0), 0.8, colors.black),  # Header bottom line
        ('LINEBELOW', (0, -1), (-1, -1), 1.2, colors.black), # Table bottom line
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ])

    story = []
    
    # ------------------- TITLE & METADATA -------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("Experimental Performance Analysis of Quicksort Pivot Selection Strategies", title_style))
    story.append(Paragraph("Algorithm Design & Analysis (CSE-323) — Assignment 01", subtitle_style))
    
    author_info = """
    <b>MD Mominul Islam</b><br/>
    Registration No: 2024331022<br/>
    Department of Computer Science and Engineering<br/>
    Shahjalal University of Science and Technology, Sylhet, Bangladesh
    """
    story.append(Paragraph(author_info, author_style))
    
    # ------------------- ABSTRACT -------------------
    story.append(Paragraph("Abstract", abstract_heading))
    abstract_p = (
        "Quicksort remains a cornerstone of sorting algorithms due to its average-case O(N log N) complexity and "
        "low memory footprint. However, its performance is highly sensitive to the choice of the pivot element. "
        "Naïve pivot selections can cause the algorithm to degenerate into an O(N²) quadratic time complexity on "
        "pre-sorted inputs. This paper conducts a rigorous empirical investigation of four pivot selection strategies: "
        "First Element, Last Element, Middle Element, and Random Element. We benchmark these strategies using arrays "
        "ranging from 10 to 5,000 elements under three initial conditions: random, sorted ascending, and sorted descending. "
        "Our empirical findings confirm the theoretical predictions: First and Last Element strategies suffer catastrophic "
        "performance degradation to O(N²) on sorted arrays, whereas the Middle and Random Element strategies consistently "
        "maintain O(N log N) complexity. The C++ implementation utilizes C. A. R. Hoare's partitioning scheme with standard "
        "recursion, showing that a stack depth of up to 5,000 is safely within Windows' default stack limits."
    )
    story.append(Paragraph(abstract_p, abstract_text))
    
    # ------------------- SECTION 1: INTRODUCTION -------------------
    story.append(Paragraph("1. Introduction", h1_style))
    intro_1 = (
        "Sorting is a fundamental problem in computer science, and C. A. R. Hoare's Quicksort is widely regarded as one of "
        "the most efficient algorithms for general-purpose sorting. Utilizing a divide-and-conquer strategy, Quicksort "
        "partitions an array around a chosen 'pivot' element such that elements smaller than the pivot are placed to its "
        "left and larger elements to its right. The sub-arrays are then recursively sorted. While the average-case "
        "performance of Quicksort is O(N log N), its worst-case behavior is O(N²). This worst-case occurs when the partitioning "
        "is extremely unbalanced, resulting in sub-problems of size 0 and N-1."
    )
    story.append(Paragraph(intro_1, body_style))
    
    intro_2 = (
        "The primary factor determining partitioning balance is the pivot selection strategy. This study analyzes the performance "
        "implications of four common pivot selection methods. By observing their behavior on various input sizes and initial "
        "orderings, we gain insight into the practical risks associated with naïve implementations and the efficacy of algorithmic "
        "remedies, such as randomized pivot selection and middle-index partitioning."
    )
    story.append(Paragraph(intro_2, body_style))
    
    # ------------------- SECTION 2: PIVOT STRATEGIES -------------------
    story.append(Paragraph("2. Pivot Selection Strategies", h1_style))
    
    strat_intro = "We implemented and analyzed the following four pivot selection strategies:"
    story.append(Paragraph(strat_intro, body_style))
    
    strat_1 = (
        "<b>2.1 First Element:</b> This strategy selects the first element of the current sub-array (index <i>low</i>) as the pivot. "
        "While computationally trivial, it is highly vulnerable to sorted inputs, where it yields the worst-case O(N²) partition."
    )
    story.append(Paragraph(strat_1, body_style))

    strat_2 = (
        "<b>2.2 Last Element:</b> This strategy selects the last element of the sub-array (index <i>high</i>) as the pivot. "
        "Symmetric to the first-element strategy, it performs poorly on pre-sorted arrays, leading to O(N²) complexity."
    )
    story.append(Paragraph(strat_2, body_style))

    strat_3 = (
        "<b>2.3 Middle Element:</b> This strategy chooses the element at index <i>low + ⌊(high-low)/2⌋</i> as the pivot. "
        "By targeting the middle element, it naturally avoids the worst-case behavior on pre-sorted inputs, acting as an "
        "approximation of the median."
    )
    story.append(Paragraph(strat_3, body_style))

    strat_4 = (
        "<b>2.4 Random Element:</b> This strategy selects a pivot uniformly at random from the range [<i>low</i>, <i>high</i>]. "
        "It provides a strong probabilistic guarantee of O(N log N) sorting time, breaking the dependency between input data "
        "ordering and execution time."
    )
    story.append(Paragraph(strat_4, body_style))

    story.append(PageBreak()) # Clean page break for methodology and results
    
    # ------------------- SECTION 3: EMPIRICAL METHODOLOGY -------------------
    story.append(Paragraph("3. Empirical Methodology", h1_style))
    
    meth_1 = (
        "To evaluate the strategies, we developed a C++ benchmarking harness. For each array size $N$ from 10 to 5,000 "
        "with a step size of 10 (i.e. $N \\in \\{10, 20, 30, \\ldots, 5000\\}$), we "
        "generated three types of arrays: (a) random permutations, (b) sorted ascending, and (c) sorted descending. "
        "To ensure fair comparisons, identical copies of the initial array were passed to each sorting strategy. "
        "The execution time was recorded using <i>std::chrono::high_resolution_clock</i>, measuring only the sorting process "
        "and excluding array initialization or copying overhead. To minimize noise and environmental factors, each measurement "
        "was averaged over <i>m = 30</i> independent repetitions."
    )
    story.append(Paragraph(meth_1, body_style))

    story.append(Paragraph("3.1 System Specifications", h2_style))
    
    # System specifications table
    sys_data = [
        [Paragraph("<b>Hardware/Software Component</b>", table_header_style), Paragraph("<b>Specification Details</b>", table_header_style)],
        [Paragraph("Laptop Model", table_cell_style), Paragraph("ASUS TUF Gaming A15 (FA506NFR)", table_cell_style)],
        [Paragraph("Processor (CPU)", table_cell_style), Paragraph("AMD Ryzen 7 7435HS (Base 3.1 GHz, Boost up to 4.5 GHz)", table_cell_style)],
        [Paragraph("CPU Core Count", table_cell_style), Paragraph("8 Cores / 16 Threads", table_cell_style)],
        [Paragraph("Graphics Card (GPU)", table_cell_style), Paragraph("NVIDIA GeForce RTX 2050 (4 GB GDDR6)", table_cell_style)],
        [Paragraph("Memory (RAM)", table_cell_style), Paragraph("16 GB DDR5-5600 MHz", table_cell_style)],
        [Paragraph("Storage (SSD)", table_cell_style), Paragraph("512 GB NVMe PCIe Gen 4 SSD (WD PC SN740)", table_cell_style)],
        [Paragraph("Display", table_cell_style), Paragraph("15.6\" FHD (1920 x 1080), 144 Hz IPS", table_cell_style)],
        [Paragraph("Operating System", table_cell_style), Paragraph("Microsoft Windows 11 Home Single Language (64-bit)", table_cell_style)],
        [Paragraph("Compiler Suite", table_cell_style), Paragraph("GNU GCC Compiler (g++ 15.1.0 via MSYS2)", table_cell_style)],
        [Paragraph("Compiler Flags", table_cell_style), Paragraph("-O3 (Full Speed Optimization, Inline Functions)", table_cell_style)],
    ]
    sys_table = Table(sys_data, colWidths=[200, 300], hAlign='CENTER')
    sys_table.setStyle(booktabs_style)
    story.append(sys_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.2 Recursion Depth and Stack Space Analysis", h2_style))
    meth_2 = (
        "Standard recursive Quicksort has a worst-case recursion depth of O(N) when partitions are highly unbalanced. "
        "On pre-sorted arrays with $N = 5,000$, the First and Last pivot strategies yield a recursion depth of 5,000. "
        "Each recursive stack frame on a modern x86_64 compiler (like g++ under MSYS2) requires approximately 48 to 64 bytes "
        "to store parameters, return addresses, and local variables. For $N = 5,000$, this results in a total stack consumption "
        "of approximately 240 to 320 KB. Since the default stack allocation on Windows is 1 MB, the standard recursive "
        "implementation successfully completes sorting without stack overflow. This confirms that for the target maximum size of 5,000, "
        "standard recursion remains practically viable."
    )
    story.append(Paragraph(meth_2, body_style))

    # ------------------- SECTION 4: EXPERIMENTAL RESULTS -------------------
    story.append(Paragraph("4. Experimental Results", h1_style))
    
    results_intro = (
        "The compiled empirical measurements are presented below. Table 1, Table 2, and Table 3 detail a representative subset "
        "of the tested array sizes, while Figure 1, Figure 2, and Figure 3 depict the complete performance trajectories."
    )
    story.append(Paragraph(results_intro, body_style))
    
    # --- EXPERIMENT 1: RANDOM ARRAYS ---
    story.append(Paragraph("4.1 Experiment 1: Random Array Distribution", h2_style))
    
    # Load and insert Table 1
    t1_data_raw = load_summarized_data(os.path.join(data_dir, "random_results.csv"))
    t1_data = []
    for r_idx, row in enumerate(t1_data_raw):
        if r_idx == 0:
            t1_data.append([Paragraph(f"<b>{col}</b>", table_header_style) for col in row])
        else:
            t1_data.append([Paragraph(col, table_cell_style) for col in row])
    
    t1_table = Table(t1_data, colWidths=[100, 100, 100, 100, 100], hAlign='CENTER')
    t1_table.setStyle(booktabs_style)
    story.append(t1_table)
    story.append(Paragraph("Table 1: Average execution times (μs) for random array configurations.", caption_style))
    
    # Add Figure 1
    story.append(Spacer(1, 5))
    img1 = Image(os.path.join(plot_dir, "plot_random.png"), width=4.5*inch, height=3.0*inch)
    img1.hAlign = 'CENTER'
    story.append(img1)
    story.append(Paragraph("Figure 1: Quicksort performance trajectories on random arrays.", caption_style))

    story.append(PageBreak())

    # --- EXPERIMENT 2A: ASCENDING ARRAYS ---
    story.append(Paragraph("4.2 Experiment 2A: Pre-Sorted Ascending Array Distribution", h2_style))
    
    t2_data_raw = load_summarized_data(os.path.join(data_dir, "ascending_results.csv"))
    t2_data = []
    for r_idx, row in enumerate(t2_data_raw):
        if r_idx == 0:
            t2_data.append([Paragraph(f"<b>{col}</b>", table_header_style) for col in row])
        else:
            t2_data.append([Paragraph(col, table_cell_style) for col in row])
            
    t2_table = Table(t2_data, colWidths=[100, 100, 100, 100, 100], hAlign='CENTER')
    t2_table.setStyle(booktabs_style)
    story.append(t2_table)
    story.append(Paragraph("Table 2: Average execution times (μs) for pre-sorted ascending array configurations.", caption_style))
    
    story.append(Spacer(1, 5))
    img2 = Image(os.path.join(plot_dir, "plot_ascending.png"), width=4.5*inch, height=3.0*inch)
    img2.hAlign = 'CENTER'
    story.append(img2)
    story.append(Paragraph("Figure 2: Performance bifurcation on ascendingly sorted arrays (logarithmic scale).", caption_style))

    story.append(PageBreak())

    # --- EXPERIMENT 2B: DESCENDING ARRAYS ---
    story.append(Paragraph("4.3 Experiment 2B: Pre-Sorted Descending Array Distribution", h2_style))
    
    t3_data_raw = load_summarized_data(os.path.join(data_dir, "descending_results.csv"))
    t3_data = []
    for r_idx, row in enumerate(t3_data_raw):
        if r_idx == 0:
            t3_data.append([Paragraph(f"<b>{col}</b>", table_header_style) for col in row])
        else:
            t3_data.append([Paragraph(col, table_cell_style) for col in row])
            
    t3_table = Table(t3_data, colWidths=[100, 100, 100, 100, 100], hAlign='CENTER')
    t3_table.setStyle(booktabs_style)
    story.append(t3_table)
    story.append(Paragraph("Table 3: Average execution times (μs) for pre-sorted descending array configurations.", caption_style))
    
    story.append(Spacer(1, 5))
    img3 = Image(os.path.join(plot_dir, "plot_descending.png"), width=4.5*inch, height=3.0*inch)
    img3.hAlign = 'CENTER'
    story.append(img3)
    story.append(Paragraph("Figure 3: Performance bifurcation on descendingly sorted arrays (logarithmic scale).", caption_style))
    
    story.append(PageBreak())

    # ------------------- SECTION 5: THEORETICAL ANALYSIS -------------------
    story.append(Paragraph("5. Theoretical Analysis & Complexity", h1_style))
    
    theory_1 = (
        "The theoretical runtime of Quicksort is governed by the recurrence relation of the partitioning step. "
        "In the best case, the pivot divides the array exactly in half, leading to the recurrence relation: "
        "<i>T(N) = 2T(N/2) + O(N)</i>. According to the Master Theorem, this evaluates to <i>O(N log N)</i>. "
        "In the worst case, the pivot is either the smallest or largest element, leading to: "
        "<i>T(N) = T(N-1) + T(0) + O(N)</i>, which expands to a summation of <i>1 + 2 + ... + N</i>, evaluating to <i>O(N²)</i>."
    )
    story.append(Paragraph(theory_1, body_style))
    
    # Complexity Comparison Table
    comp_data = [
        [
            Paragraph("<b>Pivot Selection Strategy</b>", table_header_style), 
            Paragraph("<b>Best Case</b>", table_header_style), 
            Paragraph("<b>Average Case</b>", table_header_style), 
            Paragraph("<b>Worst Case</b>", table_header_style), 
            Paragraph("<b>Space (Worst)</b>", table_header_style)
        ],
        [Paragraph("First Element", table_cell_style), Paragraph("O(N log N)", table_cell_style), Paragraph("O(N log N)", table_cell_style), Paragraph("O(N²)", table_cell_style), Paragraph("O(N)*", table_cell_style)],
        [Paragraph("Last Element", table_cell_style), Paragraph("O(N log N)", table_cell_style), Paragraph("O(N log N)", table_cell_style), Paragraph("O(N²)", table_cell_style), Paragraph("O(N)*", table_cell_style)],
        [Paragraph("Middle Element", table_cell_style), Paragraph("O(N log N)", table_cell_style), Paragraph("O(N log N)", table_cell_style), Paragraph("O(N²)", table_cell_style), Paragraph("O(N)", table_cell_style)],
        [Paragraph("Random Element", table_cell_style), Paragraph("O(N log N)", table_cell_style), Paragraph("O(N log N)", table_cell_style), Paragraph("O(N²)‡", table_cell_style), Paragraph("O(N)", table_cell_style)],
    ]
    comp_table = Table(comp_data, colWidths=[120, 95, 95, 95, 95], hAlign='CENTER')
    comp_table.setStyle(booktabs_style)
    story.append(comp_table)
    story.append(Paragraph("Table 4: Theoretical complexity comparison of the four pivot selection strategies.<br/>"
                           "<i>* Space complexity is O(N) in the worst case due to standard recursion; average case is O(log N).</i><br/>"
                           "<i>‡ Probabilistically near-zero (infinitesimally small) chance of occurrence.</i>", caption_style))
    story.append(Spacer(1, 10))

    # ------------------- SECTION 6: DISCUSSION -------------------
    story.append(Paragraph("6. Discussion and Interpretation", h1_style))
    
    disc_1 = (
        "Our empirical data matches the theoretical models. "
        "As seen in Figure 1, when the input array is random, all four strategies exhibit nearly identical trajectories. "
        "At $N = 5,000$, all average runtimes reside within a similar order of magnitude, confirming that "
        "when elements are unordered, any pivot strategy has an equal probability of achieving a reasonably "
        "balanced partition. The slight overhead observed in the Random strategy is attributed to the cost of the "
        "pseudo-random number generator (PRNG) call at each partitioning step."
    )
    story.append(Paragraph(disc_1, body_style))

    disc_2 = (
        "However, on pre-sorted arrays (Figures 2 and 3), the strategies diverge dramatically. "
        "The First and Last Element strategies degrade immediately, with execution times growing by orders of magnitude "
        "compared to the Middle and Random strategies at $N = 5,000$. "
        "Because Hoare partitioning uses two converging pointers, selecting the first element of an "
        "ascending array as the pivot (which is the smallest element) causes the left pointer to stop immediately and the "
        "right pointer to scan all the way to the left, yielding an extremely unbalanced partition split of 1 and $N-1$. "
        "This results in $N$ partition steps, each scanning the remaining elements, verifying the quadratic O(N²) behavior."
    )
    story.append(Paragraph(disc_2, body_style))

    disc_3 = (
        "Conversely, the Middle Element strategy performs extremely well on sorted inputs. For ascending inputs at $N = 5,000$, "
        "it completes in under 100 μs. This is because the middle element of a sorted array is exactly its median, "
        "which produces a balanced split of $N/2$ at every level, representing the best-case behavior of Quicksort. "
        "It is important to note, however, that the theoretical worst-case complexity of the Middle Element strategy "
        "remains O(N²), since adversarial input sequences can be constructed to force unbalanced partitions. "
        "In practice, such pathological inputs are rare, and on common distributions (sorted, reverse-sorted, random), "
        "the Middle Element strategy exhibits O(N log N) performance. "
        "The Random strategy also performs well on sorted arrays, completing significantly faster than the First and Last "
        "strategies, as it breaks the input structure and avoids the bad partition path."
    )
    story.append(Paragraph(disc_3, body_style))
    
    # ------------------- SECTION 7: CONCLUSION -------------------
    story.append(Paragraph("7. Conclusion", h1_style))
    
    concl = (
        "This performance analysis highlights the importance of pivot selection in Quicksort. "
        "Naïve pivot strategies, like selecting the first or last element, are dangerous for production environments "
        "where sorted or partially sorted inputs are common. While the Middle Element strategy performs exceptionally "
        "well on sorted arrays, the Random Element strategy provides the most robust general defense against worst-case "
        "performance degradation, regardless of input structure. Finally, understanding stack allocation limits "
        "is key when standard recursive implementations are used on worst-case inputs."
    )
    story.append(Paragraph(concl, body_style))

    # ------------------- SECTION 8: REFERENCES -------------------
    story.append(Paragraph("8. References", h1_style))
    
    ref1 = (
        "[1] C. A. R. Hoare, \"Algorithm 64: Quicksort,\" <i>Communications of the ACM</i>, vol. 4, no. 7, p. 321, Jul. 1961."
    )
    story.append(Paragraph(ref1, ref_style))
    
    ref2 = (
        "[2] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, <i>Introduction to Algorithms</i>, 3rd ed. Cambridge, MA: MIT Press, 2009."
    )
    story.append(Paragraph(ref2, ref_style))
    
    ref3 = (
        "[3] R. Sedgewick, \"Implementing Quicksort Programs,\" <i>Communications of the ACM</i>, vol. 21, no. 10, pp. 847–857, Oct. 1978."
    )
    story.append(Paragraph(ref3, ref_style))

    story.append(PageBreak())

    # ------------------- APPENDIX: C++ SOURCE CODE -------------------
    story.append(Paragraph("Appendix: C++ Source Code", h1_style))
    story.append(Paragraph("The complete C++ source code used to generate the benchmark results is presented below. "
                           "The code features Hoare partitioning and standard recursion, styled as a VSCode code editor window with line numbers and syntax highlighting.", body_no_indent))
    story.append(Spacer(1, 10))
    
    # Width of the image in points. Page width is 612pt. Margin is 108pt total. Printable width is 504pt.
    # We use 470pt for a good fit.
    w = 470
    # Aspect ratios from actual rendered images: 885x1264, 897x928, 1004x907, 1196x823
    h1 = w * (1264 / 885)
    h2 = w * (928 / 897)
    h3 = w * (907 / 1004)
    h4 = w * (823 / 1196)
    
    # Part 1
    img1 = Image(os.path.join(code_dir, "code_vscode_1.png"), width=w, height=h1)
    img1.hAlign = 'CENTER'
    story.append(img1)
    
    # Part 2
    story.append(PageBreak())
    story.append(Paragraph("Appendix: C++ Source Code (Continued)", h1_style))
    story.append(Spacer(1, 10))
    img2 = Image(os.path.join(code_dir, "code_vscode_2.png"), width=w, height=h2)
    img2.hAlign = 'CENTER'
    story.append(img2)
    
    # Part 3
    story.append(PageBreak())
    story.append(Paragraph("Appendix: C++ Source Code (Continued)", h1_style))
    story.append(Spacer(1, 10))
    img3 = Image(os.path.join(code_dir, "code_vscode_3.png"), width=w, height=h3)
    img3.hAlign = 'CENTER'
    story.append(img3)
    
    # Part 4
    story.append(Spacer(1, 10))
    img4 = Image(os.path.join(code_dir, "code_vscode_4.png"), width=w, height=h4)
    img4.hAlign = 'CENTER'
    story.append(img4)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
