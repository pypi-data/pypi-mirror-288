import os
import re
import cv2
import time
import json
import random
import string
import shutil
import zipfile
import requests
from typing import Union, List
from selenium import webdriver
from colorama import Fore, Style, init
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from collections.abc import MutableMapping, MutableSequence
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class tag():
    A = "a"
    P = "p"
    DIV = "div"
    IMG = "img"
    SPAN = "span"
    INPUT = "input"
    OPTION = "option"
    BUTTON = "button"
class mailtm():
    def __init__(self, dot="gw", proxy:str=""):
        self.dot = dot
        if proxy.count(':') == 3:
            ip, port, user, passwd = proxy.split(":")
            self.proxies = {"http": f"http://{user}:{passwd}@{ip}:{port}", "https": f"http://{user}:{passwd}@{ip}:{port}"}
        elif proxy.count(':') == 1:
            self.proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        else:
            self.proxies = {"http": "", "https": ""}
    def creat_email(self):
        for _ in range(30):
            try:
                # Tạo email mới
                domain = requests.get(f'https://api.mail.{self.dot}/domains', proxies=self.proxies, timeout=5).json()
                self.user_mail = f"{randuser().lower()}@{random.choice(domain['hydra:member'])['domain']}"
                json_data = {'address': self.user_mail,'password': '123456Aa@'}
                # Confirm email và lấy token email
                requests.post(f'https://api.mail.{self.dot}/accounts', proxies=self.proxies, json=json_data, timeout=5)
                self.token = requests.post(f'https://api.mail.{self.dot}/token', proxies=self.proxies, json=json_data, timeout=5)
                return self.user_mail, {'Authorization': f"Bearer {self.token.json()['token']}"}
            except Exception as bug:
                print(bug)
    def get_otp(self, content:str="", otp=True):
        for _ in range(30):
            try:
                time.sleep(3)
                headers = {'Authorization': f"Bearer {self.token.json()['token']}"}
                id_message = requests.get(f'https://api.mail.{self.dot}/messages', headers=headers, timeout=5).json()['hydra:member'][0]['id']
                message = requests.get(f'https://api.mail.{self.dot}/messages/{id_message}', headers=headers, timeout=5)
                if otp: # Trả về kết quả OTP là 4 hoặc 6 số
                    return re.findall(rf'{content}\s?(\b\d{{4}}\b|\b\d{{6}}\b)', message.json()['html'][0])[0]
                else:
                    return message.json()['html'][0]
            except Exception as bug:
                print(bug)
class mth_api():
    def get_phone(mth=0, prefix="vn") -> str:
        for _ in range(3):
            try:
                if prefix == "vn":
                    phone_range_name = random.choice(["vnm_2_part_1","vnm_2_part_2","vnm_2_part_3","vnm_2_part_4","vnm_2_part_5"])
                elif prefix == "cambo":
                    phone_range_name = random.choice(["cam1_1","cam1_2","cam1_3","cam2","cam1_1_part_1","cam1_1_part_2","cam1_2",
                                                     "cam4_cellcard_part_1","cam4_cellcard_part_2","cam4_cellcard_part_3",
                                                     "cam4_cellcard_part_4","cam4_cellcard_part_5","cam4_cellcard_part_6",
                                                     "cam4_cellcard_part_7","cam4_cellcard_part_8","cam4_cellcard_part_9",
                                                     "cam4_cellcard_part_10", "cam1_3_part_1","cam1_3_part_2"])
                phones = requests.get(f'https://api.bestfit.click/phones/get-random?api_key=3f82f5aefaf2e13f9a14eb20bc4c53f5&phone_range_name={phone_range_name}')
                return phones.json()['data']['prefix'] + phones.json()['data']['phone'] # Trả về số điện thoại
            except Exception as bug:
                print(bug)
    def confirm_otp(get_phone:str, list_brand:list, loop=4, delay=8) -> str:
        for i in range(loop):
            try:
                time.sleep(delay)
                for brand in list_brand:
                    try:
                        response = requests.get(f'https://api.bestfit.click/gateway/get-otp-port2?api_key=3f82f5aefaf2e13f9a14eb20bc4c53f5&phone={get_phone}&brand={brand}')
                        if len(response.text) > 15 and 'Message not found' not in response.text:
                            break
                    except:
                        pass
                if 'Message not found' in response.text or 'MessageNotExistOrMessageSetPartner' in response.text:
                    print(f"{Fore.YELLOW}Check {get_phone} {time.strftime('%H:%M:%S')} không nhận được tin nhắn{Style.RESET_ALL}")
                else:
                    scr_file.write('done.txt', f"{i}|{time.strftime('%d/%m %H:%M:%S')}|{get_phone}|{response.json()['content']}")
                    print(f"{Fore.GREEN}Check {get_phone}|{response.json()['content']}{Style.RESET_ALL}")
                    return response.json()['content']
            except Exception as bug:
                print(bug)
#---------------------------------------------------------------------------------------------------------------------
def randuser() -> str:
    list_name = ["thai","giah","hoan","tran","hoan","duon","hoan","dong","leth","hoan","huyn","ngov","thai","dova","dang","giat","hath","vanv","leda","dang","pham","minh","huyn","pham","homa","vand","vana","vanq","hoan","cong","ngok","huy8","trie","tuan","duon","duon","pham","hoxu","buim","hotr","nguy","ngoh","hoai","xuan","tran","phan","lyho","lyph","chau","lam4","minh","chau","hong","thin","chep","dang","lamd","lamv","uyen","duon",
                 "phuo","ngoc","tran","badu","khan","tran","dang","pham","ledu","nghi","dung","lehu","khac","khan","nguy","phan","tien","phan","viet","lyth","phan","dang","camt","hoan","viet","hoan","hoan","phan","ngoc","uyen","tran","lamt","nguy","khan","leng","linh","vanq","hoan","phan","quan","buik","hoan","voda","daon","binh","huyn","hoan","ngop","phuo","thua","vuma","gian","huyn","toph","ledo","chau","lych","lamv","luuk",
                 "binh","tran","thev","yenm","lelo","haph","khan","than","quan","trun","thon","hotu","luua","lemy","luum","dinh","hoan","lamk","tamt","hatr","buin","tran","manh","song","phuo","luuv","ngod","huyn","khan","datl","hoan","doan","doan","taml","dinh","trim","bich","huyn","tron","dinh","lieu","daot","tron","chin","thuo","hoch","huyn","quyn","song","hoai","dang","anht","doan","truo","huyn","datd","lamn","lehu","nguy","buin",
                 "dang","leth","vinh","lamg","linh","binh","haba","thun","toho","buit","duon","ngot","haph","maig","ledu","ngod","tran","voye","nguy","dong","dang","toda","leth","vuon","than","vuch","pham","dinh","dang","huyn","than","phan","luub","lamt","pham","tran","chau","phuo","votr","thao","tran","ngod","phun","huyn","luuh","viet","daov","hoan","nguy","nuon","tran","baok","dinh","linh","lamc","vuth","duon","tien","than",
                 "luan","hoan","hoph","hoai","tuon","giak","xuan","than","than","vinh","loan","luuq","dung","nguy","leth","haph","leho","tran","phan","namt","dung","vuan","hoan","daot","tien","buit","thuy","chau","chau","khan","minh","huyn","trac","luuh","chau","vuan","hogi","tran","sonl","phuo","dang","lamp","clap","nguy","giat","datn","xuan","truo","huyn","linh","duon","nhun","maih","thit","vuch","ngoc","chau","doan","tuye","viet",
                 "thai","pham","hoan","daot","thid","vant","vuon","hoan","thuy","hoan","cuon","dung","loan","phuo","hopd","bang","buib","letu","lamm","huut","truo","linh","dinh","buim","duyt","dinh","khie","pham","nguy","hoan","hoan","ngoc","myph","ding","duon","pham","thuh","bach","hanc","khac","phuo","namn","phuo","trin","dinh","phon","phuo","lamk","hoan","anhk","nhid","hoah","tran","truo","hong","vech","khac","Doan","Loan",
                 "Ngan","NhuT","NgaH","TaKh","LanH","DaoC","Chuo","Chie","Dang","HopD","Lieu","Khan","TaLu","Hoan","NgaL","Doan","Dung","DauC","PhiH","Khon","LeCh","LeCu","Chie","Hong","HauH","Dang","HaoN","HanH","Doan","MyBi","Mien","HuaV","OnGD","AnBa","KimD","PhiT","Diep","Vuon","Khoi","GiaO","DoNh","LaCh","NhaV","LanN","Lieu","HueD","Khon","Trie","Hong","Gian","Hoai","LyDu","LeLy","Bang","Bach","Hoan","Nhun","Tang","Gian","Lieu",
                 "Nhan","Doan","Hanh","Phon","Luon","AnMi","Nguy","LamL","Luon","Ngoc","Quac","AnhD","LaDu","MacL","NhiL","Vuon","HopN","VoLo","Dinh","HuuP","Huyn","ChuO","Nghi","Huon","Binh","Khuo","DanD","Tang","Luon","DauP","MaiK","Nong","Hieu","LeNu","ChuL","HaLe","Chin","Duon","Nhan","Dang","Hoan","Pham","Giao","Huon","Duon","Lien","LaKh","Nguy","Chie","Doan","PhiD","Bach","LocN","Dang","LePh","LoiH","Luon","BaoL","Diem",
                 "Phun","AnhD","Ngan","CamC","Nguy","HopC","ToCa","Hanh","Khon","CamL","AnhL","BaoM","Cuon","Ngon","Giap","Nguy","LyMa","LeDa","Cuon","MiBi","KimH","MacK","LoTa","LamH","Binh","HoaK","GiaH","Giao","HaiP","Diep","Nguy","Khue","MiHa","Khai","LuuA","CatH","Khuy","CuHo","Doan","Hiep","Khan","Kieu","MacC","Phun","Hiep","Luon","NgaM","ChuG","Giap","LamD","LocD","Giap","ChuN","BaoD","Khan","Loan","Khoi","Nhie","Duye","Khai",
                 "Chuo","HaAn","HauN","Truo","Diem","MyLa","VoNg","HaDo","Nguy","ChuV","LamL","MacC","HaCh","Khon","Thai","HoaN","OnGM","Chun","Tran","Huon","DoKh","NhuK","Diem","Vuon","Dieu","Khoi","Doan","Nguy","Cuon","Khuy","LyAn","CamT","OnGB","AnhD","Loan","AnhL","Trie","HaoL","BaoD","Nguy","NgaA","Truo","Gian","Duon","Huyn","CamV","CatH","HoAn","DauH","Nuon","DoQu","Nhan","Chun","Dung","HopC","Huye","HaiM","LamM","Linh"]
    ran1, ran2 = random.randint(3, 4), random.randint(3, 4)
    return f"{random.choice(list_name)[:ran1]}{random.choice(list_name)[:ran2]}" + str(random.randint(1000, 999999))
def generate_random_string() -> str:
    letters = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(5, 8)))
    numbers = ''.join(random.choice(string.digits) for _ in range(random.randint(3, 5)))
    return letters + numbers
def creat_extension_proxy(PROXY, file_path, folder=False):
    try:
        # Xóa file extension cũ
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        pass
    PROXY = PROXY.split(":")
    manifest_json = """{
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
    }"""
    background_js = """var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
                },
                bypassList: ["localhost"]
            }
            };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );""" % (PROXY[0], PROXY[1], PROXY[2], PROXY[3])
    if folder:
        os.makedirs(file_path, exist_ok=True)
        with open(os.path.join(file_path, 'manifest.json'), 'w') as manifest_file:
            manifest_file.write(manifest_json)
        with open(os.path.join(file_path, 'background.js'), 'w') as background_file:
            background_file.write(background_js)
    else:
        with zipfile.ZipFile(file_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
#---------------------------------------------------------------------------------------------------------------------
class scr_file():
    def check_exist(path_file): # Dùng để kiểm tra và tạo file
        if os.path.exists(path_file) == False:
            open(path_file, mode="w").close()
    def check_exist_folder(path_folder): # Dùng để kiểm tra và tạo folder
        if os.path.exists(path_folder) == False:
            os.mkdir(path_folder)
    def get_data(path_data, path_temp, duplicate= 1):
        data_origin = []
        with open(path_data, mode="r", encoding="utf-8-sig") as file:
            for i in file.read().strip("\n").split("\n"):
                if len(i) > 5: data_origin.append(i)
        with open(path_temp, mode="r", encoding="utf-8-sig") as file:
            data_temp = file.read().strip("\n").split("\n")
        for data in data_origin: # Lọc data
            if data_temp.count(data) < duplicate: # Số trùng
                print("Choose:", data)
                return data
        input("Đã hết file data cơ bản")
    def write(path_file, content: str, mode: str = 'a+'):
        with open(path_file, mode=mode, encoding="utf-8-sig") as file:
            file.write(content + "\n")
    def write_json(path_file, data_json):
        with open(path_file, mode="w", encoding="utf-8-sig") as file:
            json.dump(data_json, file, indent= 4)
    def read_file(path) -> str:
        with open(path, mode= "r", encoding="utf-8-sig") as file:
            return file.read()
    def read_json(path) -> json:
        with open(path, mode= "r", encoding="utf-8-sig") as file:
            return json.loads(file.read())
    def readlines(path_file) -> list:
        data = []
        with open(path_file, mode="r", encoding="utf-8-sig") as file:
            for i in file.read().strip("\n").split("\n"):
                if len(i) > 2: data.append(i)
            return data
#---------------------------------------------------------------------------------------------------------------------
class get_proxy():
    def check_proxy(proxy:str) -> dict:
        # Kiểm tra địa chỉ IP của PROXY
        if proxy.count(':') == 3:
            ip, port, user, passwd = proxy.split(":")
            proxies = {"http": f"http://{user}:{passwd}@{ip}:{port}", "https": f"http://{user}:{passwd}@{ip}:{port}"}
        else:
            proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        myip = requests.get("https://geo.myip.link/", proxies=proxies, timeout=8).json()
        # Kiểm tra xem ipv4 hay ipv6
        ipv4 = False
        if len(myip["ip"]) < 20: ipv4 = True
        return {"ip": myip["ip"], "country": myip["country"], "ipv4": ipv4}
    def detect_key(api_key, newproxy=True):
        if ':' in api_key:
            return api_key
        elif api_key[:2] == 'TL':
            return get_proxy.tinsoft(api_key, newproxy=newproxy)
        elif api_key[:2] == 'UK':
            return get_proxy.wwproxy(api_key, newproxy=newproxy)
        elif '-' in api_key:
            return get_proxy.dtproxy(api_key, newproxy=newproxy)
        elif 'tmproxy' in api_key:
            return get_proxy.tmproxy(api_key.replace('tmproxy|', ''), newproxy=newproxy)
        elif 'proxyfb' in api_key:
            return get_proxy.proxyfb(api_key.replace('proxyfb|', ''), newproxy=newproxy)
        else:
            return False
    def tinsoft(api_key, newproxy=True):
        while True:
            response = requests.get("http://proxy.tinsoftsv.com/api/changeProxy.php?key=" + api_key).json()
            print("Tinsoft:", response)
            if response["success"] == True and len(response["proxy"]) > 10:
                return response["proxy"]
            elif response["success"] == False and (response["description"] == "wrong key!" or response["description"] == "key expired!"):
                input("Key lỗi hoặc đã hết hạn key tinsoft...")
            elif response["next_change"] > 6:
                if newproxy:
                    time.sleep(response["next_change"])
                else:
                    response = requests.get("http://proxy.tinsoftsv.com/api/getProxy.php?key=" + api_key).json()
                    return response["proxy"]
            else:
                time.sleep(6)
    def tmproxy(api_key, newproxy=True):
        while True:
            response = requests.post('https://tmproxy.com/api/proxy/get-new-proxy', json= {'api_key': api_key}).json()
            print("Tmproxy:", response)
            if response["code"] == 0 and len(response["data"]["https"]) > 10:
                return response["data"]["https"]
            elif response["code"] == 5 and "retry after" in response["message"]:
                if newproxy:
                    time.sleep(response["data"]["next_request"] + 1)
                else:
                    response = requests.post('https://tmproxy.com/api/proxy/get-current-proxy', json= {'api_key': api_key}).json()
                    return response["data"]["https"]
            elif response["code"] == 11 and response["message"] == "API không tồn tại":
                input("Key lỗi hoặc đã hết hạn key tmproxy...")
    def wwproxy(api_key, newproxy=True):
        while True:
            response = requests.get("https://wwproxy.com/api/client/proxy/available?key=" + api_key).json()
            print("wwproxy:", response)
            if response["status"] == "OK" and len(response["data"]["proxy"]) > 10:
                return response["data"]["proxy"]
            elif "hai lần lấy proxy tối thiểu" in response["message"]:
                if newproxy:
                    time.sleep(15)
                else:
                    response = requests.get("https://wwproxy.com/api/client/proxy/current?key=" + api_key).json()
                    return response["data"]["proxy"]
            elif response["status"] == "BAD_REQUEST":
                input(response["message"])
            else:
                time.sleep(6)
    def dtproxy(api_key, newproxy=True):
        while True:
            authen_ips = requests.get('https://api.ipify.org/').text
            response = requests.get(f'https://app.proxydt.com/api/public/proxy/get-new-proxy?license={api_key}&authen_ips={authen_ips}').json()
            print("Dtproxy:", response)
            if response["code"] == 1 and len(response["data"]["http_ipv4"]) > 10:
                return response["data"]["http_ipv4"].replace('http://', '')
            elif response["code"] == 0 and "Đang đổi" in response["message"]:
                time.sleep(6)
            elif response["code"] == 0 and "quá nhanh" in response["message"]:
                if newproxy:
                    time.sleep(6)
                else:
                    response = requests.post(f'https://app.proxydt.com/api/public/proxy/get-current-proxy?license={api_key}&authen_ips={authen_ips}').json()
                    return response["data"]["http_ipv4"].replace('http://', '')
            elif response["code"] == 11 and response["message"] == "API không tồn tại":
                input("Key lỗi hoặc đã hết hạn key tmproxy...")
    def proxyv6(api_key, newproxy=True):
        while True:
            authen_ips = requests.get('https://api.ipify.org/').text
            response = requests.get(f"https://api.proxyv6.net/key/get-new-ip?api_key_rotating={api_key}&authIp={authen_ips}").json()
            print(response)
            if response["message"] == "SUCCESS":
                return f"{response['data']['host']}:{response['data']['port']}"
            elif response["message"] == "GET_IP_TOO_FAST":
                time.sleep(response['data']['remainTime'])
            else:
                time.sleep(10)
    def proxyfb(api_key, newproxy=True):
        while True:
            try:
                response = requests.get("http://api.proxyfb.com/api/changeProxy.php?key=" + api_key).json()
                print("Proxyfb:", response)
                try:
                    if response["success"] == True:
                        return response['proxy']
                except:
                    pass
                if "Bạn cần đợi thêm" in response['message']:
                    if newproxy:
                        time.sleep(float(response['message'].split()[-1].strip('s'))+1)
                    else:
                        response = requests.get("http://api.proxyfb.com/api/getProxy.php?key=" + api_key).json()
                        return response['proxy']
                else:
                    time.sleep(10)
            except:
                time.sleep(12)
                
#---------------------------------------------------------------------------------------------------------------------
class ChromeAPI():
    def connect(chromedriver, remotePort, delay_open=10):
        time.sleep(delay_open)
        if "127.0.0.1" not in str(remotePort):
            remotePort = "127.0.0.1:" + str(remotePort)
        service = Service(chromedriver, service_args=["--silent", "--log-path=NUL"])
        options = Options()
        options.debugger_address = remotePort
        service.creation_flags = CREATE_NO_WINDOW
        browser = webdriver.Chrome(service= service, options= options)
        return browser
    def connect_v2(chromedriver, remotePort, delay_open=10):
        time.sleep(delay_open)
        if "127.0.0.1" not in str(remotePort):
            remotePort = "127.0.0.1:" + str(remotePort)
        options = Options()
        service = Service(chromedriver)
        caps = DesiredCapabilities.CHROME
        options.debugger_address = remotePort
        service.creation_flags = CREATE_NO_WINDOW
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        browser = webdriver.Chrome(service= service, options= options,
                                   desired_capabilities=caps)
        return browser
    def get_api_url(folder_gpm = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs\\GPMLogin"):
        with open(folder_gpm + "\\api_port.dat", mode="r") as file:
            return "127.0.0.1:" + file.read()

#---------------------------------------------------------------------------------------------------------------------
def open_chrome_selenium(userdatadir, vi_tri:int, extensions:str="", clear_profile=True, deviceName:str="", list_argumemt:list=[], window_size="400,800", scale:float=1, PROXY:str="") -> webdriver.Chrome:
    if clear_profile and os.path.exists(userdatadir):
        shutil.rmtree(userdatadir)
    # Thông số khởi chạy
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    # Mở chrome selenium
    chromeoptions = webdriver.ChromeOptions()
    for argumemt in list_argumemt:
        chromeoptions.add_argument(argumemt)
    chromeoptions.add_experimental_option("prefs", prefs)
    chromeoptions.add_argument(f"--window-size={window_size}")
    if PROXY.count(':') > 1:
        creat_extension_proxy(PROXY, f'image\\extension proxy {vi_tri}.zip')
        chromeoptions.add_extension(f'image\\extension proxy {vi_tri}.zip')
    else:
        chromeoptions.add_argument("--proxy-server=%s" % PROXY)
    chromeoptions.add_argument(f"--user-data-dir={userdatadir}")
    chromeoptions.add_argument(f"--force-device-scale-factor={scale}")
    chromeoptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromeoptions.add_argument(f'--window-position={(vi_tri%6)*400},{(vi_tri//6)*700}')
    if extensions != "": # Thêm extension cho chrome
        chromeoptions.add_extension(extensions)
    if deviceName != "": # Này là lựa chọn chrome cho mobile
        chromeoptions.add_experimental_option("mobileEmulation", {"deviceName": deviceName})
    return webdriver.Chrome(service=Service('chromedriver.exe'), options= chromeoptions)
class function_chrome():
    def __init__(self, browser: webdriver, vi_tri= None, delay= 10):
        self.delay = delay
        self.vi_tri = vi_tri
        self.browser = browser
        self.action = ActionChains(browser)
        self.wait = WebDriverWait(self.browser, self.delay)
        self.browser.switch_to.window(self.browser.current_window_handle)
    def wait_element(self, by: By, value: str, delay: int = 1, sl_rt: int = 1) -> Union[WebElement, List[WebElement]]:
        self.wait.until(EC.presence_of_element_located((by, value)))
        time.sleep(delay)
        if sl_rt > 1:
            return self.browser.find_elements(by, value)
        else:
            return self.browser.find_element(by, value)
    def wait_elements(self, by: By, value: str, delay: int = 1) -> Union[List[WebElement]]:
        self.wait.until(EC.presence_of_element_located((by, value)))
        time.sleep(delay)
        return self.browser.find_elements(by, value)
    def find_element_by_text(self, value:str, tag_name:str='div') -> Union[WebElement, List[WebElement]]:
        script = f'return Array.from(document.querySelectorAll("{tag_name}")).find(el => el.textContent.trim() === "{value}")'
        return self.browser.execute_script(script)
    def find_elements_by_text(self, value:str, tag_name:str='div') -> Union[WebElement, List[WebElement]]:
        script = f'return Array.from(document.querySelectorAll("{tag_name}")).filter((el) => el.textContent.trim() === "{value}")'
        return self.browser.execute_script(script)
    def wait_text_on_html(self, txt, delay=30, n=1):
        for i in range(delay):
            matches = list(re.finditer(txt, self.browser.page_source))
            if len(matches) >= n:
                return True
            else:
                time.sleep(1)
        return False
    def wait_text_on_url(self, txt, delay=10, duration= 1):
        for i in range(delay):
            time.sleep(duration)
            if txt in self.browser.current_url:
                return True
        return False
    def wait_bypass_recaptchav2(self, wait= 15):
        self.action.move_to_element(self.browser.find_elements(By.TAG_NAME, "iframe")[0]).perform()
        time.sleep(3)
        self.browser.switch_to.frame(self.browser.find_elements(By.TAG_NAME, "iframe")[0])
        for i in range(wait):
            time.sleep(3)
            if self.browser.find_element(By.ID, "recaptcha-anchor").get_attribute("aria-checked") == "true":
                self.browser.switch_to.window(self.browser.current_window_handle)
                return True
        return False
    def send_keys(self, content, duration= 0.1):
        for key in content: # Điền lastname
            self.action.send_keys(key).pause(random.uniform(0.5*duration, 1.5*duration)).perform()
        time.sleep(random.uniform(1, 1.5))
    def get_data_from_logs(self, key):
        def find_nested_value(dic, key): # Sử dụng đệ quy lọc dict
            for key_, value_ in dic.items():
                if key_ == key:
                    return value_
                if isinstance(value_, MutableMapping):
                    item = find_nested_value(value_, key)
                    if item is not None:
                        return item
                elif isinstance(value_, MutableSequence):
                    for i in value_:
                        if isinstance(i, MutableMapping):
                            item = find_nested_value(i, key)
                            if item is not None:
                                return item
        return_ = ""
        events = self.browser.get_log("performance") # Lấy toàn bộ events
        for event in events: # Lấy event lần lượt qua các events
            if key in event['message']:
                event = json.loads(event['message'])
                value = find_nested_value(event, key)
                if value != None:
                    return_ = value
        return return_
    def find_window_by_title(self, titles, wait_time= 1):
        for i in range(wait_time):
            time.sleep(1)
            curr = self.browser.current_window_handle
            for handle in self.browser.window_handles:
                self.browser.switch_to.window(handle)
                if handle != curr:
                    for title in titles.split('|'):
                        if title in self.browser.title:
                            return True
            self.browser.switch_to.window(curr)
        return False
    def find_element(self, tag_name, data, delay= 10):
        string_ = data.replace('"', '').split("=")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, tag_name)))
        for i in range(delay): # kiểm tra element trong 10s
            time.sleep(1)
            try:
                for element in self.browser.find_elements(By.TAG_NAME, tag_name):
                    if len(string_) == 1 and string_[0].replace("\n", "").strip(" ") == element.text:
                        return element
                    elif len(string_) == 2 and string_[1] in element.get_attribute(string_[0]):
                            return element
            except: time.sleep(1)
    def find_elements(self, tag_name, data):
        element_return = []
        string_ = data.replace('"', '').split("=")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, tag_name)))
        for i in range(self.delay): # kiểm tra element trong 10s
            time.sleep(1)
            try:
                for element in self.browser.find_elements(By.TAG_NAME, tag_name):
                    if len(string_) == 1 and data.replace("\n", "").strip(" ") == element.text:
                        element_return.append(element)
                    elif len(string_) == 2 and string_[1] in element.get_attribute(string_[0]):
                        element_return.append(element)
                if len(element_return) > 0:
                    return element_return
            except: time.sleep(1)
    def find_image(self, small_image_path, loop=7, click=True, cord=False, screenshot=True, scale_x=0.5, scale_y=0.5, threshold=0.8, delay=1):
        # Đọc và lấy kích thước ảnh nhỏ
        small_image = cv2.imread(small_image_path)
        small_height, small_width, _ = small_image.shape
        print(f'Chrome {self.vi_tri+1}: Tìm kiếm hình ảnh {small_image_path}')
        for _ in range(loop):
            # Chụp ảnh màn hình và chuyển về PC
            if screenshot:
                self.browser.save_screenshot(f'image\\Capture{self.vi_tri}.png')
            large_image = cv2.imread(f'image\\Capture{self.vi_tri}.png')
            # Thực hiện template matching
            result = cv2.matchTemplate(large_image, small_image, cv2.TM_CCOEFF_NORMED)
            # Tìm vị trí tối đa của sự trùng khớp
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            # Nếu trùng khớp đạt đến một ngưỡng nhất định, vẽ hình chữ nhật
            if max_val >= threshold:
                top_left = max_loc
                bottom_right = (top_left[0] + small_width, top_left[1] + small_height)
                # Tính toán tọa độ tâm của hình chữ nhật
                center_x = top_left[0] + scale_x*(bottom_right[0] - top_left[0])
                center_y = top_left[1] + scale_y*(bottom_right[1] - top_left[1])
                if click:
                    self.action.move_by_offset(center_x, center_y).click().perform()
                    self.action.move_by_offset(-center_x, -center_y).perform()
                if cord == True:
                    return {'x1':top_left[0], 'y1':top_left[1], 'x2':bottom_right[0], 'y2':bottom_right[1]}
                return True
            else:
                if delay != 0 and loop != 1:
                    time.sleep(delay)
        return False
    def quit_chrome(self):
        try:
            for handle in self.browser.window_handles:
                self.browser.switch_to.window(handle)
                self.browser.close()
            time.sleep(3)
        except:
            pass
    def one_window(self, delay= 3):
        try:
            time.sleep(delay)
            curr = self.browser.current_window_handle
            for handle in self.browser.window_handles:
                self.browser.switch_to.window(handle)
                if handle != curr:
                    self.browser.close()
            self.browser.switch_to.window(curr)
        except:
            pass