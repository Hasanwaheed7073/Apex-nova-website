import os
import glob

HEAD_SCRIPT = """
    <script>
        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }

        function toggleDarkMode() {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.theme = 'light';
            } else {
                document.documentElement.classList.add('dark');
                localStorage.theme = 'dark';
            }
        }
    </script>
</head>
"""

NAV_BUTTON = """
            <div class="flex items-center gap-2 md:gap-4 ml-auto md:ml-0">
                <button onclick="toggleDarkMode()" class="text-stone-600 dark:text-stone-400 hover:text-orange-600 transition-colors p-2 rounded-full focus:outline-none flex items-center justify-center">
                    <span class="material-symbols-outlined dark:hidden block">dark_mode</span>
                    <span class="material-symbols-outlined dark:block hidden text-stone-200">light_mode</span>
                </button>
"""

html_files = glob.glob("*.html")

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. HEAD Script
    if "toggleDarkMode()" not in content:
        content = content.replace("</head>", HEAD_SCRIPT)

    # 2. Navbar Button
    if "dark_mode" not in content:
        if '<div class="flex items-center gap-4">' in content:
             content = content.replace('<div class="flex items-center gap-4">', NAV_BUTTON)
        elif '<div class="hidden md:flex items-center space-x-12">' in content:
            # Append to privacy policy
            content = content.replace('</div>\n        </div>\n    </nav>', '</div>\n' + NAV_BUTTON + '</div>\n        </div>\n    </nav>')
            
    # 3. Class Overrides
    
    # Body (only exact match to avoid doubling)
    if "dark:bg-stone-950" not in content.split('body class="')[1].split('"')[0]:
         content = content.replace('bg-surface font-body text-on-surface', 'bg-surface dark:bg-stone-950 font-body text-on-surface dark:text-stone-200')
    
    # Text
    content = content.replace('text-on-surface ', 'text-on-surface dark:text-stone-100 ')
    content = content.replace('text-on-surface"', 'text-on-surface dark:text-stone-100"')
    
    content = content.replace('text-secondary ', 'text-secondary dark:text-stone-400 ')
    content = content.replace('text-secondary"', 'text-secondary dark:text-stone-400"')
    
    content = content.replace('text-on-background ', 'text-on-background dark:text-stone-50 ')
    content = content.replace('text-on-background"', 'text-on-background dark:text-stone-50"')
    
    # Backgrounds
    content = content.replace('bg-surface-container-low"', 'bg-surface-container-low dark:bg-stone-900"')
    content = content.replace('bg-surface-container-low ', 'bg-surface-container-low dark:bg-stone-900 ')
    
    content = content.replace('bg-surface-container-lowest"', 'bg-surface-container-lowest dark:bg-stone-950"')
    content = content.replace('bg-surface-container-lowest ', 'bg-surface-container-lowest dark:bg-stone-950 ')
    
    content = content.replace('bg-surface-container-high"', 'bg-surface-container-high dark:bg-stone-900"')
    content = content.replace('bg-surface-container-high ', 'bg-surface-container-high dark:bg-stone-900 ')
    
    content = content.replace('bg-surface ', 'bg-surface dark:bg-stone-950 ')
    content = content.replace('bg-surface"', 'bg-surface dark:bg-stone-950"')
    
    # Forms
    content = content.replace('border-outline-variant', 'border-outline-variant dark:border-stone-700 dark:bg-stone-900')


    # Deduplicate in case of multi runs
    content = content.replace('dark:text-stone-100 dark:text-stone-100', 'dark:text-stone-100')
    content = content.replace('dark:bg-stone-950 dark:bg-stone-950', 'dark:bg-stone-950')
    content = content.replace('dark:bg-stone-900 dark:bg-stone-900', 'dark:bg-stone-900')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Applied dark mode to {len(html_files)} files.")
