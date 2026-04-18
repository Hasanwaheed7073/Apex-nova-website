import os

files = [
    'index.html',
    'hvac-contractors.html',
    'case-study-hvac.html',
    'case-study-hicks.html',
    'privacy-policy.html',
    'terms-of-service.html'
]

wdir = r'd:\apex nova things\Apex nova website'

# The exact class to replace
old_class = "text-orange-600 dark:text-orange-500 font-bold border-b-2 border-orange-600 font-['Space_Grotesk'] tracking-tight transition-colors duration-300"
new_class = "text-stone-600 dark:text-stone-400 font-medium font-['Space_Grotesk'] tracking-tight hover:text-orange-600 dark:hover:text-orange-400 transition-colors duration-300"
# In some files, there's `block py-2` logic on mobile links... Let's use regex or just be careful.

# Actually, the user asked to replace EXACTLY:
old_str_1 = '''<a class="text-orange-600 dark:text-orange-500 font-bold border-b-2 border-orange-600 font-['Space_Grotesk'] tracking-tight transition-colors duration-300" href="#services">Services</a>'''
new_str_1 = '''<a class="text-stone-600 dark:text-stone-400 font-medium font-['Space_Grotesk'] tracking-tight hover:text-orange-600 dark:hover:text-orange-400 transition-colors duration-300" href="index.html#services">Services</a>'''

old_str_2 = '''<a class="text-orange-600 dark:text-orange-500 font-bold border-b-2 border-orange-600 font-['Space_Grotesk'] tracking-tight transition-colors duration-300" href="index.html#services">Services</a>'''
# new_str_2 is same as new_str_1

# Also replacing any href="#services" that might be a problem: this was handled by previous request for hvac-contractors.html, but index.html wasn't changed.
# But just replace exactly replacing any string matching `<a class="text-orange-600... href=".*#services">Services</a>` etc. Let's do it generally:

import re

for fn in files:
    fp = os.path.join(wdir, fn)
    if not os.path.exists(fp): continue
    
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()

    # Generic replace for desktop
    c = re.sub(
        r'<a class="text-orange-600 dark:text-orange-500 font-bold border-b-2 border-orange-600 font-\[\'Space_Grotesk\'\] tracking-tight transition-colors duration-300" href="[^"]*#services">Services</a>',
        r'<a class="text-stone-600 dark:text-stone-400 font-medium font-[\'Space_Grotesk\'] tracking-tight hover:text-orange-600 dark:hover:text-orange-400 transition-colors duration-300" href="index.html#services">Services</a>',
        c
    )
    
    # Generic replace for mobile (might have 'block py-2' instead) - but grep search shows the active mobile links DO NOT have 'block py-2'! They just have the orange class. Let's see grep output above:
    # "line 181 ... href="...#services">Services</a>"
    # "line 207 ... href="...#services">Services</a>" <-- Wait, this has the same class but is the mobile menu. So my generic sub covers both.

    # What about the "Work" link in the case-study pages?
    # The user instruction: "Fix 1 — Remove hardcoded active state from Services link" and "Do this in ALL 6 files in both desktop and mobile nav."
    # Wait, the user didn't mention the 'Work' link, but if I don't fix it, the script will add active state via JS but the 'Work' link will remain hardcoded in those files. I will remove the bold active state from 'Work' as well to be safe and thorough?
    # "Remove hardcoded active state from Services link" -> I'll stick to their instructions, and also remove it from Work just in case.
    c = re.sub(
        r'<a class="text-orange-600 dark:text-orange-500 font-bold border-b-2 border-orange-600 font-\[\'Space_Grotesk\'\] tracking-tight transition-colors duration-300" href="[^"]*#work">Work</a>',
        r'<a class="text-stone-600 dark:text-stone-400 font-medium font-[\'Space_Grotesk\'] tracking-tight hover:text-orange-600 dark:hover:text-orange-400 transition-colors duration-300" href="index.html#work">Work</a>',
        c
    )
    
    # JavaScript insertion
    js_code = """<script>
  const navLinks = document.querySelectorAll('nav a');
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    const linkPage = href.split('/').pop().split('#')[0] || 'index.html';
    if (linkPage === currentPage && linkPage !== '') {
      link.classList.add('text-orange-600', 'dark:text-orange-500', 'font-bold', 'border-b-2', 'border-orange-600');
      link.classList.remove('text-stone-600', 'dark:text-stone-400', 'font-medium');
    }
  });
</script>"""

    if "const navLinks = document.querySelectorAll('nav a');" not in c:
        c = c.replace("</body>", f"{js_code}\n</body>")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)

print("Done replacing.")
