from degree_tracker import show_graduation_percentage, show_my_progress, update_course_status, backfill_start_dates, export_to_csv, migrate_database, create_and_populate_db, calculate_velocity

def main_menu():
    while True:
        print("\n1. View Progress\n2. Update Course\n3. Show Analytics\n4. Run Backfill\n5. Export to CSV\n6. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            show_my_progress()
        elif choice == '2':
            cid = input("Enter Course ID: ").upper()
            stat = input("Enter new status(Completed/In Progress/Not Started): ")
            update_course_status(cid, stat)
        elif choice == '3':
            show_graduation_percentage()
            velocity = calculate_velocity()
            if velocity > 0:
                print(f"Average Pace: {velocity:.1f} days per course")
            else:
                print("Run backfill (option 4) to see pace analytics")
        elif choice == '4':
            backfill_start_dates()
        elif choice == '5':
            export_to_csv()
        elif choice == '6':
            break
        

if __name__ == "__main__":
    #No longer need to create and populate database.
    #migrate_database()
    #create_and_populate_db()
    main_menu()