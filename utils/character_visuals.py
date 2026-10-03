"""
Character Visuals & Protagonist Portrait Generator for MythCode.
Generates deterministic, visually coherent storybook vector portraits that stay faithful
to the player's selected hair style, hair color, outfit, affinity aura, companion, and keepsake.
"""
from typing import Dict, Any, Optional

def generate_protagonist_svg(
    name: str = "Aria",
    role: str = "Rune Engineer",
    affinity: str = "Arcane",
    hair_style: str = "Braided Crown",
    hair_color: str = "Auburn",
    outfit: str = "Leather Scholar Coat",
    companion: str = "Clockwork Owl",
    keepsake: str = "Brass Chrono-Gear",
    complexion: str = "Sun-kissed bronze",
    eye_color: str = "Amber gold",
    size: int = 240
) -> str:
    """
    Constructs a detailed, coherent SVG portrait of the player's protagonist.
    Visual elements dynamically adapt to every chosen trait so the character
    has a stable, recognizable visual identity across the game.
    """
    # 1. Palette mappings
    affinity_palette = {
        "Arcane": {"primary": "#8A72B8", "secondary": "#DCD2F2", "glow": "rgba(138, 114, 184, 0.4)", "symbol": "✦"},
        "Nature": {"primary": "#5A8250", "secondary": "#C9D8C1", "glow": "rgba(90, 130, 80, 0.4)", "symbol": "🌿"},
        "Water": {"primary": "#4A8FA8", "secondary": "#BBE0EC", "glow": "rgba(74, 143, 168, 0.4)", "symbol": "💧"},
        "Light": {"primary": "#D4A338", "secondary": "#FDF0CD", "glow": "rgba(212, 163, 56, 0.4)", "symbol": "☀️"},
        "Fire": {"primary": "#C85838", "secondary": "#FAD0C4", "glow": "rgba(200, 88, 56, 0.4)", "symbol": "🔥"},
        "Wind": {"primary": "#6B9B88", "secondary": "#D2E8E0", "glow": "rgba(107, 155, 136, 0.4)", "symbol": "🍃"}
    }
    aff = affinity_palette.get(affinity, affinity_palette["Arcane"])

    hair_palette = {
        "Auburn": "#8B3E2F",
        "Silver": "#B0B5B3",
        "Midnight Black": "#232328",
        "Golden": "#D4A017",
        "Emerald": "#2D684A",
        "Copper Crimson": "#A8422B"
    }
    h_color = hair_palette.get(hair_color, "#8B3E2F")

    skin_palette = {
        "Sun-kissed bronze": "#D4A373",
        "Pale alabaster": "#FCEADE",
        "Warm mahogany": "#8D5B4C",
        "Fair with rosy flush": "#F7D1BA",
        "Golden olive": "#C69C6D"
    }
    s_color = skin_palette.get(complexion, "#E8BA9B")

    eye_palette = {
        "Amber gold": "#D4A017",
        "Deep river blue": "#2E6B8E",
        "Forest emerald": "#2D684A",
        "Obsidian dark": "#232328",
        "Amethyst violet": "#795290"
    }
    e_color = eye_palette.get(eye_color, "#D4A017")

    outfit_palette = {
        "Leather Scholar Coat": {"base": "#5C4033", "trim": "#D7B978"},
        "Traveler's Cloak": {"base": "#455A64", "trim": "#C9D8C1"},
        "Tinkerer's Vest": {"base": "#795548", "trim": "#B08D57"},
        "Celestial Silk Tunic": {"base": "#3E2723", "trim": "#DCD2F2"},
        "Scout's Tunic": {"base": "#33691E", "trim": "#8D6E63"}
    }
    matched_outfit = None
    for k, v in outfit_palette.items():
        if k.lower() in outfit.lower():
            matched_outfit = v
            break
    if not matched_outfit:
        matched_outfit = outfit_palette["Leather Scholar Coat"]

    # 2. Hair shape path based on hair_style
    hair_style_lower = hair_style.lower()
    if "braid" in hair_style_lower or "crown" in hair_style_lower:
        # Braided Crown
        hair_svg = f"""
        <!-- Braided Crown -->
        <path d="M50,85 C42,45 60,32 100,32 C140,32 158,45 150,85 C145,50 135,42 100,42 C65,42 55,50 50,85 Z" fill="{h_color}" />
        <path d="M60,45 Q100,30 140,45 Q100,38 60,45 Z" fill="{aff['secondary']}" opacity="0.6" stroke="{aff['primary']}" stroke-width="1.5" />
        <circle cx="80" cy="40" r="3" fill="{aff['primary']}" />
        <circle cx="100" cy="38" r="3" fill="{aff['primary']}" />
        <circle cx="120" cy="40" r="3" fill="{aff['primary']}" />
        <path d="M50,75 C45,100 48,118 55,125 C52,112 50,95 54,75 Z" fill="{h_color}" />
        <path d="M150,75 C155,100 152,118 145,125 C148,112 150,95 146,75 Z" fill="{h_color}" />
        """
    elif "wind" in hair_style_lower or "locks" in hair_style_lower:
        # Windswept Locks
        hair_svg = f"""
        <!-- Windswept Locks -->
        <path d="M48,82 C40,40 65,30 100,30 C135,30 162,38 152,85 C146,55 130,42 100,42 C65,42 56,55 48,82 Z" fill="{h_color}" />
        <path d="M145,60 C165,55 175,70 160,82 C150,72 145,65 145,60 Z" fill="{h_color}" />
        <path d="M45,70 C30,75 25,90 40,95 C45,85 45,75 45,70 Z" fill="{h_color}" />
        <path d="M52,70 C48,105 52,130 62,140 C55,120 52,98 56,70 Z" fill="{h_color}" />
        <path d="M148,70 C152,105 148,130 138,140 C145,120 148,98 144,70 Z" fill="{h_color}" />
        """
    elif "bob" in hair_style_lower or "sleek" in hair_style_lower:
        # Sleek Scholar's Bob
        hair_svg = f"""
        <!-- Sleek Scholar Bob -->
        <path d="M48,85 C42,42 62,32 100,32 C138,32 158,42 152,85 C148,50 135,42 100,42 C65,42 52,50 48,85 Z" fill="{h_color}" />
        <path d="M48,70 L48,105 C48,115 56,118 62,112 C56,108 55,90 55,70 Z" fill="{h_color}" />
        <path d="M152,70 L152,105 C152,115 144,118 138,112 C144,108 145,90 145,70 Z" fill="{h_color}" />
        """
    elif "curl" in hair_style_lower or "flowing" in hair_style_lower:
        # Flowing Curls
        hair_svg = f"""
        <!-- Flowing Curls -->
        <path d="M46,80 C38,40 65,30 100,30 C135,30 162,40 154,80 C148,48 132,40 100,40 C68,40 52,48 46,80 Z" fill="{h_color}" />
        <circle cx="48" cy="95" r="10" fill="{h_color}" />
        <circle cx="44" cy="115" r="12" fill="{h_color}" />
        <circle cx="52" cy="132" r="11" fill="{h_color}" />
        <circle cx="152" cy="95" r="10" fill="{h_color}" />
        <circle cx="156" cy="115" r="12" fill="{h_color}" />
        <circle cx="148" cy="132" r="11" fill="{h_color}" />
        """
    else:
        # Practical Adventurer Cropped
        hair_svg = f"""
        <!-- Practical Cropped -->
        <path d="M50,75 C45,45 68,34 100,34 C132,34 155,45 150,75 C144,52 130,42 100,42 C70,42 56,52 50,75 Z" fill="{h_color}" />
        <path d="M52,65 Q100,45 148,65 Q100,52 52,65 Z" fill="{h_color}" />
        """

    # 3. Companion Familiar Silhouette / Badge
    comp_lower = companion.lower()
    if "owl" in comp_lower:
        companion_svg = f"""
        <!-- Clockwork Owl familiar -->
        <g transform="translate(142, 115)">
            <ellipse cx="16" cy="18" rx="14" ry="16" fill="#3D3028" stroke="{aff['primary']}" stroke-width="2" />
            <circle cx="11" cy="14" r="5" fill="#FAF6EE" stroke="#D7B978" stroke-width="1.5" />
            <circle cx="21" cy="14" r="5" fill="#FAF6EE" stroke="#D7B978" stroke-width="1.5" />
            <circle cx="11" cy="14" r="2.5" fill="{aff['primary']}" />
            <circle cx="21" cy="14" r="2.5" fill="{aff['primary']}" />
            <polygon points="16,19 14,24 18,24" fill="#D7B978" />
            <!-- Tiny brass wing -->
            <path d="M26,12 Q32,20 28,26 Q24,20 26,12 Z" fill="#D7B978" opacity="0.85" />
        </g>
        """
    elif "sprite" in comp_lower:
        companion_svg = f"""
        <!-- Sylvan Sprite familiar -->
        <g transform="translate(146, 110)">
            <circle cx="14" cy="16" r="10" fill="{aff['secondary']}" opacity="0.9" />
            <circle cx="14" cy="16" r="6" fill="#FFFFFF" />
            <!-- Gossamer wings -->
            <ellipse cx="6" cy="10" rx="8" ry="4" fill="{aff['primary']}" opacity="0.6" transform="rotate(-30, 6, 10)" />
            <ellipse cx="22" cy="10" rx="8" ry="4" fill="{aff['primary']}" opacity="0.6" transform="rotate(30, 22, 10)" />
            <circle cx="14" cy="16" r="2" fill="{aff['primary']}" />
        </g>
        """
    elif "fox" in comp_lower:
        companion_svg = f"""
        <!-- Runestone Fox familiar -->
        <g transform="translate(140, 118)">
            <ellipse cx="16" cy="18" rx="13" ry="11" fill="#A8422B" stroke="{aff['primary']}" stroke-width="1.5" />
            <polygon points="6,12 11,2 14,11" fill="#A8422B" stroke="{aff['primary']}" stroke-width="1" />
            <polygon points="18,11 21,2 26,12" fill="#A8422B" stroke="{aff['primary']}" stroke-width="1" />
            <circle cx="11" cy="15" r="2" fill="#232328" />
            <circle cx="21" cy="15" r="2" fill="#232328" />
            <circle cx="16" cy="20" r="2" fill="#232328" />
            <!-- Glowing tail curve -->
            <path d="M26,22 Q34,22 32,12 Q28,14 26,22 Z" fill="#FAF6EE" stroke="{aff['primary']}" stroke-width="1.5" />
        </g>
        """
    elif "salamander" in comp_lower:
        companion_svg = f"""
        <!-- Ember Salamander familiar -->
        <g transform="translate(144, 120)">
            <ellipse cx="14" cy="16" rx="12" ry="7" fill="#C85838" stroke="#D7B978" stroke-width="1.5" />
            <circle cx="8" cy="14" r="2" fill="#FFD700" />
            <circle cx="16" cy="14" r="2" fill="#FFD700" />
            <path d="M24,16 Q32,18 30,26" stroke="#C85838" stroke-width="3" fill="none" />
            <circle cx="30" cy="26" r="3" fill="#FFD700" />
        </g>
        """
    else:  # Zephyr Finch
        companion_svg = f"""
        <!-- Zephyr Finch familiar -->
        <g transform="translate(145, 114)">
            <ellipse cx="14" cy="16" rx="10" ry="8" fill="#B0B5B3" stroke="{aff['primary']}" stroke-width="1.5" />
            <circle cx="9" cy="14" r="2" fill="#232328" />
            <polygon points="4,14 1,16 4,18" fill="#D7B978" />
            <path d="M18,14 Q26,8 24,18 Z" fill="{aff['secondary']}" opacity="0.8" />
        </g>
        """

    # 4. Keepsake Brooch / Ornament
    kp_lower = keepsake.lower()
    if "gear" in kp_lower:
        keepsake_icon = f"""
        <!-- Brass Chrono-Gear keepsake -->
        <circle cx="100" cy="142" r="7" fill="#D7B978" stroke="#5C4033" stroke-width="1.5" stroke-dasharray="3,2" />
        <circle cx="100" cy="142" r="3" fill="#5C4033" />
        """
    elif "blossom" in kp_lower or "flower" in kp_lower:
        keepsake_icon = f"""
        <!-- Star-Blossom keepsake -->
        <circle cx="100" cy="142" r="6" fill="#FDF0CD" stroke="#D7B978" stroke-width="1.5" />
        <circle cx="100" cy="142" r="2.5" fill="{aff['primary']}" />
        """
    elif "prism" in kp_lower:
        keepsake_icon = f"""
        <!-- River Prism keepsake -->
        <polygon points="100,135 106,144 100,149 94,144" fill="#BBE0EC" stroke="#4A8FA8" stroke-width="1.5" />
        <circle cx="100" cy="142" r="2" fill="#FFFFFF" />
        """
    elif "tablet" in kp_lower:
        keepsake_icon = f"""
        <!-- Carved Rune-Tablet keepsake -->
        <rect x="94" y="136" width="12" height="13" rx="2" fill="#E8DFD1" stroke="#5C4033" stroke-width="1.5" />
        <path d="M97,140 H103 M97,144 H101" stroke="{aff['primary']}" stroke-width="1.2" />
        """
    else:  # Phial or default
        keepsake_icon = f"""
        <!-- Alchemical Phial keepsake -->
        <ellipse cx="100" cy="143" rx="5" ry="6" fill="#7BB5C9" stroke="#D7B978" stroke-width="1.5" />
        <rect x="98" y="135" width="4" height="3" fill="#D7B978" />
        """

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 220" width="{size}" height="{int(size * 1.1)}">
        <defs>
            <radialGradient id="auraGrad" cx="50%" cy="45%" r="50%">
                <stop offset="0%" stop-color="{aff['secondary']}" stop-opacity="0.8" />
                <stop offset="70%" stop-color="{aff['secondary']}" stop-opacity="0.3" />
                <stop offset="100%" stop-color="{aff['primary']}" stop-opacity="0.0" />
            </radialGradient>
            <linearGradient id="frameGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#FFFDF9" />
                <stop offset="50%" stop-color="#F5ECE0" />
                <stop offset="100%" stop-color="#EFE1D0" />
            </linearGradient>
            <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>

        <!-- Outer Medallion Border -->
        <circle cx="100" cy="100" r="94" fill="url(#frameGrad)" stroke="{aff['primary']}" stroke-width="3" />
        <circle cx="100" cy="100" r="88" fill="none" stroke="#D7B978" stroke-width="1.5" stroke-dasharray="4,4" />

        <!-- Magical Affinity Aura -->
        <circle cx="100" cy="95" r="76" fill="url(#auraGrad)" />

        <!-- Floating Runic Glyphs in Aura -->
        <text x="35" y="65" font-size="11" fill="{aff['primary']}" opacity="0.6">{aff['symbol']}</text>
        <text x="160" y="70" font-size="11" fill="{aff['primary']}" opacity="0.6">{aff['symbol']}</text>
        <text x="100" y="24" font-size="12" text-anchor="middle" fill="{aff['primary']}" opacity="0.75">{aff['symbol']}</text>

        <!-- Shoulders & Outfit -->
        <path d="M42,185 C46,140 70,128 100,128 C130,128 154,140 158,185 Z" fill="{matched_outfit['base']}" stroke="#2D251E" stroke-width="2" />
        <path d="M78,130 L100,165 L122,130 Z" fill="{matched_outfit['trim']}" opacity="0.9" />
        <!-- Collar Trim Lines -->
        <path d="M68,135 Q100,148 132,135" stroke="{matched_outfit['trim']}" stroke-width="2" fill="none" />

        <!-- Neck -->
        <rect x="90" y="105" width="20" height="24" rx="4" fill="{s_color}" stroke="#2D251E" stroke-width="1" />

        <!-- Head / Face -->
        <ellipse cx="100" cy="85" rx="27" ry="32" fill="{s_color}" stroke="#2D251E" stroke-width="1.8" />

        <!-- Eyes -->
        <ellipse cx="89" cy="83" rx="4.5" ry="3.5" fill="#FAF6EE" stroke="#2D251E" stroke-width="1" />
        <ellipse cx="111" cy="83" rx="4.5" ry="3.5" fill="#FAF6EE" stroke="#2D251E" stroke-width="1" />
        <circle cx="89" cy="83" r="2.2" fill="{e_color}" />
        <circle cx="111" cy="83" r="2.2" fill="{e_color}" />
        <circle cx="88" cy="82" r="0.7" fill="#FFFFFF" />
        <circle cx="110" cy="82" r="0.7" fill="#FFFFFF" />

        <!-- Gentle Eyebrows -->
        <path d="M83,76 Q89,74 95,77" stroke="#3D3028" stroke-width="1.4" fill="none" />
        <path d="M105,77 Q111,74 117,76" stroke="#3D3028" stroke-width="1.4" fill="none" />

        <!-- Nose & Mouth -->
        <path d="M99,86 Q100,92 97,94 H103" stroke="#8D5B4C" stroke-width="1.2" fill="none" />
        <path d="M94,101 Q100,105 106,101" stroke="#8D5B4C" stroke-width="1.6" fill="none" />

        <!-- Hair Layer -->
        {hair_svg}

        <!-- Pinned Keepsake Ornament -->
        {keepsake_icon}

        <!-- Familiar Companion -->
        {companion_svg}

        <!-- Bottom Nameplate Ribbon -->
        <g transform="translate(15, 182)">
            <rect x="0" y="0" width="170" height="30" rx="8" fill="#FFFDF9" stroke="#D7B978" stroke-width="2" />
            <text x="85" y="16" text-anchor="middle" font-family="serif" font-size="11" font-weight="bold" fill="#4A3525">{name}</text>
            <text x="85" y="26" text-anchor="middle" font-family="serif" font-size="8.5" fill="#7B8F72">{role} &bull; {affinity}</text>
        </g>
    </svg>
    """
    return svg.strip()
