import json
import re

def is_senior_position(title, description):
    senior_keywords = [
        r'\bsenior\b', r'\bexpert\b', r'\blead\b', r'\bmanager\b',
        r'\barchitect\b', r'\bdirector\b', r'\bprincipal\b', r'\bconsultant\b',
        r'\bchief\b', r'\bhead\b', r'\bvp\b', r'\bvice\s*president\b', 
        r'\bexecutive\b', r'\bpresident\b', r'\bcoo\b', r'\bcfo\b', r'\bcto\b', 
        r'\bchief\s*officer\b', r'\bteam\s*lead\b', r'\bengineering\s*lead\b',
        r'\bproject\s*manager\b', r'\boperations\s*manager\b',
        r'\b5\+\s*years\b', r'\b7\+\s*years\b', r'\b10\+\s*years\b',  r'\b2\+\s*years\b', r'\b3\+\s*years\b', r'\b4\+\s*years\b',  r'\b6\+\s*years\b', r'\b8\+\s*years\b', r'\b9\+\s*years\b',
        r'\b8\+\s*years\b', r'\bhead\s*of\b', r'\bdirector\s*of\b', r'\bengineering\s*manager\b', r'\bportfolio\s*manager\b',
        r'\bSr\.\b', r'\bSr\b'  ,r'\bSsr\.\b', r'\bSsr\b'  ,r'\bOver\s*3\s*years\b',r'\bOver\s*2\s*years\b',r'\bOver\s*4\s*years\b',
        r'\bOver\s*5\s*years\b',r'\bOver\s*6\s*years\b',r'\bOver\s*7\s*years\b',r'\bOver\s*8\s*years\b',r'\bOver\s*9\s*years\b',r'\bOver\s*10\s*years\b', r'\b2\s*years\s*of\s*experience\b' , r'\b3\s*years\s*of\s*experience\b', r'\b4\s*years\s*of\s*experience\b' , r'\b5\s*years\s*of\s*experience\b' , r'\b6\s*years\s*of\s*experience\b' , r'\b7\s*years\s*of\s*experience\b' , r'\b8\s*years\s*of\s*experience\b' ,r'\b9\s*years\s*of\s*experience\b' , r'\b10\s*years\s*of\s*experience\b' ,    r'\bSoftware\s*Engineer\s*II\b', r'\bSoftware\s*Engineer\s*III\b', r'\bSoftware\s*Engineer\s*IV\b' ,   r'\b2\+\s*years\s*of\s*relevant\s*work\b',
    r'\b3\+\s*years\s*of\s*relevant\s*work\b',
    r'\b4\+\s*years\s*of\s*relevant\s*work\b',
    r'\b5\+\s*years\s*of\s*relevant\s*work\b',
    r'\b6\+\s*years\s*of\s*relevant\s*work\b',
    r'\b7\+\s*years\s*of\s*relevant\s*work\b',
    r'\b8\+\s*years\s*of\s*relevant\s*work\b',
    r'\b9\+\s*years\s*of\s*relevant\s*work\b',
    r'\b10\+\s*years\s*of\s*relevant\s*work\b',
    r'\byears\s*of\s*relevant\s*work\s*experience\b',
    r'\byears\s*of\s*work\s*experience\b',


    ]
    
    combined_text = f"{title} {description}".lower()
    
    for keyword in senior_keywords:
        if re.search(keyword, combined_text, re.IGNORECASE):
            return True
    
    return False

# Load the jobs from jobs_no.json
with open('jobs_no.json', 'r') as file:
    jobs = json.load(file)

for job in jobs:
    job['done'] = 'no'  # Add the new key

# Filter out senior positions
filtered_jobs = [job for job in jobs if not is_senior_position(job['job_info'], job['job_description'])]

# Print the results
print(f"Total jobs before filtering: {len(jobs)}")
print(f"Jobs after filtering: {len(filtered_jobs)}")

# Save the filtered jobs to a new file
with open('filtered_jobs_no.json', 'w') as file:
    json.dump(filtered_jobs, file, indent=2)

print("Filtered jobs saved to filtered_jobs_no.json")



# ['NA','no','yes','me']