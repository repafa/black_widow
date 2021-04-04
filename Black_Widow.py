#!/usr/bin/env python

import requests
import time
import re
import urlparse
import pyfiglet
from termcolor import colored, cprint


try:
    print_red = lambda x: cprint(x, 'red')
    print_grey = lambda x: cprint(x, 'grey')

    ascii_banner = pyfiglet.figlet_format("Black Widow")
    print_red(ascii_banner)

    with open("spider.txt", "r") as spider_file:
        for line in spider_file:
            print_red(line.rstrip())

    print_red("Choose Mode:"), print_grey("a1.Subdomains(http://)                            a2.Subdomains(https://)\nb1.Directories(http://)                           b2.Directories(https://)\nc1.Recursive(Specify http:// or https://)         c2.Post(URL)\n")
    option = raw_input("Option > ")
    target_url = raw_input("Target > ")
    target_links = []
except KeyboardInterrupt:
    print_red("\n[+] Crawling back down...")
    exit()

if option == "a1":
    def request(url):
        try:
            return requests.get("http://" + url)
        except requests.exceptions.ConnectionError:
            pass
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            exit()


    with open("subdomains-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            try:
                time.sleep(5)
                word = line.strip()
                test_url = word + "." + target_url
                response = request(test_url)
                if "200" in str(response):
                    print_grey("[+] Discovered Subdomain --> " + test_url)
            except KeyboardInterrupt:
                print_red("\n[+] Crawling back down...")
                exit()

    print_red("Crawling Complete.")


if option == "a2":
    def request(url):
        try:
            return requests.get("https://" + url)
        except requests.exceptions.ConnectionError:
            pass
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            exit()


    with open("subdomains-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            try:
                time.sleep(5)
                word = line.strip()
                test_url = word + "." + target_url
                response = request(test_url)
                if "200" in str(response):
                    print_grey("[+] Discovered Subdomain --> " + test_url)
            except KeyboardInterrupt:
                print_red("\n[+] Crawling back down...")
                exit()

    print_red("Crawling Complete.")


if option == "b1":
    def request(url):
        try:
            return requests.get("http://" + url)
        except requests.exceptions.ConnectionError:
            pass
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            exit()


    with open("files-and-dirs-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = target_url + "/" + word
            response = request(test_url)
            if "200" in str(response):
                print_grey("[+] Discovered Directory --> " + test_url)

    print_red("Crawling Complete.")


if option == "b2":
    def request(url):
        try:
            return requests.get("https://" + url)
        except requests.exceptions.ConnectionError:
            pass
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            exit()


    with open("files-and-dirs-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = target_url + "/" + word
            response = request(test_url)
            if "200" in str(response):
                print_grey("[+] Discovered Directory --> " + test_url)

    print_red("Crawling Complete.")


if option == "c1":
    def extract_links_from(url):
        response = requests.get(url)
        return re.findall('(?:href=")(.*?)"', response.content)


    def crawl(url):
        href_links = extract_links_from(url)
        for link in href_links:
            link = urlparse.urljoin(url, link)

            if "#" in link:
                link = link.split("#")[0]

            if target_url in link and link not in target_links:
                target_links.append(link)
                print_grey(link)
                crawl(link)


    crawl(target_url)
    print_red("Web Complete.")


if option == "c2":
    data_dict = {"username": "admin", "password": "", "Login": "submit"}


    with open("passwords.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            data_dict["password"] = word
            response = requests.post(target_url, data=data_dict)
            if "Login failed" not in response.content:
                print_red("[+] Password obtained! --> " + word)
                exit()

    print_red("[+] Reached end of line.")
