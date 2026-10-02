"""
Cloudflare Illustration Integration for MythCode (PART 5).
Manages AI image generation, in-memory/disk caching, and rich SVG storybook fallbacks.
Never exposes credentials in frontend and operates with zero crash risk when offline.
"""
import os
import json
import urllib.request
import urllib.error
import base64
from typing import Dict, Any, Optional
from utils.logger import setup_logger

logger = setup_logger("CloudflareImages")

# In-memory image cache to avoid regenerating illustrations on Streamlit reruns
_IMAGE_CACHE: Dict[str, str] = {}

class CloudflareImageService:
    """Provides storybook fantasy illustrations via Cloudflare Workers AI or local SVG fallbacks."""

    def __init__(self):
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
        self.api_token = os.getenv("CLOUDFLARE_API_TOKEN", "")
        self.model = os.getenv(
            "CLOUDFLARE_IMAGE_MODEL",
            "@cf/stabilityai/stable-diffusion-xl-base-1.0"
        )

        # Check Streamlit secrets if running in Streamlit
        try:
            import streamlit as st
            if hasattr(st, "secrets"):
                if "cloudflare" in st.secrets:
                    cf_sec = st.secrets["cloudflare"]
                    self.account_id = cf_sec.get("account_id", self.account_id)
                    self.api_token = cf_sec.get("api_token", self.api_token)
                    self.model = cf_sec.get("image_model", self.model)
                elif "CLOUDFLARE_API_TOKEN" in st.secrets:
                    self.api_token = st.secrets["CLOUDFLARE_API_TOKEN"]
                    self.account_id = st.secrets.get("CLOUDFLARE_ACCOUNT_ID", self.account_id)
        except Exception:
            pass

    @property
    def is_available(self) -> bool:
        return bool(self.account_id and self.api_token and self.api_token != "YOUR_API_TOKEN_HERE")

    def get_illustration(self, category: str, custom_prompt: Optional[str] = None) -> str:
        """
        Retrieves cached illustration or generates a new one.
        Returns data URL (base64 PNG or SVG).
        """
        cache_key = f"{category}_{custom_prompt or 'default'}"
        if cache_key in _IMAGE_CACHE:
            return _IMAGE_CACHE[cache_key]

        # If Cloudflare credentials are configured, attempt generation
        if self.is_available:
            generated = self._generate_cloudflare_image(category, custom_prompt)
            if generated:
                _IMAGE_CACHE[cache_key] = generated
                return generated

        # Local storybook SVG fallback
        svg = self._get_fallback_svg(category)
        _IMAGE_CACHE[cache_key] = svg
        return svg

    def _generate_cloudflare_image(self, category: str, custom_prompt: Optional[str]) -> Optional[str]:
        """Calls Cloudflare Workers AI REST endpoint to generate an image."""
        style_prompt = (
            "Fantasy storybook illustration, whimsical magical art, soft pastel color palette, "
            "parchment and warm cream tones, lavender and sage accents, gentle natural lighting, "
            "friendly children's book aesthetic, masterpiece, high detail."
        )
        base_prompts = {
            "world_intro": "Enchanted fantasy kingdom of Elarion with floating crystalline waterfalls and ancient runic stones.",
            "Whispering Village": "Quaint fantasy storybook village with cobblestone square, dried stone fountain, timber workshops, and flower gardens.",
            "River Aqueduct": "Massive ancient stone and bronze waterwheel aqueduct spanning a rocky river bed with a resting clockwork sentinel.",
            "Ancient Grove": "Ethereal mystical forest clearing with giant weeping willow trees, glowing bioluminescent emerald moss, and an ancient runic archway.",
            "Clockwork Ruins": "Subterranean ancient hall with gleaming brass gears, five glowing runic floor conduits, and crystal conduits.",
            "character_portrait": "Expressive young fantasy adventurer scholar with curiosity in their eyes, magical runes glowing on their clothing, companion animal resting on shoulder.",
            "puzzle_solved": "Magical burst of glowing pastel light, ancient gears spinning smoothly, clear sparkling water flowing joyously into crystalline fountains."
        }

        prompt = f"{custom_prompt or base_prompts.get(category, base_prompts['world_intro'])}, {style_prompt}"

        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"
        payload = {"prompt": prompt}

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.api_token}",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=8.0) as resp:
                image_bytes = resp.read()
                b64_img = base64.b64encode(image_bytes).decode("utf-8")
                data_url = f"data:image/png;base64,{b64_img}"
                logger.info(f"Cloudflare illustration generated successfully for '{category}'")
                return data_url
        except Exception as e:
            logger.warning(f"Cloudflare AI image request failed: {e}. Using storybook SVG fallback.")
            return None

    def _get_fallback_svg(self, category: str) -> str:
        """Returns handcrafted, warm storybook SVG illustrations."""
        svg_palette = {
            "bg_parchment": "#F7F1E6",
            "lavender": "#DCD2F2",
            "sage": "#C9D8C1",
            "gold": "#D7B978",
            "peach": "#F2CDBD",
            "ink": "#453D4C"
        }

        if category == "River Aqueduct":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 240" width="100%" height="100%">
                <defs>
                    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="{svg_palette['lavender']}" />
                        <stop offset="60%" stop-color="{svg_palette['bg_parchment']}" />
                        <stop offset="100%" stop-color="{svg_palette['sage']}" />
                    </linearGradient>
                </defs>
                <rect width="600" height="240" rx="16" fill="url(#skyGrad)" />
                <path d="M0,180 Q150,160 300,185 T600,175 L600,240 L0,240 Z" fill="{svg_palette['sage']}" opacity="0.8" />
                <!-- Aqueduct Arch -->
                <rect x="180" y="80" width="240" height="20" rx="4" fill="{svg_palette['gold']}" />
                <path d="M220,100 A40,40 0 0,0 300,100 V180 H220 Z" fill="{svg_palette['bg_parchment']}" stroke="{svg_palette['gold']}" stroke-width="3" />
                <path d="M300,100 A40,40 0 0,0 380,100 V180 H300 Z" fill="{svg_palette['bg_parchment']}" stroke="{svg_palette['gold']}" stroke-width="3" />
                <!-- Gear wheel -->
                <circle cx="200" cy="140" r="30" fill="none" stroke="{svg_palette['gold']}" stroke-width="8" stroke-dasharray="8,6" />
                <circle cx="200" cy="140" r="12" fill="{svg_palette['peach']}" stroke="{svg_palette['gold']}" stroke-width="3" />
                <!-- Clockwork Guardian silhouette -->
                <rect x="420" y="130" width="30" height="45" rx="6" fill="{svg_palette['ink']}" opacity="0.85" />
                <circle cx="435" cy="118" r="14" fill="{svg_palette['ink']}" opacity="0.85" />
                <circle cx="435" cy="118" r="4" fill="{svg_palette['gold']}" />
                <text x="300" y="220" text-anchor="middle" font-family="serif" font-size="14" font-weight="bold" fill="{svg_palette['ink']}">RIVER AQUEDUCT & CLOCKWORK SENTINEL</text>
            </svg>
            """
        elif category == "Ancient Grove":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 240" width="100%" height="100%">
                <defs>
                    <linearGradient id="groveGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="{svg_palette['sage']}" />
                        <stop offset="70%" stop-color="{svg_palette['bg_parchment']}" />
                        <stop offset="100%" stop-color="{svg_palette['lavender']}" />
                    </linearGradient>
                </defs>
                <rect width="600" height="240" rx="16" fill="url(#groveGrad)" />
                <!-- Ancient Willow Trees -->
                <path d="M70,240 C90,160 50,110 80,70 C120,80 140,140 130,240 Z" fill="{svg_palette['sage']}" opacity="0.7" />
                <path d="M530,240 C510,160 550,110 520,70 C480,80 460,140 470,240 Z" fill="{svg_palette['sage']}" opacity="0.7" />
                <!-- Glowing Runic Arch -->
                <path d="M250,200 V100 A50,50 0 0,1 350,100 V200 Z" fill="none" stroke="{svg_palette['sage']}" stroke-width="12" />
                <circle cx="300" cy="90" r="18" fill="{svg_palette['peach']}" stroke="{svg_palette['gold']}" stroke-width="4" />
                <!-- Runic glyph sparkles -->
                <circle cx="280" cy="130" r="3" fill="{svg_palette['gold']}" />
                <circle cx="320" cy="130" r="3" fill="{svg_palette['gold']}" />
                <circle cx="300" cy="150" r="4" fill="{svg_palette['lavender']}" />
                <text x="300" y="225" text-anchor="middle" font-family="serif" font-size="14" font-weight="bold" fill="{svg_palette['ink']}">ANCIENT GROVE OF SYLVAN</text>
            </svg>
            """
        elif category == "Clockwork Ruins":
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 240" width="100%" height="100%">
                <defs>
                    <linearGradient id="ruinsGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="{svg_palette['lavender']}" />
                        <stop offset="50%" stop-color="{svg_palette['bg_parchment']}" />
                        <stop offset="100%" stop-color="{svg_palette['gold']}" />
                    </linearGradient>
                </defs>
                <rect width="600" height="240" rx="16" fill="url(#ruinsGrad)" />
                <!-- Five Conduits Tiles -->
                <g transform="translate(140, 110)">
                    <rect x="0" y="0" width="50" height="35" rx="6" fill="{svg_palette['bg_parchment']}" stroke="{svg_palette['gold']}" stroke-width="3" />
                    <rect x="65" y="0" width="50" height="35" rx="6" fill="{svg_palette['bg_parchment']}" stroke="{svg_palette['gold']}" stroke-width="3" />
                    <rect x="130" y="0" width="50" height="35" rx="6" fill="{svg_palette['bg_parchment']}" stroke="{svg_palette['gold']}" stroke-width="3" />
                    <rect x="195" y="0" width="50" height="35" rx="6" fill="{svg_palette['bg_parchment']}" stroke="{svg_palette['gold']}" stroke-width="3" />
                    <rect x="260" y="0" width="50" height="35" rx="6" fill="{svg_palette['bg_parchment']}" stroke="{svg_palette['gold']}" stroke-width="3" />
                </g>
                <path d="M100,128 H140 M190,128 H205 M255,128 H270 M320,128 H335 M385,128 H400 M450,128 H490" stroke="{svg_palette['peach']}" stroke-width="4" stroke-dasharray="4,4" />
                <text x="300" y="210" text-anchor="middle" font-family="serif" font-size="14" font-weight="bold" fill="{svg_palette['ink']}">SUBTERRANEAN RESONANCE TILES</text>
            </svg>
            """
        else:  # Whispering Village or default
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 240" width="100%" height="100%">
                <defs>
                    <linearGradient id="villageGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="{svg_palette['peach']}" />
                        <stop offset="50%" stop-color="{svg_palette['bg_parchment']}" />
                        <stop offset="100%" stop-color="{svg_palette['sage']}" />
                    </linearGradient>
                </defs>
                <rect width="600" height="240" rx="16" fill="url(#villageGrad)" />
                <!-- Cottage Roofs -->
                <polygon points="60,140 120,90 180,140" fill="{svg_palette['gold']}" />
                <rect x="80" y="140" width="80" height="60" fill="{svg_palette['bg_parchment']}" stroke="{svg_palette['ink']}" stroke-width="2" />
                <polygon points="420,130 480,80 540,130" fill="{svg_palette['gold']}" />
                <rect x="440" y="130" width="80" height="70" fill="{svg_palette['bg_parchment']}" stroke="{svg_palette['ink']}" stroke-width="2" />
                <!-- Village Fountain -->
                <ellipse cx="300" cy="180" rx="60" ry="20" fill="{svg_palette['lavender']}" stroke="{svg_palette['gold']}" stroke-width="3" />
                <path d="M295,180 V140 H305 V180 Z" fill="{svg_palette['gold']}" />
                <circle cx="300" cy="135" r="8" fill="{svg_palette['peach']}" />
                <text x="300" y="225" text-anchor="middle" font-family="serif" font-size="14" font-weight="bold" fill="{svg_palette['ink']}">WHISPERING VILLAGE & DRIED SPRINGS</text>
            </svg>
            """

        clean_svg = svg_content.strip()
        b64_svg = base64.b64encode(clean_svg.encode("utf-8")).decode("utf-8")
        return f"data:image/svg+xml;base64,{b64_svg}"

_service_instance: Optional[CloudflareImageService] = None

def get_image_service() -> CloudflareImageService:
    global _service_instance
    if _service_instance is None:
        _service_instance = CloudflareImageService()
    return _service_instance
