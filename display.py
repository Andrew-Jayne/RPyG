import os


class Display:

    @staticmethod
    def clear_display():
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For macOS and Linux
        else:
            os.system('clear')

## Player Messages
    @staticmethod
    def progress_message(player_instance):
        print(f"""
You Progress 10 Miles further.
You have traveled {player_instance.progress * 10} Miles Total.
""")
        
    @staticmethod
    def player_attack_message(player_instance):
        print(f"You Attack with {player_instance.attack_name} and inflict {player_instance.attack_power} damage")


    @staticmethod
    def player_critical_attack_message(player_instance):
        print(f"You Attack with {player_instance.attack_name} and inflict {player_instance.attack_power * 2} damage")
        print(f"{player_instance.name} got a critical hit!!")

## Generic Actor Messages
    @staticmethod
    def defeated_message(actor_instance):
        print(f"{actor_instance.name} has been defeated" , end='\n\n')

    @staticmethod
    def actor_attack_message(actor_instance):
        print(f"{actor_instance.name} attacks with {actor_instance.attack_name} inflicting {actor_instance.attack_power} damage")

    @staticmethod
    def actor_critical_attack_message(actor_instance):
        print(f"{actor_instance.name} attacks with {actor_instance.attack_name} inflicting {actor_instance.attack_power * 2} damage")
        print(f"{actor_instance.name} got a critical hit!!")

    @staticmethod
    def actor_health_message(actor_instance):
        print(f"{actor_instance.name} has {actor_instance.health} Health remaining", end='\n\n')


