
######  Since I do not have any VK account of my own for solving this hometask I am to use the data from our diploma, i.e. the very TOKEN provided and ids of E.Shmargunov's friends for comparison (the following IDs you could check by your own: 47255626, 44791055, 52612027, 33728375, 15431923, 3076020, 2562369, 143611, 71491, 58439).

######  However, we are to cite here the very procedure of requesting token from this social network if you'd like to acquire your own for further usage.

import requests
from urllib.parse import urlencode
import time
import json
from pprint import pprint
from termcolor import colored

###### There is a procedure for acquiring the very token from VK social network placed some below.

# APP_ID =               
###### Herewith you are  to place your own APP ID to use it for acquiring the very token

# OAUTH_URL = 'https://oauth.vk.com/authorize'

# OAUTH_PARAMS = {
#   'client_id': APP_ID,
#   'display': 'page',
#   'response_type': 'token',
#   'scope': "friends, status, wall, groups, stats, offline",
#   'v': '5.103'
#   }

# print("?".join((OAUTH_URL, urlencode(OAUTH_PARAMS))))


# TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

class VK_user:
    
    def __init__(self, vk_user_id):

        self.vk_user_id = vk_user_id
        self.params = {
            'access_token': TOKEN,
            'v': 5.103,
            'user_ids': self.vk_user_id,
            'extended': 1,
            'count': 1000
            }
   
    def acquiring_vkuser_name(self):

        response = requests.get(
          'https://api.vk.com/method/users.get',
          self.params
        )
        
        response_json = response.json()

        if response_json.get('error') and (response_json['error']['error_msg'] \
        == 'Too many requests per second'):
            print(colored(f"\nIt is necessary to wait for some seconds because of the error \
            {response_json['error']['error_msg']}.", 'green'))
            time.sleep(2)
            response_json = response.json()

        self.vk_user_id = response_json['response'][0]['id'] 
        vkuser_full_name = " ".join((response_json['response'][0]['first_name'],response_json['response'][0]['last_name']))
        
        return vkuser_full_name


    def determining_vkfriends(self):
        
        self.params["user_id"] = self.vk_user_id
        response = requests.get(
          'https://api.vk.com/method/friends.get',
          self.params
        )
        response_json = response.json()

        if response_json.get('error') and (response_json['error']['error_msg'] \
        == 'Too many requests per second'):
            print(colored(f"\nIt is necessary to wait for some seconds because of the error \
            {response_json['error']['error_msg']}.", 'green'))
            time.sleep(2)
            response_json = response.json()
        
        return response_json['response']['items']

    def __and__(self, targeted_vk_user):
        
        principal_vkuser = self.determining_vkfriends()
        referral_vkuser = targeted_vk_user.determining_vkfriends()
        principal_vkuser_friends = set(principal_vkuser)
        referral_vkuser_friends = set(referral_vkuser)
        joint_friends = principal_vkuser_friends & referral_vkuser_friends
        joint_friends_dict = {}
        joint_friends_list = []
        
        for friend in joint_friends:

            joint_friends_list.append(VK_user(friend))
            name = VK_user(friend).acquiring_vkuser_name()
            joint_friends_dict[name] = {'id': friend, 'url': 'https://vk.com/id' + str(friend)}
        
        print(colored(f'\nThe VK users {principal_vk_user.acquiring_vkuser_name()} and {referral_vk_user.acquiring_vkuser_name()} have {len(joint_friends_list)} common friend(-s).\n', 'red'))
        print(colored('\nPersonal reference links of their common friends are provided immediately below.', 'green'))
        
        for person in joint_friends_list:

            print(colored(f"\nThe VK user {person.acquiring_vkuser_name()} has the following personal link in the VK social network -- {joint_friends_dict[person.acquiring_vkuser_name()]['url']}", 'green'))
            

if __name__ == "__main__":

    TOKEN = input("\nEnter the access token you are to use to comply with the requirements of the VK API: ")

    principal_vk_user = VK_user(input('\nEnter a personal id number a of VK user you are interested in for your analysis (e.g. for our tutor E.Shmargunov - 171691064): '))
    referral_vk_user = VK_user(input('\nEnter a personal id number a of VK user you are interested in for your analysis (e.g. for a friend of E.Shmargunov - 71491):  ')) 

    print(colored(f"\nThe VK user {principal_vk_user.acquiring_vkuser_name()}  has {len(principal_vk_user.determining_vkfriends())} friends in this social network.", 'blue'))
    print(colored(f"\nThe VK user {referral_vk_user.acquiring_vkuser_name()}  has {len(referral_vk_user.determining_vkfriends())} friends in this social network.", 'blue'))

    principal_vk_user & referral_vk_user
