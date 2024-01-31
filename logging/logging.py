from interaction.interaction_utilities import sanitize

def write_log(message:str) -> None:
    pass
# Disabled for now, due to dissatifaction with implementation
    #with open('log.txt', 'a') as log_file:
    #   log_file.write(f"{sanitize(message,max_length=256)}\n")

def clear_log() -> None:
    pass
    # Disabled for now, due to dissatifaction with implementation
    #with open('log.txt', 'w') as log_file:
        #log_file.write("")