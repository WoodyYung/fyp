import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os

# Check for required dependencies
try:
    import openpyxl
except ImportError:
    print("Required package 'openpyxl' is missing.")
    print("Please install it using: pip install openpyxl")
    sys.exit(1)

class HotelScraperGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hotels Scraper")
        self.root.geometry("800x600")

        # Styles
        self.title_font = ("Helvetica", 16, "bold")
        self.label_font = ("Helvetica", 12)
        self.button_font = ("Helvetica", 12, "bold")
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.button_text_color = "white"

        self.root.configure(bg=self.bg_color)
        self.setup_gui()
        self.setup_results_window()  # Add this line

    def setup_gui(self):
        # Title
        tk.Label(self.root, text="Hotels Scraper", font=self.title_font, bg=self.bg_color).pack(pady=10)

        # Create main frame with two columns
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid columns to be equal width
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(3, weight=1)

        # Left column inputs
        self.create_input_field(main_frame, "City:", 0, 0)
        self.create_input_field(main_frame, "Country:", 1, 0)
        
        # Right column inputs
        self.create_date_section(main_frame, 0, 2)  # New method for dates
        self.create_travelers_section(main_frame, 2, 0)  # New method for traveler inputs
        
        # Output path selection (spans both columns)
        self.create_path_selection(main_frame, 5, 0)
        
        # Status text (spans both columns)
        self.status_text = tk.Text(main_frame, height=8, width=60, font=("Helvetica", 10))
        self.status_text.grid(row=6, column=0, columnspan=4, pady=10, padx=5, sticky="ew")

        # Scrape button (spans both columns)
        tk.Button(
            main_frame,
            text="Start Scraping",
            font=self.button_font,
            bg=self.button_color,
            fg=self.button_text_color,
            command=self.start_scraping
        ).grid(row=7, column=0, columnspan=4, pady=10)

    def create_input_field(self, parent, label, row, col):
        tk.Label(parent, text=label, font=self.label_font, bg=self.bg_color).grid(row=row, column=col, pady=5, padx=5, sticky="e")
        entry = tk.Entry(parent, font=self.label_font)
        entry.grid(row=row, column=col+1, pady=5, padx=5, sticky="ew")
        setattr(self, label.lower().replace(":", ""), entry)

    def create_date_section(self, parent, row, col):
        # Check-in date
        tk.Label(parent, text="Check-in Date:", font=self.label_font, bg=self.bg_color).grid(row=row, column=col, pady=5, padx=5, sticky="e")
        self.checkin_date = tk.Entry(parent, font=self.label_font)
        self.checkin_date.grid(row=row, column=col+1, pady=5, padx=5, sticky="ew")
        self.checkin_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Check-out date
        tk.Label(parent, text="Check-out Date:", font=self.label_font, bg=self.bg_color).grid(row=row+1, column=col, pady=5, padx=5, sticky="e")
        self.checkout_date = tk.Entry(parent, font=self.label_font)
        self.checkout_date.grid(row=row+1, column=col+1, pady=5, padx=5, sticky="ew")
        self.checkout_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def create_travelers_section(self, parent, row, col):
        # Create a frame for travelers info
        travelers_frame = ttk.LabelFrame(parent, text="Travelers Info", padding="5")
        travelers_frame.grid(row=row, column=col, columnspan=4, pady=10, padx=5, sticky="ew")
        
        # Create three columns for Adults, Children, and Rooms
        for i, label in enumerate(["Adults", "Children", "Rooms"]):
            tk.Label(travelers_frame, text=label, font=self.label_font, bg=self.bg_color).grid(row=0, column=i*2, pady=5, padx=5)
            spinbox = ttk.Spinbox(travelers_frame, from_=1, to=10, width=5)
            spinbox.grid(row=0, column=i*2+1, pady=5, padx=15)
            spinbox.set(1)
            setattr(self, label.lower(), spinbox)

    def create_path_selection(self, parent, row, col):
        tk.Label(parent, text="Save Location:", font=self.label_font, bg=self.bg_color).grid(row=row, column=col, pady=5, padx=5, sticky="e")
        self.path_var = tk.StringVar(value=os.getcwd())
        path_entry = tk.Entry(parent, textvariable=self.path_var, font=self.label_font)
        path_entry.grid(row=row, column=col+1, columnspan=2, pady=5, padx=5, sticky="ew")
        tk.Button(parent, text="Browse", command=self.browse_path).grid(row=row, column=col+3, pady=5, padx=5)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def log_message(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update()

    def setup_results_window(self):
        # Create a new window for results
        self.results_window = None
        self.tree = None

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        
        try:
            if col == "Price":
                # Remove 'EGP', commas, and whitespace, then convert to float
                l.sort(key=lambda t: float(''.join(filter(str.isdigit, t[0]))) if t[0] != "N/A" else -1, reverse=reverse)
            elif col == "Rating":
                l.sort(key=lambda t: float(t[0]) if t[0] != "N/A" else -1, reverse=reverse)
            else:
                l.sort(reverse=reverse)
        except ValueError:
            # Fallback to string sorting if conversion fails
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def create_charts(self, hotels_list):
        def format_hotel_name(name, max_length=20):
            return str(name)[:max_length] + ('...' if len(str(name)) > max_length else '')

        def show_price_chart():
            try:
                data = []
                for hotel in hotels_list:
                    try:
                        if hotel['Price'] != "N/A":
                            price_str = ''.join(filter(str.isdigit, hotel['Price']))
                            if price_str:
                                price = float(price_str)
                                data.append((price, format_hotel_name(hotel['Hotel'])))
                    except (ValueError, KeyError):
                        continue
                
                if data:
                    # Sort by price in descending order and take top 10
                    data.sort(reverse=True)
                    data = data[:10]
                    prices, names = zip(*data)
                    
                    plt.figure(figsize=(12, 6))
                    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial']
                    bars = plt.bar(range(len(prices)), prices)
                    plt.xticks(range(len(prices)), names, rotation=45, ha='right')
                    plt.title('Top 10 Most Expensive Hotels', fontsize=12)
                    plt.xlabel('Hotels', fontsize=10)
                    plt.ylabel('Price (HKD)', fontsize=10)
                    
                    # Add value labels with HKD
                    for bar in bars:
                        height = bar.get_height()
                        plt.text(bar.get_x() + bar.get_width()/2., height,
                                f'HKD {int(height):,}',
                                ha='center', va='bottom')
                    
                    plt.tight_layout()
                    plt.show()
                else:
                    messagebox.showwarning("No Data", "No valid price data available to display")
            except Exception as e:
                messagebox.showerror("Error", f"Error creating price chart: {str(e)}")

        def show_rating_chart():
            try:
                data = []
                for hotel in hotels_list:
                    try:
                        rate = hotel['Overall Rate']
                        if rate != "N/A":
                            score = ''.join(c for c in rate if c.isdigit() or c == '.')
                            if score:
                                rating = float(score)
                                if 0 <= rating <= 10:
                                    data.append((rating, format_hotel_name(hotel['Hotel'])))
                    except (ValueError, KeyError, IndexError):
                        continue
                
                if data:
                    # Sort by rating in descending order and take top 10  
                    data.sort(reverse=True)
                    data = data[:10]
                    ratings, names = zip(*data)
                    
                    plt.figure(figsize=(12, 6))
                    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial']  # Better font support
                    bars = plt.bar(range(len(ratings)), ratings)
                    plt.xticks(range(len(ratings)), names, rotation=45, ha='right')
                    plt.title('Top 10 Highest Rated Hotels', fontsize=12)
                    plt.xlabel('Hotels', fontsize=10)
                    plt.ylabel('Rating', fontsize=10)
                    
                    # Add value labels
                    for bar in bars:
                        height = bar.get_height()
                        plt.text(bar.get_x() + bar.get_width()/2., height,
                                f'{height:.1f}',
                                ha='center', va='bottom')
                    
                    plt.tight_layout()
                    plt.show()
                else:
                    messagebox.showwarning("No Data", "No valid rating data available to display")
            except Exception as e:
                messagebox.showerror("Error", f"Error creating rating chart: {str(e)}")

        return show_price_chart, show_rating_chart

    def show_results(self, hotels_list):
        try:
            # Create new window if it doesn't exist or was closed
            if not self.results_window or not tk.Toplevel.winfo_exists(self.results_window):
                self.results_window = tk.Toplevel(self.root)
                self.results_window.title("Hotels Results")
                self.results_window.geometry("800x600")

                # Create buttons frame
                buttons_frame = ttk.Frame(self.results_window)
                buttons_frame.pack(side="top", fill="x", padx=5, pady=5)

                # Add chart buttons
                show_price_chart, show_rating_chart = self.create_charts(hotels_list)
                ttk.Button(buttons_frame, text="Show Price Chart", command=show_price_chart).pack(side="left", padx=5)
                ttk.Button(buttons_frame, text="Show Rating Chart", command=show_rating_chart).pack(side="left", padx=5)

                # Create Treeview
                self.tree = ttk.Treeview(self.results_window, columns=("Hotel", "Price", "Rating"), show="headings")
                
                # Configure columns with sort functionality
                for col in ("Hotel", "Price", "Rating"):
                    self.tree.heading(col, text=col, command=lambda c=col: self.treeview_sort_column(self.tree, c, False))
                
                # Configure column widths
                self.tree.column("Hotel", width=400)
                self.tree.column("Price", width=150)
                self.tree.column("Rating", width=150)

                # Add scrollbar
                scrollbar = ttk.Scrollbar(self.results_window, orient="vertical", command=self.tree.yview)
                self.tree.configure(yscrollcommand=scrollbar.set)

                # Pack elements
                self.tree.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

            else:
                # Clear existing items
                for item in self.tree.get_children():
                    self.tree.delete(item)

            # Insert data
            for hotel in hotels_list:
                try:
                    name = hotel['Hotel']
                    price = hotel['Price']
                    rating = hotel['Overall Rate'].split('-')[0].strip() if hotel['Overall Rate'] != "N/A" else "N/A"
                    self.tree.insert("", "end", values=(name, price, rating))
                except Exception as e:
                    self.log_message(f"Error adding hotel to display: {str(e)}")

        except Exception as e:
            self.log_message(f"Error showing results: {str(e)}")

    def start_scraping(self):
        # Get all input values
        params = {
            'city': self.city.get(),
            'country': self.country.get(),
            'checkin_date': self.checkin_date.get(),
            'checkout_date': self.checkout_date.get(),
            'adults_no': self.adults.get(),
            'children_no': self.children.get(),
            'rooms_no': self.rooms.get(),
            'path': self.path_var.get().strip()
        }
        
        # Validate inputs
        if not all(params.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        self.log_message("Starting scraping process...")
        
        try:
            with sync_playwright() as p:
                # Construct the booking.com URL with query parameters
                page_url = f'https://www.booking.com/searchresults.html?ss={params["city"]}%2C+{params["country"]}&checkin={params["checkin_date"]}&checkout={params["checkout_date"]}&group_adults={params["adults_no"]}&no_rooms={params["rooms_no"]}&group_children={params["children_no"]}'
                self.log_message(f"Navigating to: {page_url}")

                # Launch browser
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()

                # Navigate to URL
                try:
                    page.goto(page_url, timeout=30000)
                    page.wait_for_load_state("networkidle", timeout=30000)
                except Exception as e:
                    raise Exception(f"Navigation failed: {str(e)}\nPlease check your internet connection.")

                # Handle popup
                try:
                    x_sign_in = page.get_by_role("button", name="Dismiss sign-in info.")
                    x_sign_in.wait_for(timeout=10000)
                    x_sign_in.click()
                except Exception:
                    self.log_message("Warning: Could not dismiss sign-in popup. Continuing anyway...")

                # Initialize pagination
                next_button = page.get_by_text('Load more results')

                # Scroll and load all listings
                while True:
                    page.keyboard.press("End")
                    self.log_message("Scrolling down...")
                    page.wait_for_load_state("networkidle")
                    try:
                        next_button.wait_for()
                        next_button.click()
                    except Exception:
                        hotels = page.get_by_test_id("property-card").all()
                        break

                self.log_message(f"Number of hotels found: {len(hotels)}")
                self.log_message("Extracting data from search results...")

                # Extract hotel details
                hotels_list = []
                for hotel in hotels:
                    hotel_dict = {}
                    try:
                        hotel_dict['Hotel'] = hotel.get_by_test_id("title").inner_text()
                    except Exception:
                        hotel_dict['Hotel'] = "N/A"
                    
                    try:
                        hotel_dict['Price'] = hotel.get_by_test_id("price-and-discounted-price").inner_text().replace('&nbsp;', ' ').strip()
                    except Exception:
                        hotel_dict['Price'] = "N/A"
                    
                    try:
                        hotel_dict['Taxes & Charges'] = hotel.get_by_test_id("taxes-and-charges").inner_text().replace('taxes and fees', '').replace('+', '').replace('&nbsp;', ' ').replace('Includes ', 'EGP 0').strip()
                    except Exception:
                        hotel_dict['Taxes & Charges'] = "N/A"

                    try:
                        hotel_dict['Total Cost'] = f"EGP {int(hotel_dict['Price'].replace('EGP', '').replace(',','').strip()) + int(hotel_dict['Taxes & Charges'].replace('EGP', '').replace(',','').strip())}"
                    except ValueError:
                        hotel_dict['Total Cost'] = "N/A"

                    review_count = hotel.get_by_test_id("review-score").locator('//div[2]/div[2]')
                    if review_count.is_visible():
                        try:
                            hotel_dict['Reviews Count'] = review_count.inner_text()
                        except Exception:
                            hotel_dict['Reviews Count'] = "N/A"
                    else:
                        hotel_dict['Reviews Count'] = "N/A"
                    
                    overall_rate = hotel.get_by_test_id("review-score").locator('//div[1]/div[1]')
                    gpa = hotel.get_by_test_id("review-score").locator('//div[2]/div[1]')

                    if overall_rate.is_visible() and gpa.is_visible():
                        hotel_dict['Overall Rate'] = overall_rate.inner_text().replace('Scored ', '') + " - " + gpa.inner_text()
                    else:
                        hotel_dict['Overall Rate'] = "N/A"

                    hotels_list.append(hotel_dict)

                # Save results
                if hotels_list:
                    df = pd.DataFrame(hotels_list)
                    filename = "hotels_list.xlsx"
                    full_path = os.path.join(params['path'], filename)
                    
                    try:
                        os.makedirs(params['path'], exist_ok=True)
                        df.to_excel(full_path, index=False)
                        self.log_message(f"Excel file created successfully at: {full_path}")
                        # Show results in table view instead of matplotlib
                        self.show_results(hotels_list)
                    except Exception as e:
                        fallback_path = os.path.join(os.getcwd(), filename)
                        df.to_excel(fallback_path, index=False)
                        self.log_message(f"Saved to fallback location: {fallback_path}")
                else:
                    self.log_message("No hotels found!")

                browser.close()
                self.log_message("Scraping completed!")

        except Exception as e:
            self.log_message(f"Error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = HotelScraperGUI()
    app.run()
