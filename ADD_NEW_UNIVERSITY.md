# How to Add a New University

This project is modular — each university has its own scraping function because HTML structures differ.

## Quick Steps

1.  **Inspect the department page**
    Open the URL from `input/Universities.csv` in Chrome → `F12` → Elements.
    Find one lecturer card. Note selectors for:
    - Name (e.g., `h4.name`, `h2`, `a`)
    - Position (e.g., `span`, `h4`, `p.position`)
    - Image (`img[src]`)
    - Faculty/Department header (`div.header-sitename`, `h3`)

2.  **Copy template**
    Copy `scraper_template.py:scrape_example_university` to `scraper.py` as `scrape_myuni(url)`.

3.  **Adjust selectors**
    Replace `.staff-card` with what you found. See `scraper.py:22` (ABU) and `scraper.py:71` (Unilorin) as working examples.

4.  **Test locally**
    ```python
    from scraper import scrape_myuni
    print(scrape_myuni("https://your-university.edu/dept"))
    ```

5.  **Register**
    In `scraper.py:128` `scrape_university()`:
    ```python
    elif university == "my university name":
        return scrape_myuni(url)
    ```

6.  **Add to input**
    Add row to `input/Universities.csv`:
    ```
    My University Name,https://your-university.edu/dept
    ```

7.  **Run**
    ```bash
    python main.py
    ```

## Generic Fallback

If you don't want to write custom logic, `scraper.py:generic` `scrape_generic()` will try common selectors (`div.col-lg-3`, `div.team-member`, etc.). Just add the URL to `Universities.csv` with any university name — it will auto-try generic parsing and log the selector used.

For production, always write a dedicated function — generic is ~70% accurate.

## Debugging Tips

- `fetch_page()` uses `config.py:2` `HEADERS`. Some sites block without User-Agent.
- Save HTML locally: `open("debug.html","w",encoding="utf8").write(soup.prettify())`
- Check `output/logs/app.log` for `WARNING` lines.
