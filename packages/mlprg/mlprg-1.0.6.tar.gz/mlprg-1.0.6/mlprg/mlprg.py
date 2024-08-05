import pkg_resources

def prg(program_number):
    file_path = pkg_resources.resource_filename(__name__, 'prgs.txt')
    
    with open(file_path, 'r') as file:
        programs = file.read().split('# Program ')
    
    programs = [program.strip() for program in programs if program.strip()]
    
    for program in programs:
        if program.startswith(f"{program_number}\n") or program.startswith(f"{program_number} "):
            print(program)
    return None

def prgl(program_number):
    file_path = pkg_resources.resource_filename(__name__, 'prgsl.txt')
    
    with open(file_path, 'r') as file:
        programs = file.read().split('# Program ')
    
    programs = [program.strip() for program in programs if program.strip()]
    
    for program in programs:
        if program.startswith(f"{program_number}\n") or program.startswith(f"{program_number} "):
            print(program)
    return None

