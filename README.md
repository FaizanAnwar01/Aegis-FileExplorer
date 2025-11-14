# Python GUI File Manager (OS Mini Project)

A modern, user-friendly file management tool built with Python and Tkinter using `ttkbootstrap` styling. Perform secure move, delete, search, and undo operations on files with real-time feedback and visual interface.

---

##  Features

 Move files by single extension (e.g. `.txt`)  
 Delete files by extension with confirmation  
 Search files by name (partial match supported)  
 List:
- All files in a folder  
- Files matching a specific extension

Undo last delete/move operation via backup ZIP  
Backup created automatically before deletion or move  
Live status updates and progress bar  
Clean and responsive UI with proper layout spacing  
Logs all actions to `logs/file_manager.log`

---

##  GUI Layout

Source Folder  Search Files by Name
Destination Folder Undo Last Action
File Extension (.txt)  Move | Delete
 List Files by Extension List All Files
---


##  How to Run

### 1. Clone or Download
Place these files in the same folder:
- `main.py`
- `file_operations.py`

### 2. Install Required Package
```bash
pip install ttkbootstrap

---

## Run the App

python main.py


---

###  Folder Structure

```
FileManagerProject/  
├── main.py  
├── file_operations.py  
├── logs/  
│   └── file_manager.log  
├── backup/  
│   ├── backup.zip  
│   └── undo_restore/  

---
