import matplotlib.pyplot as plt 
import csv 
import numpy as np


def get_avgs():
    scores = {}
    with open("think-judging-results.csv", "r", newline = None) as f:
        raw_results = csv.reader(f)
        categoryScores = {}
        next(raw_results, None)
        
        for row in raw_results:
            insert_results(scores, row)
        for titles in scores.keys():
            avg_impact = (int(scores[titles]["judge1"]["impact"]) + int(scores[titles]["judge2"]["impact"]))/2
            avg_innovation = (int(scores[titles]["judge1"]["innovation"]) + int(scores[titles]["judge2"]["innovation"]))/2
            avg_clarity = (int(scores[titles]["judge1"]["clarity"]) + int(scores[titles]["judge2"]["clarity"]))/2  
            avg_feasibility = (int(scores[titles]["judge1"]["feasibility"]) + int(scores[titles]["judge2"]["feasibility"]))/2 
            categoryScores[titles] = (avg_impact, avg_innovation, avg_clarity, avg_feasibility)            
        return categoryScores
    
def insert_results(results, row):
    title = row[2]
    judge_number = "judge1" if title not in results else "judge2"
    if title not in results:
        results[title] = {}
    results[title][judge_number] = {"impact": row[5],"innovation": row[6], "clarity": row[7], "feasibility": row[8]}

def graph_results():
    scores = get_avgs()
    results = {}
    index = np.arange(len(scores))
    plt.xlabel("Categories")
    plt.ylabel("Score (/5)")
    plt.grid(True)
    for proj in scores.keys():
        fig = plt.figure()
        plt.title(proj + " Avg. Category Scores")
        plt.bar(index,scores[proj],0.35, align= 'center')
        plt.xticks(index,["impact","innovation", "Clarity", "Feasibility"])
        plt.ylim([0,5])
        results[proj.lower()]=fig.savefig(proj.lower() + '.png')
        #plt.show()
    
def main():
    graph_results()

if __name__ == "__main__": main()