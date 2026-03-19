import random
from django.conf import settings


class AIService:
    """
    Modular AI service. Connects to Claude API if AI_API_KEY is set in .env.
    Falls back to curated template responses when no API key is configured.
    """

    def __init__(self):
        self.api_key = getattr(settings, 'AI_API_KEY', '')
        self.model = getattr(settings, 'AI_MODEL', 'claude-opus-4-6')

    def _call_claude(self, prompt: str) -> str:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            msg = client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{'role': 'user', 'content': prompt}],
            )
            return msg.content[0].text.strip()
        except Exception as e:
            return f"[Claude API error: {e}]"

    def generate_product_description(self, product_name: str, category: str = '', price: str = '') -> str:
        if self.api_key:
            return self._call_claude(
                f"Write a compelling 2-3 sentence product description for a cosmetics product called "
                f"'{product_name}'{f' in the {category} category' if category else ''}. "
                f"Highlight sensory benefits and luxury appeal. Keep it under 80 words."
            )
        templates = [
            f"Indulge in the pure luxury of {product_name}. Crafted with premium ingredients, this exquisite product delivers exceptional results while enveloping you in a signature scent. A must-have for every beauty connoisseur.",
            f"Experience the magic of {product_name} — your new beauty essential. Rich, nourishing, and beautifully fragranced, it transforms your daily routine into a moment of pure self-care.",
            f"Discover {product_name} and elevate your beauty ritual. Designed for those who appreciate the finest in self-care, this premium product delivers visible results and a sensorial experience unlike any other.",
        ]
        return random.choice(templates)

    def generate_instagram_caption(self, product_name: str, category: str = '') -> str:
        if self.api_key:
            return self._call_claude(
                f"Write an engaging Instagram caption for a cosmetics product called '{product_name}'. "
                f"Make it aspirational, include a call to action, and keep it under 150 characters. "
                f"Add 3-5 relevant emojis."
            )
        captions = [
            f"✨ Treat yourself to luxury. {product_name} is your new daily essential 🌸 Shop now — link in bio! 💕",
            f"💄 Because you deserve the best. {product_name} — now available at M Cosmetics. DM to order! 🛍️✨",
            f"🌟 New drop alert! {product_name} is here and it's everything 😍 Limited stock — grab yours today! 💖",
        ]
        return random.choice(captions)

    def generate_marketing_copy(self, product_name: str) -> str:
        if self.api_key:
            return self._call_claude(
                f"Write short marketing copy for a cosmetics product called '{product_name}' sold in Zimbabwe. "
                f"Focus on luxury, self-care, and value. Include a headline and 2 bullet points. Keep it punchy."
            )
        return (
            f"✨ Introducing {product_name}\n\n"
            f"Premium quality. Affordable luxury.\n\n"
            f"• Elevate your daily self-care routine\n"
            f"• Long-lasting fragrance and nourishing formula\n\n"
            f"Order today via WhatsApp or shop online at M Cosmetics."
        )

    def suggest_hashtags(self, product_name: str, category: str = '') -> str:
        if self.api_key:
            return self._call_claude(
                f"Suggest 10 relevant Instagram hashtags for a Zimbabwe cosmetics store selling '{product_name}'. "
                f"Include a mix of general beauty, Zimbabwe-specific, and product-specific tags. Return as a single line."
            )
        base = "#MCosmetics #ZimbabweBeauty #LuxuryFragrance #SelfCare #PerfumeZW #BeautyZimbabwe"
        product_tag = f"#{product_name.replace(' ', '')}".replace("'", '')
        category_tag = f"#{category.replace(' ', '')}" if category else "#Cosmetics"
        return f"{product_tag} {category_tag} {base} #BathAndBodyWorks #BeautyRoutine #GlowUp"

    def answer_store_question(self, question: str, context: str = '') -> str:
        if self.api_key:
            system = (
                "You are a helpful assistant for M Cosmetics, a cosmetics store in Zimbabwe. "
                "You help the store owner with business insights, product advice, and marketing. "
                f"Store context: {context}"
            )
            return self._call_claude(f"[System: {system}]\n\nQuestion: {question}")
        return (
            "To get AI-powered answers, add your Claude API key to the .env file as AI_API_KEY. "
            "Get your key at console.anthropic.com"
        )
