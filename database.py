import sqlite3
import os
import json

def init_db():
    conn = sqlite3.connect('horizon.db')
    cursor = conn.cursor()

    # Jobs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT NOT NULL,
        salary TEXT,
        type TEXT NOT NULL,
        posted_date TEXT NOT NULL,
        description TEXT,
        requirements TEXT
    )
    ''')

    # Preparation Material Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prep_materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        roadmap TEXT,
        notes TEXT,
        questions TEXT
    )
    ''')

    # Companies Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        logo_url TEXT,
        hiring_process TEXT,
        syllabus TEXT,
        exam_pattern TEXT,
        eligibility TEXT
    )
    ''')

    # Practice Problems Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS practice_problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        problem_name TEXT NOT NULL,
        link TEXT,
        difficulty TEXT
    )
    ''')

    # Seed Jobs
    jobs = [
        ("Software Engineer", "Google", "Bangalore, India", "₹20L - ₹40L", "Full-time", "2 days ago", "Work on cutting edge AI features.", "Python, React, System Design"),
        ("Data Scientist", "Meta", "Remote", "$150k - $220k", "Full-time", "1 day ago", "Help us build the metaverse.", "ML, PyTorch, SQL"),
        ("Product Manager", "Apple", "Mumbai, India", "₹15L - ₹30L", "Full-time", "5 hours ago", "Shape the future of consumer tech.", "Agile, Product Vision"),
        ("Frontend Developer", "Netflix", "Hyderabad, India", "₹18L - ₹35L", "Contract", "3 days ago", "Build high performance UI for millions.", "Next.js, Tailwind, CSS"),
        ("Backend Architect", "Amazon", "Pune, India", "₹25L - ₹50L", "Full-time", "1 week ago", "Architect scalable cloud services.", "Java, AWS, Microservices"),
        ("UX Designer", "Airbnb", "Remote", "₹12L - ₹20L", "Full-time", "4 days ago", "Design beautiful travel experiences.", "Figma, User Research"),
        ("Cloud Engineer", "Microsoft", "Delhi, India", "₹16L - ₹28L", "Full-time", "2 days ago", "Manage Azure infrastructure.", "Terraform, Kubernetes, Azure"),
        ("ML Engineer", "NVIDIA", "Bangalore, India", "₹30L - ₹60L", "Full-time", "Today", "Optimizing deep learning kernels.", "C++, CUDA, DL"),
        ("Junior Developer", "StartupX", "Remote", "₹6L - ₹10L", "Internship", "1 day ago", "Fast paced learning environment.", "HTML, CSS, JS"),
        ("Security Analyst", "GlobalBank", "Gurgaon, India", "₹14L - ₹25L", "Full-time", "6 days ago", "Ensure banking security.", "Cybersecurity, PenTesting")
    ]

    cursor.executemany('''
    INSERT INTO jobs (title, company, location, salary, type, posted_date, description, requirements)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', jobs)

    # Seed Prep Materials
    prep = [
        (
            "Aptitude", "Quantitative Mastery", 
            "Comprehensive guide to mastering numerical ability for placements.",
            json.dumps(["Number Systems & Simplification", "Percentages, Profit & Loss", "Averages, Ratio & Proportion", "Time, Speed & Distance", "Simple & Compound Interest", "Permutation, Combination & Probability"]),
            "Quantitative aptitude is the cornerstone of technical placements. To succeed, focus on two things: Speed and Accuracy.",
            json.dumps([{"q": "A can do a work in 15 days and B in 20 days. If they work together for 4 days, what fraction of work is left?", "a": "8/15."}])
        ),
        (
            "Coding", "Dynamic Programming Essentials", 
            "Learn the art of optimizing recursive solutions using DP.",
            json.dumps(["Recursion Fundamentals", "Memoization Strategy", "Tabulation (Bottom-Up)"]),
            "Dynamic Programming (DP) is often the most feared topic in coding interviews. However, it's just recursion with storage.",
            json.dumps([{"q": "What is the core difference between Memoization and Tabulation?", "a": "Memoization is Top-Down, Tabulation is Bottom-Up."}])
        ),
        (
            "Interview", "System Design for Beginners", 
            "Master the high-level architecture of scalable applications.",
            json.dumps(["Introduction to Scalability", "Load Balancers", "Caching"]),
            "In System Design, there is no single 'correct' answer; it's all about tradeoffs.",
            json.dumps([{"q": "What is the CAP Theorem?", "a": "Consistency, Availability, and Partition Tolerance."}])
        ),
        (
            "Aptitude", "Logical Reasoning", 
            "Sharpen your analytical skills with logical puzzles and patterns.",
            json.dumps(["Syllogisms", "Blood Relations", "Seating Arrangements"]),
            "Logical reasoning tests your ability to structured thinking.",
            json.dumps([{"q": "All cats are dogs. No dogs are birds. Can we say some cats are birds?", "a": "No."}])
        ),
        (
            "Coding", "SQL for Data Science", 
            "Essential data manipulation skills using SQL.",
            json.dumps(["Relational Database Basics", "Advanced JOIN Operations"]),
            "SQL is the bread and butter of data roles.",
            json.dumps([{"q": "How do you find the second highest salary?", "a": "Using subqueries or LIMIT/OFFSET."}])
        ),
        (
            "Interview", "HR Rounds: Top 50 Questions", 
            "Master soft skills and behavioral questions for the final round.",
            json.dumps(["The 'Tell Me About Yourself' pitch", "STAR Method"]),
            "HR rounds check if you are a culture fit.",
            json.dumps([{"q": "Why should we hire you?", "a": "Align your skills with the company mission."}])
        )
    ]

    cursor.executemany('''
    INSERT INTO prep_materials (category, title, description, roadmap, notes, questions)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', prep)

    # Seed Companies
    companies_data = [
        (
            "TCS", 
            "Tata Consultancy Services is a global leader in IT services, consulting & business solutions.",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Tata_Consultancy_Services_Logo.svg/512px-Tata_Consultancy_Services_Logo.svg.png",
            "1. TCS NQT (National Qualifier Test), 2. Technical Interview, 3. HR Interview.",
            "Numerical Ability, Verbal Ability, Reasoning Ability, Programming Logic, and Hands-on Coding.",
            "Cognitive (60 mins), Technical (60 mins). Total duration: 180 mins.",
            "60% throughout Tenth, Twelfth, Diploma, Graduation and Post-Graduation."
        ),
        (
            "Wipro", 
            "A leading global information technology, consulting and business process services company.",
            "https://upload.wikimedia.org/wikipedia/commons/a/a0/Wipro_Primary_Logo_Color_RGB.svg",
            "1. Online Assessment, 2. Technical Interview, 3. HR Interview.",
            "Quantitative Aptitude, Logical Reasoning, Verbal Ability, Basic Programming, and Essay Writing.",
            "Aptitude (48 mins), Written Communication (20 mins), Online Programming (60 mins).",
            "60% in 10th and 12th standard. 60% or 6.0 CGPA in Graduation."
        ),
        (
            "Google", 
            "Google's mission is to organize the world's information and make it universally accessible and useful.",
            "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
            "1. Online Coding Challenge, 2. Technical Phone Screen, 3. Virtual Onsite (4-5 rounds).",
            "Advanced Data Structures, Algorithms, System Design, and Googliness.",
            "45 minutes per round with one or two complex problems.",
            "Bachelor's degree in Computer Science or equivalent practical experience."
        ),
        (
            "Microsoft", 
            "Microsoft enables digital transformation for the era of an intelligent cloud and an intelligent edge.",
            "https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg",
            "1. Online Assessment, 2. Technical Interview Rounds, 3. System Design/HM Round.",
            "DSA, Object-Oriented Design, System Design, and Behavioral Questions.",
            "Multiple technical rounds (45-60 mins each).",
            "CGPA of 7 or above. No standing backlogs."
        ),
        (
            "Amazon", 
            "Amazon is guided by four principles: customer obsession and passion for invention.",
            "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
            "1. Online Assessment, 2. Technical Phone Screen, 3. Virtual Onsite (The 'Loop').",
            "Data Structures, Algorithms, Scalability, and Amazon's Leadership Principles.",
            "Heavy emphasis on Leadership Principles. 4-5 rounds.",
            "Strong academic record. Proficiency in at least one modern programming language."
        )
    ]

    cursor.executemany('''
    INSERT INTO companies (name, description, logo_url, hiring_process, syllabus, exam_pattern, eligibility)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', companies_data)

    # Seed Practice Problems
    practice = [
        ("NUMBERS", "Climbing Stairs", "https://leetcode.com/problems/climbing-stairs", "Easy"),
        ("NUMBERS", "Check if a given year is leap year", "https://www.geeksforgeeks.org/program-check-given-year-leap-year/", "Easy"),
        ("NUMBERS", "Prime Numbers", "https://www.geeksforgeeks.org/prime-numbers/", "Easy"),
        ("NUMBERS", "Valid Perfect Square", "https://leetcode.com/problems/valid-perfect-square/", "Easy"),
        ("NUMBERS", "Add Digits", "https://leetcode.com/problems/add-digits/", "Easy"),
        ("NUMBERS", "Power of Two", "https://leetcode.com/problems/power-of-two/", "Easy"),
        ("ARRAYS", "Two Sum", "https://leetcode.com/problems/two-sum", "Easy"),
        ("ARRAYS", "Move Zeroes", "https://leetcode.com/problems/move-zeroes", "Easy"),
        ("ARRAYS", "Contains Duplicate", "https://leetcode.com/problems/contains-duplicate", "Easy"),
        ("ARRAYS", "Best Time to Buy and Sell Stock", "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/", "Easy"),
        ("ARRAYS", "Maximum Subarray (Kadane's)", "https://leetcode.com/problems/maximum-subarray/", "Medium"),
        ("ARRAYS", "Rotate Array", "https://leetcode.com/problems/rotate-array/", "Medium"),
        ("ARRAYS", "3Sum", "https://leetcode.com/problems/3sum/", "Medium"),
        ("ARRAYS", "Product of Array Except Self", "https://leetcode.com/problems/product-of-array-except-self/", "Medium"),
        ("STRINGS", "Reverse String", "https://leetcode.com/problems/reverse-string/", "Easy"),
        ("STRINGS", "Valid Anagram", "https://leetcode.com/problems/valid-anagram/", "Easy"),
        ("STRINGS", "Valid Palindrome", "https://leetcode.com/problems/valid-palindrome/", "Easy"),
        ("STRINGS", "Longest Common Prefix", "https://leetcode.com/problems/longest-common-prefix/", "Easy"),
        ("STRINGS", "Longest Substring Without Repeating Characters", "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "Medium"),
        ("STRINGS", "Group Anagrams", "https://leetcode.com/problems/group-anagrams/", "Medium"),
        ("RECURSION", "Fibonacci Number", "https://leetcode.com/problems/fibonacci-number/", "Easy"),
        ("RECURSION", "Permutations", "https://leetcode.com/problems/permutations/", "Medium"),
        ("RECURSION", "Subsets", "https://leetcode.com/problems/subsets/", "Medium"),
        ("SORTING", "Merge Sorted Array", "https://leetcode.com/problems/merge-sorted-array/", "Easy"),
        ("SORTING", "Sort Colors", "https://leetcode.com/problems/sort-colors/", "Medium"),
        ("SORTING", "Kth Largest Element in an Array", "https://leetcode.com/problems/kth-largest-element-in-an-array/", "Medium"),
        ("DP", "Coin Change", "https://leetcode.com/problems/coin-change/", "Medium"),
        ("DP", "Longest Increasing Subsequence", "https://leetcode.com/problems/longest-increasing-subsequence/", "Medium"),
        ("DP", "House Robber", "https://leetcode.com/problems/house-robber/", "Medium"),
        ("DP", "Edit Distance", "https://leetcode.com/problems/edit-distance/", "Hard")
    ]

    cursor.executemany('''
    INSERT INTO practice_problems (topic, problem_name, link, difficulty)
    VALUES (?, ?, ?, ?)
    ''', practice)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    if os.path.exists('horizon.db'):
        os.remove('horizon.db')
    init_db()
    print("Database with Jobs, Prep Materials, Companies, and Practice Questions initialized successfully.")
