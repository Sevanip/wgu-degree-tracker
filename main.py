import degree_tracker as dt

def main_menu():
    while True:
        print("\n1. View Progress\n2. Update Course\n3. Show Analytics\n4. Run Backfill\n5. Export to CSV\n6. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            dt.show_my_progress()
        elif choice == '2':
            cid = input("Enter Course ID: ").upper()
            stat = input("Enter new status(Completed/In Progress/Not Started): ")
            dt.update_course_status(cid, stat)
        elif choice == '3':
            dt.show_graduation_percentage()
            velocity = dt.calculate_velocity()
            if velocity > 0:
                print(f"Average Pace: {velocity:.1f} days per course")

                #New Prediction
                prediction, rem_courses, days_left = dt.predict_graduation_date()
                print(f"\n---PREDCTIVE ANALYTICS---")
                print(f"Remaining Courses: {rem_courses}")
                print(f"Estimated Days Remaining: {int(days_left)} days")
                print(f"Projected Graduation Date: {prediction.strftime('%B %Y')}")
                print(f"Based on your current speed, you're finishing in {prediction.year}!")
            else:
                print("Run backfill (option 4) to see pace analytics")
        elif choice == '4':
            dt.backfill_start_dates()
        elif choice == '5':
            dt.export_to_csv()
        elif choice == '6':
            break
        

if __name__ == "__main__":
    #No longer need to create and populate database.
    #migrate_database()
    #create_and_populate_db()
    main_menu()