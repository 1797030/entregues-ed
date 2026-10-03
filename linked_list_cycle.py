class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def hasCycle(head: ListNode) -> bool:
    visitats = set()
    cicle = False
    final = False
    visitats.add(head)
    seguent = head.next
    while cicle == False and final == False:
        visitats.add(seguent)
        seguent = seguent.next
        if seguent in visitats:
            cicle = True
        elif seguent == None:
            final = True
    if final == True:
        return False
    else:
        return True


