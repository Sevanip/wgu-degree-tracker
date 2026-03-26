import csv
import sqlite3
from datetime import date, datetime, timedelta
import matplotlib.pyplot as plt


def create_and_populate_db():
    conn = sqlite3.connect('wgu_degree.db')  #connect and create the db
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS

    degree_progress (
            course_id TEXT PRIMARY KEY,
            course_name TEXT,
            status TEXT,
            date_finished TEXT,
            date_started TEXT
            )
        ''')



    courses = [ ('D370', 'IT Leadership Foundations', 'Completed', '2024-08-21'),
                ('D491', 'Intoduction to Analytics', 'Completed', '2024-10-06'),
                ('D278', 'Scripting and Programming - Foundations', 'Completed', '2024-11-13'),
                ('D388', 'Fundamentals of Spreadsheets and Data Presentations', 'Completed', '2025-11-20'),
                ('D426', 'Data Management - Foundations', 'Completed', '2025-01-23'),
                ('C721', 'Change Management', 'Completed', '2025-02-07'),
                ('D427', 'Data Management - Applications', 'Completed', '2025-03-11'),
                ('D326', 'Advanced Data Management', 'Completed', '2025-04-15'),
                ('D315', 'Network and Security - Foundations', 'Completed', '2025-06-07'),
                ('D335', 'Introduction to Programming in Python', 'Completed', '2025-07-28'),
                ('D197', 'Version Control', 'Completed', '2025-09-02'),
                ('D428', 'Design Thinking for Business', 'Completed', '2025-10-10'),
                ('D276', 'Web Development Foundations', 'Completed', '2025-10-16'),
                ('D282', 'Cloud Foundations', 'Completed', '2025-12-14'),
                ('D386', 'Hardware and Operating Systems Essentials', 'Completed', '2026-01-13'),
                ('D494', 'Data and Information Governance', 'Completed', '2026-01-24'),
                ('D492', 'Data Analytics - Applications', 'Completed', '2026-02-25'),
                ('D493', 'Scripting and Programming - Applications', 'In Progress', None),
                ('D324', 'Business of IT - Project Management', 'Not Started', None),
                ('D495', 'Big Data Foundations', 'Not Started', None),
                ('D246', 'Influential Communication through Visual Design and Storytelling', 'Not Started', None),
                ('C949', 'Data Structures and Algorithms I', 'Not Started', None),
                ('D496', 'Introduction to Data Science', 'Not Started', None),
                ('D497', 'Data Wrangling', 'Not Started', None),
                ('D498', 'Data Analysis with R', 'Not Started', None),
                ('D499', 'Machine Learning', 'Not Started', None),
                ('D500', 'Data Visualization', 'Not Started', None),
                ('D501', 'Machine Learning DevOps', 'Not Started', None),
                ('D372', 'Introduction to Systems Thinking', 'Not Started', None),
                ('D502', 'Data Analytics Capstone', 'Not Started', None)
                ]

#using executemany to insert the list all at once
    cursor.executemany('''
    INSERT OR IGNORE INTO
    degree_progress (course_id, course_name, status, date_finished)
    VALUES (?, ?, ?, ?)
        ''', courses)

    conn.commit()
    conn.close()
    print("Databade created and courses loaded successfully!")


def migrate_database():
    conn = sqlite3.connect('wgu_degree.db')
    cursor = conn.cursor()

    try:
        # This adds the column to the existing table
        cursor.execute("ALTER TABLE degree_progress ADD COLUMN date_started TEXT")
        conn.commit()
        print("Migration Successful: 'date_started' column added.")
    except sqlite3.OperationalError:
        # If the column already exists, SQLite will throw an error.
        # We catch it so the script doesn't crash.
        print("Note: 'date_started' column already exists.")

    conn.close()

def backfill_start_dates():
    #in order to perform some analysis i want to add start date to my data
    #I used what i learn about handling missing data and my understanding of how wgu works to fill in missing data
    conn = sqlite3.connect('wgu_degree.db')
    cursor = conn.cursor()

    #some start dates i know because it's when my term starts
    term_starts = {
        'D370': '2024-08-01',
        'C721': '2025-02-01',
        'D197': '2025-08-01',
        'D386': '2026-02-01'
    }


    cursor.execute("SELECT course_id, date_finished FROM degree_progress WHERE status = 'Completed' ORDER BY date_finished ASC")
    completed = cursor.fetchall()

    #When i finish a course i start a new one so, the end date of one course is the start date of the one right after it.
    previous_finish = None
    for cid, finish in completed:
        if cid in term_starts:
            start = term_starts[cid]
        else:
            start = previous_finish if previous_finish else '2024-08-01'
            
            cursor.execute("UPDATE degree_progress SET date_started = ? WHERE course_id = ?", (start, cid))
        previous_finish = finish

    conn.commit()
    conn.close()
    print("Historical data backfilled successfully!")



def update_course_status(course_id, new_status):
    conn = sqlite3.connect('wgu_degree.db')  #connect and create the db
    cursor = conn.cursor()

    completion_date = date.today().strftime("%Y-%m-%d") if new_status == 'Completed' else None

    cursor.execute('''
                    UPDATE degree_progress
                    SET status = ?, date_finished = ?
                    WHERE course_id = ?
                ''', (new_status, completion_date, course_id))
    conn.commit()
    conn.close()
    print(f"Updated: {course_id} to {new_status}")

#Adding a view tool to see my progress
def show_my_progress():
    conn = sqlite3.connect('wgu_degree.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM degree_progress")
    rows = cursor.fetchall()

    print("\n--- MY WGU DEGREE TRACKER ---")

    for row in rows:
        print(f"ID: {row[0]} | Status: {row[2]} | Name: {row[1]}")
    conn.close()


def show_graduation_percentage():
    conn = sqlite3.connect('wgu_degree.db')
    cursor = conn.cursor()

    #get the total number of courses in my degree plan
    cursor.execute("SELECT COUNT(*) FROM degree_progress")
    total = cursor.fetchone()[0]

    #get the number of courses i completed
    cursor.execute("SELECT COUNT(*) FROM degree_progress WHERE status = 'Completed' ")
    done = cursor.fetchone()[0]

    conn.close()

    if total > 0:
        percent = (done/total) * 100
        print("\n--- GRADUATION PROGRESS---")
        print(f"Courses Completed: {done}/{total}")
        print(f"Progress: {percent:.1f}%")
        print("Keep going! You're Almost There!")

        if percent == 100:
             print("Congratulations, Graduate!")
    else:
        print("No courses found in the database")

def calculate_velocity():
    conn = sqlite3.connect('wgu_degree.db')
    cursor = conn.cursor()
    cursor.execute("SELECT date_started, date_finished FROM degree_progress WHERE status = 'Completed' AND date_started IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()

    if not rows: return 0

    total_days = 0
    for s, e in rows:
        total_days += (datetime.strptime(e, "%Y-%m-%d") - datetime.strptime(s, "%Y-%m-%d")).days

    return total_days / len(rows)

def export_to_csv():
    conn = sqlite3.connect('wgu_degree.db')
    cursor = conn.cursor()

    #fetch all data
    cursor.execute("SELECT * FROM degree_progress")
    rows = cursor.fetchall()

    #get column names from the db schema
    column_names = [description[0] for description in cursor. description]

    file_name = "wgu_progress_report.csv"

    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names) #writes the header row
        writer.writerows(rows) #write all the data

    conn.close()
    print(f"\nSuccess! Data exported to {file_name}")

def predict_graduation_date():
    conn = sqlite3.connect('wgu_degree.db')
    cursor = conn.cursor()

    #get current velocity
    avg_days = calculate_velocity() #Using my existing function

    #Get count of remaining courses
    cursor.execute("SELECT COUNT(*) FROM degree_progress WHERE status != 'Completed'")
    remaining_count = cursor.fetchone()[0]
    conn.close()

    if avg_days == 0:
        return "Not enough data to predict yet. Complete more Courses!"
    
    #Calculate total estimate days
    total_days_left = remaining_count * avg_days

    #project the date from today
    predicted_date = date.today() + timedelta(days=int(total_days_left))

    return predicted_date, remaining_count, total_days_left

def show_progress_chart():
    conn = sqlite3.connect('wgu_degree.db')
    cursor = conn.cursor()

    #Count courses by status
    cursor.execute("SELECT status, COUNT(*) FROM degree_progress GROUP BY status")
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No data to graph!")
        return
    
    #prepare data for chart
    statuses = [row[0] for row in data]
    counts = [row[1] for row in data]
    colors = ['#2ecc71','#f1c40f', '#e74c3c' ] #Green, Yellow, Red

    #create the plot
    plt.figure(figsize=(8, 6))
    plt.bar(statuses, counts, color=colors[:len(statuses)])

    plt.title('WGU Degree Progress Chart')
    plt.xlabel('Course Status')
    plt.ylabel('Number of Courses')

    #Add a "Goal" line for total courses
    plt.axhline(y=30, color='gray', linestyle='--', label='Total Courses (30)')
    plt.legend()

    print("Opening chart... close window to return to the menu")
    plt.show()