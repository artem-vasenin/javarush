from shared.forum.branches.forum import Branch
from shared.forum.menu import Beginning

beginning = Beginning()
branch = Branch()

if __name__=="__main__":
    beginning.print_menu()
    beginning.choose_action()
