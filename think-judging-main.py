import csv

def parse_results():
	with open("think-judging-results.csv", "rU") as f:
		parsed_results = {}
		raw_results = csv.reader(f)
		next(raw_results, None)
		for row in raw_results:
			insert_results(parsed_results, row)
		bins = separate_results(parsed_results)
		for bin in bins:
			write_output(bins, bin)


def insert_results(results, row):
	title = row[2]
	judge_number = "judge1" if title not in results else "judge2"
	if title not in results:
		results[title] = {}
	results[title][judge_number] = {"judge": row[1], "area": row[3], "summary": row[4], "impact": row[5],\
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

def write_output(bins, bin_name):
	paper_list = bins[bin_name]
	with open(bin_name+".docx", 'a') as f:
		for paper in paper_list:
			f.write(paper + "\n\n")
			f.write("Judge 1:\n\n")
			write_judging_results(f, paper_list[paper]["judge1"])
			f.write("Judge 2:\n\n")
			write_judging_results(f, paper_list[paper]["judge2"])


def write_judging_results(f, results):
	f.write("Judge Name: " + results["judge"] + "\n\n")
	f.write("Area: " + results["area"] + "\n")
	f.write("Summary: " + results["summary"] + "\n\n")
	f.write("Impact: " + results["impact"] + "\n")
	f.write("Innovation: " + results["innovation"] + "\n")
	f.write("Clarity: " + results["clarity"] + "\n")
	f.write("Feasibility: " + results["feasibility"] + "\n\n")
	f.write("General Notes: " + results["benefit"] + "\n\n")
	f.write("Personal Benefit to Applicant: " + results["gen-notes"] + "\n\n")
	f.write("What's Good: " + results["good"] + "\n\n")
	f.write("What's Bad: " + results["bad"] + "\n\n")
	f.write("Decision: " + results["decision"] + "\n\n")
	f.write("Final Notes: " + results["addl-notes"] + "\n\n")


def main():
	parse_results()

if __name__ == "__main__": main()
