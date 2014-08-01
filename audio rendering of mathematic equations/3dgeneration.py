import sfml as sf


def main(song):
    # load an ogg music file
    music = sf.Music.from_file(song)

    # display music informations
    print("subscript.wav:")
    print("{0} seconds".format(music.duration))
    print("{0} samples / sec".format(music.sample_rate))
    print("{0} channels".format(music.channel_count))

    music.relative_to_listener = False
    music.min_distance = 200
	
    music.attenuation = 1
    position = sf.Vector3(-250, -250, 0)
    sf.Listener.set_position(position)
    x, y, _ = position
    
    running = True
    
    music.play()
    position.y-=5

    sf.Listener.set_position(position)

    x, y, z = position
    
    music.play()
    
    music.play()
    
    music.play()
    
    while running:
    
        position.y-=5
    
        sf.Listener.set_position(position)

        x, y, z = position

        position.y+=5
    
        sf.Listener.set_position(position)

        x, y, z = position

        choice=input("Press x to exit")

        if choice == 'x':
            running= False
        else:    
            main("F:\media\superscript.wav")

        
        
        
    

if __name__ == "__main__":
     main("F:\media\superscript.wav")
