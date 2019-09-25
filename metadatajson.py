import json, os, time

class MetadataJson:
    '''
        This class is used to record the data of the bundler object that gets backed up.
        This file is consumable to create automation, or display in gui.
    '''
    def write_to_file(self, data, path):
        static_name = "backup"
        unique_name = static_name + str(time.time()) + ".json"
        file_path = os.path.join(path[1], unique_name)
        print("json file: " + file_path)

        with open(file_path, "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def deserialize_json(file_name):
        with open(file_name, "r") as read_file:
            data = json.load(read_file)

        return data

"""
JSON structure
{
  "backup_time": 0
  "total_size": 0,
  "star_files": [
    {
      "name": "star 1",
      "size": 1,
      "volume_paths": [
        "volume1",
        "volume2"
      ]
    },
    {
      "name": "star 2",
      "size": 1,
      "volume_paths": [
        "volume1",
        "volume2"
      ]
    }
  ]
}
"""
