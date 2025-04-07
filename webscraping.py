import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ----------------------------------------
# PHASE 1: SCRAPE PAGINATED TABLES
# ----------------------------------------

base_url = "https://www.shl.com/solutions/products/product-catalog/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}

all_tables_html = []

# The catalog paginates in steps of 12, up to 132
for start in range(0, 133, 12):
    url = f"{base_url}?start={start}&type=1"
    print(f"Fetching: {url}")
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("div", class_="custom__table-responsive")

    if table:
        all_tables_html.append(table.prettify())
    else:
        print(f"No table found at: {url}")

# Combine all tables and save to file
with open("shl_tables.html", "w", encoding="utf-8") as f:
    f.write("\n\n".join(all_tables_html))

print("✅ Table scraping complete and saved to shl_tables.html")

# ----------------------------------------
# PHASE 2: PARSE TABLE AND EXTRACT BASIC INFO
# ----------------------------------------

with open("shl_tables.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

results = []

# Each row represents a product with a course ID
rows = soup.select("table tr[data-course-id]")

for row in rows:
    title_tag = row.select_one(".custom__table-heading__title a")
    solution_name = title_tag.text.strip()
    solution_link = f"https://www.shl.com{title_tag['href']}"

    # Check for remote testing and adaptive/IRT support
    remote_test = row.select("td")[1].find("span", class_="catalogue__circle -yes")
    adaptive_irt = row.select("td")[2].find("span", class_="catalogue__circle -yes")
    
    remote_test_status = "Yes" if remote_test else "No"
    adaptive_irt_status = "Yes" if adaptive_irt else "No"

    # Get test types
    test_types = [span.text.strip() for span in row.select(".product-catalogue__key")]

    results.append({
        "name": solution_name,
        "link": solution_link,
        "remote_testing": remote_test_status,
        "adaptive_irt": adaptive_irt_status,
        "test_types": ", ".join(test_types)
    })

# Save initial catalog data
df = pd.DataFrame(results)
df.to_csv("solutions_data.csv", index=False)
print("✅ Basic solution data saved to solutions_data.csv")

# ----------------------------------------
# PHASE 3: SCRAPE INDIVIDUAL PRODUCT DETAIL PAGES
# ----------------------------------------

# Load the previously saved catalog data
df = pd.read_csv("solutions_data.csv")
urls = df["link"].tolist()

def scrape_detail_page(url):
    """Scrape a solution detail page and extract extra info."""
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Helper to get <p> text immediately following an <h4>
    def get_p_after_h4(text):
        h4 = soup.find("h4", string=text)
        if h4:
            p = h4.find_next_sibling("p")
            return p.get_text(strip=True) if p else ""
        return ""

    # Extract key fields
    description = get_p_after_h4("Description")
    levels_text = get_p_after_h4("Job levels")
    languages_text = get_p_after_h4("Languages")
    length_text = get_p_after_h4("Assessment length")

    job_levels = [lvl.strip() for lvl in levels_text.split(",") if lvl.strip()]
    languages = [lang.strip() for lang in languages_text.split(",") if lang.strip()]
    duration = length_text.split("=", 1)[1].strip() if "=" in length_text else length_text

    return {
        "description": description,
        "job_levels": job_levels,
        "languages": languages,
        "duration": duration or "N/A"
    }

# Scrape each detail page
detail_records = []
start = time.time()

for url in urls:
    print(f"Scraping {url}")
    detail_records.append(scrape_detail_page(url))

print(f"✅ Scraped {len(urls)} detail pages in {time.time() - start:.2f} seconds")

# Combine detail data with initial data
sample_df = df.reset_index(drop=True)
details_df = pd.DataFrame(detail_records)
enriched = pd.concat([sample_df, details_df], axis=1)

# Save enriched dataset
enriched.to_csv("data_shl.csv", index=False)

# Print a preview
print("\nSample of enriched data:")
print(enriched[["name", "duration", "job_levels", "languages", "description"]].head())
