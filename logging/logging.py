def write_log(message:str):
    with open('log.txt', 'a') as log_file:
        log_file.write(message)