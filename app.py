import random
import subprocess
import time

import chess
import chess.engine
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def find_executable(executable):
    result = subprocess.run(['which', executable], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip()

CHROMEDRIVER_PATH = find_executable('chromedriver')
STOCKFISH_PATH = find_executable('stockfish')

LICHESS_URL = 'https://lichess.org/'
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
WINDOW_POSITION_X = 0
WINDOW_POSITION_Y = 0

SECONDS_LOADING_LICHESS = 2
SECONDS_LOADING_SIGN_IN = 2
SECONDS_LOADING_PAIRING_PAGE = 2
SECONDS_LICHESS_UPDATING_WEBPAGE_TITLE = .5
SECONDS_OPEN_AFTER_GAME_ENDS = 300

LICHESS_USERNAME = ''
LICHESS_PASSWORD = ''
TIME_CONTROL = '3+0'
ENGINE_ANALYSIS_TIME = .1
DISTANCE_BETWEEN_TOP_OF_SCREEN_AND_LICHESS = 184
ANONYMOUS_MODE = True

class ChessEngine:
    def __init__(self, path):
        self.engine = chess.engine.SimpleEngine.popen_uci(path)

    def convert_moves_to_board(self, moves):
        board = chess.Board()
        for move in moves:
            board.push_san(move)
        return board

    def get_best_move(self, moves):
        board = self.convert_moves_to_board(moves)
        result = self.engine.play(board, chess.engine.Limit(time=ENGINE_ANALYSIS_TIME))
        return result.move.uci()

    def close(self):
        self.engine.quit()

def extract_moves(driver):
    move_elements = driver.find_elements(By.TAG_NAME, 'kwdb')
    moves = []
    for move_element in move_elements:
        move_text = move_element.text.strip()
        if move_text:
            moves.append(move_text)
    return moves

def set_fixed_window_size(driver, width, height):
    driver.set_window_size(width, height)

def log_in(driver, username, password):
    sign_in_button = driver.find_element(By.LINK_TEXT, 'SIGN IN')
    sign_in_button.click()
    time.sleep(SECONDS_LOADING_SIGN_IN)
    username_field = driver.find_element(By.ID, 'form3-username')
    username_field.send_keys(username)
    password_field = driver.find_element(By.ID, 'form3-password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

def select_time_control(driver, time_control):
    button_selector = f'div[data-id="{time_control}"]'
    time_control_button = driver.find_element(By.CSS_SELECTOR, button_selector)
    time_control_button.click()

def await_game_start(driver):
    while True:
        title = driver.execute_script('return document.title;')
        if 'Your turn' in title or 'Waiting for opponent' in title:
            return True

def get_player_color(driver):
    try:
        driver.find_element(By.CLASS_NAME, 'orientation-white')
        return 'white'
    except:
        return 'black'

def check_game_status(driver):
    while True:
        title = driver.execute_script('return document.title;')
        if 'Game Over' in title:
            return 'game_over'
        if 'Your turn' in title:
            return 'your_move'

def get_moves(driver):
    move_elements = driver.find_elements(By.TAG_NAME, 'kwdb')
    moves = [element.text.strip() for element in move_elements if element.text.strip()]
    return moves

def get_square_pixel_coordinates(square, square_size, chessboard_location, player_color):
    def file_to_zero_based_index(file, color):
        index = ord(file) - ord('a')
        return 7 - index if color == 'black' else index

    def rank_to_zero_based_index(rank, color):
        return 8 - int(rank) if color == 'white' else int(rank) - 1

    file_index = file_to_zero_based_index(square[0], player_color)
    rank_index = rank_to_zero_based_index(square[1], player_color)

    pixel_x = chessboard_location['x'] + (file_index * square_size) + (square_size / 2)
    pixel_y = chessboard_location['y'] + (rank_index * square_size) + (square_size / 2) + DISTANCE_BETWEEN_TOP_OF_SCREEN_AND_LICHESS
    return (pixel_x, pixel_y)

def play_game(driver, engine, color):
    while True:
        status = check_game_status(driver)
        if status == 'game_over':
            time.sleep(SECONDS_OPEN_AFTER_GAME_ENDS)
        if status == 'your_move':
            all_moves = get_moves(driver)
            best_next_move = engine.get_best_move(all_moves)
            execute_move(driver, best_next_move, color)
            time.sleep(SECONDS_LICHESS_UPDATING_WEBPAGE_TITLE)

def extract_squares_from_long_algebraic_notation(move):
    return move[:2], move[2:]

def get_chessboard_location_and_square_size(driver):
    chessboard = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'cg-board'))
    )
    chessboard_location = chessboard.location
    chessboard_size = chessboard.size
    square_size = chessboard_size['width'] / 8
    return chessboard_location, square_size

def automate_move_with_pyautogui(source_coords, target_coords):
    pyautogui.moveTo(source_coords[0], source_coords[1], duration=.05)
    pyautogui.click()
    pyautogui.moveTo(target_coords[0], target_coords[1], duration=.05)
    pyautogui.click()

def execute_move(driver, move, color):
    source_square, target_square = extract_squares_from_long_algebraic_notation(move)
    chessboard_location, square_size = get_chessboard_location_and_square_size(driver)
    source_coords = get_square_pixel_coordinates(source_square, square_size, chessboard_location, color)
    target_coords = get_square_pixel_coordinates(target_square, square_size, chessboard_location, color)
    automate_move_with_pyautogui(source_coords, target_coords)

def main():
    service = webdriver.chrome.service.Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service)

    driver.get(LICHESS_URL)
    set_fixed_window_size(driver, WINDOW_WIDTH, WINDOW_HEIGHT)
    driver.set_window_position(WINDOW_POSITION_X, WINDOW_POSITION_Y)
    time.sleep(SECONDS_LOADING_LICHESS)

    engine = ChessEngine(STOCKFISH_PATH)

    if not ANONYMOUS_MODE:
        log_in(driver, LICHESS_USERNAME, LICHESS_PASSWORD)
        time.sleep(SECONDS_LOADING_PAIRING_PAGE)

    select_time_control(driver, TIME_CONTROL)
    await_game_start(driver)
    player_color = get_player_color(driver)
    play_game(driver, engine, player_color)

    engine.close()

if __name__ == '__main__':
    main()
