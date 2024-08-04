import os
import time
import threading
import http.server
import socketserver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import cv2
import numpy as np
from loguru import logger

class SlideCapturer:
    def __init__(self, output_dir, port=8000, html_file='index.html', slide_dir="slides"):
        self.output_dir = output_dir        
        self.save_dir  = os.path.join(output_dir, 'slides')
        self.save_dir_img  = os.path.join(self.save_dir, 'img')
        self.save_dir_video  = os.path.join(self.save_dir, 'video')
        os.makedirs(self.save_dir_img, exist_ok=True)
        os.makedirs(self.save_dir_video, exist_ok=True)
        
        self.port = port
        self.html_file = html_file
        self.server = None
        self.server_thread = None

    def start_server(self):
        output_dir = self.output_dir
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=output_dir, **kwargs)

        self.server = socketserver.TCPServer(("", self.port), Handler)
        logger.info(f"サーバーが http://localhost:{self.port} で起動しました")
        self.server.serve_forever()

    def stop_server(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    def capture_slides_as_png(self):
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        time.sleep(2)  # サーバーの起動を待つ

        options = Options()
        # options.add_argument('-headless')  # ヘッドレスモードを有効にする場合はコメントを外す
        driver = webdriver.Firefox(options=options)

        try:
            driver.get(f'http://localhost:{self.port}/{self.html_file}')

            slides = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'step'))
            )

            for i in tqdm(range(len(slides)), desc="スライドのキャプチャ"):
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f".step:nth-child({i+1})"))
                )
                
                time.sleep(5)  # スライドの表示を待つ
                
                driver.save_screenshot(f'{self.save_dir_img}/slide_{i+1}.png')
                
                if i < len(slides) - 1:
                    webdriver.ActionChains(driver).send_keys(Keys.RIGHT).perform()
                
                time.sleep(1)  # アニメーションの完了を待つ

            logger.success("全てのスライドのキャプチャが完了しました。")
        except Exception as e:
            logger.error(f"キャプチャ中にエラーが発生しました: {str(e)}")
        finally:
            driver.quit()
            self.stop_server()

    def capture_slides_as_video(self, fps=30, duration=5):
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        time.sleep(2)  # サーバーの起動を待つ

        options = Options()
        # options.add_argument('-headless')  # ヘッドレスモードを有効にする場合はコメントを外す
        driver = webdriver.Firefox(options=options)

        try:
            driver.get(f'http://localhost:{self.port}/{self.html_file}')

            slides = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'step'))
            )

            frame_count = 0
            for i in tqdm(range(len(slides)), desc="スライドのキャプチャ"):
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f".step:nth-child({i+1})"))
                )

                for j in range(fps * duration):
                    driver.save_screenshot(f'{self.save_dir_video}/slide_{frame_count:05d}.png')
                    frame_count += 1
                    time.sleep(1 / fps)

                if i < len(slides) - 1:
                    webdriver.ActionChains(driver).send_keys(Keys.RIGHT).perform()
                    for j in range(fps):  # 1秒間のトランジションを仮定
                        driver.save_screenshot(f'{self.save_dir_video}/slide_{frame_count:05d}.png')
                        frame_count += 1
                        time.sleep(1 / fps)

            logger.success("全てのスライドのキャプチャが完了しました。")
        except Exception as e:
            logger.error(f"キャプチャ中にエラーが発生しました: {str(e)}")
        finally:
            driver.quit()
            self.stop_server()

    def create_video_from_images(self, image_folder, output_video_name, fps=30):
        images = [img for img in os.listdir(self.save_dir_video) if img.endswith(".png")]
        images.sort()

        if not images:
            logger.warning("画像ファイルが見つかりません。")
            return

        frame = cv2.imread(os.path.join(self.save_dir_video, images[0]))
        height, width, layers = frame.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_video_name, fourcc, fps, (width, height))

        for image in tqdm(images, desc="動画の作成"):
            video.write(cv2.imread(os.path.join(self.save_dir_video, image)))

        cv2.destroyAllWindows()
        video.release()
        logger.success(f"動画の作成が完了しました: {output_video_name}")
