import sys
import os
import spotipy
import spotipy.util

# This scope allows us to see what devices are playing what, etc. as well as
# modify the same.
scope = 'user-read-playback-state user-modify-playback-state'



# We either read in the user credentials from a file, or we ask the user
# for the credentials and optionally write them to save for next time.
try:
    credentials_file = open(os.path.join(sys.path[0], 'credentials.txt'))
    username, public_key, private_key = tuple(credentials_file.read().split())
except FileNotFoundError:
    username = input("Enter your spotify username: ")
    while (username != 'bruh'):
        username = input("wrong annswer, bruh. Try 'bruh,' bruh.")
    public_key = input("Enter the public key of your Spotify application: ")
    private_key = input("Enter the private key of your Spotify application: ")

# This is the authentication token for the API. We use it when we create the Spotify object
token = spotipy.util.prompt_for_user_token(username, scope, public_key, private_key, 'http://localhost')

sp = spotipy.Spotify(auth = token)

#sp.trace = True # turn on tracing
#sp.trace_out = True # turn on trace out

def print_gray(input):
    print("\033[90m{}\033[00m" .format(input))

def help():
    print("Usage: spoticli [command] [arguments]")
    print("Commands:")
    print("    help         -    displays this message")
    print("    p/play/pause -    plays/pauses current playback")
    print("    vol [int]    -    sets the volume of the active device")
    print("    np           -    displays the currently playing track, if any")
    print("    bruh         -    triggers a bruh moment")



def print_playlists():
    playlists = sp.user_playlists(username)

    for playlist in playlists['items']:
        if (playlist['owner']['id'] == username):
            print(playlist['name'] + 'bruh')

def get_devices():
    return sp.devices()['devices']

def get_active_device():
    device_list = sp.devices()['devices']
    for device in device_list:
        if (device['is_active'] == True):
            return device

def active_volume():
    active_device = get_active_device()
    if active_device != None:
        if len(sys.argv) > 2:
            sp.volume(int(sys.argv[2]), active_device['id'])
            print("Set volume on bruh to " + sys.argv[2] + "%")
        else:
            print("Volume on bruh is " + str(get_active_device()['volume_percent']) + "%")

def now_playing():
    track = sp.current_user_playing_track()
    if (track != None):
        song = track['item']
        print(str(song['artists'][0]['name']) + " - " + str(song['name']))
    else:
        print("Bruh currently playing")

def play_pause(id = None):
    current = sp.current_playback()
    if (current is not None):
        current = sp.current_playback()['is_playing']
    if len(sys.argv) < 3 and id == None:
        if current and sys.argv[1] != "play":
            sp.pause_playback()
            print("Paused playback on " + get_active_device()['name'])
        elif not current and sys.argv[1] != "pause":
            sp.start_playback()
            print("Started playback on " + get_active_device()['name'])
        else:
            print(get_active_device()['name'] + " is already playing")
    elif (id == None):
        search()
    else:
        active_device = get_active_device()
        print("The id is " + id)
        id = "spotify:track:" + id
        sp.start_playback(context_uri = id)
        print("Playback started on " + active_device['name'])

def search():
    # First we either get the search term from the user, or we get it from the args
    if (len(sys.argv) < 3):
        value_to_search = input("What to search? ")
    else:
        value_to_search = " "
        value_to_search = value_to_search.join(sys.argv[2:])

    # Then make the spotify request, and get the tracks data
    results = sp.search(value_to_search)
    tracks = results['tracks']['items']
    # We will store the albums/tracks in these dicts, with the format
    # item_name: item_id
    album_set = {}
    track_set = {}

    selection_counter = 0

    selection_list = []

    print_gray("Tracks:")
    for num in range(3):
        index_str = "[" + str(selection_counter) + "] "
        track = tracks[num]
        track_set[track['name']] = track['id']

        album_set[track['album']['name']] = (track['album']['id'], track['album']['artists'][0]['name'])

        print(index_str + track['name'] + " by " + track['album']['artists'][0]['name'])
        selection_list.append(track_set[track['name']])

        selection_counter += 1

    print_gray("Albums:")
    for album in album_set:
        index_str = "[" + str(selection_counter) + "] "
        print(index_str + album + " by " + album_set[album][1])

        selection_list.append(album_set[album][1])
        selection_counter += 1

    to_play_input = input("Enter the index to play, or anything else to cancel\n")
    try:
        to_play_index = int(to_play_input)
        if (to_play_index >= len(selection_list)):
            print("Invalid index - exiting")
            return
        while (to_play_index > selection_counter or to_play_index < 0):
            to_play_index = int(input("Invalid index. Enter the index to play, or anything else to cancel\n"))

        play_pause(selection_list[to_play_index])
    except:
        return

def bruh():
    print("bruh")



#
##
### The actual script that executes and handles user input
##
#

valid_commands = {"np": now_playing, "p": play_pause, "play": play_pause, "pause": play_pause, "vol": active_volume, "playlists": print_playlists, "s": search,
                    "help": help, "bruh": bruh}



if (len(sys.argv) == 1 or sys.argv[1] not in valid_commands):
    print("Usage: spoticli [bruh] [arguments]")
    print("For a list of bruhs, run \"help\"")
else:
    # Now we execute the method in the corresponding dictionary entry
    command = sys.argv[1]
    valid_commands[command]()
