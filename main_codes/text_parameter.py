def keyword(test):
    if "yourself" in test:
        name_file = r'C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\LAGERTHA_introduction.mp3'
    elif "ability" in test:
        name_file = r'C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\LAGERTHA_ability.mp3'
    elif "animation" in test:
        name_file = r'C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\LED_Animation.mp3'
    elif "brightness" in test:
        name_file = r'C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\LED_Brightness.mp3'
    elif "send" in test or "whatsapp" in test or "phone" in test:
        name_file = r'C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\Weather_whatsapp.mp3'
    elif "goodbye" in test:
        name_file = r'C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\Closing_off.mp3'
    elif "good bye" in test:
        name_file = r'C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\Closing_off.mp3'
    elif "whatsapp" in test:
        name_file = r'C:\Users\user\Documents\pythonFiles\LAGERTHA_Project\main_program\Weather_whatsapp.mp3'
    elif "LED" in test:
        name_file = r''
    else:
        return False, "nothing"
    return True, name_file
