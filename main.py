from monitors import api, app, resource
from monitors.core import PresentMomentSystemResource


class PresentMomentSystemResourceView(resource):

    def __init__(self):
        self.sr = PresentMomentSystemResource()

    def get(self):
        memory = self.sr.memory_usage()
        disks = self.sr.disk_usage()
        cpu = self.sr.cpu_usage()
        pid = self.sr.process_id()
        return {
            "cpu": cpu,
            "memory": memory,
            "disks": disks,
            "pid": pid,
        }


api.add_resource(PresentMomentSystemResourceView, '/')

if __name__ == '__main__':
    app.run(debug=False)
