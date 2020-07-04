import time
import joblib
import requests
import numpy as np
from bs4 import BeautifulSoup
from urllib.parse import unquote
from scipy.spatial import distance


class Utils:
    model = joblib.load('model.joblib')
    base = 'https://en.wikipedia.org'
    empty = np.array([0.5 for i in range(50)])
    invalid = {'/wiki/main_page', '#wikipedians'}

    @staticmethod
    def get_text(href):
        """ Get href text before converting to vector """
        href = href.lower()
        return unquote(href.split('/')[2]).replace('_', ' ')

    @staticmethod
    def get_vector(text):
        """ Get vector for given text """
        words = text.split(' ')
        try:
            return Utils.model[words[0]]
        except KeyError:
            return Utils.empty

    @staticmethod
    def get_distance(text, target_vector):
        """ Calculate distance """
        vector = Utils.get_vector(text)
        return distance.cosine(vector, target_vector)

    @staticmethod
    def anchor_is_valid(anchor):
        """ """
        try:
            anchor['href'] = anchor['href'].lower()
            href = anchor['href']
        except KeyError:
            return False
        if href[0:6] != '/wiki/' or (':' in href) or ('.' in href):
            return False
        anchor['href'] = anchor['href'].lower()

        if anchor['href'] in Utils.invalid:
            return False

        return True


class Page:
    def __init__(self, prev, href: str, target_vector: np.array):
        self.prev = prev
        self.href = href
        self.text = Utils.get_text(self.href)
        self.distance = Utils.get_distance(self.text, target_vector)
        self.branch_indexes = {}
        self.branches = []

    def explore(self, target_vector):
        """ Explores the pages and creates branches to more pages """
        data = requests.get(f'{Utils.base}/{self.href}').text
        soup = BeautifulSoup(data, 'html.parser')
        anchors = soup.find_all('a')

        for anchor in anchors:
            if Utils.anchor_is_valid(anchor):
                # Create branch
                href = anchor['href']
                page = Page(self, href, target_vector)
                self.branches.append(page)
                self.branch_indexes[href] = None

        # Sort pages by most ascending in distance (most relevant to least relevant)
        self.branches.sort(key=lambda page: page.distance)
        for i, branch in enumerate(self.branches):
            self.branch_indexes[branch.href] = i

    def has_solution(self, target_href):
        """ The page has a link to the target """
        return target_href in self.branch_indexes

    def get(self, href):
        """ Get a branch """
        return self.branches[self.branch_indexes[href]]


class Solver:
    def __init__(self, start_href: str, target_href: str, explore_limit=200):
        self.start_href = start_href
        self.target_href = target_href
        self.target_vector = Utils.get_vector(Utils.get_text(target_href))

        self.explored = set()                                               # Explored pages
        self.explore_limit = explore_limit                                  # Maximum number of pages to explore
        self.queue = []                                                     # Queue of pages to explore
        self.queue.append(Page(None, start_href, self.target_vector))       # Add the first page

    def solve(self) -> Page:
        """ Finds the target page """
        print(f'SOLVING: {self.start_href} -> {self.target_href}')
        start = time.time()

        explored = 0
        while explored < self.explore_limit:
            # Explore the next page
            page = self.queue.pop(0)
            if page.href in self.explored:
                continue

            print(f'distance: {round(page.distance, 3)}, exploring: {page.href}', )
            page.explore(self.target_vector)
            self.explored.add(page.href)

            # Check for the target page
            if page.has_solution(self.target_href):
                page = page.get(self.target_href)
                end = time.time()
                print(f'SOLVED: {Solver.path(page)} ({round(end - start, 1)} seconds)')
                return page

            # Add the 4 most relevant branches
            self.queue += page.branches[:4]

        raise Exception(f'Could not find a path from {self.start_href} to {self.target_href}')

    @staticmethod
    def path(page: Page) -> str:
        """ Creates the path from start href to target href """
        path = [page.href]
        while page.prev is not None:
            page = page.prev
            path.append(page.href)
        path.reverse()
        return ' -> '.join(path)


solver = Solver('/wiki/crocodile', '/wiki/salad')
target = solver.solve()
