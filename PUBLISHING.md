# Publishing Pixel Fighters - Complete Guide

## What Has Been Created

Your game is now ready to be published on the web! Here's what's been set up:

### 1. Web Version (Pygbag Build)
- **Location**: `build/web/`
- The game has been converted to WebAssembly and can run in any modern browser
- Includes all assets, sounds, and game files
- Compatible with Chrome, Firefox, Safari, and Edge

### 2. Professional Website
- **Location**: `website/`
- Beautiful, responsive website to showcase your game
- Includes:
  - Embedded playable game
  - Feature showcase
  - Controls guide
  - How to play instructions
  - Download section

## How to Publish

### Option 1: GitHub Pages (Free & Easy)

1. **Create a GitHub repository:**
   ```bash
   cd /home/raffaga/Code/h_d_game
   git init
   git add .
   git commit -m "Initial commit - Pixel Fighters"
   ```

2. **Create repo on GitHub.com:**
   - Go to github.com and create a new repository called "pixel-fighters"
   - Don't initialize with README (you already have one)

3. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/pixel-fighters.git
   git branch -M main
   git push -u origin main
   ```

4. **Enable GitHub Pages:**
   - Go to repository Settings > Pages
   - Source: Deploy from a branch
   - Branch: main, folder: /website
   - Save

5. **Your game will be live at:**
   `https://YOUR_USERNAME.github.io/pixel-fighters/`

### Option 2: Itch.io (Gaming Platform)

1. **Create account at itch.io**

2. **Create a new project:**
   - Go to Dashboard > Create new project
   - Title: Pixel Fighters
   - Project URL: pixel-fighters

3. **Upload web build:**
   - Kind of project: HTML
   - Upload: Zip the entire `build/web/` folder
   - Check "This file will be played in the browser"
   - Set embed dimensions: 1200x700

4. **Add details:**
   - Description: Copy from README.md
   - Screenshots: Take some in-game screenshots
   - Tags: fighting, multiplayer, pixel-art, 2-player

5. **Publish!**

### Option 3: Netlify (Professional Hosting)

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Deploy:**
   ```bash
   cd website
   netlify deploy --prod
   ```

3. **Follow prompts:**
   - Connect to GitHub (optional)
   - Choose deploy folder: `../build/web`
   - Get instant deployment!

### Option 4: Your Own Domain

1. **Buy a domain** (GoDaddy, Namecheap, etc.)

2. **Get web hosting** (HostGator, Bluehost, etc.)

3. **Upload via FTP:**
   - Upload `website/` contents to public_html
   - Upload `build/web/` to public_html/build/web/

4. **Configure DNS:**
   - Point your domain to the hosting
   - Your game is live!

## Local Testing

Before publishing, test the website locally:

```bash
cd /home/raffaga/Code/h_d_game/website
python3 -m http.server 8000
```

Then visit: `http://localhost:8000`

## Building for Updates

When you make changes to the game:

1. **Rebuild web version:**
   ```bash
   cd /home/raffaga/Code/h_d_game
   ./venv/bin/pygbag --build .
   ```

2. **Test changes locally**

3. **Push to GitHub** (if using GitHub Pages):
   ```bash
   git add .
   git commit -m "Update game"
   git push
   ```

## Creating Downloadable Versions

To let people download and run the game:

### Windows Executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "assets:assets" main.py
```

### Mac/Linux:

```bash
pip install pyinstaller
pyinstaller --onefile --add-data "assets:assets" main.py
```

The executable will be in `dist/`

## Marketing Your Game

### Social Media
- Share on Twitter with #indiegame #pygame #pixelart
- Post on Reddit: r/gamedev, r/pygame, r/IndieGaming
- Upload gameplay video to YouTube

### Game Communities
- Share on itch.io community
- Post on indie game Discord servers
- GameJolt (another hosting platform)

### Get Feedback
- Ask friends to playtest
- Post on game dev forums
- Stream development on Twitch

## Screenshots & Media

Create promotional materials:

1. **Take screenshots** during gameplay
2. **Record gameplay video** (OBS Studio is free)
3. **Create a GIF** showing combat
4. **Make a banner** with the logo and title

## Monetization Options

If you want to monetize:

- **Itch.io**: Set a price or "pay what you want"
- **Donations**: Add Ko-fi or PayPal button
- **Steam**: More complex, requires Steamworks setup
- **Ads**: Can add to web version (Google AdSense)

## License & Legal

Current license: Open Source

Consider adding a LICENSE file:
- MIT License (very permissive)
- GPL (must share modifications)
- Creative Commons (for assets)

Add to README which assets/sounds are yours vs downloaded.

## Next Steps

1. ✅ Game is web-ready
2. ✅ Website is created
3. Choose a hosting platform
4. Upload and deploy
5. Share with the world!

## Support

If you need help:
- Open an issue on your GitHub repo
- Ask on r/pygame
- Check pygame.org documentation
- itch.io has great tutorials

---

**Your game is ready to launch! Good luck! 🎮🚀**
