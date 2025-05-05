import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter
import os, re
from colorama import Fore, Style, init
import validators  # To check if URL is valid

init(autoreset=True)

def banner():
    os.system("clear")  # Clear screen
    print(Fore.CYAN + """
███╗   ██╗ ██████╗ ███████╗██████╗ ███████╗
████╗  ██║██╔═══██╗██╔════╝██╔══██╗██╔════╝
██╔██╗ ██║██║   ██║█████╗  ██████╔╝███████╗
██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗╚════██║
██║ ╚████║╚██████╔╝███████╗██║  ██║███████║
╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝
     Web Data Extractor v1.0 (Pro)
        
              By: C0D3 BR34K3R 
              Termux Edition 🔥
 
YouTube: @TayyabExploits 
 GitHub: github.com/TayyabExploits
    """ + Style.RESET_ALL)

def clean_text(text):
    return re.findall(r'\b\w+\b', text.lower())

def scrape_website(url):
    try:
        print(Fore.YELLOW + "\n🔍 Scraping website, please wait...\n")
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) TermuxScraper/2.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string.strip() if soup.title else "No Title Found"
        meta_desc = soup.find('meta', attrs={"name": "description"})
        description = meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else "Not Found"
        language = soup.find("html").get("lang", "Unknown")

        headings = {tag: [h.get_text(strip=True) for h in soup.find_all(tag)] for tag in ["h1", "h2", "h3"]}

        domain = urlparse(url).netloc
        all_links = [urljoin(url, a.get("href")) for a in soup.find_all("a") if a.get("href")]
        internal = [link for link in all_links if domain in urlparse(link).netloc]
        external = [link for link in all_links if domain not in urlparse(link).netloc]

        images = [urljoin(url, img.get("src")) for img in soup.find_all("img") if img.get("src")]

        text = soup.get_text(separator=' ')
        word_count = len(text.split())

        words = clean_text(text)
        stopwords = {"the", "and", "is", "in", "to", "of", "a", "for", "on", "it", "with"}
        filtered_words = [word for word in words if word not in stopwords]
        top_keywords = Counter(filtered_words).most_common(10)

        print(Fore.GREEN + f"📄 Title: {title}")
        print(f"🌐 Language: {language}")
        print(f"📝 Meta Description: {description}")
        print(f"🔢 Word Count: {word_count}")

        print(Fore.MAGENTA + "\n🔠 Headings Found:")
        for tag, items in headings.items():
            print(Fore.CYAN + f"\n{tag.upper()} Tags:")
            for i, text in enumerate(items, 1):
                print(f"{i}. {text}")

        print(Fore.YELLOW + f"\n🔗 Internal Links ({len(internal)}):")
        for i, link in enumerate(internal, 1):
            print(f"{i}. {link}")

        print(Fore.RED + f"\n🌍 External Links ({len(external)}):")
        for i, link in enumerate(external, 1):
            print(f"{i}. {link}")

        print(Fore.BLUE + f"\n🖼️ Images Found ({len(images)}):")
        for i, img in enumerate(images, 1):
            print(f"{i}. {img}")

        print(Fore.GREEN + "\n📊 Top 10 Keywords:")
        for word, count in top_keywords:
            print(f"{word}: {count}")

        save = input(Fore.YELLOW + "\n💾 Save output to file? (y/n): ").strip().lower()
        if save == "y":
            with open("scrape_result.txt", "w", encoding="utf-8") as f:
                f.write(f"Title: {title}\nLanguage: {language}\nDescription: {description}\nWord Count: {word_count}\n\n")
                f.write("Top 10 Keywords:\n")
                for word, count in top_keywords:
                    f.write(f"{word}: {count}\n")
                f.write("\nInternal Links:\n" + "\n".join(internal))
                f.write("\n\nExternal Links:\n" + "\n".join(external))
                f.write("\n\nImages:\n" + "\n".join(images))
            print(Fore.GREEN + "✅ Output saved to scrape_result.txt")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"❌ Request Error: {e}")
    except Exception as e:
        print(Fore.RED + f"❌ Error: {e}")

if __name__ == "__main__":
    banner()  # Display the banner first
    
    while True:
        print(Fore.YELLOW + "\n🔗 Enter your website URL for scraping (e.g., https://example.com)")
        target_url = input(Fore.CYAN + "> " + Style.RESET_ALL).strip()
        
        if not target_url:
            print(Fore.RED + "❌ Please enter a URL")
            continue
            
        if not validators.url(target_url):
            print(Fore.RED + "❌ Invalid URL format. Please enter a valid website URL (e.g., https://example.com)")
            continue
            
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'https://' + target_url
            print(Fore.YELLOW + f"⚠️ Added https:// prefix. Trying with: {target_url}")
            
        try:
            scrape_website(target_url)
            break
        except:
            print(Fore.RED + "❌ Failed to scrape the website. Please check the URL and try again")
