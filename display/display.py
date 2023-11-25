from display.display_utilities import clear_display
from display.messages_actor import defeated_message, encounter_message, actor_attack_message, actor_health_message, actor_critical_attack_message
from display.messages_encouter import flee_failure_message, flee_success_message
from display.messages_battle import battle_hud_message, battle_start_message
from display.messages_player import player_progress_message, player_attack_message, player_critical_attack_message

class Display:

    # Utilities
    @staticmethod
    def clear_display():
        clear_display()

    # Actor Messages
    @staticmethod
    def defeated_message(actor_name):
        defeated_message(actor_name)
    
    @staticmethod
    def encounter_message(actor_name):
        encounter_message(actor_name)
    
    @staticmethod
    def actor_attack_message(actor_instance):
        actor_attack_message(actor_instance)
    
    @staticmethod
    def actor_health_message(actor_instance):
        actor_health_message(actor_instance)

    @staticmethod
    def actor_critical_attack_message(actor_instance):
        actor_critical_attack_message(actor_instance)

    # Battle Messages
    @staticmethod
    def battle_hud_message(player_instance, enemy_instance):
        battle_hud_message(player_instance, enemy_instance)
    
    @staticmethod
    def battle_start_message():
        battle_start_message()

    # Encouter Messages
    @staticmethod
    def flee_failure_message(enemy_name):
        flee_failure_message(enemy_name)
    
    @staticmethod
    def flee_success_message(enemy_name):
        flee_success_message(enemy_name)

    # Player Messages
    @staticmethod
    def player_progress_message(player_instance):
        player_progress_message(player_instance)

    @staticmethod
    def player_attack_message(player_instance):
        player_attack_message(player_instance)

    @staticmethod
    def player_critical_attack_message(player_instance):
        player_critical_attack_message(player_instance)
