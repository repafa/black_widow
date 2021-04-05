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

    print_red("Choose Mode:"), print_grey("1, 2, 3, 4, 5 or 6\n")
    print_red("Type help for more info\n")
    option = raw_input("-------> ")

    if option == "help":
        try:
            print_red(
                "\nType 1 to crawl a subdomain using http.\nType 2 to crawl a subdomain using https.\nType 3 to crawl a directory using http.\nType 4 to crawl a subdomain using https.\nType 5 to recursively crawl a website.\nType 6 to send post requests to a login on a web page.\n")
            option = raw_input("-------> ")
            target_url = raw_input("Target > ")
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            exit()

    if option == "1" or "2" or "3" or "4" or "5" or "6":
        target_url = raw_input("Target > ")
    else:
        pass
    target_links = []
except KeyboardInterrupt:
    print_red("\n[+] Crawling back down...")
    exit()


if option == "1":
    def request(url):
        try:
            return requests.get("http://" + url)
        except requests.exceptions.ConnectionError:
            pass
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            with open("1.txt", "r") as spider_file:
                for line in spider_file:
                    print_red(line.rstrip())
            exit()


    with open("subdomains-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            try:
                time.sleep(30)
                word = line.strip()
                test_url = word + "." + target_url
                response = request(test_url)
                if "200" in str(response):
                    print_grey("[+] Discovered Subdomain --> " + test_url)
            except KeyboardInterrupt:
                print_red("\n[+] Crawling back down...")
                with open("1.txt", "r") as spider_file:
                    for line in spider_file:
                        print_red(line.rstrip())
                exit()

    print_red("Crawling Complete.")


if option == "2":
    def request(url):
        try:
            return requests.get("https://" + url)
        except requests.exceptions.ConnectionError:
            pass
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            with open("2.txt", "r") as spider_file:
                for line in spider_file:
                    print_red(line.rstrip())
            exit()


    with open("subdomains-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            try:
                time.sleep(30)
                word = line.strip()
                test_url = word + "." + target_url
                response = request(test_url)
                if "200" in str(response):
                    print_grey("[+] Discovered Subdomain --> " + test_url)
            except KeyboardInterrupt:
                print_red("\n[+] Crawling back down...")
                with open("2.txt", "r") as spider_file:
                    for line in spider_file:
                        print_red(line.rstrip())
                exit()

    print_red("Crawling Complete.")


if option == "3":
    def request(url):
        try:
            return requests.get("http://" + url)
        except requests.exceptions.ConnectionError:
            pass
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            with open("3.txt", "r") as spider_file:
                for line in spider_file:
                    print_red(line.rstrip())
            exit()


    with open("files-and-dirs-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = target_url + "/" + word
            response = request(test_url)
            if "200" in str(response):
                print_grey("[+] Discovered Directory --> " + test_url)
    with open("3.txt", "r") as spider_file:
        for line in spider_file:
            print_red(line.rstrip())
    print_red("Crawling Complete.")


if option == "4":
    def request(url):
        try:
            return requests.get("https://" + url)
        except requests.exceptions.ConnectionError:
            pass
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            with open("4.txt", "r") as spider_file:
                for line in spider_file:
                    print_red(line.rstrip())
            exit()


    with open("files-and-dirs-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = target_url + "/" + word
            response = request(test_url)
            if "200" in str(response):
                print_grey("[+] Discovered Directory --> " + test_url)

    with open("4.txt", "r") as spider_file:
        for line in spider_file:
            print_red(line.rstrip())
    print_red("Crawling Complete.")


if option == "5":
    def extract_links_from(url):
        try:
            response = requests.get(url)
            return re.findall('(?:href=")(.*?)"', response.content)
        except KeyboardInterrupt:
            print_red("\n[+] Crawling back down...")
            with open("5.txt", "r") as spider_file:
                for line in spider_file:
                    print_red(line.rstrip())
            exit()

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
    with open("5.txt", "r") as spider_file:
        for line in spider_file:
            print_red(line.rstrip())
    print_red("Web Complete.")


if option == "6":
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
