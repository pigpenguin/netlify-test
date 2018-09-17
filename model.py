class User:
   users = dict()
   def __init__(self, steam_id, display_name):
      self.steam_id = steam_id
      self.display_name = display_name
      self.results = dict()
      self.users[steam_id] = self
      self.first_place = 0
      self.page_one = 0

   def community_url(self):
      return "http://steamcommunity.com/profiles/" + str(self.steam_id)

   def add_result(self, level_id, rank):
      self.results[level_id] = rank
      if rank <= 15:
         if rank == 1:
            self.first_place += 1
         self.page_one += 1

   @classmethod
   def from_json(cls, json_data):
      steam_id = json_data["steamID"]

      if steam_id in cls.users:
         return cls.users[steam_id]

      display_name = json_data["displayName"]
      return User(steam_id, display_name)

   @classmethod
   def compute_stats(cls):
      print("Sorting Users")
      users = sorted(cls.users.items(), key = lambda kv: len(kv[1].results), reverse=True)
      print("Computing Stats")
      stats=dict()
      stats["total users"] = len(users)
      average = 0
      for steamid, user in users:
         average += len(user.results)
      stats["total times"] = average
      stats["average times"] = average//stats["total users"]
      return users, stats

class Level:
   levels = dict()
   def __init__(self, author, display_name, description, level_id, file_name, up_votes, down_votes, leaderboard):
      self.author = author
      self.display_name = display_name
      self.description = description
      self.level_id = level_id
      self.file_name = file_name
      self.up_votes = up_votes
      self.down_votes = down_votes
      self.leaderboard = leaderboard
      self.levels[level_id] = self

   @classmethod
   def compute_stats(cls):
      print("Sorting Levels")
      levels = sorted(cls.levels.items(), key = lambda kv: len(kv[1].leaderboard), reverse=True)
      print("Computing Stats")
      stats = dict()
      stats["level count"] = len(levels)
      average = 0
      for level in levels:
         average += len(level[1].leaderboard)
      stats["total entries"] = average
      stats["average entries"] = average//stats["level count"]
      return levels, stats


   def workshop_url(self):
      return "https://steamcommunity.com/sharedfiles/filedetails/?id=" + str(self.level_id)

   @classmethod
   def from_json(cls, json_data):
      author = User.from_json(json_data["author"])
      description = json_data["description"]
      display_name = json_data["displayName"]
      level_id = json_data["id"]
      file_name = json_data["fileName"]
      up_votes = json_data["upvotes"]
      down_votes = json_data["downvotes"]
      leaderboard = []

      for rank, element in enumerate(json_data["leaderboard"]):
         player = User.from_json(element["player"])
         User.users[player.steam_id].add_result(level_id, rank+1)
         leaderboard.append((player,element["time"]))

      return Level(author, display_name, description, level_id, file_name, up_votes, down_votes, leaderboard)
