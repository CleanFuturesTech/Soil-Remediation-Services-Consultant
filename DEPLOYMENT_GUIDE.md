# Deployment Guide: GitHub + Streamlit Cloud

## Complete Step-by-Step Process

### PART 1: Set Up GitHub Repository

#### Step 1: Create GitHub Account (if needed)
1. Go to https://github.com
2. Sign up for a free account (or log in if you have one)

#### Step 2: Create New Repository
1. Click the **"+"** icon in top right → **"New repository"**
2. Repository settings:
   - **Repository name:** `clean-futures-recommendation-tool` (or your preferred name)
   - **Description:** "Intelligent soil remediation decision support system for the Permian Basin"
   - **Public** or **Private** (your choice - Streamlit Cloud works with both)
   - ✅ Check **"Add a README file"** (we'll replace it with ours)
   - **Add .gitignore:** Choose "Python" template
   - **Choose a license:** Optional (MIT is common for open source)
3. Click **"Create repository"**

#### Step 3: Upload Files to GitHub

**Option A: Using GitHub Web Interface (Easiest)**

1. In your new repository, click **"Add file"** → **"Upload files"**
2. Drag and drop these files:
   - `clean_futures_recommendation_tool.py`
   - `permian_facilities_db.json`
   - `README.md`
   - `requirements.txt`
   - `.gitignore`
3. Scroll down, add commit message: "Initial commit - Clean Futures tool v1.0"
4. Click **"Commit changes"**

**Option B: Using Git Command Line (Advanced)**

If you have git installed locally:

```bash
# Navigate to your project folder
cd /path/to/your/files

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Clean Futures tool v1.0"

# Connect to GitHub (replace YOUR-USERNAME and YOUR-REPO)
git remote add origin https://github.com/YOUR-USERNAME/clean-futures-recommendation-tool.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### Step 4: Verify Upload
1. Go to your repository page on GitHub
2. You should see all 5 files listed
3. Click on each to verify content uploaded correctly

---

### PART 2: Deploy to Streamlit Cloud

#### Step 1: Create Streamlit Cloud Account
1. Go to https://streamlit.io/cloud
2. Click **"Sign up"** or **"Get started"**
3. **Sign in with GitHub** (recommended - makes deployment seamless)
4. Authorize Streamlit to access your GitHub account

#### Step 2: Deploy Your App

1. From Streamlit Cloud dashboard, click **"New app"**

2. Configure deployment settings:
   - **Repository:** Select `YOUR-USERNAME/clean-futures-recommendation-tool`
   - **Branch:** `main` (or master)
   - **Main file path:** `clean_futures_recommendation_tool.py`
   - **App URL:** Choose your subdomain (e.g., `clean-futures` → clean-futures.streamlit.app)

3. Click **"Deploy!"**

4. Wait 2-5 minutes for initial deployment
   - You'll see logs as it installs dependencies
   - Status will change from "Building" → "Running"

#### Step 3: Access Your Live App

Once deployed, your app will be live at:
```
https://YOUR-CHOSEN-NAME.streamlit.app
```

Example: `https://clean-futures.streamlit.app`

---

### PART 3: Making Updates

#### To Update Your App:

1. **Edit files on GitHub:**
   - Go to your repository
   - Click on the file you want to edit
   - Click the pencil icon (Edit)
   - Make your changes
   - Scroll down and commit changes

2. **Automatic redeployment:**
   - Streamlit Cloud automatically detects changes
   - App will redeploy within 1-2 minutes
   - No manual trigger needed!

#### To Update the Facilities Database:

1. Go to GitHub repository
2. Click `permian_facilities_db.json`
3. Click pencil icon to edit
4. Modify landfill/facility data
5. Commit changes
6. App updates automatically

---

### PART 4: Advanced Configuration (Optional)

#### Custom Domain
If you want to use your own domain (e.g., tools.cleanfutures.com):

1. In Streamlit Cloud app settings, click **"Settings"**
2. Under **"General"**, find **"Custom subdomain"**
3. Follow DNS configuration instructions

#### Environment Variables / Secrets
If you need to store sensitive data:

1. In Streamlit Cloud app settings → **"Secrets"**
2. Add key-value pairs in TOML format:
```toml
[database]
api_key = "your-key-here"
```

3. Access in code:
```python
import streamlit as st
api_key = st.secrets["database"]["api_key"]
```

#### App Settings
In Streamlit Cloud → **"Settings"**:
- Change Python version
- Adjust resource limits
- Configure secrets
- Manage custom domains

---

### PART 5: Sharing Your App

#### Public Link
Share your app URL with anyone:
```
https://your-app-name.streamlit.app
```

#### Embed in Website
Add iframe to your website:
```html
<iframe 
  src="https://your-app-name.streamlit.app" 
  width="100%" 
  height="800px"
  frameborder="0">
</iframe>
```

#### QR Code
Generate QR code for mobile access:
1. Use any QR code generator (e.g., qr-code-generator.com)
2. Enter your Streamlit app URL
3. Download and share QR code

---

### Troubleshooting Common Issues

#### Issue: App won't deploy
**Solution:**
- Check that `requirements.txt` is in root directory
- Verify file path in deployment settings
- Check logs in Streamlit Cloud for specific errors

#### Issue: Database not found
**Solution:**
- Verify `permian_facilities_db.json` is in the same directory as the Python file
- Check file path in code: should be relative path

#### Issue: App is slow
**Solutions:**
- Streamlit Cloud free tier has resource limits
- Consider caching with `@st.cache_data` decorator
- Optimize calculations

#### Issue: Need to revert changes
**Solution:**
- Go to GitHub repository
- Click "Commits"
- Find the previous working version
- Click "..." → "Revert"

---

### Best Practices

1. **Version Control:**
   - Commit changes with descriptive messages
   - Use branches for major new features
   - Tag releases (v1.0, v1.1, etc.)

2. **Testing:**
   - Test changes locally before pushing
   - Keep a local copy of working version

3. **Documentation:**
   - Update README.md when adding features
   - Document configuration changes
   - Keep facility database documentation current

4. **Security:**
   - Never commit API keys or passwords
   - Use Streamlit secrets for sensitive data
   - Keep private repository if needed

5. **Monitoring:**
   - Check app regularly to ensure it's running
   - Monitor Streamlit Cloud dashboard for issues
   - Review logs if errors occur

---

### Quick Reference: File Structure

Your GitHub repository should look like this:

```
clean-futures-recommendation-tool/
│
├── clean_futures_recommendation_tool.py  # Main app
├── permian_facilities_db.json            # Database
├── requirements.txt                      # Dependencies
├── README.md                             # Documentation
└── .gitignore                           # Git exclusions
```

---

### Support Resources

- **Streamlit Documentation:** https://docs.streamlit.io
- **Streamlit Community Forum:** https://discuss.streamlit.io
- **GitHub Docs:** https://docs.github.com
- **Streamlit Cloud Status:** https://status.streamlit.io

---

### Next Steps After Deployment

1. ✅ Test the live app thoroughly
2. ✅ Share link with Clean Futures team
3. ✅ Gather feedback from first users
4. ✅ Update facility database as needed
5. ✅ Add new features based on user requests

---

**Congratulations! Your app is now live and accessible to the world! 🎉**

Any questions or issues, refer back to this guide or check the Streamlit documentation.
