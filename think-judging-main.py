import csv
from docx import Document
from testPlotLib import graph_results

def parse_results():
	with open("think-judging-results.csv", "rU") as f:
         parsed_results = {}
         raw_results = csv.reader(f)
         next(raw_results, None)
         for row in raw_results:
             insert_results(parsed_results, row)
         bins = separate_results(parsed_results)
         for bin in bins:
             write_output_new(bins, bin)


def insert_results(results, row):
	title = row[2].lower()
	judge_number = "judge1" if title not in results else "judge2"
	if title not in results:
		results[title] = {}
	results[title][judge_number] = {"judge": row[1], "area": row[3], "summary": row[4], "impact": row[5], \
									 "innovation": row[6], "clarity": row[7], "feasibility": row[8], \
									"gen-notes": row[9], "benefit": row[10], "good": row[11], "bad": row[12],\
									 "decision": row[13], "addl-notes": row[14]}

def separate_results(parsed_results):
	bins = {}
	for paper in parsed_results:
		decisions = sorted([parsed_results[paper]["judge1"]["decision"], parsed_results[paper]["judge2"]["decision"]])
		if decisions == ["Yes","Yes"]:
			bins.setdefault('2y',{})[paper] = parsed_results[paper]
		elif decisions == ["Maybe","Yes"]:
			bins.setdefault('1y1m',{})[paper] = parsed_results[paper]
		elif decisions == ["No","Yes"]:
			bins.setdefault('1n1y',{})[paper] = parsed_results[paper]
		elif decisions == ["Maybe","Maybe"]:
			bins.setdefault('2m',{})[paper] = parsed_results[paper]
		elif decisions == ["Maybe","No"]:
			bins.setdefault('1m1n',{})[paper] = parsed_results[paper]
		elif decisions == ["No","No"]:
			bins.setdefault('2n',{})[paper] = parsed_results[paper]
	return bins

def write_output_new(bins, bin_name):
      paper_list = bins[bin_name]
      document = Document()
      graph_results()
      for paper in paper_list:
         document.add_heading(paper.title(), 0)
         document.add_heading('Judge 1: ' + paper_list[paper]["judge1"]["judge"] , level=1)
         write_judging_results_new(document, paper_list[paper]["judge1"])
         document.add_heading('Judge 2: ' + paper_list[paper]["judge2"]["judge"], level=1)
         write_judging_results_new(document, paper_list[paper]["judge2"])
         document.add_picture(paper+'.png')
         document.add_page_break()
      document.save(bin_name + ".docx")

def write_judging_results_new(document, results):
    document.add_heading("Area: " + results["area"], level=2)

    document.add_heading("Summary: ", level=2)
    document.add_paragraph(results["summary"])

    table = document.add_table(rows=1, cols=4, style= "Light Shading Accent 1")
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Impact'
    hdr_cells[1].text = 'Innovation'
    hdr_cells[2].text = 'Clarity'
    hdr_cells[3].text = 'Feasibility'
    row_cells = table.add_row().cells
    row_cells[0].text = results["impact"]
    row_cells[1].text = results["innovation"]
    row_cells[2].text = results["clarity"]
    row_cells[3].text = results["feasibility"] 
            
    document.add_heading("General Notes: ", level=2)
    document.add_paragraph(results["gen-notes"])

    document.add_heading("Personal Benefit to Applicant: ", level=2)
    document.add_paragraph(results["benefit"])

    document.add_heading("What's Good: ", level=2)
    document.add_paragraph(results["good"])

    document.add_heading("What's Bad: ", level=2)
    document.add_paragraph(results["bad"])

    document.add_heading("Decision: " + results["decision"], level=1)

    document.add_heading("Final Notes: ", level=2)
    document.add_paragraph(results["addl-notes"])

def main():
	parse_results()

if __name__ == "__main__": main()
