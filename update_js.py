with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add activePerson
content = content.replace("let activeTheme = 'all';", "let activeTheme = 'all';\n        let activePerson = 'all';")

# 2. Extract persons
content = content.replace("themes: (entry.dataset.themes || '').split(' '),", "themes: (entry.dataset.themes || '').split(' '),\n                persons: (entry.dataset.persons || '').split(' '),")

# 3. Add person filter click event
# We'll insert it right after the theme logic
theme_event_logic = """        // Theme Filters
        document.querySelectorAll('.theme-grid .pill').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.theme-grid .pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activeTheme = btn.dataset.theme;
                update();
            });
        });"""

person_event_logic = """        // Theme Filters
        document.querySelectorAll('#sidebar > .theme-grid:nth-of-type(1) .pill').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('#sidebar > .theme-grid:nth-of-type(1) .pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activeTheme = btn.dataset.theme;
                update();
            });
        });

        // Person Filters
        document.querySelectorAll('#person-filters .pill').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('#person-filters .pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activePerson = btn.dataset.person;
                update();
            });
        });"""
# Wait, let's just do a regex replace for the original theme logic
import re

theme_pattern = re.compile(r"document\.querySelectorAll\('\.theme-grid \.pill'\)\.forEach\(btn => \{.*?\}\);\n        \}\);", re.DOTALL)
match = theme_pattern.search(content)

if match:
    # First, let's modify the CSS selector to target only the first theme grid if we have two, but earlier I added an ID 'person-filters' to the second one.
    # So we can just change '.theme-grid .pill' to '.theme-grid:not(#person-filters) .pill' for the theme.
    new_theme_logic = match.group(0).replace("'.theme-grid .pill'", "'.theme-grid:not(#person-filters) .pill'")
    
    person_logic = """
        document.querySelectorAll('#person-filters .pill').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('#person-filters .pill').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                activePerson = btn.dataset.person;
                update();
            });
        });
"""
    content = content.replace(match.group(0), new_theme_logic + person_logic)

# 4. Update the update() function
content = content.replace("const themeMatch = activeTheme === 'all' || data.themes.includes(activeTheme);", "const themeMatch = activeTheme === 'all' || data.themes.includes(activeTheme);\n                const personMatch = activePerson === 'all' || data.persons.includes(activePerson);")
content = content.replace("const show = periodMatch && themeMatch && searchMatch;", "const show = periodMatch && themeMatch && personMatch && searchMatch;")

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("JS updated successfully.")
