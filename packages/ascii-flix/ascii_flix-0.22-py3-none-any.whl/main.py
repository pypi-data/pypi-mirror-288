from modules import HomeScreen,VideoPlayer

def main_function():
    video_player=VideoPlayer()
    homescr=HomeScreen()
    homescr.create_logo()
    homescr.display_home_screen(video_player=video_player)

if __name__=="__main__":
    main_function()