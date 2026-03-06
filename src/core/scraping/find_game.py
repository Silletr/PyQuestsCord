from parser import find_games_by_name

game_name = input("Enter the game name (corresponding correct name): ")
results = find_games_by_name(game_name)
if results:
    for name, exe in results:
        print(f"{name} → {exe}")
else:
    print("No games found")
