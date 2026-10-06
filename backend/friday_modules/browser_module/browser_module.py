import webbrowser
from urllib.parse import quote
from playwright.sync_api import sync_playwright
from .content_extractor import generate_content
from pathlib import Path
from datetime import datetime
from ...helpers.llm_request import llm_request
from ..persistent_memory import storage_declarations


class BrowserModule:

    def __init__(self):
        self.actions = {
            "open_website": self.open_website,
            "summarize_website": self.summarize_website,
            "search_specific_website": self.search_specific_website,
        }
        self.search_engines = {
            "youtube": "https://www.youtube.com/results?search_query={}",
            "google": "https://www.google.com/search?q={}",
            "github": "https://www.github.com/search?q={}&type=repositories",
            "wikipedia": "https://en.wikipedia.org/wiki/{}",
            "reddit": "https://www.reddit.com/search/?q={}",
            "amazon": "https://www.amazon.in/s?k={}",
            "linkedin": "https://www.linkedin.com/search/results/all/?keywords={}",
            "facebook": "https://www.facebook.com/search/top?q={}",
            "instagram": "https://www.instagram.com/explore/tags/{}/",
            "twitter": "https://twitter.com/search?q={}",
            "x": "https://twitter.com/search?q={}",
            "spotify": "https://open.spotify.com/search/{}",
        }

    def open_website(self, task):
        webbrowser.open(task.parameters.url)

    def search_specific_website(self, task):
        query = quote(task.parameters.query)
        website_name = task.parameters.website_name
        search_url = self.search_engines[website_name.strip().lower()]
        webbrowser.open(search_url.format(query))

    def summarize_website(self, task):
        browser = None
        engine = None
        chunk_size = 6000
        llm_mode = storage_declarations.settings_details["llm_mode"]
        api_key = storage_declarations.settings_details["api_key"]
        system_prompt = """
            You are Friday's webpage summarization module.

            Your task is to summarize the webpage content provided by the user.

            RULES:
            - Summarize only the provided webpage content.
            - Do not use outside knowledge.
            - Preserve the important facts, names, dates, numbers, claims, and key details.
            - Remove irrelevant navigation text, menus, advertisements, cookie notices, repeated text, and other webpage clutter when present.
            - Do not invent, assume, or infer information that is not present in the provided content.
            - Do not repeat information unnecessarily.
            - Write a concise, factual summary in plain text.
            - Do not use Markdown formatting.
            - Do not use asterisks (*), backticks (`), headings, or decorative symbols.
            - Do not add phrases such as "Here is the summary", "This section discusses", or "The provided text says".
            - Do not mention that you are summarizing a chunk.
            - Return only the summary text.
            - If the provided content contains no meaningful information, return insufficient content available.
            - Keep the summary focused on information that would be useful to someone who wants to understand the webpage.

            The content provided may be only one portion of a larger webpage. Summarize this portion independently without assuming that other portions are available.
            """

        try:
            url = task.parameters.url
            if not url.startswith("http"):
                url = f"https://{url}"

            engine = sync_playwright().start()
            browser = engine.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            text = page.locator("body").inner_text()

            summarised_content = ""
            chunk_num = 0
            while True:
                chunk = text[
                    (chunk_num * chunk_size) : (chunk_num * chunk_size) + chunk_size
                ]
                if chunk_num == 20:
                    break
                if chunk:
                    content = llm_request(chunk, system_prompt, llm_mode, api_key)
                    summarised_content += content
                    chunk_num += 1
                else:
                    break

            path = (
                Path.home()
                / "Downloads"
                / f"summarized_{datetime.now().strftime('%d_%m_%Y-%H-%M-%S')}.txt"
            )
            path.write_text(summarised_content, encoding="utf-8")
            return "The summarized content has been saved to your Downloads folder."
        except Exception as err:
            print(str(err))
            return "Failed to summarise the webpage."
        finally:
            if browser:
                browser.close()
            if engine:
                engine.stop()

    def execute(self, task):
        action = self.actions.get(task.action)
        if action:
            return action(task)
