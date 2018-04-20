import urllib.request, re, sys
from bs4 import BeautifulSoup 
from tkinter import *
from tkinter import messagebox, filedialog

def format(string):
    """Convert input appropriate for url"""
    return re.sub(r" ","",string.lower())

def get_lyrics(event):
    """Get lyrics from azlrics and show in Text"""
    lyricsText.delete('1.0',END)
    artist = format(artistEntry.get())
    song = format(songEntry.get())

    url = 'https://www.azlyrics.com/lyrics/'+ artist + "/" + song + '.html'
    try: 
        html = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        messagebox.showerror("Error", e.reason)
        return 
    soup = BeautifulSoup(html,"html.parser")
    container = soup.find_all('div')[21]
    lyrics = container.text
    lyricsText.insert(INSERT, lyrics)

def save_file(event):
    """Save as text file"""
    f = filedialog.asksaveasfile(mode='w', defaultextension="*.txt", filetypes = (("text files","*.txt"),("all files","*.*")))
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save = str(lyricsText.get(1.0, END)) # starts from `1.0`, not `0.0`
    f.write(text2save)
    f.close() # `()` was missing.


#GUI application

root = Tk()
root.minsize(width=500,height=500)
root.maxsize(width=700,height=500)
root.title("Lyrics Finder")

Label(root,text="Artist:").grid(row=0,sticky=W,padx=220)

artistEntry = Entry(root)
artistEntry.grid(row=0, pady=10)

Label(root,text="Song:").grid(row=1, sticky=W, padx=220)

songEntry = Entry(root)
songEntry.grid(row=1, pady=10)

search = Button(root, text="Search")
search.bind("<ButtonRelease-1>",get_lyrics)
search.grid(row=3, pady=5)

frame = Frame(root,relief = SUNKEN)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

scrollbar = Scrollbar(frame)
scrollbar.grid(row=0, column=1, sticky=N+S)

lyricsText = Text(frame, wrap=NONE, bd=0, yscrollcommand=scrollbar.set)
lyricsText.insert(INSERT,"Search for song lyrics by entering artist and song name.")
lyricsText.grid(row=0, column=0, sticky=N+S+E+W)

scrollbar.config(command=lyricsText.yview)

frame.grid(row=4)

save = Button(root, text="Save")
save.bind("<ButtonRelease-1>",save_file)
save.grid(row=4,column=1)

root.mainloop()