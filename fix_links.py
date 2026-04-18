import os

paths = ['hvac-contractors.html', 'privacy-policy.html', 'terms-of-service.html']
wdir = r'd:\apex nova things\Apex nova website'

for p in paths:
    fp = os.path.join(wdir, p)
    if not os.path.exists(fp): continue
    
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if p == 'hvac-contractors.html':
        c = c.replace('href="#services"', 'href="index.html#services"')
        c = c.replace('href="#work"', 'href="index.html#work"')
        c = c.replace('href="#seo"', 'href="index.html#seo"')
        c = c.replace('href="#testimonials"', 'href="index.html#testimonials"')
        c = c.replace('href="#contact"', 'href="index.html#contact"')

    # Fix the logo
    c = c.replace('href="#" class="flex items-center"', 'href="index.html" class="flex items-center"')
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(c)

print("Done.")
