from pathlib import Path
import time

from resume_extr import parse_resume, read_resume
from resume_score import final_score
from job_desc import job

resume_folder = Path("resumes")
all_results=[]
for file_path in resume_folder.iterdir():
    
    if file_path.suffix.lower() not in [".pdf", ".docx"]:
        continue
    print("\nProcessing:", file_path.name)
    resume_text = read_resume(file_path)
    parsed_resume=parse_resume(resume_text) # llm call1
    time.sleep(5)
    result = final_score(job, parsed_resume) #llm caLL2
   
    time.sleep(5)
    print("Score:", result.score)
    all_results.append({
        "name": parsed_resume.name,
        "score": result.score,
        "details": result.details
    })
    print(all_results)