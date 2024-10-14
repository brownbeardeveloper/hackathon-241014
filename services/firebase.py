import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Firebase:
    def __init__(self) -> None:
        try:
            # Initialize Firebase
            cred = credentials.Certificate("hackathon-firebase.json")
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            self.users_ref = db.collection("users")

        except Exception as e:
            print(e)  # TODO: make a better error handling here...

    def read_data(self, highscore_list: list):
        """
        Fetches user data from the 'users' collection in Firestore and appends
        tuples of 'name' and 'score' to the provided highscore_list.

        Args:
            highscore_list (list): A list where each entry will be a tuple
                                   containing a user's 'name' (str) and 'score' (int).

        Firestore Document Structure:
            Each document is expected to have the following fields:
            - 'name' (str): The name of the user.
            - 'score' (int): The user's score.

        The function appends only documents where both 'name' and 'score' fields are present.
        """
        docs = self.users_ref.stream()

        for doc in docs:
            # Convert Firestore document to dictionary
            data = doc.to_dict()

            # Check if both 'name' and 'score' are present
            if "name" in data and "score" in data:
                highscore_list.append((data["name"], data["score"]))

    def get_sorted_highscore(self, highscore_list: list, limit: int) -> None:
        # Sort the highscore list and limit to the top 'limit' entries
        highscore_list.sort(key=self.get_score, reverse=True)

    def get_score(self, player: tuple):
        return player[1]

    def add_player_score(self, name: str, score: int) -> bool:
        try:
            self.users_ref.add({"name": name, "score": score})
            return True
        except Exception as e:
            print(e)  # TODO: make a better error handling here...


if __name__ == "__main__":
    db = Firebase()  # Initialize Firebase
    name_list = []  # Set up a list
    db.read_data(name_list)  # Retrieve the data from the database
    print(name_list)
    print("*******")

    # Sort the list and set a limit for how many players should be in the list
    db.get_sorted_highscore(name_list, 5)
    print(name_list)
    print("*******")

    player = input("Enter player's name: ").title()
    score = int(input("Enter score: "))

    if db.add_player_score(player, score):
        print("Succe")
        print("*******")

    db.read_data(name_list)
    db.get_sorted_highscore(name_list, 5)
    print(name_list)
