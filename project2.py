import time as t


class Time:
    """Class of time(duration of song)"""
    def __init__(self, time):
        """Initialization method"""
        self.time = time
        self.seconds = Time.convert_to_seconds(self.time)

    def __str__(self):
        return self.time

    def __repr__(self):
        return self.time

    @staticmethod
    def convert_to_seconds(value):
        value = value.split(':')
        if len(value) == 2:
            return int(value[0]) * 60 + int(value[1])
        else:
            return int(value[0]) * 60 * 60 + int(value[1]) * 60 + int(value[2])

    @staticmethod
    def convert_to_time(seconds):
        time = []
        if seconds // 3600 > 0:
            time.append(str(seconds // 3600))
            seconds -= (seconds // 3600) * 3600
        if seconds // 60 > 0:
            time.append(str(seconds // 60))
            seconds -= (seconds // 60) * 60
        time.append(str(seconds))
        for value in time:
            if len(value) == 1:
                num = time.index(value)
                time[num] = '0' + value
        if len(time) == 1:
            time = ['00'] + time
        return ':'.join(time)

    def __lt__(self, other):
        """Method for comparison"""
        return self.seconds < other.seconds

    def __le__(self, other):
        """Method for comparison"""
        return self.seconds <= other.seconds

    def __eq__(self, other):
        """Method for comparison"""
        return self.seconds == other.seconds

    def __ne__(self, other):
        """Method for comparison"""
        return self.seconds != other.seconds

    def __gt__(self, other):
        """Method for comparison"""
        return self.seconds > other.seconds

    def __ge__(self, other):
        """Method for comparison"""
        return self.seconds >= other.seconds

    def __add__(self, other):
        """"Method for calculating"""
        return Time(Time.convert_to_time(self.seconds + other.seconds))

    def __sub__(self, other):
        """"Method for calculating"""
        return Time(Time.convert_to_time(self.seconds - other.seconds))


class Load:
    """Class for loading data"""
    songs = []
    albums = []

    @classmethod
    def load_data(cls, file_name):
        """Method for loading data from file"""
        data = {}
        with open(file_name, 'r') as file:
            count = len(file.readlines())
        with open(file_name, 'r') as file:
            for _ in range(count):
                line = file.readline()
                line = line.replace('\n', '')
                info = line.split(';')
                song = Song(info[0], info[1], info[2], info[3], info[4],
                            info[5])
                Load.songs.append(song)
                if song.album not in data:
                    data[song.album] = [song]
                else:
                    data[song.album] += [song]
        for album_name in data:
            song = data[album_name][0]
            album = Album(album_name, song.author, song.release_year,
                          song.genre, data[album_name])
            number = 0
            for song in data[album_name]:
                number += 1
                song.number = number
            Load.albums.append(album)


class Album:
    """Class of albums of music"""
    def __init__(self, name, author, release_year, genre, songs):
        """Initialization method"""
        self.name = name
        self.author = author
        self.release_year = release_year
        self.genre = genre
        self.songs = songs
        self.total_duration = Album.calc_duration(self.songs)

    def __str__(self):
        return 'Name: {}\nAuthor: {}\nRelease year: {}\nTotal duration: ' \
               '{}\nGenre: {}\nSongs: {}\n'.format(self.name, self.author,
                                                   self.release_year,
                                                   self.total_duration,
                                                   self.genre,
                                                   str(self.songs))

    def __repr__(self):
        return self.name

    @staticmethod
    def calc_duration(lst_songs):
        duration = Time('00:00')
        for song in lst_songs:
            duration += song.duration
        return duration


class Playlist:
    """Class of user's playlist"""
    start_playing = None

    @staticmethod
    def print_menu(num):
        if num == 1:
            print('+' + '-' * 100 + '+')
            print('|{:<100}|'.format('MAIN MENU'))
            print('+' + '-' * 100 + '+')
            print('|{:<100}|'.format('1. Show my playlist.'))
            print('|{:<100}|'.format('2. Listen to album.'))
            print('|{:<100}|'.format('3. Shut down the program.'))
            print('+' + '-' * 100 + '+')
        elif num == 0:
            print('+' + '-' * 100 + '+')
            print('|{:<100}|'.format('MENU'))
            print('+' + '-' * 100 + '+')
            print('|{:<100}|'.format('1. Continue listening.'))
            print('|{:<100}|'.format('2. Go to the main menu.'))
            print('|{:<100}|'.format('3. Shut down the program.'))
            print('+' + '-' * 100 + '+')
        else:
            print('+' + '-' * 100 + '+')
            print('|{:<100}|'.format('MENU'))
            print('+' + '-' * 100 + '+')
            print('|{:<100}|'.format('1. Show my playlist.'))
            print('|{:<100}|'.format('2. Show song, which is played.'))
            print('|{:<100}|'.format('3. Pause the song.'))
            print('|{:<100}|'.format('4. Stop listening.'))
            print('|{:<100}|'.format('5. Shut down the program.'))
            print('+' + '-' * 100 + '+')
        num = input('Input number: ')
        return num

    @staticmethod
    def show_playing(info):
        if info is None:
            print('Song is not played.')
            return
        current_time = Time(t.strftime("%H:%M:%S", t.gmtime()))
        start_time = Time(info[0])
        if len(info) == 3:
            start_time = start_time + (current_time - info[2])
            Playlist.start_playing[0] = Time(Playlist.start_playing[0]) + \
                                        (current_time - info[2])
            Playlist.start_playing = [current_time, info[1]]
        period = current_time - start_time
        if isinstance(info[1], Album):
            for song in info[1].songs:
                if period >= info[1].total_duration:
                    print('Album {} was played during {} and already is over.'.\
                          format(info[1].name,str(info[1].total_duration)))
                    break
                elif period < song.duration:
                    print('IS PLAYID NOW:')
                    print(song)
                    print('TIME LEFT: {}'.format(str(song.duration - period)))
                    break
                elif period < info[1].total_duration:
                    period -= song.duration

    @staticmethod
    def show_playlist():
        for album in Load.albums:
            print(album)

    @staticmethod
    def menu():
        _exitt = False
        _exit = False
        while True:
            if _exit:
                break
            action = Playlist.print_menu(1)
            if action == '1':
                Playlist.show_playlist()
            elif action == '2':
                album = input('Input name of album: ')
                for albums in Load.albums:
                    if albums.name.lower() == album.lower():
                        album = albums
                        break
                if isinstance(album, Album):
                    print('START LISTENING {}'.format(album.name))
                    Playlist.start_playing = [t.strftime("%H:%M:%S",
                                                         t.gmtime()), album]
                    while True:
                        if _exitt:
                            break
                        act = Playlist.print_menu(2)
                        if act == '1':
                            Playlist.show_playlist()
                        elif act == '2':
                            Playlist.show_playing(Playlist.start_playing)
                        elif act == '3':
                            start_pause = Time(t.strftime("%H:%M:%S",
                                                          t.gmtime()))
                            Playlist.start_playing.append(start_pause)
                            while True:
                                act = Playlist.print_menu(0)
                                if act == '1':
                                    Playlist.show_playing(Playlist.start_playing)
                                    break
                                elif act == '2':
                                    _exitt = True
                                    break
                                elif act == '3':
                                    _exit = True
                                    _exitt = True
                                    break
                                else:
                                    print('Input data is incorrect, try again.')
                        elif act == '4':
                            Playlist.start_playing = None
                            Playlist.show_playing(Playlist.start_playing)
                            break
                        elif act == '5':
                            _exit = True
                            break
                        else:
                            print('Input data is incorrect, try again.')

                else:
                    print('Input data is incorrect, try again.')
            elif action == '3':
                break
            else:
                print('Input data is incorrect, try again.')


class Song:
    """Class of songs"""
    def __init__(self, name, duration, author, album, release_year,
                 genre):
        """Initialization method"""
        self.number = 0
        self.name = name
        self.author = author
        self.release_year = release_year
        self.genre = genre
        self.album = album
        self.duration = Time(duration)

    def __str__(self):
        return 'Name: {}\nAuthor: {}\nDuration: {}\nAlbum: ' \
               '{}\nRelease year: {}\nGenre: {}\n'.format(self.name,
                                                          self.author,
                                                          str(self.duration),
                                                          self.album,
                                                          self.release_year,
                                                          self.genre)

    def __repr__(self):
        return str(self.number) + '. ' + self.name


