import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from wikipedia_api import fetch_revisions

# I thought that the raw timestamp looked weird in the GUI
# so I format it. My formatted one displays all the info
# as a raw one so I hope this is in line with the project
# requirements
def format_timestamp(ts):
    # expects something like "2025‑04‑30T03:01:44Z"
    try:
        if ts.endswith('Z'):
            dt = datetime.datetime.fromisoformat(ts[:-1])
        else:
            dt = datetime.datetime.fromisoformat(ts)
    except ValueError:
        dt = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    # Format with AM/PM
    return dt.strftime("%Y/%m/%d (%I:%M:%S %p)")

def search():
    article = entry.get().strip()
    if not article:
        messagebox.showerror("Input Error", "Please enter an article name.")
        return

    search_btn.config(state=tk.DISABLED)
    status_label.config(text="Searching...") # set to searching while its searching ofc
    root.update_idletasks()

    try:
        result = fetch_revisions(article)
    except ValueError:
        status_label.config(text="Error: Article not found.")
        messagebox.showerror("Error", "Article not found.")
        search_btn.config(state=tk.NORMAL)
        return
    except ConnectionError:
        status_label.config(text="Error: Network issue.")
        messagebox.showerror("Error", "Network error occurred.")
        search_btn.config(state=tk.NORMAL)
        return

    title = result.get("title", article)
    redirected = result.get("redirected", False)
    revisions = result.get("revisions", [])

    info_label.config(text=f"Results for: {title}" + (" (redirected)" if redirected else ""))

    # clear existing table rows
    # (this is for if the user does anothre search
    # but there is a search already happened)
    for row in tree.get_children():
        tree.delete(row)

    # insert into table
    for idx, rev in enumerate(revisions, start=1):
        ts_raw = rev.get('timestamp', '')
        user = rev.get('user', '')
        ts_fmt = format_timestamp(ts_raw)
        tree.insert("", tk.END, values=(idx, ts_fmt, user))

    status_label.config(text=f"{len(revisions)} revisions loaded.")
    search_btn.config(state=tk.NORMAL)

# GUI setup
# tkinter was not my strong suit so fun fact about development of this
# I actually made this in uikit catalyst and then redid it in tkinter
# bc i had more experience with uikit so i worked more comfortable with it
# if that makes any sense
#
# to be honest i probably should have more comments under these
# but i have no idea what to comment on because it's kind of basic
# gui stuff, like once i explain for one item I'm creating its frame
# there really isn't a reason to explain it for all other items, if anyone
# knows stuff I can say aboiut it ig lmk
root = tk.Tk()
root.title("CS222 Project 1")

frame_top = ttk.Frame(root, padding=10)
frame_top.pack(fill=tk.X)

ttk.Label(frame_top, text="Enter Wikipedia Article Name:").pack(side=tk.LEFT)
entry = ttk.Entry(frame_top, width=40)
entry.pack(side=tk.LEFT, padx=(5, 0))
search_btn = ttk.Button(frame_top, text="Search", command=search)
search_btn.pack(side=tk.LEFT, padx=(5, 0))

info_label = ttk.Label(root, text="Results for: -", padding=(10,5))
info_label.pack(anchor=tk.W)

frame_table = ttk.Frame(root, padding=10)
frame_table.pack(fill=tk.BOTH, expand=True)

cols = ("#", "Timestamp", "User")
tree = ttk.Treeview(frame_table, columns=cols, show="headings", selectmode="browse")
tree.heading("#", text="#")
tree.heading("Timestamp", text="Timestamp")
tree.heading("User", text="User")
tree.column("#", width=30, anchor=tk.CENTER)
tree.column("Timestamp", width=200, anchor=tk.W)
tree.column("User", width=150, anchor=tk.W)

vsb = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

status_label = ttk.Label(root, text="Idle.", padding=(10,5))
status_label.pack(anchor=tk.W)

root.mainloop()