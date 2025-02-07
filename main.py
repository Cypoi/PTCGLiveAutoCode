import sys
import controller

def main():
    app = controller.instance.init_window()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()