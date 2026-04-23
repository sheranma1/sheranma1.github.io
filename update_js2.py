with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the periods array
content = content.replace("const periods = ['1625', '1626-1628', '1627',", "const periods = ['1625', '1626', '1627', '1628',")

# 2. Add activePerson
content = content.replace("let activeTheme = 'all';", "let activeTheme = 'all';\n        let activePerson = 'all';")

# 3. Extract persons
content = content.replace("themes: (entry.dataset.themes || '').split(' '),", "themes: (entry.dataset.themes || '').split(' '),\n                persons: (entry.dataset.persons || '').split(' '),")

# 4. Add person filter click event
import re
theme_pattern = re.compile(r"document\.querySelectorAll\('\.pill'\)\.forEach\(btn => \{.*?\}\);\n        \}\);", re.DOTALL)
match = theme_pattern.search(content)

if match:
    new_theme_logic = match.group(0).replace("'.pill'", "'.theme-grid:not(#person-filters) .pill'")
    
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

# 5. Update the update() function
content = content.replace("const themeMatch = activeTheme === 'all' || data.themes.includes(activeTheme);", "const themeMatch = activeTheme === 'all' || data.themes.includes(activeTheme);\n                const personMatch = activePerson === 'all' || data.persons.includes(activePerson);")
content = content.replace("const show = periodMatch && themeMatch && searchMatch;", "const show = periodMatch && themeMatch && personMatch && searchMatch;")

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("JS updated successfully.")
