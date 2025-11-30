import pymysql

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "movie_system",
    "charset": "utf8mb4"
}

movies = [
    # (title, release_year, language, duration, director, description, avg_score, rating_count)
    ("Inside Out 2", 2024, "English", 95, "Kelsey Mann", "Pixar emotional‑adventure sequel exploring internal feelings.", 8.5, 150000),
    ("Deadpool & Wolverine", 2024, "English", 119, "Shawn Levy", "Marvel universe crossover featuring anti‑hero and mutant legend.", 8.2, 200000),
    ("Moana 2", 2024, "English", 107, "Dave Derrick Jr.", "Disney animated sequel continuing Moana's ocean journey.", 8.0, 120000),
    ("Despicable Me 4", 2024, "English", 103, "Pierre Coffin & Chris Renaud", "Gru and Minions return in a brand‑new comedic heist adventure.", 7.9, 110000),
    ("Wicked", 2024, "English", 134, "Jon M. Chu", "Musical fantasy based on the Broadway show about witches and destiny.", 7.8, 90000),
    ("Dune: Part Two", 2024, "English", 155, "Denis Villeneuve", "Epic sci‑fi saga continues on Arrakis with political intrigue and war.", 8.6, 180000),
    ("Godzilla x Kong: The New Empire", 2024, "English", 140, "Adam Wingard", "Monster‑versus‑monster spectacle in a world‑shaking showdown.", 7.5, 85000),
    ("Kung Fu Panda 4", 2024, "English", 95, "Cal Brunker", "Po returns for a new martial‑arts adventure with heart and humor.", 7.4, 75000),
    ("Sonic the Hedgehog 3", 2024, "English", 99, "Jeff Fowler", "Faster‑than‑ever hedgehog back in action in this live‑action/CGI sequel.", 7.3, 80000),
    ("The Super Mario Bros. Movie 2", 2024, "English", 100, "Aaron Horvath & Michael Jelenic", "Animated adventure based on the iconic Nintendo franchise.", 7.2, 95000),
    ("Mufasa: The Lion King", 2024, "English", 118, "Barry Jenkins", "Live‑action / CGI musical drama continuing the Lion King legacy.", 8.1, 130000),
    ("Venom: The Last Dance", 2024, "English", 110, "Kelly Marcel", "Venom's latest outing mixing horror, action and anti‑hero drama.", 7.0, 70000),
    ("Twisters", 2024, "English", 130, "Lee Isaac Chung", "Disaster thriller about massive tornadoes threatening the US heartland.", 6.9, 65000),
    ("Kingdom of the Planet of the Apes", 2024, "English", 145, "Wes Ball", "Sci‑fi epic exploring legacy, survival and uprising in a new ape world.", 7.6, 90000),
    ("Bad Boys: Ride or Die", 2024, "English", 125, "Adil & Bilall", "High‑octane action comedy with two cops on a wild mission.", 6.8, 60000),
    ("Alien: Romulus", 2024, "English", 118, "Fede Álvarez", "Sci‑fi horror continuing the Alien franchise with new crew and threats.", 7.1, 72000),
    ("Twilight of the Gods", 2024, "English", 142, "Denis Villeneuve", "Visionary sci‑fi/fantasy film exploring cosmic destiny and humanity's future.", 8.4, 85000),
    ("The Garfield Movie", 2024, "English", 105, "Mark Dindal", "Animated comedy bringing the lazy cat Garfield back to the big screen.", 6.5, 50000),
    ("The Wild Robot", 2024, "English", 120, "Chris Sanders", "Animated sci‑fi adventure about a robot surviving on an unknown planet.", 7.7, 78000),
    ("A Quiet Place: Day One", 2024, "English", 110, "Michael Sarnoski", "Horror‑thriller prequel exploring first day of alien invasion.", 7.3, 68000),
    ("It Ends With Us", 2024, "English", 125, "Justin Baldoni", "Romantic drama adapted from bestseller novel.", 7.5, 72000),
    ("Snow White: Legacy", 2024, "English", 130, "Marc Webb", "Dark fantasy re‑imagining the classic fairy tale Snow White.", 6.9, 62000),
    ("Spider‑Man: Beyond the Spider‑Verse", 2024, "English", 115, "Joaquim Dos Santos", "Animated multiverse Spider‑Man adventure crossing realities.", 8.0, 140000),
    ("Gladiator II", 2024, "English", 160, "Ridley Scott", "Epic historical drama continuing the saga of Roman gladiators.", 8.2, 125000),
    ("Transformers: One", 2024, "English", 140, "Steven Caple Jr.", "Action‑packed reboot exploring the origin of Transformers war.", 7.0, 80000),
    ("Mad Max: Wasteland", 2024, "English", 150, "George Miller", "Post‑apocalyptic action film set in the Mad Max universe.", 7.4, 90000),
    ("Beetlejuice Beetlejuice", 2024, "English", 102, "Tim Burton", "Horror‑comedy sequel bringing back the iconic ghost with new chaos.", 6.8, 60000),
    ("Jurassic World: Extinction", 2024, "English", 130, "Colin Trevorrow", "Dinosaurs run wild again in this action‑adventure reboot.", 7.2, 95000),
    ("Avatar: The Way of Water 2", 2024, "English", 165, "James Cameron", "Epic sci‑fi fantasy continuing the saga on Pandora.", 8.3, 150000),
    ("The Flash: Time Paradox", 2024, "English", 125, "Andy Muschietti", "Superhero adventure with time travel and multiverse stakes.", 7.1, 85000),
    ("Deadpool 3", 2025, "English", 120, "Shawn Levy", "Marvel action comedy — merc with a mouth returns for new chaotic adventure.", 8.4, 160000),
    ("Guardians of the Galaxy Vol. 4", 2025, "English", 145, "James Gunn", "Galactic action‑comedy continuing the adventures of the Guardians.", 8.0, 120000),
    ("Star Wars: Legacy", 2025, "English", 150, "Patty Jenkins", "Space‑opera epic continuing the Star Wars saga.", 8.2, 140000),
    ("Batman: Shadow of Gotham", 2025, "English", 135, "Matt Reeves", "Dark superhero thriller in Gotham city.", 7.9, 110000),
    ("Thor: Ragnarok Reborn", 2025, "English", 130, "Taika Waititi", "Superhero fantasy adventure with cosmic stakes.", 7.8, 100000),
    ("Black Panther: Rising", 2025, "English", 140, "Ryan Coogler", "Superhero epic exploring Wakanda's new challenges.", 8.1, 125000),
    ("Mission Impossible: Dead Reckoning Part 3", 2025, "English", 140, "Christopher McQuarrie", "Spy‑thriller series continuation with global stakes.", 7.7, 90000),
    ("John Wick: Chapter 4", 2023, "English", 169, "Chad Stahelski", "Neo‑noir action thriller following the legendary hitman.", 8.4, 170000),
    ("Oppenheimer", 2023, "English", 180, "Christopher Nolan", "Historical biopic about the birth of the atomic bomb.", 8.9, 210000),
    ("Barbie", 2023, "English", 114, "Greta Gerwig", "Comedy‑fantasy film exploring identity and culture.", 7.6, 200000),
    ("Spider-Man: Across the Spider‑Verse", 2023, "English", 140, "Joaquim Dos Santos", "Animated superhero multiverse film exploring multiple realities.", 8.1, 190000),
    ("Guardians of the Galaxy Vol. 3", 2023, "English", 150, "James Gunn", "Galactic action‑comedy concluding the Guardians trilogy.", 8.0, 180000),
    ("Top Gun: Maverick", 2022, "English", 131, "Joseph Kosinski", "Action‑drama about elite fighter pilots.", 8.5, 220000),
    ("Everything Everywhere All at Once", 2022, "English", 139, "Dan Kwan & Daniel Scheinert", "Multiverse sci‑fi comedy exploring identity and family.", 8.5, 160000),
    ("Knives Out 2", 2022, "English", 130, "Rian Johnson", "Mystery‑thriller sequel with twists and clever plotting.", 7.8, 140000),
    ("Dune", 2021, "English", 155, "Denis Villeneuve", "Sci‑fi epic about politics, prophecy and desert planet.", 8.2, 150000),
    ("Blade Runner 2049", 2017, "English", 163, "Denis Villeneuve", "Neo‑noir sci‑fi exploring humanity and artificial intelligence.", 8.1, 130000),
    ("Interstellar", 2014, "English", 169, "Christopher Nolan", "Epic sci‑fi journey through space and time.", 8.6, 240000),
    ("The Dark Knight", 2008, "English", 152, "Christopher Nolan", "Legendary superhero film exploring chaos and morality.", 9.0, 300000),
    ("Inception", 2010, "English", 148, "Christopher Nolan", "Mind‑bending sci‑fi heist film exploring dreams within dreams.", 8.8, 280000),
]

def insert_movies(movies):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    for m in movies:
        try:
            cursor.execute("""
                INSERT INTO movie (title, release_year, language, duration, director, description, avg_score, rating_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, m)
        except pymysql.MySQLError as e:
            print("❌ 插入失败，电影:", m[0], "错误:", e)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 插入 50 条电影数据完成！")

if __name__ == "__main__":
    insert_movies(movies)
