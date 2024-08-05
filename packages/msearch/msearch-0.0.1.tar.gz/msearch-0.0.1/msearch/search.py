import re
import traceback
import urllib.parse

import git
import requests
from bs4 import BeautifulSoup
from github import Github, GithubException
from mrender.web2md import html_to_markdown_with_depth
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.spinner import Spinner
from rich.text import Span, Text

from msearch.browse import browse

console = Console(style="bold white on cyan1", soft_wrap=True)
blue_console = Console(style="bold white on blue", soft_wrap=True)
print = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="red", overflow="fold")) for arg in args), **kwargs) # noqa
print_bold = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="bold", overflow="fold")) for arg in args), **kwargs)
input = lambda arg, **kwargs: Confirm.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, default="y", **kwargs) # noqa
ask = lambda arg, **kwargs: Prompt.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, **kwargs) # noqa


def cmd_web(args):
        "Search the web and display results"
        if not args.strip():
            self.io.tool_error("Please provide a search query.")
            return

        search_url = f"https://www.google.com/search?q={args}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            response = requests.get(search_url, headers=headers, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            search_results = []
            for result in soup.select('div.g'):
                title_elem = result.select_one('h3')
                link_elem = result.select_one('a')
                snippet_elem = result.select_one('div.VwiC3b')
                
                if title_elem and link_elem and snippet_elem:
                    title = title_elem.text
                    link = link_elem['href']
                    snippet = snippet_elem.text.strip()
                    search_results.append((title, link, snippet))

            if not search_results:
                print("No results found.")
                return "No results found."

            result_string = "Web Search Results:\n"
            for i, (title, link, snippet) in enumerate(search_results, 1):
                result_string += f"{i}. Title: {title}\nURL: {link}\nSnippet: {snippet}\n\n"
            
            print(result_string)
            choice = ask("Enter a number to view: or q to quit ", choices=["q"] + [str(i) for i in range(1, len(search_results) + 1)])
            if choice == "q":
                return
            else:
                choice = int(choice)
                if choice < 1 or choice > len(search_results):
                    print("Invalid choice.")
                    return
                browse([search_results[choice - 1][1]])
            return result_string
        except Exception as e:
            print(f"An error occurred: {traceback.format_exc()}")
            return None

def search_github(args):
        """Search GitHub using current git credentials and the Python GitHub library.

        Usage: /github_search [repo:owner/name] [user:username] [language:lang] [filename:name] search_term.
        """
        if Github is None:
            return "The 'github' module is not installed. Please install it using: pip install PyGithub"


        try:
            # Get the current repository
            repo = git.Repo(".", search_parent_directories=True)
            
            # Get the GitHub token from git config
            try:
                token = repo.git.config('--get', 'github.token')
            except git.exc.GitCommandError:
                print("Failed to retrieve GitHub token from git config.")
                print("Please set your GitHub token using: git config --global github.token YOUR_TOKEN")
                print("If you don't have a token, create one at https://github.com/settings/tokens")
                return
            
            if not token:
                print("GitHub token not found in git config.")
                print("Please set your GitHub token using: git config --global github.token YOUR_TOKEN")
                print("If you don't have a token, create one at https://github.com/settings/tokens")
                return

            # Create a Github instance
            g = Github(token)

            parts = args.split()
            qualifiers = {}
            search_term = []

            for part in parts:
                if part.startswith(("repo:", "user:", "language:", "filename:")):
                    qualifiers.update({part.split(":")[0]: part.split(":")[1]})
                else:
                    search_term.append(part)
            if not qualifiers:
                qualifiers = {"language": "python"}

            if not search_term:
                print("Please provide a search term.")
                return

            
            sort = "stars" if "stars" in search_term else "updated" if "updated" in search_term else None
            query = " ".join(search_term)
            query.replace("stars", "").replace("updated", "").replace("sort:", "").replace("sort", "").strip()
            # Perform the search
            try:
                print(f"Searching GitHub for: {query}")
                if sort:
                  results = g.search_repositories(query= query,
                                                  sort=sort, 
                                                  order="desc",
                                                  qualifiers=qualifiers
                                                  )

                else:
                  results = g.search_repositories(query= query,
                  sort="stars",
                  order="desc",
                                                  qualifiers=qualifiers
                                                  )

                # Display results in GitHub light theme
                print_bold(f"Search results for: {query}")
                
                page_size = 5
                page = 1
                total_results = results.totalCount
                
                while True:
                    start_idx = (page - 1) * page_size
                    end_idx = start_idx + page_size
                    
                    for item in list(results)[start_idx:end_idx]:
                        print_bold(f"\nFile: {item.name}")
                        print_bold(f"Repository: {item.repository.full_name}")
                        print_bold(f"URL: {item.html_url}")
                        
                        if ask("Do you want to read the code?",choices=["y", "n"]) == "y":
                            try:
                                content = g.search_code(f"{query} repo:{item.repository.full_name}", sort=sort)[0].decoded_content.decode()
                                print_bold("Content:")
                                print_bold(content)
                            except Exception as content_error:
                                print_bold(f"Error fetching content: {str(content_error)}")
                    
                    print_bold(f"\nPage {page} of {(total_results + page_size - 1) // page_size}")
                    
                    if end_idx >= total_results:
                        break
                    
                    if ask("View next page?", choices=["y", "n"]) != "y":
                        break
                    
                    page += 1

                if results.totalCount > 0:
                    first_result = next(iter(results))
                    repo_name = first_result.repository.full_name
                    if input(f"Would you like to browse the repository {repo_name}?", choices=["y", "n"]) == "y":
                        return browse([repo_name])
              
                return None

            except GithubException as github_error:
                print(f"GitHub API error: {github_error}")
                print(traceback.format_exc())

            except Exception as e:
                print(f"An error occurred while searching GitHub: {traceback.format_exc()}")

        except git.exc.InvalidGitRepositoryError:
            print("The current directory is not a valid Git repository.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        return None
  
if __name__ == "__main__":
  # Sample search query
  query = "repo:python/cpython language:python asyncio"
  repo = git.Repo(".", search_parent_directories=True)

  # Get the GitHub token from git config
  try:
      token = repo.git.config('--get', 'github.token')
  except git.exc.GitCommandError:
    raise Exception("Failed to retrieve GitHub token from git config.")  # noqa: B904

  g = Github(token)
  # Perform the search
  results = g.search_code(query="python org:mbodiai", qualifiers={"language": "python"})
  print(results)

  # Create a Github instance  
  results = cmd_web("python asyncio")

  print(results)
    