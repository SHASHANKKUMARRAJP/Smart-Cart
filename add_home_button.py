import glob
import os

html_files = glob.glob(r'c:\Users\sshas\OneDrive\Desktop\final yearproject - developed version\app\templates\*.html')

back_button_code = """
    <!-- Floating Home/Back Button added for navigation -->
    <a href="/" style="position: fixed; bottom: 20px; left: 20px; z-index: 9999; background: #667eea; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3); text-decoration: none;" title="Go Home">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
    </a>
</body>
"""

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Floating Home/Back Button' not in content and '</body>' in content:
        content = content.replace('</body>', back_button_code)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            print(f"Added home button to {os.path.basename(file_path)}")
