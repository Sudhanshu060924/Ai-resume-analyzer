import json
import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("api error")
client = Groq(api_key=api_key)
model="llama-3.3-70b-versatile"

job_des="""
Software Development Engineer (SDE)

Job Summary
A Software Development Engineer (SDE) designs, develops, tests, and maintains scalable software applications. They work closely with product managers, designers, and other engineers to build high-quality, reliable, and efficient software solutions while following industry best practices.

Key Responsibilities
Design, develop, and maintain software applications and backend services.
Write clean, efficient, maintainable, and well-documented code.
Build scalable RESTful APIs and integrate third-party services.
Develop responsive and user-friendly web applications.
Optimize application performance, security, and scalability.
Debug, troubleshoot, and resolve software defects.
Collaborate with cross-functional teams during the software development lifecycle.
Participate in code reviews and maintain coding standards.
Write unit, integration, and end-to-end tests.
Work with databases to design schemas and optimize queries.
Use Git for version control and CI/CD pipelines for automated deployments.
Stay updated with emerging technologies and industry trends.
Required Skills
Strong understanding of Data Structures and Algorithms (DSA).
Proficiency in one or more programming languages such as Java, Python, C++, JavaScript, or Go.
Knowledge of Object-Oriented Programming (OOP) and design principles.
Experience with Git/GitHub.
Understanding of Operating Systems, Computer Networks, and DBMS.
Familiarity with SQL and NoSQL databases.
Experience building REST APIs.
Strong problem-solving and debugging skills.
Good communication and teamwork abilities.
Preferred Skills
Experience with cloud platforms (AWS, Azure, or GCP).
Knowledge of Docker, Kubernetes, and CI/CD.
Familiarity with microservices architecture.
Understanding of system design and distributed systems.
Experience with Agile/Scrum development.
Common Tech Stack
Languages: Java, Python, JavaScript, TypeScript, Go, C++
Frontend: React, Next.js, HTML, CSS, Tailwind CSS
Backend: Spring Boot, Node.js, Express, FastAPI
Databases: PostgreSQL, MySQL, MongoDB, Redis
Tools: Git, GitHub, Docker, Kubernetes, Jenkins, Postman
Cloud: AWS, Azure, Google Cloud
Qualifications
Bachelor's degree in Computer Science, Information Technology, or a related field (or equivalent experience).
Strong coding and problem-solving skills.
Understanding of software engineering fundamentals and best practices.
What Companies Look For in SDE Candidates
Strong DSA and coding interview performance.
Ability to build real-world projects.
Knowledge of system design (for experienced roles).
Clean coding practices and debugging skills.
Team collaboration and communication.
Continuous learning mindset.
"""

class Job_desc(BaseModel):
    role: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: float | None
    education_requirements: list[str]
    responsibilities: list[str]

job_schema = Job_desc.model_json_schema()

system_prompt = f"""
You are an expert HR assistant.

Your job is to analyze job descriptions and extract
structured information from them.

Return ONLY valid JSON matching this schema:

{job_schema}
IMPORTANT:
Do NOT return the schema itself.
Do NOT return fields like "properties", "title" or "type".
Fill the schema with actual information extracted from the job description.

If minimum experience is not mentioned, return null.
If information for a list is missing, return an empty list.
Do not invent information.
"""

user_propmt = f"""
Analyse the following job description: {job_des}
"""

mess_sys={
    "role":"system",
    "content":system_prompt
}
mess_user={
    "role":"user",
    "content":user_propmt
}
response_format={
    "type":"json_object"
}
messages=[mess_sys,mess_user]
response = client.chat.completions.create(model=model , messages=messages , response_format=response_format)

ans = response.choices[0].message.content

raw_json = ans #get the json of job desc
job_data=json.loads(raw_json)

job = Job_desc(**job_data)

    



