from interaction.interaction_utilities import sanitize

def write_log(message:str):
    with open('log.txt', 'a') as log_file:
        log_file.write(sanitize(message))