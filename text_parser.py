import spacy

# Загрузка модели spaCy
nlp = spacy.load("ru_core_news_sm")

def parse_input_text_to_data(text):

    data = {
        "radiant_team_name": None,
        "dire_team_name": None,
        "radiant_player_1_hero": None,
        "radiant_player_1_name": None,
        "radiant_player_2_hero": None,
        "radiant_player_2_name": None,
        "radiant_player_3_hero": None,
        "radiant_player_3_name": None,
        "radiant_player_4_hero": None,
        "radiant_player_4_name": None,
        "radiant_player_5_hero": None,
        "radiant_player_5_name": None,
        "dire_player_1_hero": None,
        "dire_player_1_name": None,
        "dire_player_2_hero": None,
        "dire_player_2_name": None,
        "dire_player_3_hero": None,
        "dire_player_3_name": None,
        "dire_player_4_hero": None,
        "dire_player_4_name": None,
        "dire_player_5_hero": None,
        "dire_player_5_name": None
    }

    # Обрабатываем текст через spaCy
    doc = nlp(text)

    radiant_counter = 1
    dire_counter = 1
    current_team = None

    for sent in doc.sents:
        if "Команда Radiant" in sent.text:
            # Извлекаем название команды Radiant
            data["radiant_team_name"] = sent.text.split(":")[1].strip().rstrip('.')
            current_team = "Radiant"

        elif "Команда Dire" in sent.text:
            # Извлекаем название команды Dire
            data["dire_team_name"] = sent.text.split(":")[1].strip().rstrip('.')
            current_team = "Dire"

        if "Игроки:" in sent.text:
            players_and_heroes = sent.text.split("Игроки:")[1].strip().rstrip('.').split(", ")
            for entry in players_and_heroes:
                if " на " in entry:
                    player, hero = entry.split(" на ")
                    if current_team == "Radiant":
                        data[f"radiant_player_{radiant_counter}_hero"] = hero.strip()
                        data[f"radiant_player_{radiant_counter}_name"] = player.strip()
                        radiant_counter += 1
                    elif current_team == "Dire":
                        data[f"dire_player_{dire_counter}_hero"] = hero.strip()
                        data[f"dire_player_{dire_counter}_name"] = player.strip()
                        dire_counter += 1

    return data
