import json, os, time, glob

class MetadataJson:
    '''
        This class is used to record the data of the bundler object that gets backed up.
        This file is consumable to create automation, or display in gui.
    '''
    def write_to_file(self, data, path):
        static_name = "backup"
        unique_name = static_name + str(time.time()) + ".json"
        file_path = os.path.join(path, unique_name)
        print("json file: " + file_path)

        with open(file_path, "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def deserialize_json(file_name):
        with open(file_name, "r") as read_file:
            data = json.load(read_file)
        return data

    def create_obj():
        data = {}
        bundled_file_arr = []
        data['bundled_files'] = bundled_file_arr
        data['backup_time'] = backup_time

    def create_file_obj(tar_size):
        bundled_file_data = {}
        volume_path_arr = []
        file_path_arr = []

        bundled_file_data['name'] = tar_path
        bundled_file_data['size'] = tar_size
        bundled_file_data['volume_paths'] = volume_path_arr
        bundled_file_data['file_paths'] = file_path_arr
        volume_path_arr.append(dir_list[0])

        for file in os.listdir(dir_list[0]):
            if os.path.isfile(os.path.join(dir_list[0], file)):
                file_path_arr.append(file)

    @staticmethod
    def get_metadata_file(dest_path):
        metadata_path = ""
        for file in os.listdir(dest_path):
            if file.endswith('.json'):
                metadata_path = os.path.join(dest_path, file)
                break
        return metadata_path


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
