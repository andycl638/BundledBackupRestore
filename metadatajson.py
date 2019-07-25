import json

class MetadataJson:
    '''
        This class is used to record the data of the bundler object that gets backed up.
        This file is consumable to create automation, or display in gui.
    '''
    #def __init__(self):
    #    """ nothing"""





    def write_to_file(self, data):
        with open("testfile.json", "w") as write_file:
            json.dump(data, write_file)

    def deserialize_json(self, file_name):
        with open(file_name, "r") as read_file:
            data = json.load(read_file)

        return data
"""
    def create_file:

    def serialize_json():

    def deserialize_json():
"""
"""
{
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
