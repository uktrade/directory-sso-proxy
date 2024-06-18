class AppCheck:
    name = 'app'

    def check(self):
        return True, ''


health_check_services = (AppCheck,)
