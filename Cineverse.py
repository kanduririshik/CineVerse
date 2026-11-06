import random
import datetime


class MovieBooking:

    # ================= INITIALIZATION =================
    def __init__(self):

        # -------- MOVIES --------
        self.movies = {
            1: "Raja Saab",
            2: "KGF 3",
            3: "Peddi",
            4: "Spirit",
            5: "Ustaad Bhagat Singh",
            6: "Kalki",
            7: "Paradise"
        }

        # -------- THEATERS --------
        self.theaters = {
            1: "PVR Cinemas",
            2: "INOX",
            3: "ART Cinemas",
            4: "IMAX",
            5: "AMB Cinemas"
        }

        # -------- TIMINGS --------
        self.timings = {
            1: "7AM - 10AM",
            2: "10AM - 1PM",
            3: "2PM - 5PM",
            4: "7PM - 10PM"
        }

        # -------- SEATS --------
        self.rows = list("ABCDEFGHIJ")
        self.columns = list(range(1, 13))

        self.price = {
            'A': 400, 'B': 400,
            'C': 300, 'D': 300,
            'E': 250, 'F': 250,
            'G': 200, 'H': 200,
            'I': 150, 'J': 150
        }

        self.seats = [['O' for _ in self.columns] for _ in self.rows]

        # -------- FOOD MENU --------
        self.food_menu = {
            1: ("Popcorn", 150),
            2: ("Coke", 80),
            3: ("Momos", 120),
            4: ("Burger", 180)
        }

        # -------- COUPONS --------
        self.coupons = {
            "SAVE10": 0.10,
            "MOVIE20": 0.20
        }

        # -------- BOOKING DATA --------
        self.username = ""
        self.booking_id = ""
        self.selected_movie = ""
        self.selected_theater = ""
        self.selected_date = ""
        self.selected_timings = ""
        self.seats_booked = []
        self.food_order = []
        self.total_price = 0

    # ================= LOGIN =================
    def login(self):
        self.username = input("Enter your name: ")
        print(f"\nWelcome {self.username} to ITS SHOW TIME 🎬")

    # ================= SELECT DATE =================
    def select_date(self):

        today = datetime.date.today()

        print("\nSelect Booking Date")
        print("Format: YYYY-MM-DD")
        print("Today:", today)

        while True:
            date_input = input("Enter the Date: ").strip()

            try:
                user_date = datetime.datetime.strptime(
                    date_input, "%Y-%m-%d").date()

                if user_date < today:
                    print("❌ Cannot select past dates!")
                else:
                    self.selected_date = user_date
                    print("Date selected:", self.selected_date)
                    break

            except:
                print("Invalid format! Example: 2026-02-18")

    # ================= CATEGORY =================
    def seat_category(self, row):
        if row in ['A', 'B']:
            return "Platinum"
        elif row in ['C', 'D', 'E', 'F']:
            return "Gold"
        else:
            return "Silver"

    # ================= MOVIE =================
    def select_movies(self):
        print("\nMovies Available:")
        for k, v in self.movies.items():
            print(k, ".", v)

        choice = int(input("Choose movie: "))
        if choice in self.movies:
            self.selected_movie = self.movies[choice]
            return True
        return False

    # ================= THEATER =================
    def select_theater(self):
        print("\nTheaters:")
        for k, v in self.theaters.items():
            print(k, ".", v)

        choice = int(input("Choose theater: "))
        self.selected_theater = self.theaters[choice]

    # ================= TIMINGS =================
    def select_timings(self):
        print("\nShow Timings:")
        for k, v in self.timings.items():
            print(k, ".", v)

        choice = int(input("Choose timing: "))
        self.selected_timings = self.timings[choice]

    # ================= DISPLAY SEATS =================
    def display_layout(self):
        print("\n   ", end="")
        for c in self.columns:
            print(c, end=" ")
        print()

        for i, r in enumerate(self.rows):
            print(r, " ", " ".join(self.seats[i]))

    # ================= SEAT BOOKING =================
    def select_seats(self):

        while True:
            self.display_layout()

            row = input("Enter row: ").upper()
            col = int(input("Enter column: "))
            
            self.rows = ['A','B','C','D','E','F','G','H','I','J']
            self.columns = list(range(1, 13))

            if row not in self.rows or col not in self.columns:
                print("Invalid seat!")
                continue

            r = self.rows.index(row)
            c = self.columns.index(col)

            if self.seats[r][c] == 'X':
                print("Seat already booked!")
                continue

            price = self.price[row]
            category = self.seat_category(row)

            confirm = input(
                f"{row}{col} ({category}) Rs.{price} confirm? (yes/no): ")

            if confirm.lower() == "yes":
                self.seats[r][c] = 'X'
                self.seats_booked.append((row, col, price))
                print("Seat booked!")

            more = input("Book another seat? (yes/no): ")
            if more.lower() != "yes":
                break

        self.calculate_bill()

    # ================= FOOD ORDER =================
    def order_food(self):

        print("\n🍿 Food Menu")
        for k, v in self.food_menu.items():
            print(f"{k}. {v[0]} - Rs.{v[1]}")

        cart = {}

        while True:
            choice = int(input("Select item (0 to stop): "))

            if choice == 0:
                break

            if choice not in self.food_menu:
                print("Invalid choice")
                continue

            qty = int(input("Quantity: "))
            item, price = self.food_menu[choice]

            if item in cart:
                cart[item]['qty'] += qty
            else:
                cart[item] = {'price': price, 'qty': qty}

            print("Added!")

        self.food_order.clear()

        print("\nFood Summary:")
        for item, data in cart.items():
            total = data['price'] * data['qty']
            self.food_order.append((item, data['qty'], total))
            print(f"{item} x{data['qty']} = Rs.{total}")

        self.calculate_bill()

    # ================= BILL =================
    def calculate_bill(self):

        seat_total = sum(s[2] for s in self.seats_booked)
        food_total = sum(f[2] for f in self.food_order)

        gst = 0.18 * (seat_total + food_total)

        self.total_price = seat_total + food_total + gst

        print("\n----- BILL -----")
        print("Seat Total :", seat_total)
        print("Food Total :", food_total)
        print("GST (18%)  :", round(gst, 2))
        print("Grand Total:", round(self.total_price, 2))

    # ================= COUPON =================
    def apply_coupon(self):

        code = input("Enter coupon code (or press Enter): ").upper().strip()

        if code in self.coupons:
            discount = self.total_price * self.coupons[code]
            self.total_price -= discount
            print("Coupon applied! Saved Rs.", round(discount, 2))
        else:
            print("No coupon applied")

    # ================= PAYMENT =================
    def proceed_to_pay(self):

        choice = input("Proceed to pay? (yes/no): ").strip()

        if choice.lower() == "yes":
            self.booking_id = "BK" + str(random.randint(1000, 9999))

            print("\nPayment Successful ✅")
            print("Booking ID:", self.booking_id)

            self.save_booking()
            self.display_booking()

    # ================= SAVE FILE =================
    def save_booking(self):

        with open("bookings.txt", "a") as f:
            f.write("\n====================\n")
            f.write(f"Booking ID: {self.booking_id}\n")
            f.write(f"User: {self.username}\n")
            f.write(f"Movie: {self.selected_movie}\n")
            f.write(f"Theater: {self.selected_theater}\n")
            f.write(f"Date: {self.selected_date}\n")
            f.write(f"Timing: {self.selected_timings}\n")
            f.write("Seats: " +
                    ", ".join([f"{s[0]}{s[1]}" for s in self.seats_booked]) + "\n")
            f.write(f"Total Paid: {round(self.total_price,2)}\n")
            f.write(f"Saved Time: {datetime.datetime.now()}\n")

    # ================= HISTORY =================
    def view_history(self):

        try:
            with open("bookings.txt", "r") as f:
                data = f.read()

                if data.strip() == "":
                    print("No bookings yet.")
                else:
                    print("\n===== BOOKING HISTORY =====")
                    print(data)

        except FileNotFoundError:
            print("No history found.")

    # ================= ADMIN PANEL =================
    def admin_panel(self):

        password = input("Enter admin password: ").strip()

        if password == "admin123":
            print("\nADMIN MODE")
            self.display_layout()

            reset = input("Reset seats? (yes/no): ").strip()
            if reset.lower() == "yes":
                self.seats = [['O' for _ in self.columns]
                              for _ in self.rows]
                print("All seats reset!")
        else:
            print("Wrong password!")

    # ================= RECEIPT =================
    def display_booking(self):

        print("\n===== BOOKING RECEIPT =====")
        print("User:", self.username)
        print("Movie:", self.selected_movie)
        print("Theater:", self.selected_theater)
        print("Date:", self.selected_date)
        print("Timing:", self.selected_timings)

        print("\nSeats:")
        for s in self.seats_booked:
            print(f"{s[0]}{s[1]}")

        print("Total Paid:", round(self.total_price, 2))
        print("Enjoy your movie 🎬")


# ================= MAIN MENU =================
def main():

    booking = MovieBooking()
    booking.login()

    while True:

        print("\n===== ITS SHOW TIME =====")
        print("1. Book Ticket")
        print("2. View Booking History")
        print("3. Admin Panel")
        print("4. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            if booking.select_movies():
                booking.select_theater()
                booking.select_date()
                booking.select_timings()
                booking.select_seats()
                booking.order_food()
                booking.apply_coupon()
                booking.proceed_to_pay()

        elif choice == '2':
            booking.view_history()

        elif choice == '3':
            booking.admin_panel()

        elif choice == '4':
            print("Thank you for using ITS SHOW TIME!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
