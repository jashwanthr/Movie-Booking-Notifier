#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 12:56:33 2019

@author: Jashwanth
"""
import sys
import requests
import time
from bs4 import BeautifulSoup
from way2sms import WAY2SMS


class MovieCrawler():
    def __init__(self, movieName, mobileNum):
        """Constructor : Initializes necessary variables."""
        self.bookmyshowUrl = 'https://in.bookmyshow.com/bangalore/movies/'
        self.paytmUrl = 'https://paytm.com/movies/bangalore'
        self.way2sms = WAY2SMS()
        self.movieName = movieName
        self.mobileNum = mobileNum

    def ParsebookMyShow(self):
        """Checks whether given movie is available in Bookmyshow website."""
        data = requests.get(self.bookmyshowUrl)
        soup = BeautifulSoup(data.text, 'html.parser')
        mydivs = soup.findAll("div", {"class": "movie-card-container"})
        for div in mydivs:
            if (self.movieName in div.find('h4').text.upper() and 'ENGLISH' in div['data-language-filter'].upper()):
                print("FOUND IN BMS")
                return "BMS"
        return ""

    def ParsePaytm(self):
        """Checks whether given movie is available in Paytm website."""
        data = requests.get(self.paytmUrl)
        soup = BeautifulSoup(data.text, 'html.parser')
        mydivs = soup.findAll("div", {"id": "popular-movies"})[0].find_all('li')
        for div in mydivs:
            if (self.movieName in div.find_all('div')[-2].text.upper()):
                print("FOUND IN PAYTM")
                return "PAYTM"
        return ""

    def CheckMovieBookings(self):
        """Checks Bookmyshow/Paytm websites for the availability of given movie."""
        return ' '.join(filter(None, [self.ParsebookMyShow(), self.ParsePaytm()]))

    def SendSMS(self, message, num):
        """Sends SMS to given mobile number using 'way2sms' instance if requested movie is live. In case of errors, tries for a maximum of 3 times."""
        for try in range(3):
            resp = self.way2sms.sendPostRequest(message, num)
            if (resp != '200'):
                print("Error sending SMS.. Try - " + str(try))
            else:
                print("SMS Sent")
                break

    def Work(self):
        """Checks for the given movie bookings every five minutes and if found sends SMS to given mobile number with the list of websites where the movie booking is live."""
        count = 0
        print("Starting work for " + self.movieName + ".....")
        while (True):
            count += 1
            resp = self.CheckMovieBookings()
            if (resp != ''):
                self.SendSMS(self.movieName + " MOVIE LIVE NOW IN " + resp + "!!!", self.mobileNum)
                break
            else:
                print("Could not locate in " + str(count) + " tries")
                time.sleep(60 * 5)


if __name__ == '__main__':
    movieCrawler = MovieCrawler(sys.argv[1], sys.argv[2])
    movieCrawler.Work()