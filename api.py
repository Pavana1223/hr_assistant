mport os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HR_DATA = """
You are an HR Assistant. Always answer from the below company policies.

COMPANY BENEFITS:
1. Health Insurance: ₹3,00,000 coverage for employee + family.
2. Work From Home Policy: 2 days per week allowed.
3. Annual Bonus: Performance-based.
4. Transport Allowance: Provided for office commuters.
5. PF Contribution: Company contributes 12%.

LEAVE POLICIES:
1. Sick Leave: 12 paid sick leaves per year.
2. Casual Leave: 10 days per year.
3. Earned Leave: 15 days per year.
4. Maternity Leave: 26 weeks paid leave.
5. Paternity Leave: 2 weeks paid leave.

COMPANY RULES:
1. Office Timings: 9 AM – 6 PM.
2. Notice Period: 1 month.
3. Dress Code: Smart casuals.
4. Probation Period: 6 months.

If a question is outside this HR data, reply:
"I'm sorry, I don't have information about that in the current HR policies."
"""

def run_hr_agent(user_question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": HR_DATA},
            {"role": "user", "content": user_question}
        ],
        max_tokens=250
    )
    return response.choices[0].message["content"]