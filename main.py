import requests
from bs4 import BeautifulSoup
import csv


class IPLDataScraper:
    def __init__(self):
        self.urls = {
            'most_matches_career': 'https://www.espncricinfo.com/records/trophy/individual-most-matches-career/indian'
                                   '-premier-league-117',
            'most_runs_career': 'https://www.espncricinfo.com/records/trophy/batting-most-runs-career/indian-premier'
                                '-league-117',
            'most_runs_innings': 'https://www.espncricinfo.com/records/trophy/batting-most-runs-innings/indian'
                                 '-premier-league-117',
            'most_sixes_career': 'https://www.espncricinfo.com/records/trophy/batting-most-sixes-career/indian'
                                 '-premier-league-117',
            'highest_strike_rate_career': 'https://www.espncricinfo.com/records/trophy/batting-highest-career-strike'
                                          '-rate/indian-premier-league-117',
            'most_fours': 'https://timesofindia.indiatimes.com/sports/cricket/ipl/stats/batsman-most-fours'
        }

    def scrape_data_espncricinfo(self, url, player_col, stat_col):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table').find('tbody')
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            player_name = cols[player_col].text.strip().split('(')[0].strip()
            stat = cols[stat_col].text.strip()
            if stat.endswith('*'):
                stat = stat[:-1]  # Remove the last character
            data.append([player_name, stat])
        return data

    def scrape_data_timesofindia(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        players = soup.find_all('span', {'class': 'team'})
        stats = soup.find_all('h2')[1:]
        data = []
        for player, stat in zip(players, stats):
            player_name = player.text.strip().split('(')[0].strip()
            stat = stat.text.strip()
            data.append([player_name, stat])
        return data

    def save_to_csv(self, data, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def scrape_most_matches_career(self):
        data = self.scrape_data_espncricinfo(self.urls['most_matches_career'], 0, 2)
        self.save_to_csv(data, 'ipl_most_matches_career.csv')

    def scrape_most_runs_career(self):
        data = self.scrape_data_espncricinfo(self.urls['most_runs_career'], 0, 5)
        self.save_to_csv(data, 'ipl_most_runs_career.csv')

    def scrape_most_runs_innings(self):
        data = self.scrape_data_espncricinfo(self.urls['most_runs_innings'], 0, 1)
        self.save_to_csv(data, 'ipl_most_runs_innings.csv')

    def scrape_most_sixes_career(self):
        data = self.scrape_data_espncricinfo(self.urls['most_sixes_career'], 0, 14)
        self.save_to_csv(data, 'ipl_most_sixes_career.csv')

    def scrape_highest_strike_rate_career(self):
        data = self.scrape_data_espncricinfo(self.urls['highest_strike_rate_career'], 0, 9)
        self.save_to_csv(data, 'ipl_highest_strike_rate_career.csv')

    def scrape_most_fours(self):
        data = self.scrape_data_timesofindia(self.urls['most_fours'])
        self.save_to_csv(data, 'ipl_most_fours.csv')

    def main(self):
        self.scrape_most_matches_career()
        self.scrape_most_runs_career()
        self.scrape_most_runs_innings()
        self.scrape_most_sixes_career()
        self.scrape_highest_strike_rate_career()
        self.scrape_most_fours()


if __name__ == "__main__":
    scraper = IPLDataScraper()
    scraper.main()
