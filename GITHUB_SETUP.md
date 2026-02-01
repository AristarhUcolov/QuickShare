# 🚀 QuickShare - GitHub Repository Setup Guide

## Step 1: Initialize Git Repository

```powershell
# Navigate to project folder
cd "c:\Users\Artur\Desktop\The Projects\Server"

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: QuickShare v2.0 - LAN File Transfer with GUI"
```

## Step 2: Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click **"+"** → **"New repository"**
3. Fill in details:
   - **Repository name**: `quickshare`
   - **Description**: `🚀 Fast and beautiful LAN file sharing with GUI - Transfer files in your local network with drag & drop, QR codes, and multi-language support`
   - **Visibility**: Public ✅ (or Private if you prefer)
   - **DO NOT** initialize with README (we already have one)
4. Click **"Create repository"**

## Step 3: Connect and Push

```powershell
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/quickshare.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Create Release with .exe Files

### Build the executables first:
```powershell
# Build .exe files
python build_all.py
```

### Create GitHub Release:

1. Go to your repository on GitHub
2. Click **"Releases"** (right sidebar)
3. Click **"Create a new release"**
4. Fill in:
   - **Tag version**: `v2.0`
   - **Release title**: `QuickShare v2.0 - Full Release`
   - **Description**:
```markdown
# 🚀 QuickShare v2.0 - Full Release

## ✨ Features
- 🎨 Beautiful modern UI with dark theme
- 📤 Drag & Drop file upload
- 📁 Folder upload with ZIP download
- 🔍 Search and sort files
- 📱 QR code for mobile access
- 🌍 Multi-language (English & Russian)
- 🖥️ Professional GUI launcher

## 📥 Download

Choose your version:
- **QuickShare_GUI.exe** - Full GUI version (Recommended) ⭐
- **QuickShare_Simple.exe** - Lightweight command-line version

## 🚀 Quick Start
1. Download the .exe file
2. Run it
3. Start sharing files!

No installation required! Just run and go.

## 📖 Documentation
See [README.md](README.md) for full documentation in English and Russian.
```

5. **Attach files**: Drag and drop from `dist/` folder:
   - `QuickShare_GUI.exe`
   - `QuickShare_Simple.exe`

6. Click **"Publish release"**

## Step 5: Update README.md (Optional - Add Screenshots)

You can add screenshots later by:

1. Taking screenshots of the app
2. Uploading to GitHub Issues (creates a URL)
3. Adding to README.md:

```markdown
## 📸 Screenshots

### Web Interface
![Web Interface](https://user-images.githubusercontent.com/...)

### GUI Launcher  
![GUI Launcher](https://user-images.githubusercontent.com/...)
```

## Step 6: Add Topics (Tags) to Repository

Go to repository main page:
- Click **⚙️ About** (top right)
- Add topics:
  - `file-sharing`
  - `lan`
  - `python`
  - `flask`
  - `gui`
  - `tkinter`
  - `file-transfer`
  - `qr-code`
  - `multilingual`
  - `drag-and-drop`

## Step 7: Create LICENSE File

If not exists, create `LICENSE` file:

```powershell
# Create LICENSE file
echo "MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE." > LICENSE

git add LICENSE
git commit -m "Add MIT license"
git push
```

## ✅ Checklist

- [ ] Git repository initialized
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] .exe files built
- [ ] Release v2.0 created
- [ ] .exe files attached to release
- [ ] Topics added
- [ ] LICENSE file added
- [ ] README.md looks good on GitHub

## 🎉 Done!

Your repository is now live! Share the link:
```
https://github.com/YOUR_USERNAME/quickshare
```

## 📊 Optional: Add Badge to README

Add download counter badge at top of README.md:

```markdown
![GitHub release](https://img.shields.io/github/v/release/YOUR_USERNAME/quickshare)
![GitHub downloads](https://img.shields.io/github/downloads/YOUR_USERNAME/quickshare/total)
```

---

## 🔄 Future Updates

When you make changes:

```powershell
# Add changes
git add .

# Commit
git commit -m "Description of changes"

# Push
git push

# For new release:
# 1. Build new .exe files
# 2. Create new release on GitHub
# 3. Upload new .exe files
```

---

## 💡 Tips

1. **Good commit messages** help track changes
2. **Regular commits** keep history clean
3. **Releases** make it easy for users to download
4. **Documentation** in multiple languages reaches more users
5. **Screenshots** show what the app looks like

---

## 🌟 Promote Your Project

After publishing:
1. Share on social media
2. Post on Reddit (r/Python, r/selfhosted)
3. Share in programming communities
4. Add to awesome lists
5. Write a blog post

---

**Good luck with your project!** 🚀
