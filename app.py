import streamlit as st
import sqlite3
import datetime
import random

# Define unique CSS styles
def apply_styles(dark_mode):
    if dark_mode:
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(to right, #333, #666);
                color: #e0e0e0;
            }
            .css-1d391kg {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            .css-18e3th9 {
                background-color: #2c2c2c;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                color: #333;
            }
            .css-1d391kg {
                background-color: #ffffff;
                color: #333;
            }
            .css-18e3th9 {
                background-color: #ffffff;
                border-radius: 10px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }
            </style>
        """, unsafe_allow_html=True)

# Database setup
def create_connection():
    conn = sqlite3.connect('tasks.db')
    return conn

def create_table(conn):
    query = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        priority TEXT,
        due_date DATE,
        category TEXT,
        recurrence TEXT,
        comments TEXT,
        progress INTEGER DEFAULT 0
    )
    '''
    conn.execute(query)
    conn.commit()

def update_task_progress(conn, task_id, progress, status):
    query = '''
    UPDATE tasks
    SET progress = ?, status = ?
    WHERE id = ?
    '''
    conn.execute(query, (progress, status, task_id))
    conn.commit()

def get_task_completion_summary(conn):
    completed_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'").fetchone()[0]
    total_count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    return completed_count, total_count

# Main App Logic
def main():
    conn = create_connection()
    create_table(conn)

    st.title("Task Management System")
    dark_mode = st.sidebar.checkbox("Enable Dark Mode")
    apply_styles(dark_mode)

    menu = ["Home", "Create Task", "View Tasks", "Task Progress Tracker", "Delete Task", "AI Task Suggestions"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome to the Task Management System!")

    elif choice == "Create Task":
        st.subheader("Create Task")
        title = st.text_input("Title")
        description = st.text_area("Description")
        status = st.selectbox("Status", ["Pending", "Ongoing", "Completed"])
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        due_date = st.date_input("Due Date")
        category = st.selectbox("Category", ["Work", "Personal", "Study", "Health", "Leisure"])
        recurrence = st.selectbox("Recurrence", ["None", "Daily", "Weekly", "Monthly"])
        comments = st.text_area("Comments")

        if st.button("Add Task"):
            query = '''
            INSERT INTO tasks (title, description, status, priority, due_date, category, recurrence, comments)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            conn.execute(query, (title, description, status, priority, due_date, category, recurrence, comments))
            conn.commit()
            st.success(f"Task '{title}' added successfully!")

    elif choice == "View Tasks":
        st.subheader("View Tasks")
        tasks = conn.execute("SELECT * FROM tasks").fetchall()
        if tasks:
            for task in tasks:
                st.write(f"**Task ID {task[0]}** | **Title:** {task[1]} | **Status:** {task[3]}")
                st.write(f"Progress: {task[9]}%")
                st.write(f"Description: {task[2]}")
                
                if st.button(f"View Task {task[0]}"):
                    st.write(f"**Task ID {task[0]}** | **Title:** {task[1]} | **Status:** {task[3]}")
                    st.write(f"**Priority:** {task[4]} | **Due Date:** {task[5]} | **Category:** {task[6]}")
                    st.write(f"**Recurrence:** {task[7]} | **Comments:** {task[8]}")
                    st.write(f"**Progress:** {task[9]}%")
        else:
            st.write("No tasks found.")

    elif choice == "Task Progress Tracker":
        st.subheader("Task Progress Tracker")
        completed, total = get_task_completion_summary(conn)
        st.info(f"Tasks Completed: {completed} / {total}")

        tasks = conn.execute("SELECT id, title, progress, status FROM tasks").fetchall()
        if tasks:
            for task in tasks:
                st.write(f"**Task ID {task[0]}: {task[1]}**")
                progress = st.slider(f"Progress for Task {task[0]}", min_value=0, max_value=100, value=task[2])
                status = "Completed" if progress == 100 else task[3]

                if st.button(f"Update Progress for Task {task[0]}"):
                    update_task_progress(conn, task[0], progress, status)
                    st.success(f"Task '{task[1]}' progress updated to {progress}%!")
                    st.rerun()  # This will refresh the app and show the updated task list
        else:
            st.write("No tasks found.")

    elif choice == "Delete Task":
        st.subheader("Delete Task")
        tasks = conn.execute("SELECT id, title FROM tasks").fetchall()
        task_options = {f"Task {task[0]}: {task[1]}": task[0] for task in tasks}

        if task_options:
            selected_task = st.selectbox("Select a Task to Delete", list(task_options.keys()))
            task_id = task_options[selected_task]

            if st.button(f"Delete Task {task_id}"):
                query = "DELETE FROM tasks WHERE id = ?"
                conn.execute(query, (task_id,))
                conn.commit()
                st.success(f"Task ID {task_id} deleted successfully!")
        else:
            st.write("No tasks available for deletion.")

    elif choice == "AI Task Suggestions":
        st.subheader("AI Task Suggestions")
        categories = ["Work", "Personal", "Study", "Health", "Leisure"]
        priorities = ["Low", "Medium", "High"]
        descriptions = {
            "Work": ["Prepare presentation", "Code review", "Submit report"],
            "Personal": ["Plan family outing", "Clean the house", "Grocery shopping"],
            "Study": ["Read research paper", "Complete assignment", "Prepare for exam"],
            "Health": ["Morning exercise", "Doctor's appointment", "Cook healthy meal"],
            "Leisure": ["Watch a movie", "Read a book", "Play a video game"]
        }

        for _ in range(3):
            category = random.choice(categories)
            priority = random.choice(priorities)
            description = random.choice(descriptions[category])
            st.write(f"**Title:** {category} Task | **Priority:** {priority}")
            st.write(f"Description: {description}")
            if st.button(f"Add {category} Task"):
                query = '''
                INSERT INTO tasks (title, description, status, priority, category)
                VALUES (?, ?, 'Pending', ?, ?)
                '''
                conn.execute(query, (f"{category} Task", description, priority, category))
                conn.commit()
                st.success(f"Suggested task '{category} Task' added!")

if __name__ == "__main__":
    main()
