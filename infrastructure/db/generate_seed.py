"""
HR Seed Data Generator
Fully aligned with Demographics-1.csv — all 30 columns preserved
Run: pip install faker bcrypt
     python infrastructure/db/generate_seed.py
"""


import random
from datetime import date, timedelta
from faker import Faker


fake = Faker()
random.seed(42)
Faker.seed(42)


# ── All values extracted directly from Demographics-1.csv ─────────────────────


GENDERS = ["Male", "Female", "Genderqueer", "Bigender", "Non-binary", "Polygender", "Agender", "Genderfluid"]
GENDER_WEIGHTS = [42, 40, 5, 4, 3, 3, 2, 1]


LEVELS = ["Associate", "Professional", "Senior Associate", "Team Lead", "Manager",
          "Senior Manager", "Director", "Senior Director", "VP", "SVP"]
LEVEL_WEIGHTS = [18, 20, 22, 10, 12, 8, 5, 2, 2, 1]


DEPT_L1 = ["Engineering", "Analytics", "Sales", "Product Development",
           "Finance", "Marketing", "Human Resource", "Business analyst"]
DEPT_L1_WEIGHTS = [22, 18, 14, 16, 8, 10, 7, 5]


DEPT_L2 = [
    "Engineering", "Finance", "IT", "Customer Service", "Sales", "Operations",
    "Human Resources", "Legal", "Risk Management", "Supply Chain", "Marketing",
    "Product Development", "Logistics", "Quality Assurance", "Training",
    "Compliance", "Information Security", "Administration", "Facilities Management",
    "Strategic Planning", "Business Development", "Health and Safety", "Purchasing",
    "Public Relations", "Research and Development", "Internal Audit"
]


DEPT_L3 = [
    "IT", "Accounting", "Purchasing", "Training", "Quality Assurance", "Engineering",
    "Human Resources", "Risk Management", "Operations", "Finance", "Logistics",
    "Data Analytics", "Compliance", "Marketing", "Sales", "Project Management",
    "Administration", "Strategic Planning", "Internal Audit", "Corporate Communications",
    "Business Development", "Information Security", "Vendor Management", "Supply Chain",
    "Research and Development", "Product Development", "Public Relations"
]


BUSINESS_TITLES = [
    "Software Engineer IV", "Senior Engineer", "Data Coordinator",
    "Computer Systems Analyst I", "Computer Systems Analyst IV", "Electrical Engineer",
    "VP Marketing", "VP Product Management", "VP Accounting", "VP Quality Control",
    "Nuclear Power Engineer", "Human Resources Manager", "Director of Sales",
    "Financial Analyst", "Senior Financial Analyst", "Actuary",
    "Web Developer I", "Web Developer II", "Web Developer III",
    "Web Designer II", "Web Designer III", "Project Manager", "Marketing Manager",
    "Marketing Assistant", "Analog Circuit Design manager", "Developer I", "Developer III",
    "Programmer IV", "Programmer Analyst III", "Account Executive",
    "Account Representative III", "Account Coordinator", "Sales Associate",
    "Sales Representative", "Senior Sales Associate", "Recruiter", "Recruiting Manager",
    "Quality Engineer", "Quality Control Specialist", "Cost Accountant", "Tax Accountant",
    "Accountant I", "Accountant IV", "Administrative Officer", "Administrative Assistant III",
    "Help Desk Operator", "Help Desk Technician", "Desktop Support Technician",
    "Systems Administrator I", "Systems Administrator II", "Systems Administrator III",
    "Database Administrator I", "Structural Engineer", "Structural Analysis Engineer",
    "Mechanical Systems Engineer", "Chemical Engineer", "Civil Engineer",
    "Design Engineer", "Chief Design Engineer", "Product Engineer",
    "Geological Engineer", "Geologist II", "Biostatistician II", "Statistician II",
    "Research Associate", "Research Assistant I", "Registered Nurse", "Nurse Practicioner",
    "Clinical Specialist", "Occupational Therapist", "Social Worker", "Paralegal",
    "Legal Assistant", "Internal Auditor", "Financial Advisor",
    "Business Systems Development Analyst", "Information Systems Manager",
    "GIS Technical Architect", "Automation Specialist II", "Automation Specialist III",
    "Software Test Engineer II", "Software Test Engineer IV", "Software Consultant",
    "Senior Developer", "Community Outreach Specialist", "Executive Secretary",
    "Junior Executive", "General Manager", "Professor", "Associate Professor",
    "Assistant Professor", "Teacher", "Pharmacist", "Librarian", "Operator",
    "Engineer I", "Engineer II", "Engineer III", "Graphic Designer", "Senior Editor"
]


PRIMARY_SKILLS = [
    "Customer Service", "Research", "Marketing", "Software Testing", "Web Development",
    "Graphic Design", "Social Media Management", "Accounting", "SEO Optimization",
    "Program Management", "Data Analysis", "Video Editing", "Event Coordination",
    "Production Support", "Copywriting", "Sales", "Software Development",
    "Project Management", "Public Relations"
]


SECONDARY_SKILLS = [
    "UI/UX Design", "Teamwork", "Attention to Detail", "Problem Solving",
    "Event Planning", "Coding", "Machine Learning", "Financial Literacy",
    "Negotiation", "Communication", "Organization", "Leadership",
    "Database Management", "Mobile App Development", "Interpersonal Skills",
    "Writing Skills", "Time Management", "Presentation Skills", "Cloud Computing",
    "Artificial Intelligence", "Cybersecurity", "Blockchain Technology",
    "Critical Thinking", "Adaptability", "Conflict Resolution", "Analytical Skills",
    "Content Creation", "Decision Making", "Email Marketing", "Networking",
    "Research Skills", "Technical Skills", "Collaboration", "Creativity",
    "Public Speaking", "Photography", "Foreign Language Proficiency"
]


EMP_CATEGORIES = ["Regular", "Contractor", "Intern"]
EMP_CATEGORY_WEIGHTS = [82, 12, 6]
EMP_TYPES = ["Full time", "Part time"]
EMP_TYPE_WEIGHTS = [75, 25]
WORK_MODES = ["Hybrid", "Onsite", "Remote"]
WORK_MODE_WEIGHTS = [55, 30, 15]


WORK_CITIES = [
    "San Francisco", "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "Charlotte", "Indianapolis", "Seattle", "Denver",
    "Nashville", "Baltimore", "Louisville", "Portland", "Las Vegas", "Milwaukee",
    "Albuquerque", "Tucson", "Fresno", "Sacramento", "Long Beach", "Kansas City",
    "Mesa", "Virginia Beach", "Atlanta", "Colorado Springs", "Omaha", "Raleigh",
    "Miami", "Oakland", "Minneapolis", "Tulsa", "Memphis", "Detroit", "Boston",
    "Washington", "Oklahoma City", "Philadelphia", "Wichita", "El Paso"
]


CITY_TO_STATE = {
    "San Francisco": "California",   "Los Angeles": "California",    "San Jose": "California",
    "San Diego": "California",       "Sacramento": "California",     "Long Beach": "California",
    "Fresno": "California",          "Oakland": "California",        "New York": "New York",
    "Chicago": "Illinois",           "Houston": "Texas",             "San Antonio": "Texas",
    "Dallas": "Texas",               "Fort Worth": "Texas",          "Austin": "Texas",
    "El Paso": "Texas",              "Phoenix": "Arizona",           "Tucson": "Arizona",
    "Mesa": "Arizona",               "Colorado Springs": "Colorado", "Denver": "Colorado",
    "Seattle": "Washington",         "Washington": "Washington DC",  "Nashville": "Tennessee",
    "Memphis": "Tennessee",          "Louisville": "Kentucky",       "Miami": "Florida",
    "Jacksonville": "Florida",       "Atlanta": "Georgia",           "Indianapolis": "Indiana",
    "Columbus": "Ohio",              "Charlotte": "North Carolina",  "Raleigh": "North Carolina",
    "Las Vegas": "Nevada",           "Portland": "Oregon",           "Boston": "Massachusetts",
    "Detroit": "Michigan",           "Baltimore": "Maryland",        "Minneapolis": "Minnesota",
    "Omaha": "Nebraska",             "Wichita": "Kansas",            "Albuquerque": "New Mexico",
    "Milwaukee": "Wisconsin",        "Kansas City": "Missouri",      "Virginia Beach": "Virginia",
    "Philadelphia": "Pennsylvania",  "Oklahoma City": "Oklahoma",
}


TERMINATION_REASONS = [
    "Voluntary - Dissatisfied by Compensation",    "Voluntary - Dissatisfied by Manager",
    "Voluntary - Better Opportunity",              "Voluntary - Personal Reasons",
    "Voluntary - Return to School",                "Voluntary - Career Development",
    "Voluntary - Career Change",                   "Voluntary - Relocation",
    "Voluntary - Health Reasons",                  "Voluntary - Dissatisfied by Work Conditions",
    "Involuntary - Reduction in Force",            "Involuntary - Misconduct",
    "Involuntary - Unsatisfactory Performance",    "Involuntary - Mutual Consent",
]
TERM_WEIGHTS = [15, 12, 12, 8, 7, 7, 6, 6, 6, 5, 5, 4, 4, 3]


EXIT_TYPE_MAP = {
    "Voluntary - Dissatisfied by Compensation":   ("voluntary",   "compensation mismatch"),
    "Voluntary - Dissatisfied by Manager":         ("voluntary",   "management issues"),
    "Voluntary - Better Opportunity":              ("voluntary",   "better opportunity"),
    "Voluntary - Personal Reasons":                ("voluntary",   "personal reasons"),
    "Voluntary - Return to School":                ("voluntary",   "higher education"),
    "Voluntary - Career Development":              ("voluntary",   "career growth"),
    "Voluntary - Career Change":                   ("voluntary",   "career change"),
    "Voluntary - Relocation":                      ("voluntary",   "relocation"),
    "Voluntary - Health Reasons":                  ("voluntary",   "health reasons"),
    "Voluntary - Dissatisfied by Work Conditions": ("voluntary",   "work conditions"),
    "Involuntary - Reduction in Force":            ("involuntary", "reduction in force"),
    "Involuntary - Misconduct":                    ("involuntary", "misconduct"),
    "Involuntary - Unsatisfactory Performance":    ("involuntary", "performance"),
    "Involuntary - Mutual Consent":                ("involuntary", "mutual consent"),
}


JOB_PROJECTS = [
    "Operation Thunderbolt", "Operation Firestorm", "Operation Phoenix", "Operation Rampage",
    "Operation Avalanche",   "Operation Renegade",  "Operation Blackout", "Mission Alpha",
    "Mission Chaos",         "Mission Horizon",     "Mission Stealth",    "Mission Vortex",
    "Mission Apocalypse",    "Task Force Delta",    "Task Force Thunder", "Task Force Havoc",
    "Task Force Blizzard",   "Task Force Cyclone",  "Task Force Armada",
    "Project Omega",         "Project Nemesis",     "Project Eclipse",    "Project Inferno",
    "Project X",             "Project Armageddon",
]


HR_BPS = [
    "Laura Thompson", "Patrick Scott", "Jessica Garcia", "Eric Hall", "Michael Johnson",
    "Hannah Parker",  "Brian White",   "Kevin Lee",      "Olivia Lewis",  "Samantha King",
    "Rachel Hernandez","Daniel Adams", "Andrew Nelson",  "Nicole Turner", "Lauren Ramirez",
    "Mark Taylor",    "Matthew Wright","Emily Davis",    "Sarah Brown",   "Joshua Morris",
    "Brandon Cooper", "Chris Wilson",  "Megan Young",    "Kimberly Baker","Steven Clark",
    "Amanda Rodriguez","Jane Smith",   "Stephanie Roberts","David Martinez","John Doe"
]


SALARY_BY_LEVEL = {
    "Associate":        (45000,  75000), "Professional":    (60000,  95000),
    "Senior Associate": (80000, 120000), "Team Lead":       (90000, 135000),
    "Manager":         (110000, 160000), "Senior Manager":  (130000, 185000),
    "Director":        (160000, 220000), "Senior Director": (190000, 260000),
    "VP":              (230000, 320000), "SVP":             (300000, 420000),
}


RATING_DIST    = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
RATING_WEIGHTS = [2,   5,   10,  25,  30,  18,  7,   3]


# ── Pre-computed hashes — generated inside container with bcrypt==4.0.1 ───────
# Passwords: analyst123 | manager123 | admin123
# Regenerate ONLY by running inside hr_backend container:
#   docker exec -it hr_backend python -c "
#     from passlib.context import CryptContext
#     ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
#     print(ctx.hash('analyst123'))
#     print(ctx.hash('manager123'))
#     print(ctx.hash('admin123'))
#   "
USERS = [
    ("Analyst User",    "analyst@hr.com", "$2b$12$I04nCWJWMQMrSk5WJyimEuLh93Qwi5bep4UHlDeG5VBvCDEih7ROq", "analyst",  "1"),
    ("Michael Manager", "manager@hr.com", "$2b$12$uKBwhAbwSv2cod5LpB8d8upTiobnfkF7uVqumaY5/OsIEaH0aydT2", "manager",  "1"),
    ("Admin Lisa",      "admin@hr.com",   "$2b$12$L8b8ZjaHufhshGdTzPFihuIzY4d7KHLUrBICDYRsjz29pORrk3pyW", "hr_admin", "1"),
]


# ── Helpers ───────────────────────────────────────────────────────────────────


def esc(s):
    return str(s).replace("'", "''") if s else ""


def rdate(start, end):
    delta = end - start
    if delta.days <= 0:
        return start
    return start + timedelta(days=random.randint(0, delta.days))


def dob_for_level(lvl):
    ranges = {
        "Associate":(22,30), "Professional":(24,35), "Senior Associate":(27,40),
        "Team Lead":(28,42), "Manager":(30,48), "Senior Manager":(33,52),
        "Director":(35,55), "Senior Director":(38,58), "VP":(40,60), "SVP":(44,62)
    }
    lo, hi = ranges.get(lvl, (25, 50))
    age = random.randint(lo, hi)
    t = date.today()
    return date(t.year - age, random.randint(1, 12), random.randint(1, 28))


def opt(v):
    return f"'{v}'" if v else "NULL"


def row(emp_id, fn, ln, em, g, dob, ttl, lvl, ps, ss, ec, et, sts, md,
        ct, co, st, sd, td, lp, ljc, sf, sl, sr, dept, d2, d3, bp, pr, cl, tr, salary):
    return (
        f"INSERT INTO employees (id,first_name,last_name,email,gender,date_of_birth,"
        f"business_title,level,primary_skill,secondary_skill,employment_category,"
        f"employment_type,employment_status,work_mode,work_city,work_country,work_state,"
        f"start_date,termination_date,last_promotion_date,last_job_change_date,"
        f"supervisor_first_name,supervisor_last_name,supervisor_id,"
        f"department_l1,department_l2,department_l3,hr_bp_name,job_project,job_client,"
        f"termination_reason,salary) VALUES ("
        f"{emp_id},'{esc(fn)}','{esc(ln)}','{esc(em)}','{g}','{dob}',"
        f"'{esc(ttl)}','{lvl}','{esc(ps)}','{esc(ss)}','{ec}','{et}',"
        f"'{sts}','{md}','{esc(ct)}','{co}','{st}',"
        f"'{sd}',{opt(td)},{opt(lp)},{opt(ljc)},"
        f"'{esc(sf)}','{esc(sl)}',{sr},"
        f"'{dept}','{d2}','{d3}','{esc(bp)}','{esc(pr)}','{esc(cl)}',"
        f"{opt(tr)},{salary});"
    )


# ── Generate ──────────────────────────────────────────────────────────────────


lines = []
lines.append("-- ============================================================")
lines.append("-- Seed data: aligned with Demographics-1.csv (all 30 columns)")
lines.append("-- 500 employees | 8 dept supervisors | ~200 inactive with exits")
lines.append("-- ============================================================")
lines.append("SET search_path TO hr;")
lines.append("")


sup_map = {}
all_emp = []


# ── Pass 1: One supervisor per Dept L1 ───────────────────────────────────────
lines.append("-- Supervisors (8)")
for idx, dept in enumerate(DEPT_L1, start=1):
    g   = random.choices(GENDERS, weights=GENDER_WEIGHTS)[0]
    fn  = fake.first_name_male() if g == "Male" else fake.first_name_female()
    ln  = fake.last_name()
    em  = f"sup.{dept.lower().replace(' ', '.')}{idx}@company.com"
    dob = dob_for_level("Manager")
    ttl = random.choice([t for t in BUSINESS_TITLES if "Manager" in t or "Director" in t])
    ct  = random.choice(WORK_CITIES)
    st  = CITY_TO_STATE.get(ct, "California")
    sd  = rdate(date(2015, 1, 1), date(2020, 12, 31))
    sal = round(random.uniform(*SALARY_BY_LEVEL["Manager"]), 2)
    pr  = random.choice(JOB_PROJECTS)
    bp  = random.choice(HR_BPS)
    cl  = random.choice(HR_BPS)
    d2  = random.choice(DEPT_L2)
    d3  = random.choice(DEPT_L3)
    ps  = random.choice(PRIMARY_SKILLS)
    ss  = random.choice(SECONDARY_SKILLS)
    md  = random.choices(WORK_MODES, weights=WORK_MODE_WEIGHTS)[0]
    sup_map[dept] = (fn, ln, idx)
    lines.append(row(idx, fn, ln, em, g, dob, ttl, "Manager", ps, ss, "Regular", "Full time",
                     "Active", md, ct, "United States", st, sd, None, None, None,
                     "HR Admin", "System", "NULL", dept, d2, d3, bp, pr, cl, None, sal))
    all_emp.append({"id": idx, "dept": dept, "level": "Manager", "status": "Active", "tr": None})


lines.append("")
lines.append("-- Individual contributors (492)")
eid = 9


for _ in range(492):
    dept = random.choices(DEPT_L1, weights=DEPT_L1_WEIGHTS)[0]
    lvl  = random.choices(LEVELS, weights=LEVEL_WEIGHTS)[0]
    g    = random.choices(GENDERS, weights=GENDER_WEIGHTS)[0]
    fn   = fake.first_name_male() if g == "Male" else fake.first_name_female()
    ln   = fake.last_name()
    em   = f"{fake.user_name()}{eid}@company.com"
    dob  = dob_for_level(lvl)
    ttl  = random.choice(BUSINESS_TITLES)
    ps   = random.choice(PRIMARY_SKILLS)
    ss   = random.choice(SECONDARY_SKILLS)
    ec   = random.choices(EMP_CATEGORIES, weights=EMP_CATEGORY_WEIGHTS)[0]
    et   = random.choices(EMP_TYPES, weights=EMP_TYPE_WEIGHTS)[0]
    md   = random.choices(WORK_MODES, weights=WORK_MODE_WEIGHTS)[0]
    ct   = random.choice(WORK_CITIES)
    st   = CITY_TO_STATE.get(ct, "California")
    co   = random.choices(["United States", "India", "United Kingdom", "Australia", ""],
                          weights=[65, 18, 10, 3, 4])[0]
    sd   = rdate(date(2015, 1, 1), date(2025, 10, 1))
    sts  = random.choices(["Active", "Inactive"], weights=[60, 40])[0]
    td   = None; tr = None
    if sts == "Inactive":
        td = rdate(sd + timedelta(days=180), date(2025, 12, 31))
        tr = random.choices(TERMINATION_REASONS, weights=TERM_WEIGHTS)[0]
    end_ref = td or date(2025, 12, 31)
    lp  = rdate(sd, end_ref) if random.random() < 0.45 else None
    ljc = rdate(sd, end_ref) if random.random() < 0.50 else None
    sup = sup_map.get(dept)
    sf  = sup[0] if sup else "HR"
    sl  = sup[1] if sup else "Admin"
    sr  = str(sup[2]) if sup else "NULL"
    d2  = random.choice(DEPT_L2)
    d3  = random.choice(DEPT_L3)
    bp  = random.choice(HR_BPS)
    pr  = random.choice(JOB_PROJECTS)
    cl  = random.choice(HR_BPS)
    sal = round(random.uniform(*SALARY_BY_LEVEL[lvl]), 2)
    lines.append(row(eid, fn, ln, em, g, dob, ttl, lvl, ps, ss, ec, et, sts, md,
                     ct, co, st, sd, td, lp, ljc, sf, sl, sr, dept, d2, d3, bp, pr, cl, tr, sal))
    all_emp.append({"id": eid, "dept": dept, "level": lvl, "status": sts, "tr": tr})
    eid += 1


lines.append("")
lines.append("-- Employee exits (from all Inactive employees)")
for e in all_emp:
    if e["status"] == "Inactive":
        tr = e["tr"] or random.choices(TERMINATION_REASONS, weights=TERM_WEIGHTS)[0]
        xt, xr = EXIT_TYPE_MAP.get(tr, ("voluntary", "other"))
        xd = rdate(date(2023, 1, 1), date(2026, 1, 31))
        lines.append(
            f"INSERT INTO employee_exits (employee_id,exit_date,exit_type,reason) "
            f"VALUES ({e['id']},'{xd}','{xt}','{esc(xr)}');"
        )


lines.append("")
lines.append("-- Performance reviews (2 cycles, active employees)")
active_ids = [e["id"] for e in all_emp if e["status"] == "Active"]
for rid in random.sample(active_ids, min(350, len(active_ids))):
    dept_of = next((e["dept"] for e in all_emp if e["id"] == rid), DEPT_L1[0])
    rv_id   = sup_map.get(dept_of, (None, None, 1))[2]
    for rd in [date(2024, 6, 30), date(2024, 12, 31)]:
        rat = random.choices(RATING_DIST, weights=RATING_WEIGHTS)[0]
        lines.append(
            f"INSERT INTO performance_reviews (employee_id,review_date,rating,reviewer_id) "
            f"VALUES ({rid},'{rd}',{rat},{rv_id});"
        )


lines.append("")
lines.append("-- Hiring requisitions (25)")
for _ in range(25):
    dept = random.choices(DEPT_L1, weights=DEPT_L1_WEIGHTS)[0]
    od   = rdate(date(2025, 1, 1), date(2026, 1, 15))
    sts  = random.choices(["open", "filled", "cancelled"], weights=[45, 40, 15])[0]
    cv   = f"'{rdate(od, date(2026, 2, 20))}'" if sts != "open" else "NULL"
    lines.append(
        f"INSERT INTO hiring_requisitions (department,open_date,close_date,status) "
        f"VALUES ('{dept}','{od}',{cv},'{sts}');"
    )


lines.append("")
lines.append("-- App users (3 test accounts — hashes verified with bcrypt==4.0.1 inside container)")
for uname, email, hashed, role, er in USERS:
    lines.append(
        f"INSERT INTO users (name,email,hashed_password,role,employee_id) "
        f"VALUES ('{esc(uname)}','{email}','{esc(hashed)}','{role}',{er});"
    )


inactive_n = sum(1 for e in all_emp if e["status"] == "Inactive")
active_n   = sum(1 for e in all_emp if e["status"] == "Active")
lines.append(f"\n-- TOTALS: {eid-1} employees | {active_n} active | {inactive_n} inactive | {inactive_n} exits | {min(350,len(active_ids))*2} reviews")


with open("infrastructure/db/seed_data.sql", "w") as f:
    f.write("\n".join(lines))


print(f"✅ seed_data.sql written to infrastructure/db/seed_data.sql")
