
from view.main_view import MainView
from controller.app_controller import AppController

if __name__ == "__main__":
    # if not request_camera_permission():
    #     pass
    controller = AppController()
    view = MainView(controller)
    controller.view = view
    view.run()