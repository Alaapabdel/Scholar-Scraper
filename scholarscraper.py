import os
import sys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException, NoSuchWindowException
from bs4 import BeautifulSoup
import time
import fitz
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import Menu
from tkinter import PhotoImage

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def download_pdf(url, save_path):
    for _ in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
        except requests.RequestException as e:
            log(f"Error downloading {url}: {e}", "error")
    return False

def is_valid_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        return True
    except:
        return False

def initialize_driver():
    options = Options()
    # Remove headless mode so you can see and solve the CAPTCHA manually
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver_path = resource_path('./driver/chromedriver.exe')
    service = ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def log(message, level="info"):
    if level == "error":
        log_text.insert(tk.END, message + "\n", "error")
    else:
        log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)  # Auto-scroll to the bottom
    root.update()

def search_google_scholar(query, num_papers, save_path):
    driver = initialize_driver()

    def show_captcha_button():
        captcha_button.grid(row=7, column=1, padx=10, pady=10)
        root.update()

    def hide_captcha_button():
        captcha_button.grid_forget()
        root.update()

    try:
        search_url = f"https://scholar.google.com/scholar?hl=en&q={requests.utils.quote(query)}"
        driver.get(search_url)
        time.sleep(3)  # Allow some time for the page to load

        papers_downloaded = 0

        while papers_downloaded < num_papers:
            try:
                # Check for CAPTCHA and pause for manual resolution
                if "captcha" in driver.page_source.lower():
                    log("CAPTCHA detected! Please resolve it manually.", "error")
                    show_captcha_button()
                    captcha_button.wait_variable(captcha_solved)
                    hide_captcha_button()

                # Parse the results
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Process each link on the Google Scholar search results page
                for result in soup.find_all('div', class_='gs_ri'):
                    if papers_downloaded >= num_papers:
                        break
                    pdf_link = result.find('a', href=True)
                    if pdf_link and pdf_link['href'].endswith('.pdf'):
                        pdf_url = pdf_link['href']
                        pdf_name = os.path.basename(pdf_url)
                        pdf_path = os.path.join(save_path, pdf_name)

                        # Download the PDF
                        if download_pdf(pdf_url, pdf_path):
                            if is_valid_pdf(pdf_path):
                                log(f"Downloaded: {pdf_path}")
                                papers_downloaded += 1
                            else:
                                log(f"Corrupted PDF: {pdf_path}", "error")
                                os.remove(pdf_path)
                        else:
                            log(f"Failed to Download: {pdf_url}", "error")

                # Check if the required number of papers has been downloaded
                if papers_downloaded >= num_papers:
                    break

                # Find the "Next" button and navigate to the next page if it exists
                try:
                    next_button = driver.find_element(By.XPATH, "//td/a/span[@class='gs_ico gs_ico_nav_next']/..")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)  # Allow some time for the next page to load
                except (NoSuchElementException, ElementClickInterceptedException) as e:
                    #log(f"No more pages or error finding 'Next' button: {e}", "error")
                    log(f"No more pages or error finding 'Next' button.", "error")
                    break

            except NoSuchWindowException:
                log("Browser window closed. Reinitializing the browser...", "error")
                driver = initialize_driver()
                driver.get(search_url)
                time.sleep(3)  # Allow some time for the page to load

        if papers_downloaded == 0:
            log("No PDFs found for the given topic.", "error")
        else:
            log("All possible PDFs for the topic have been downloaded.", "info")
            
    finally:
        driver.quit()
        prompt_search_again()

def prompt_search_again():
    if messagebox.askyesno("Search Again?", "Do you want to search for a different topic?"):
        query_var.set("")
        num_papers_var.set("")
    else:
        root.quit()

def main():
    def browse_save_path():
        path = filedialog.askdirectory()
        if path:
            save_path_var.set(path)

    def start_download():
        save_path = save_path_var.get()
        query = query_var.get()
        num_papers = num_papers_var.get()

        if not save_path or not query or not num_papers:
            messagebox.showwarning("Input Error", "Please fill out all fields.")
            return

        try:
            num_papers = int(num_papers)
        except ValueError:
            messagebox.showwarning("Input Error", "Number of papers must be an integer!")
            return

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        log_text.delete(1.0, tk.END)  # Clear log text
        search_google_scholar(query, num_papers, save_path)
        messagebox.showinfo("Done", "Download completed!")

    def resolve_captcha():
        captcha_solved.set(True)

    def set_theme(theme):
        if theme == "Floral Theme":
            root.configure(bg="#000000")
            log_text.configure(bg="#44475A", fg="#F8F8F2", insertbackground="#F8F8F2")
            log_text.tag_config("error", foreground="#FF5555")
            banner_label.configure(fg="#FFC4C4", bg="#000000")
            for widget in [save_path_label, query_label, num_papers_label]:
                widget.configure(fg="#FFC4C4", bg="#000000")
            start_button.configure(bg="#FFC4C4", fg="#000000")
            browse_button.configure(bg="#FFC4C4", fg="#000000")
            captcha_button.configure(bg="#FFC4C4", fg="#000000")
        else:  # Default Theme
            root.configure(bg="#F0F0F0")
            log_text.configure(bg="#FFFFFF", fg="#000000", insertbackground="#000000")
            log_text.tag_config("error", foreground="#FF0000")
            banner_label.configure(fg="#000000", bg="#F0F0F0")
            for widget in [save_path_label, query_label, num_papers_label]:
                widget.configure(fg="#000000", bg="#F0F0F0")
            start_button.configure(bg="#F0F0F0", fg="#000000")
            browse_button.configure(bg="#F0F0F0", fg="#000000")
            captcha_button.configure(bg="#F0F0F0", fg="#000000")

    # Set up GUI
    global root, log_text, captcha_button, captcha_solved, query_var, num_papers_var, save_path_var, save_path_label, query_label, num_papers_label, start_button, browse_button
    root = tk.Tk()
    root.title("SCH✿LΛR SCRΛPƎR")

    # Set custom icon
    icon_path = resource_path('icon.png')  # Replace 'your_icon.ico' with the path to your icon file
    root.iconphoto(False, PhotoImage(file=icon_path))

    banner = r"""
   .-'''-.     _______   .---.  .---.     ,-----.      .---.        ____    .-------.     
  / _     \   /   __  \  |   |  |_ _|   .'  .-,  '.    | ,_|      .'  __ `. |  _ _   \    
 (`' )/`--'  | ,_/  \__) |   |  ( ' )  / ,-.|  \ _ \ ,-./  )     /   '  \  \| ( ' )  |    
(_ o _).   ,-./  )       |   '-(_{;}_);  \  '_ /  | :\  '_ '`)   |___|  /  ||(_ o _) /    
 (_,_). '. \  '_ '`)     |      (_,_) |  _`,/ \ _/  | > (_)  )      _.-`   || (_,_).' __  
.---.  \  : > (_)  )  __ | _ _--.   | : (  '\_/ \   ;(  .  .-'   .'   _    ||  |\ \  |  | 
\    `-'  |(  .  .-'_/  )|( ' ) |   |  \ `"/  \  ) /  `-'`-'|___ |  _( )_  ||  | \ `'   / 
 \       /  `-'`-'     / (_{;}_)|   |   '. \_/``".'    |        \\ (_ o _) /|  |  \    /  
  `-...-'     `._____.'  '(_,_) '---'     '-----'      `--------` '.(_,_).' ''-'   `'-'   
   .-'''-.     _______   .-------.       ____    .-------.     .-''-.  .-------.          
  / _     \   /   __  \  |  _ _   \    .'  __ `. \  _(`)_ \  .'_ _   \ |  _ _   \         
 (`' )/`--'  | ,_/  \__) | ( ' )  |   /   '  \  \| (_ o._)| / ( ` )   '| ( ' )  |         
(_ o _).   ,-./  )       |(_ o _) /   |___|  /  ||  (_,_) /. (_ o _)  ||(_ o _) /         
 (_,_). '. \  '_ '`)     | (_,_).' __    _.-`   ||   '-.-' |  (_,_)___|| (_,_).' __       
.---.  \  : > (_)  )  __ |  |\ \  |  |.'   _    ||   |     '  \   .---.|  |\ \  |  |      
\    `-'  |(  .  .-'_/  )|  | \ `'   /|  _( )_  ||   |      \  `-'    /|  | \ `'   /      
 \       /  `-'`-'     / |  |  \    / \ (_ o _) //   )       \       / |  |  \    /       
  `-...-'     `._____.'  ''-'   `'-'   '.(_,_).' `---'        `'-..-'  ''-'   `'-'        
    """

    banner_label = tk.Label(root, text=banner, font=("Courier", 10), fg="#FFC4C4", bg="#000000", justify=tk.LEFT)
    banner_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    save_path_label = tk.Label(root, text="Save Path:", fg="#FFC4C4", bg="#000000")
    save_path_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    save_path_var = tk.StringVar()
    save_path_entry = tk.Entry(root, textvariable=save_path_var, width=50, bg="#44475A", fg="#F8F8F2")
    save_path_entry.grid(row=1, column=1, padx=10, pady=5)
    browse_button = tk.Button(root, text="Browse", command=browse_save_path, bg="#FFC4C4", fg="#000000")
    browse_button.grid(row=1, column=2, padx=10, pady=5)

    query_label = tk.Label(root, text="Search Query:", fg="#FFC4C4", bg="#000000")
    query_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    query_var = tk.StringVar()
    query_entry = tk.Entry(root, textvariable=query_var, width=50, bg="#44475A", fg="#F8F8F2")
    query_entry.grid(row=2, column=1, padx=10, pady=5)

    num_papers_label = tk.Label(root, text="Number of Papers:", fg="#FFC4C4", bg="#000000")
    num_papers_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    num_papers_var = tk.StringVar()
    num_papers_entry = tk.Entry(root, textvariable=num_papers_var, width=50, bg="#44475A", fg="#F8F8F2")
    num_papers_entry.grid(row=3, column=1, padx=10, pady=5)

    start_button = tk.Button(root, text="Start Download", command=start_download, bg="#FFC4C4", fg="#000000")
    start_button.grid(row=4, column=1, padx=10, pady=20)

    log_text = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD, bg="#44475A", fg="#F8F8F2", insertbackground="#F8F8F2")
    log_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
    log_text.tag_config("error", foreground="#FF5555")

    captcha_button = tk.Button(root, text="CAPTCHA Resolved", command=resolve_captcha, bg="#FFC4C4", fg="#000000")
    captcha_solved = tk.BooleanVar(value=False)

    # Create menu bar
    menu_bar = Menu(root)
    root.config(menu=menu_bar)

    # Create "Theme" menu
    theme_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Theme", menu=theme_menu)

    theme_menu.add_command(label="Floral Theme", command=lambda: set_theme("Floral Theme"))
    theme_menu.add_command(label="Default Theme", command=lambda: set_theme("Default Theme"))

    # Set default theme
    set_theme("Default Theme")

    root.mainloop()

if __name__ == "__main__":
    main()
