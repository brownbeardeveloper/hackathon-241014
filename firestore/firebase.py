import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin.exceptions import FirebaseError


class Firebase:
    def __init__(self) -> None:
        """
        Initialize the Firebase connection and set up the Firestore database.

        This constructor attempts to establish a connection to Firebase using the
        provided service account credentials. It initializes the Firestore client
        and sets a reference to the 'users' collection.

        Raises:
            Exception: If the Firebase initialization fails, an exception is caught
                        and printed. Consider implementing better error handling
                        for production use.

        Attributes:
            users_ref (CollectionReference): A reference to the 'users' collection
                                              in Firestore.
        """
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Initialize Firebase
                cred = credentials.Certificate("hackathon-firebase.json")
                firebase_admin.initialize_app(cred)

            # Initialize Firestore DB
            db = firestore.client()

            # Set reference to 'users' collection
            self.users_ref = db.collection("users")

        except FirebaseError as e:
            print(f"Firebase-related error: {e}")
            raise FirebaseError(
                "An error occurred while connecting to Database. Please try again later."
            )

    def _read_data(self, highscore_list: list):
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

    def get_sorted_highscore_list_from_db(self, limit: int):
        """
        Retrieve and sort a list of players from the database.

        This method initializes an empty list for players, retrieves data from the
        database by calling the _read_data method, sorts the player list based on
        high scores, and limits the results to the specified number of top players.

        Args:
            limit (int): The maximum number of high scores to retain in the sorted list.

        Returns:
            list: A sorted list of players retrieved from the database, limited
                  to the top 'limit' scores. The list may be empty if no data is found.
        """
        player_list = []
        self._read_data(player_list)
        self._set_sorted_highscore(player_list, limit)
        return player_list

    def _set_sorted_highscore(self, highscore_list: list, limit: int) -> None:
        """
        Sort the highscore list in descending order and limit it to the top 'limit' entries.

        Args:
            highscore_list (list): A list of player tuples, where each tuple
                                   contains player information and the score.
            limit (int): The maximum number of high scores to retain in the list.

        Returns:
            None: This method modifies the highscore_list in place.
        """
        # Sort the highscore list in descending order based on player scores
        highscore_list.sort(key=self._get_score, reverse=True)

        # Limit the list to the top 'limit' entries
        del highscore_list[limit:]

    def _get_score(self, player: tuple):
        """
        Retrieve the score of a player.

        Args:
            player (tuple): A tuple representing the player, where
                            the second element contains the player's score.

        Returns:
            The score of the player (usually an integer or float).
        """
        return player[1]

    def add_player_to_db(self, name: str, score: int) -> bool:
        """
        Add a player's score to the Firestore database.

        This method attempts to add a new player entry with the given name and score
        to the 'users' collection in Firestore.

        Args:
            name (str): The name of the player to be added.
            score (int): The score of the player to be added.

        Returns:
            bool: True if the player score was added successfully;
                  False if an exception occurred during the process.

        Raises:
            Exception: If there is an error during the addition of the player score,
                        it is caught and printed. Consider implementing better error
                        handling for production use.
        """
        try:
            self.users_ref.add({"name": name, "score": score})
            return True
        except Exception as e:
            print(e)  # TODO: make a better error handling here...


if __name__ == "__main__":
    # Initialize Firebase
    db = Firebase()

    # Retrieve the list of player names and scores from the database
    highscore_list = db.get_sorted_highscore_list_from_db(3)
    print(highscore_list)  # Display the current list of players

    # Prompt the user for a new player's name and score
    player = input("Enter player's name: ").title()
    score = int(input("Enter score: "))

    # Add the player's score to the database and confirm success
    if db.add_player_to_db(player, score):
        print("Score added successfully!")
