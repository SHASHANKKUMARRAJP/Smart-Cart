import os
import glob

back_button_html = """
                <!-- Back Button -->
                <a href="javascript:history.back()" class="flex items-center space-x-2 text-gray-300 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/5 mr-2 md:mr-6">
                    <i data-lucide="arrow-left" class="w-6 h-6"></i>
                    <span class="text-xl font-bold text-white">Back</span>
                </a>
"""

files = glob.glob('app/templates/*.html')
updated = []

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has back button
    if 'history.back()' in content:
        continue
    # Skip main entry points
    if any(x in filepath for x in ['index.html', 'landing-premium.html', 'login', 'register']):
        continue
    
    # Find Branding block and wrap it
    if '<!-- Branding -->' in content:
        parts = content.split('<!-- Branding -->')
        if len(parts) == 2:
            after = parts[1]
            end_a = after.find('</a>')
            if end_a != -1:
                branding = after[:end_a+4]
                rest = after[end_a+4:]
                
                # If branding includes 'hidden md:flex', we should remove that so the logo is still visible, 
                # OR just wrap it safely
                new_content = parts[0] + '<div class="flex items-center">' + back_button_html + '\n                <!-- Branding -->' + branding + '\n                </div>' + rest
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated.append(filepath)

print(f"Updated {len(updated)} files:")
for f in updated:
    print(f"- {f}")
