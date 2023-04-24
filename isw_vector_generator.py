import isw_html_to_txt
import isw_txt_to_vec
import isw_year_total_scraper


def main():
    isw_year_total_scraper.main()
    print("Refreshed isw reports")
    isw_html_to_txt.main()
    print("Cleaned new isw reports")
    isw_txt_to_vec.main()
    print("Regenerated isw vectors")
