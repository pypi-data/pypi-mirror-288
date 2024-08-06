from vergen.Application import Application
import sys
    
def main():
    try:
        app = Application()
        app.run()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
