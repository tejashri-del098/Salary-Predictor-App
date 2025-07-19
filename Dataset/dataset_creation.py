import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for generating realistic data
fake = Faker()

def generate_employee_salary_dataset(num_rows=5000):
    """
    Generates a synthetic employee salary dataset.

    Args:
        num_rows (int): The number of rows (employees) to generate.

    Returns:
        pandas.DataFrame: A DataFrame containing the generated dataset.
    """

    data = []

    # Define possible categories for various features
    departments = [
        "Human Resources", "Engineering", "Sales", "Marketing",
        "Finance", "Operations", "Customer Support", "Research & Development",
        "Legal", "IT"
    ]
    job_titles_by_department = {
        "Human Resources": ["HR Manager", "HR Specialist", "Recruiter", "HR Coordinator"],
        "Engineering": ["Software Engineer", "Senior Software Engineer", "DevOps Engineer", "QA Engineer", "Engineering Manager"],
        "Sales": ["Sales Representative", "Account Manager", "Sales Manager", "Business Development Rep"],
        "Marketing": ["Marketing Specialist", "Content Creator", "SEO Analyst", "Marketing Manager"],
        "Finance": ["Financial Analyst", "Accountant", "Finance Manager", "Auditor"],
        "Operations": ["Operations Manager", "Logistics Coordinator", "Supply Chain Analyst"],
        "Customer Support": ["Customer Support Rep", "Customer Success Manager"],
        "Research & Development": ["Research Scientist", "Data Scientist", "R&D Engineer"],
        "Legal": ["Legal Counsel", "Paralegal"],
        "IT": ["IT Support Specialist", "Network Administrator", "System Administrator", "Cybersecurity Analyst"]
    }
    education_levels = ["High School", "Associate's Degree", "Bachelor's Degree", "Master's Degree", "PhD"]

    # Base salary ranges for different education levels and job titles
    # This makes the salary generation more realistic
    education_salary_boost = {
        "High School": 1.0,
        "Associate's Degree": 1.1,
        "Bachelor's Degree": 1.3,
        "Master's Degree": 1.6,
        "PhD": 2.0
    }

    job_title_salary_multiplier = {
        "HR Coordinator": 1.0, "HR Specialist": 1.1, "Recruiter": 1.2, "HR Manager": 1.5,
        "Software Engineer": 1.3, "QA Engineer": 1.2, "DevOps Engineer": 1.4, "Senior Software Engineer": 1.7, "Engineering Manager": 2.0,
        "Sales Representative": 1.1, "Business Development Rep": 1.2, "Account Manager": 1.4, "Sales Manager": 1.6,
        "Marketing Specialist": 1.1, "Content Creator": 1.05, "SEO Analyst": 1.15, "Marketing Manager": 1.5,
        "Financial Analyst": 1.2, "Accountant": 1.1, "Auditor": 1.3, "Finance Manager": 1.5,
        "Logistics Coordinator": 1.0, "Supply Chain Analyst": 1.1, "Operations Manager": 1.4,
        "Customer Support Rep": 1.0, "Customer Success Manager": 1.2,
        "Research Scientist": 1.5, "Data Scientist": 1.6, "R&D Engineer": 1.4,
        "Paralegal": 1.0, "Legal Counsel": 1.5,
        "IT Support Specialist": 1.0, "Network Administrator": 1.2, "System Administrator": 1.3, "Cybersecurity Analyst": 1.4
    }

    for i in range(num_rows):
        employee_id = 10000 + i
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}@{fake.domain_name()}"
        phone_number = fake.phone_number()

        # Generate hire date within a reasonable past range (e.g., last 20 years)
        hire_date = fake.date_between(start_date='-20y', end_date='today')
        
        # Calculate years of experience based on hire date
        # Assuming current date is today for simplicity in a synthetic dataset
        years_of_experience = (datetime.now().year - hire_date.year) - \
                              (1 if (datetime.now().month, datetime.now().day) < (hire_date.month, hire_date.day) else 0)
        years_of_experience = max(0, years_of_experience + random.randint(-2, 2)) # Add some variance
        years_of_experience = min(years_of_experience, 30) # Cap experience at 30 years

        department = random.choice(departments)
        job_title = random.choice(job_titles_by_department[department])
        education_level = random.choice(education_levels)
        city = fake.city()
        state = fake.state_abbr()

        # Calculate base salary with some randomness
        base_salary = random.uniform(40000, 120000)

        # Adjust salary based on years of experience, education level, and job title
        salary = base_salary * (1 + years_of_experience * 0.02) # 2% increase per year of experience
        salary *= education_salary_boost.get(education_level, 1.0)
        salary *= job_title_salary_multiplier.get(job_title, 1.0)

        # Add some random noise to the final salary
        salary = salary * random.uniform(0.9, 1.1)
        salary = round(salary, 2) # Round to 2 decimal places

        data.append([
            employee_id, first_name, last_name, email, phone_number,
            hire_date.strftime('%Y-%m-%d'), department, job_title,
            years_of_experience, education_level, city, state, salary
        ])

    # Create a Pandas DataFrame
    df = pd.DataFrame(data, columns=[
        "employee_id", "first_name", "last_name", "email", "phone_number",
        "hire_date", "department", "job_title", "years_of_experience",
        "education_level", "city", "state", "salary"
    ])

    return df

if __name__ == "__main__":
    print("Generating employee salary dataset...")
    employee_df = generate_employee_salary_dataset(num_rows=5000)

    # Save the DataFrame to a CSV file
    file_name = "employee_salary_dataset.csv"
    employee_df.to_csv(file_name, index=False)
    print(f"Dataset with {len(employee_df)} rows and {len(employee_df.columns)} features generated successfully!")
    print(f"Saved to {file_name}")
    print("\nFirst 5 rows of the generated dataset:")
    print(employee_df.head())
