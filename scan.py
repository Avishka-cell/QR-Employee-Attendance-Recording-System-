import cv2
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import Label, Canvas, messagebox, Radiobutton, StringVar
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector

# Database connection
def fetch_data_from_db(qr_data):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='abc'
        )

        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM shedule WHERE id = %s"
        cursor.execute(query, (qr_data,))
        result = cursor.fetchone()

        cursor.close()  # Close the cursor after fetching the result

        if result:
            return result
        else:
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if connection and connection.is_connected():
            connection.close()

def insert_or_update_attendance_record(emp_data, arrival_time=None, departure_time=None):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='abc'
        )

        cursor = connection.cursor()

        if arrival_time:
            query = """
                INSERT INTO attendance (id, arrival, depature, date)
                VALUES (%s, %s, '-', %s)
                ON DUPLICATE KEY UPDATE arrival=%s, date=%s
            """
            values = (emp_data['id'], arrival_time, arrival_time, arrival_time, arrival_time)
        elif departure_time:
            query = """
                UPDATE attendance
                SET depature = %s, date = %s
                WHERE id = %s AND depature = '-'
            """
            values = (departure_time, departure_time, emp_data['id'])

        cursor.execute(query, values)
        connection.commit()
        cursor.close()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Attendance record saved successfully.")
        else:
            messagebox.showerror("Error", "Failed to update attendance record. No matching arrival record found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if connection and connection.is_connected():
            connection.close()

def update_frame(canvas, cap, canvas_width, canvas_height):
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray)
        for obj in decoded_objects:
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(points)
                points = hull

            n = len(points)
            for j in range(n):
                cv2.line(frame, tuple(points[j]), tuple(points[(j + 1) % n]), (0, 255, 0), 3)

            qr_data = obj.data.decode("utf-8")
            emp_data = fetch_data_from_db(qr_data)
            if emp_data:
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if selected_option.get() == "arrival":
                    insert_or_update_attendance_record(emp_data, arrival_time=current_datetime)
                    employee_info = (f"ID: {emp_data['id']}\n"
                                     f"Arrival Time: {current_datetime}")
                else:
                    insert_or_update_attendance_record(emp_data, departure_time=current_datetime)
                    employee_info = (f"ID: {emp_data['id']}\n"
                                     f"Departure Time: {current_datetime}")

                messagebox.showinfo("Employee Details", employee_info)
            else:
                messagebox.showerror("Error", "No data found for the scanned QR code")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((canvas_width, canvas_height))
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        canvas.imgtk = imgtk

    canvas.after(10, update_frame, canvas, cap, canvas_width, canvas_height)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("QR Code Scanner")
    root.geometry("800x600")

    def minimize_window():
        root.iconify()

    def update_time():
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%b/%d/%Y")
        label_time.config(text=current_time)
        label_date.config(text=current_date)
        root.after(1000, update_time)

    canvas_width, canvas_height = 640, 480
    canvas = Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack(pady=20)

    

    label_date = Label(root, font=("Helvetica", 25))
    label_date.pack()

    label_time = Label(root, font=("Helvetica", 14))
    label_time.pack()

    selected_option = StringVar(value="arrival")

    radio_arrival = Radiobutton(root, text="Arrival", variable=selected_option, value="arrival")
    radio_arrival.pack(anchor=tk.W)

    radio_departure = Radiobutton(root, text="Departure", variable=selected_option, value="departure")
    radio_departure.pack(anchor=tk.W)

    cap = cv2.VideoCapture(0)
    update_time()
    update_frame(canvas, cap, canvas_width, canvas_height)
    root.mainloop()

    cap.release()
    cv2.destroyAllWindows()
