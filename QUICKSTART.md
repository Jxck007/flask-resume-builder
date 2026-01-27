# Flask Resume Builder - Quick Start

## 🚀 Getting Started (2 minutes)

### Prerequisites
- Python 3.7+ installed
- Virtual environment (included)
- Modern web browser

### Step 1: Navigate to Project
```bash
cd flask-resume-builder
```

### Step 2: Activate Virtual Environment
**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application
```bash
python main.py
```

You should see:
```
 * Serving Flask app 'website'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 5: Open in Browser
Click or navigate to: **http://localhost:5000**

---

## 🎨 Try It Out!

### Test Theme Toggle
1. Look in navbar for theme button (🌙)
2. Click to cycle through themes
3. Watch smooth color transitions
4. Refresh page - theme stays! ✓

### Test Resume Features
1. Sign up with test account
2. Create a new resume
3. Upload a profile picture
4. Fill in your information
5. Click "Download PDF" - watch it pulse!
6. Open downloaded file to verify

### Test Image Upload
1. Upload a profile picture
2. Upload a different picture
3. Verify only new image shows (no overlapping)
4. Hard refresh (Ctrl+Shift+R) - still shows correct image ✓

---

## 📊 What's New in Phase 2

✨ **Modern Themes**
- Light (default, bright)
- Dark (perfect for evening)
- Minimal (clean, professional)

✨ **Smooth Animations**
- Form sections slide in
- Resume sections appear with stagger
- Buttons lift on hover
- Download button pulses
- Theme transitions smoothly

✨ **Bug Fixes**
- PDF download now works reliably
- Image upload no longer shows old images
- No browser caching conflicts
- Better error handling

---

## 📁 Project Structure

```
flask-resume-builder/
├── main.py                    # Application entry point
├── requirements.txt           # Dependencies
├── website/
│   ├── __init__.py           # Flask app factory
│   ├── auth.py               # Login/signup routes
│   ├── views.py              # Main app routes (UPDATED)
│   ├── models.py             # Database models
│   ├── static/
│   │   ├── style.css         # Styling (UPDATED with themes/animations)
│   │   ├── script.js         # JavaScript (UPDATED with theme toggle)
│   │   ├── resume_*.html     # Resume templates
│   │   └── uploads/          # User profile pictures
│   └── templates/
│       ├── base.html         # Base template (UPDATED)
│       ├── home.html         # Home page
│       ├── resumetemplate.html # Resume editor
│       └── resume_base.html   # Resume viewer (UPDATED)
├── instance/                 # Database file
├── IMPROVEMENTS_PHASE2.md     # Detailed changes
├── TESTING_GUIDE.md           # Testing instructions
└── IMPLEMENTATION_SUMMARY.md  # Complete overview
```

---

## 🔧 Troubleshooting

### Python Not Found
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

### Port Already in Use
```bash
# Run on different port
python main.py --port 5001
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### CSS Not Loading
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Clear browser cache
- Check browser console (F12)

### Theme Not Persisting
- Clear localStorage: 
  - Open DevTools (F12)
  - Application → LocalStorage → Clear All
  - Refresh page

### PDF Download Fails
- Check browser console (F12) for errors
- Verify Playwright installed: `pip install playwright`
- Download Playwright browsers: `playwright install chromium`

---

## 📝 File Modifications Summary

### views.py
- Added `_generate_pdf_async()` for reliable PDF generation
- Enhanced image upload with unique filenames
- Added proper error handling and cleanup
- Imports: `time`, `uuid`, `datetime`, `os`

### style.css (795 lines)
- Added CSS variables for theming
- Added 8 animation keyframes
- Theme definitions: light, dark, minimal
- Applied animations throughout UI

### script.js
- Added theme management system
- LocalStorage persistence for theme
- Theme toggle event handler

### base.html
- Added theme toggle button to navbar

### resume_base.html
- Added download button animation feedback

---

## 🎯 Key Features

### 1. Three Professional Themes
| Theme | Perfect For |
|-------|------------|
| Light | Daytime, printing |
| Dark | Evening, low light |
| Minimal | Professional, clean |

### 2. Smooth Animations
- Form entries slide in with stagger
- Resume sections appear sequentially
- Buttons lift on hover
- Smooth theme transitions

### 3. Reliable PDF Download
- Proper async error handling
- Fallback navigation if needed
- Automatic cleanup
- Works every time

### 4. Perfect Image Upload
- No cache conflicts
- Unique filenames prevent collisions
- Old images properly cleaned up
- Instant visual feedback

---

## 📱 Mobile Friendly

The app is fully responsive:
- **Mobile (375px):** Single column, touch-friendly
- **Tablet (768px):** Two-column layout
- **Desktop (1024px+):** Full layout

All themes and animations work on mobile devices!

---

## 💡 Tips & Tricks

### Create Multiple Resumes
1. Go to "Manage" → "Create New"
2. Pick different template (Modern/Classic)
3. Different names differentiate them

### Compare Themes
1. Create resume in light theme
2. Download as PDF
3. Switch to dark theme
4. Create same content again
5. Compare outputs

### Perfect Profile Picture
- Use high-resolution image
- Square format works best
- Shows as circular thumbnail
- 150px display size

### Resume Tips
- Keep summary under 200 words
- Use clear job titles
- Include links to projects
- Numbers/metrics impress employers

---

## 🎓 Learning Resources

### Understanding the Code
1. Start with `main.py` - app initialization
2. Check `auth.py` - login/signup flow
3. Review `views.py` - main features (see PDF fix!)
4. Explore `models.py` - data structure
5. Inspect `style.css` - see theme system

### CSS Variables
```css
:root {
  --primary-color: #667eea;
  --bg-primary: #ffffff;
  --text-primary: #333;
  /* ... more variables ... */
}

html[data-theme="dark"] {
  --bg-primary: #1a1a1a;
  --text-primary: #e0e0e0;
  /* ... overrides ... */
}
```

### Theme Toggle Code
```javascript
function toggleTheme() {
  currentThemeIndex = (currentThemeIndex + 1) % themes.length;
  applyTheme(themes[currentThemeIndex]);
  localStorage.setItem('theme', themes[currentThemeIndex]);
}
```

---

## 🐛 Reporting Issues

If you find a bug:
1. Note the exact steps to reproduce
2. Check console (F12) for error messages
3. Clear cache and try again
4. Check if it happens in different theme
5. Try different browser

Common issues are already documented in TESTING_GUIDE.md

---

## ✅ Verification

Quick test to verify everything works:

1. **Start app** - `python main.py` ✓
2. **Load page** - http://localhost:5000 ✓
3. **Test theme** - Click navbar button ✓
4. **Create resume** - Fill out form ✓
5. **Upload picture** - Add profile pic ✓
6. **Download PDF** - Get PDF file ✓
7. **Change theme** - Try dark mode ✓
8. **Refresh page** - Theme stays ✓

If all 8 pass, you're good to go! 🎉

---

## 📚 Documentation

For detailed information:
- **IMPROVEMENTS_PHASE2.md** - What was fixed/added
- **TESTING_GUIDE.md** - How to test features
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **code comments** - In the source files

---

## 🚀 Next Steps

1. **Explore the app** - Create resumes, try themes
2. **Read TESTING_GUIDE.md** - Detailed test instructions
3. **Check IMPROVEMENTS_PHASE2.md** - See what's new
4. **Review code changes** - Understand the fixes
5. **Deploy** - Ready for production use!

---

## 📞 Support

**Something not working?**
1. Check TESTING_GUIDE.md troubleshooting section
2. Look at browser console (F12) for errors
3. Try hard refresh (Ctrl+Shift+R)
4. Clear cache and try again
5. Restart the application

**Everything working?** 🎉
- You're ready to use the app!
- You can deploy it to a server
- You can share with others
- You can customize further

---

**Version:** 2.0 (Phase 2 Complete)  
**Status:** ✅ Ready to Use  
**Last Updated:** 2024  
**Quality:** Production Ready

Happy resume building! 📄✨
