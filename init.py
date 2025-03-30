import pymediainfo
import json
import tkinter as tk
from tkinter import filedialog, ttk
import math
import os

root = tk.Tk()
root.title("Sean's Media Info")
root.geometry("400x700")

miStyle = ttk.Style()
miStyle.configure('TFrame', background='white')
miStyle.configure('LowerFrame.TFrame', background='green')

bottomgrid = ttk.Frame(root, style='TFrame')
bottomgrid.pack(fill=tk.BOTH, pady=5, padx=5)

lowergrid = ttk.Frame(root, style='LowerFrame.TFrame')
lowergrid.pack(fill=tk.BOTH, pady=5, padx=5)



# Function to process the file
def process_file():
    file_path = filedialog.askopenfilename(
        title='Choose Your Weapon!',
        filetypes=[
            ('Videos', '*.mkv'),
            ('Videos', '*.mov'),
            ('Videos', '*.avi'),
            ('Videos', '*.mp4'),
            ('Videos', '*.flv'),
            ('Videos', '*.wmv'),
            ('Videos', '*.webm'),
            ('Videos', '*.mpeg'),
            ('Videos', '*.mpg'),
            ('Videos', '*.3gp'),
            ('Videos', '*.ogv'),
            ('Videos', '*.rm'),
            ('Videos', '*.m4v')
        ]
    )

    if not file_path:
        return

    openJsonmi = pymediainfo.MediaInfo.parse(file_path, output="JSON")
    track = json.loads(openJsonmi)["media"]["track"][0]
    video = json.loads(openJsonmi)["media"]["track"][1]
    audio = json.loads(openJsonmi)["media"]["track"][2]

    for widget in bottomgrid.winfo_children():
        widget.destroy()

    create_bold_label(bottomgrid, '', '', 'TRACK')
    create_bold_label(bottomgrid, 'Filepath:', os.path.dirname(track["CompleteName"]))
    create_bold_label(bottomgrid, 'Filename:', track["CompleteName"].split("/")[-1])
    create_bold_label(bottomgrid, 'Format:', track["Format"])
    create_bold_label(bottomgrid, 'Video Codec:', track["Video_Codec_List"])
    create_bold_label(bottomgrid, 'Audio Codec:', audio["Format"])
    create_bold_label(bottomgrid, 'Rounded Duration:', f'{math.ceil(float(track["Duration"]) / 60)}m')
    create_bold_label(bottomgrid, 'QC Time (x1.25):', f'{math.ceil((float(track["Duration"]) / 60) * 1.25)}m')
    create_bold_label(bottomgrid, 'TC Duration:', video["Duration_String4"])
    create_bold_label(bottomgrid, 'File Size:', track["FileSize_String4"], width=500)

    # Video
    create_bold_label(bottomgrid, '', '', 'VIDEO')
    create_bold_label(bottomgrid, f"Width & Height:", f"{video['Width']} x {video['Height']}")
    create_bold_label(bottomgrid, f'Pixel Aspect Ratio:', video["PixelAspectRatio"])
    create_bold_label(bottomgrid, f'Aspect Ratio:',
                      f'{video["DisplayAspectRatio_String"]} {video["DisplayAspectRatio"]}')
    create_bold_label(bottomgrid, f'Framerate:', f'{round(float(video["FrameRate"]))} fps')
    create_bold_label(bottomgrid, f'Color Space:', video["ColorSpace"])
    create_bold_label(bottomgrid, f'Chroma Subsampling:', video["ChromaSubsampling"])
    create_bold_label(bottomgrid, f'Scan Type:', video["ScanType"])
    create_bold_label(bottomgrid, f'Color Primaries:', video["colour_primaries"])

    # Audio
    create_bold_label(bottomgrid, '', '', 'AUDIO')
    create_bold_label(bottomgrid, f'Audio Channels:', audio["Channels"])
    audio_layout = audio["ChannelLayout"].replace('Bfl', 'Ls').replace('Bfr', 'Rs')
    create_bold_label(bottomgrid, f'Channels Layout:', audio_layout)
    create_bold_label(bottomgrid, f'Sample Rate:', audio["SamplingRate_String"])



def create_bold_label(parent, bold_text, regular_text, headline_text='', font_bold=('Helvetica', 10, 'bold'),
                      font_regular=('Helvetica', 10), font_headline=('Helvetica', 12, 'bold', 'underline'), width=100):
    bold_label = ttk.Label(parent, text=bold_text, anchor='w', font=font_bold, background='white', foreground='black')
    bold_label.grid(row=parent.grid_size()[1], column=0, sticky='w')


    regular_label = ttk.Label(parent, text=regular_text, anchor='w', font=font_regular, background='white',
                              foreground='black')
    regular_label.grid(row=parent.grid_size()[1] - 1, column=1, sticky='w')


    if headline_text:
        headline_label = ttk.Label(parent, text=headline_text, anchor='w', font=font_headline, background='white',
                                   foreground='black')
        headline_label.grid(row=parent.grid_size()[1], columnspan=2, sticky='w')



def exit():
    root.quit()


openbutton = ttk.Button(lowergrid, text="Open", command=process_file)
openbutton.pack(anchor='e')

exitbutton = ttk.Button(lowergrid, text="Exit", command=exit)
exitbutton.pack(anchor='e')

root.mainloop()
