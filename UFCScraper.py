import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def scrape_fighters(url):
    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    fighters = []
    fighter_tags = soup.find_all(class_='t-b-fcc')
    num_fighters = len(fighter_tags)
    for i in range(0, num_fighters, 2):
        fighter1 = fighter_tags[i].text.strip()
        fighter2 = fighter_tags[i+1].text.strip()
        match_number = f"Match ({num_fighters // 2 - i // 2})"
        fighters.append((match_number, fighter1, fighter2))

    driver.quit()

    return fighters


def write_to_csv(fighters, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Match Number', 'Fighter 1', 'Fighter 2'])
        for match_number, fighter1, fighter2 in fighters:
            writer.writerow([match_number, fighter1, fighter2])


if __name__ == '__main__':
    url = 'https://www.bestfightodds.com/events/ufc-292-2886'
    fighters = scrape_fighters(url)
    write_to_csv(fighters, 'fighters.csv')
    print('Data has been scraped and saved to fighters.csv')
