class Display:

    @staticmethod
    def progress(player_instance):
        print(f"""
You Progress 10 Miles further.
You have traveled {player_instance.progress * 10} Miles Total.
""")
        pass

    @staticmethod
    def defeated(actor_instance):
        print(f"{actor_instance.name} has been defeated" , end='\n\n')