import re

with open('sohyeon_sillok.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the sidebar periods
old_periods = """                <li><button data-period="1626-1628" style="--pc:#ca6f1e">
                    <span class="nav-year">1626–28</span>
                    <span class="nav-event">大慼 · 服制 · 明使</span>
                </button></li>
                <li><button data-period="1627" style="--pc:#c0392b">
                    <span class="nav-year">1627</span>
                    <span class="nav-event">丁卯胡亂 分朝</span>
                </button></li>"""

new_periods = """                <li><button data-period="1626" style="--pc:#ca6f1e">
                    <span class="nav-year">1626</span>
                    <span class="nav-event">迎接明使</span>
                </button></li>
                <li><button data-period="1627" style="--pc:#c0392b">
                    <span class="nav-year">1627</span>
                    <span class="nav-event">胡亂 · 嘉禮 · 舉哀</span>
                </button></li>
                <li><button data-period="1628" style="--pc:#d35400">
                    <span class="nav-year">1628</span>
                    <span class="nav-event">奏請遲延</span>
                </button></li>"""

content = content.replace(old_periods, new_periods)

# Also update the periods array in JS
content = content.replace("const periods = ['1625', '1626-1628', '1627', '1637',", "const periods = ['1625', '1626', '1627', '1628', '1637',")

with open('sohyeon_sillok.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated sidebar and JS periods.")
