import re
import urllib.parse

import requests
from bs4 import BeautifulSoup
from mrender.web2md import html_to_markdown_with_depth
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.spinner import Spinner
from rich.text import Span, Text

console = Console(style="bold white on cyan1", soft_wrap=True)
blue_console = Console(style="bold white on blue", soft_wrap=True)
print = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="red", overflow="fold")) for arg in args), **kwargs) # noqa
print_bold = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="bold", overflow="fold")) for arg in args), **kwargs)
input = lambda arg, **kwargs: Confirm.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, default="y", **kwargs) # noqa
ask = lambda arg, **kwargs: Prompt.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, **kwargs) # noqa

def is_valid_url(url) -> bool:
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def get_pages(url) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it up
        text = soup.get_text(separator='\n', strip=True)
        text = '\n'.join(line for line in text.splitlines() if line.strip())
        
        # Split the text into sections of 2000 characters each
        sections = [text[i:i+2000] for i in range(0, len(text), 2000)]
    
        for i, section in enumerate(sections):
            panel = Panel(
                section,
                title=f"Content of {url} (Section {i+1}/{len(sections)})",
                expand=False,
                border_style="blue",
                padding=(1, 1),
            )
            console.print(panel)
            
            
            if i < len(sections) - 1 or input("Show next section?", choices=["y", "n"]) == "n":
                    break
            
        
        # Fetch links
        links = []
        if input("Show links found on the webpage?", choices=["y", "n"]) == "y":
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith('http'):
                    links.append(href)
            print_bold(f"Links found on the webpage:\n{', '.join(links)}")
        
        if input("Add the entire webpage content to the chat? y", choices=["y", "n"]) == "y":
            content = f"Webpage content from {url}:\n\n{sections[:i+1]}"
            if links:
                content += f"\n\nLinks found on the webpage:\n{', '.join(links)}"
            return html_to_markdown_with_depth(response.text, 10)
    except requests.RequestException as e:
      print(f"Error fetching the webpage: {str(e)}")

def full_page(url) -> str:
    if not is_valid_url(url):
        return "Invalid URL. Please enter a valid URL including the protocol (e.g., http:// or https://)."
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        # # Extract and append links
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if not href.startswith(('http://', 'https://')):
                href = urllib.parse.urljoin(url, href)
            links.append(f"[{a.text.strip()}]({href})")
        plain_text = '\n\n## Links found on the page:\n\n' + '\n'.join(links) if links else ''
        
        pretty_soup = html_to_markdown_with_depth(soup.prettify(formatter="minimal"), 4)

        
        return pretty_soup + plain_text
    except requests.exceptions.RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"Error parsing the webpage: {str(e)}"

def browse(urls=None):
    predefined_urls = urls or [
        "https://www.example.com",
        "https://www.python.org",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.wikipedia.org"
    ]
    
    while True:
        print("Choose a webpage to view:")
        for i, url in enumerate(predefined_urls, 1):
            print(f"{i}. {url}")
        print("0. Quit")
        
        choice = ask("Enter your choice",choices=[str(i) for i in range(len(predefined_urls) + 1)], show_default=False)   
        print(f"Choice: {choice}")
        if choice == 'q':
            break
        
        try:
            url = predefined_urls[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
            continue
        
        # print(fetch_and_display(url))
        get_pages(url)
        print("getting page")
        page = full_page(url)
        # console.print("Webpage content:")
        console.print(Panel(Markdown(page), title=f"Webpage: {url}", border_style="bold", style="on cyan1", padding=(0,1,1,1)))
        
        continue_viewing = input("Do you want to view another webpage?", choices=["y", "n"])
        if continue_viewing == "n":
            break

if __name__ == "__main__":
    prompt_for_webpage()
